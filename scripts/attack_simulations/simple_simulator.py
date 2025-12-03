#!/usr/bin/env python3
"""
Simple Attack Simulator for CyberPulse
"""

import time
import random
import json
from datetime import datetime

class SimpleAttackSimulator:
    def __init__(self):
        self.events = []
    
    def simulate_brute_force(self):
        print("Simulating brute force attack...")
        events = []
        ip = f"192.168.1.{random.randint(100, 200)}"
        
        for i in range(8):
            event = {
                'timestamp': datetime.now().isoformat(),
                'source_ip': ip,
                'username': 'admin',
                'event_type': 'failed_login',
                'service': 'ssh'
            }
            events.append(event)
            self.events.append(event)
            time.sleep(0.2)
        
        print(f"Created {len(events)} failed login attempts")
        return events
    
    def simulate_port_scan(self):
        print("Simulating port scan...")
        event = {
            'timestamp': datetime.now().isoformat(),
            'source_ip': '10.0.0.50',
            'event_type': 'port_scan',
            'ports': random.randint(50, 1000)
        }
        self.events.append(event)
        return [event]
    
    def simulate_powershell(self):
        print("Simulating PowerShell attack...")
        events = []
        commands = [
            "IEX (New-Object Net.WebClient).DownloadString()",
            "Start-Process -WindowStyle Hidden"
        ]
        
        for cmd in commands:
            event = {
                'timestamp': datetime.now().isoformat(),
                'source_ip': '172.16.0.100',
                'command': cmd,
                'event_type': 'powershell_abuse'
            }
            events.append(event)
            self.events.append(event)
            time.sleep(0.3)
        
        return events
    
    def simulate_sudo_abuse(self):
        print("Simulating sudo abuse...")
        event = {
            'timestamp': datetime.now().isoformat(),
            'source_ip': '10.10.10.10',
            'command': 'sudo cat /etc/shadow',
            'event_type': 'privilege_escalation'
        }
        self.events.append(event)
        return [event]
    
    def test_rapid_logins(self):
        print("Testing rapid failed login detection...")
        events = []
        
        for i in range(15):
            event = {
                'timestamp': datetime.now().isoformat(),
                'source_ip': '10.0.0.123',
                'username': f'user{i}',
                'event_type': 'failed_login'
            }
            events.append(event)
            self.events.append(event)
            time.sleep(2)
        
        print(f"Created {len(events)} rapid failed logins")
        return events
    
    def run_all(self):
        print("="*50)
        print("Running all attack simulations")
        print("="*50)
        
        self.simulate_brute_force()
        print()
        self.simulate_port_scan()
        print()
        self.simulate_powershell()
        print()
        self.simulate_sudo_abuse()
        print()
        self.test_rapid_logins()
        
        # Save results
        with open('attack_results.json', 'w') as f:
            json.dump(self.events, f, indent=2)
        
        print("\n" + "="*50)
        print(f"Total events generated: {len(self.events)}")
        print("Results saved to: attack_results.json")
        print("="*50)

if __name__ == "__main__":
    simulator = SimpleAttackSimulator()
    simulator.run_all()
