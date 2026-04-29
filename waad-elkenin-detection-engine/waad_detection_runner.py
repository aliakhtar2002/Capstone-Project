#!/usr/bin/env python3
"""
WAAD ELKENIN - Detection Runner
Handles the main detection loop and event processing
"""

import time
import json
import os
from datetime import datetime
from waad_detection_engine import DetectionEngine

def run_detector():
    """Main detection loop"""
    print("🚀 WAAD Detection Runner started")
    print(f"📅 {datetime.now().isoformat()}")
    print("=" * 50)
    
    try:
        # Initialize detection engine
        engine = DetectionEngine()
        print("✅ Detection engine initialized")
        
        # This is where you'd normally listen for events
        # For now, we'll run in simulation mode
        print("🔄 Running in continuous monitoring mode")
        print("Press Ctrl+C to stop\n")
        
        # Simulate checking for events every 5 seconds
        while True:
            # In a real implementation, this would:
            # 1. Read from a queue, log file, or API
            # 2. Process events through the detection engine
            # 3. Send alerts to the API
            
            # For now, just show it's alive
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Monitoring for threats...")
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n👋 Detection runner stopped by user")
    except Exception as e:
        print(f"❌ Error in detection runner: {e}")
        raise

def process_event(event):
    """Process a single event through the detection engine"""
    engine = DetectionEngine()
    alerts = engine.process_event(event)
    
    if alerts:
        print(f"🚨 Generated {len(alerts)} alerts")
        for alert in alerts:
            print(f"   - {alert.get('title', 'Alert')}")
    
    return alerts

if __name__ == "__main__":
    run_detector()
