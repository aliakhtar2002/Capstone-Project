import requests
import subprocess
import socket
import json

def print_test(name, passed):
    symbol = "[PASS]" if passed else "[FAIL]"
    print(f"{symbol} {name}")

def test_api_health():
    try:
        r = requests.get("http://localhost:5000/api/health", timeout=5)
        return r.status_code == 200
    except:
        return False

def test_api_add_detection():
    try:
        r = requests.post("http://localhost:5000/api/add-detection",
                          json={"event_type": "audit_test", "source_ip": "127.0.0.1", "description": "Test audit alert"},
                          timeout=5)
        return r.status_code == 200
    except:
        return False

def test_docker_running():
    try:
        out = subprocess.check_output(["sudo", "docker", "ps", "--format", "{{.Names}}"])
        return "capstone-test" in out.decode()
    except:
        return False

def test_git_connected():
    try:
        out = subprocess.check_output(["git", "remote", "-v"], stderr=subprocess.DEVNULL)
        return "origin" in out.decode()
    except:
        return False

def test_github_reachable():
    try:
        r = requests.get("https://github.com/aliakhtar2002/Capstone-Project", timeout=10)
        return r.status_code == 200
    except:
        return False

def test_ec2_ssh():
    try:
        hostname = socket.gethostname()
        return "ip-" in hostname
    except:
        return False

print("\nSOC INTEGRATION AUDIT REPORT")
print("=" * 40)
print_test("API Health Endpoint", test_api_health())
print_test("API Add Detection Endpoint", test_api_add_detection())
print_test("Docker Container Running", test_docker_running())
print_test("Git Remote Configured", test_git_connected())
print_test("GitHub Repo Reachable", test_github_reachable())
print_test("Running on EC2", test_ec2_ssh())
print("=" * 40)
print("Audit complete.\n")
