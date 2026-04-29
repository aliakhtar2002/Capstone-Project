#!/usr/bin/env python3
"""
================================================
  export_soc_report.py
  SOC Report Generator — EC2 → Claude AI → PDF → S3
================================================
  INSTALL (one-time):
    pip install psycopg2-binary reportlab pypdf boto3 requests

  RUN:
    python3 export_soc_report.py

  WHAT IT DOES:
    1. Connects to PostgreSQL (capstone_soc)
    2. Pulls victoria_attack_events data
    3. Sends to Claude AI for threat analysis
    4. Creates a password-protected PDF report
    5. Uploads to S3 bucket (cyberpulse-backups-grishab)
    6. Prints a download link valid for 1 hour
================================================
"""

import os
import sys
import json
import datetime
import getpass
import boto3
import requests
import psycopg2
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from pypdf import PdfReader, PdfWriter

# ── Configuration ─────────────────────────────────────────────
DB_HOST     = "127.0.0.1"
DB_PORT     = "5432"
DB_NAME     = "capstone_soc"
DB_USER     = "api_user"
DB_TABLE    = "victoria_attack_events"
QUERY_LIMIT = 10

S3_BUCKET   = "cyberpulse-backups-grishab"
S3_REGION   = "us-east-2"
LINK_EXPIRY = 3600  # 1 hour in seconds

ANTHROPIC_MODEL = "claude-sonnet-4-20250514"

# ── Colour Palette ─────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#1F3864")
MID_BLUE    = colors.HexColor("#2E75B6")
LIGHT_BLUE  = colors.HexColor("#EBF3FB")
RED         = colors.HexColor("#C00000")
WHITE       = colors.white
GREY        = colors.HexColor("#707070")
LIGHT_GREY  = colors.HexColor("#F2F2F2")

# ══════════════════════════════════════════════════════════════
#  STEP 0 — Gather credentials
# ══════════════════════════════════════════════════════════════
print("\n╔══════════════════════════════════════════╗")
print("║   SOC PDF Report Generator               ║")
print("╚══════════════════════════════════════════╝\n")

db_password  = getpass.getpass(f"[1/3] PostgreSQL password for '{DB_USER}': ")
doc_password = getpass.getpass("[2/3] Password to protect the PDF: ")
if not doc_password:
    print("ERROR: PDF password cannot be empty.")
    sys.exit(1)

api_key = os.environ.get("ANTHROPIC_API_KEY") or getpass.getpass("[3/3] Anthropic API key: ")
if not api_key:
    print("ERROR: Anthropic API key is required.")
    sys.exit(1)

# ══════════════════════════════════════════════════════════════
#  STEP 1 — Pull data from PostgreSQL
# ══════════════════════════════════════════════════════════════
print("\n[*] Connecting to PostgreSQL...")
try:
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=db_password
    )
    cur = conn.cursor()
    cur.execute(f"""
        SELECT
            attack_type,
            attack_subtype,
            source_ip,
            event_time_utc AT TIME ZONE 'UTC' AT TIME ZONE 'America/Chicago' AS texas_time
        FROM {DB_TABLE}
        ORDER BY event_time_utc DESC
        LIMIT {QUERY_LIMIT}
    """)
    columns = [d[0] for d in cur.description]
    rows    = [dict(zip(columns, [str(v) for v in r])) for r in cur.fetchall()]
    conn.close()
    print(f"[+] Retrieved {len(rows)} records from {DB_TABLE}.")
except Exception as e:
    print(f"[!] Database error: {e}")
    sys.exit(1)

# ══════════════════════════════════════════════════════════════
#  STEP 2 — Send to Claude AI
# ══════════════════════════════════════════════════════════════
print("[*] Sending data to Claude AI for analysis...")

table_text = " | ".join(columns) + "\n" + "-" * 80 + "\n"
for row in rows:
    table_text += " | ".join(row[c] for c in columns) + "\n"

prompt = f"""You are a cybersecurity analyst at a Security Operations Center (SOC).
Analyze the following attack event data and produce a professional threat intelligence report.

DATA:
{table_text}

Write your report with these exact sections:
1. Executive Summary
2. Attack Type Breakdown
3. Top Source IPs
4. Timeline Analysis (Texas/CT time)
5. Key Findings & Recommendations

Be concise, professional, and security-focused."""

try:
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": ANTHROPIC_MODEL,
            "max_tokens": 1500,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=60
    )
    response.raise_for_status()
    ai_analysis = response.json()["content"][0]["text"]
    print("[+] Claude AI analysis complete.")
except Exception as e:
    print(f"[-] Claude AI unavailable ({e}). Continuing with raw data only.")
    ai_analysis = "AI analysis unavailable. Please review the raw data table below."

# ══════════════════════════════════════════════════════════════
#  STEP 3 — Build PDF
# ══════════════════════════════════════════════════════════════
print("[*] Generating PDF report...")

timestamp   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
tmp_pdf     = f"/tmp/SOC_Report_{timestamp}.pdf"
enc_pdf     = f"/tmp/SOC_Report_{timestamp}_PROTECTED.pdf"
s3_key      = f"soc-reports/SOC_Report_{timestamp}_PROTECTED.pdf"

doc = SimpleDocTemplate(
    tmp_pdf,
    pagesize=letter,
    topMargin=0.75*inch,
    bottomMargin=0.75*inch,
    leftMargin=1*inch,
    rightMargin=1*inch
)

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    "ReportTitle",
    parent=styles["Title"],
    fontSize=22,
    textColor=DARK_BLUE,
    spaceAfter=6,
    alignment=TA_CENTER,
    fontName="Helvetica-Bold"
)
subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontSize=10,
    textColor=GREY,
    spaceAfter=20,
    alignment=TA_CENTER
)
h1_style = ParagraphStyle(
    "H1",
    parent=styles["Heading1"],
    fontSize=14,
    textColor=DARK_BLUE,
    spaceBefore=16,
    spaceAfter=8,
    fontName="Helvetica-Bold"
)
h2_style = ParagraphStyle(
    "H2",
    parent=styles["Heading2"],
    fontSize=12,
    textColor=MID_BLUE,
    spaceBefore=10,
    spaceAfter=6,
    fontName="Helvetica-Bold"
)
body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontSize=10,
    leading=14,
    spaceAfter=6,
    alignment=TA_JUSTIFY
)
bullet_style = ParagraphStyle(
    "Bullet",
    parent=styles["Normal"],
    fontSize=10,
    leading=14,
    spaceAfter=4,
    leftIndent=20,
    bulletIndent=10
)
confidential_style = ParagraphStyle(
    "Confidential",
    parent=styles["Normal"],
    fontSize=10,
    textColor=RED,
    alignment=TA_CENTER,
    fontName="Helvetica-Bold"
)

story = []

# ── Title Page ────────────────────────────────────────────────
story.append(Spacer(1, 0.5*inch))
story.append(Paragraph("SOC Threat Intelligence Report", title_style))
story.append(Paragraph(
    f"Generated: {datetime.datetime.now().strftime('%B %d, %Y at %H:%M CT')}&nbsp;&nbsp;|&nbsp;&nbsp;"
    f"Source: {DB_TABLE}&nbsp;&nbsp;|&nbsp;&nbsp;Records: {len(rows)}",
    subtitle_style
))
story.append(HRFlowable(width="100%", thickness=2, color=DARK_BLUE, spaceAfter=20))

# ── AI Analysis Section ───────────────────────────────────────
story.append(Paragraph("AI-Generated Threat Analysis", h1_style))
story.append(HRFlowable(width="100%", thickness=0.5, color=MID_BLUE, spaceAfter=10))

for line in ai_analysis.split("\n"):
    line = line.strip()
    if not line:
        story.append(Spacer(1, 4))
        continue
    if line.startswith("##"):
        story.append(Paragraph(line.lstrip("#").strip(), h2_style))
    elif line[0].isdigit() and len(line) > 2 and line[1] in ".":
        story.append(Paragraph(f"<b>{line}</b>", body_style))
    elif line.startswith(("- ", "* ", "• ")):
        story.append(Paragraph(f"• {line[2:]}", bullet_style))
    elif line.startswith("**") and line.endswith("**"):
        story.append(Paragraph(f"<b>{line.strip('*')}</b>", body_style))
    else:
        story.append(Paragraph(line, body_style))

# ── Raw Data Table ────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("Raw Event Data", h1_style))
story.append(HRFlowable(width="100%", thickness=0.5, color=MID_BLUE, spaceAfter=10))
story.append(Paragraph(
    f"Showing {len(rows)} most recent attack events ordered by time (Texas/CT).",
    body_style
))
story.append(Spacer(1, 10))

# Build table data
header = [col.replace("_", " ").title() for col in columns]
data   = [header] + [[row[c] for c in columns] for row in rows]

col_count  = len(columns)
page_width = letter[0] - 2*inch
col_width  = page_width / col_count

tbl = Table(data, colWidths=[col_width] * col_count, repeatRows=1)
tbl.setStyle(TableStyle([
    # Header
    ("BACKGROUND",   (0, 0), (-1, 0),  DARK_BLUE),
    ("TEXTCOLOR",    (0, 0), (-1, 0),  WHITE),
    ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
    ("FONTSIZE",     (0, 0), (-1, 0),  9),
    ("ALIGN",        (0, 0), (-1, 0),  "CENTER"),
    ("BOTTOMPADDING",(0, 0), (-1, 0),  8),
    ("TOPPADDING",   (0, 0), (-1, 0),  8),
    # Data rows alternating
    ("BACKGROUND",   (0, 1), (-1, -1), LIGHT_BLUE),
    ("ROWBACKGROUNDS",(0, 1),(-1, -1), [LIGHT_BLUE, WHITE]),
    ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE",     (0, 1), (-1, -1), 8),
    ("ALIGN",        (0, 1), (-1, -1), "LEFT"),
    ("TOPPADDING",   (0, 1), (-1, -1), 5),
    ("BOTTOMPADDING",(0, 1), (-1, -1), 5),
    ("LEFTPADDING",  (0, 0), (-1, -1), 6),
    # Grid
    ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
    ("BOX",          (0, 0), (-1, -1), 1,   DARK_BLUE),
]))
story.append(tbl)

# ── Footer ────────────────────────────────────────────────────
story.append(Spacer(1, 20))
story.append(HRFlowable(width="100%", thickness=1, color=RED, spaceAfter=8))
story.append(Paragraph(
    "CONFIDENTIAL — This document contains sensitive security data. Handle with care.",
    confidential_style
))

doc.build(story)
print("[+] PDF created successfully.")

# ══════════════════════════════════════════════════════════════
#  STEP 4 — Password-protect the PDF
# ══════════════════════════════════════════════════════════════
print("[*] Encrypting PDF with password...")
reader = PdfReader(tmp_pdf)
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)
writer.encrypt(doc_password, doc_password)
with open(enc_pdf, "wb") as f:
    writer.write(f)
os.remove(tmp_pdf)
print("[+] PDF encrypted successfully.")

# ══════════════════════════════════════════════════════════════
#  STEP 5 — Upload to S3
# ══════════════════════════════════════════════════════════════
print(f"[*] Uploading to S3 bucket '{S3_BUCKET}'...")
try:
    s3 = boto3.client("s3", region_name=S3_REGION)
    s3.upload_file(
        enc_pdf,
        S3_BUCKET,
        s3_key,
        ExtraArgs={"ContentType": "application/pdf"}
    )
    os.remove(enc_pdf)

    # Generate presigned download URL
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": S3_BUCKET, "Key": s3_key},
        ExpiresIn=LINK_EXPIRY
    )

    print("\n╔══════════════════════════════════════════╗")
    print("║   ✅  REPORT READY!                       ║")
    print("╚══════════════════════════════════════════╝")
    print(f"\n  S3 Location : s3://{S3_BUCKET}/{s3_key}")
    print(f"\n  Download URL (valid for 1 hour):")
    print(f"  {url}")
    print(f"\n  Open with password: [the password you entered]")
    print("\n  TIP: Paste the URL into your browser to download the PDF directly.\n")

except Exception as e:
    print(f"[!] S3 upload failed: {e}")
    print(f"    The encrypted PDF is still saved locally at: {enc_pdf}")
    sys.exit(1)
