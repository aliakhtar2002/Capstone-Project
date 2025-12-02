#!/usr/bin/env python3
"""
CyberPulse Security Event Simulator
Generates simulated attack events for SOC testing and validation.
"""

import time
import random
import json
import sys
from datetime import datetime

class SecurityEventSimulator:
    def __init__(self):
        self.events = []
    
    def run_brute_force(self):
        print("Simulating brute force attack...")
        events = []
        for i in range(8):
            event = {
                'id': len(self.events) + 1,
                'time': datetime.now().isoformat(),
                'type': 'failed_login',
                'ip': f"192.168.1.{random.randint(100, 200)}",
                'user': 'admin'
            }
            events.append(event)
            self.events.append(event)
            time.sleep(0.1)
        return events
    
    def run_port_scan(self):
        print("Simulating port scan...")
        event = {
            'id': len(self.events) + 1,
            'time': datetime.now().isoformat(),
            'type': 'port_scan',
            'ip': '10.0.0.100'
        }
        self.events.append(event)
        return [event]
    
    def run_powershell(self):
        print("Simulating PowerShell attack...")
        events = []
        for i in range(3):
            event = {
                'id': len(self.events) + 1,
                'time': datetime.now().isoformat(),
                'type': 'powershell_abuse',
                'ip': f"172.16.{i}.100"
            }
            events.append(event)
            self.events.append(event)
            time.sleep(0.2)
        return events
    
    def run_privilege_escalation(self):
        print("Simulating privilege escalation...")
        event = {
            'id': len(self.events) + 1,
            'time': datetime.now().isoformat(),
            'type': 'privilege_escalation',
            'ip': '10.10.10.10'
        }
        self.events.append(event)
        return [event]
    
    def run_rapid_logins(self):
        print("Testing rapid login detection...")
        events = []
        for i in range(15):
            event = {
                'id': len(self.events) + 1,
                'time': datetime.now().isoformat(),
                'type': 'failed_login',
                'ip': '10.0.0.123'
            }
            events.append(event)
            self.events.append(event)
            time.sleep(2)
        return events
    
    def run_all(self):
        print("="*50)
        print("CyberPulse Attack Simulation")
        print("="*50)
        
        self.run_brute_force()
        self.run_port_scan()
        self.run_powershell()
        self.run_privilege_escalation()
        self.run_rapid_logins()
        
        with open('simulation_results.json', 'w') as f:
            json.dump(self.events, f, indent=2)
        
        print(f"\nGenerated {len(self.events)} events")
        print("Saved to simulation_results.json")

def main():
    simulator = SecurityEventSimulator()
    simulator.run_all()

if __name__ == "__main__":
    main()
