#!/usr/bin/env python3
"""
CyberPulse Attack Simulation Module
Author: Victoria Omosowon
Tasks: VOSF1-VOSF4
"""

import subprocess
import time
import random
import json
import sys
from datetime import datetime, timedelta

class AttackSimulator:
    def __init__(self, target_ip="127.0.0.1"):
        self.target_ip = target_ip
        self.results = []
        self.events = []
    
    def simulate_hydra_attack(self):
        """VOSF1: Simulate brute force attacks"""
        print("[VOSF1] Simulating Hydra brute force attack...")
        events = []
        for i in range(10):
            event = {
                'timestamp': datetime.now().isoformat(),
                'source_ip': f"10.0.0.{random.randint(100, 200)}",
                'username': 'admin',
                'event_type': 'failed_login',
                'service': 'ssh',
                'simulation': 'hydra_brute_force'
            }
            events.append(event)
            time.sleep(0.2)
        return events
    
    def simulate_nmap_scan(self):
        """VOSF1: Simulate port scanning"""
        print("[VOSF1] Simulating Nmap port scan...")
        try:
            subprocess.run(['nmap', '-sS', '-T4', '-F', 'localhost'], 
                         capture_output=True, timeout=10)
            return [{
                'timestamp': datetime.now().isoformat(),
                'source_ip': '192.168.1.100',
                'event_type': 'port_scan',
                'simulation': 'nmap_scan'
            }]
        except:
            return []
    
    def simulate_powershell_attack(self):
        """VOSF2: Simulate PowerShell abuse"""
        print("[VOSF2] Simulating PowerShell attack...")
        events = []
        commands = [
            "IEX (New-Object Net.WebClient).DownloadString()",
            "Start-Process -WindowStyle Hidden",
            "Get-Process | Where-Object {$_.CPU -gt 50}"
        ]
        for cmd in commands:
            events.append({
                'timestamp': datetime.now().isoformat(),
                'source_ip': '10.0.0.50',
                'command': cmd,
                'event_type': 'powershell_abuse',
                'simulation': 'powershell_attack'
            })
            time.sleep(0.3)
        return events
    
    def simulate_sudo_abuse(self):
        """VOSF3: Simulate sudo abuse"""
        print("[VOSF3] Simulating sudo abuse...")
        return [{
            'timestamp': datetime.now().isoformat(),
            'source_ip': '172.16.0.100',
            'username': 'user1',
            'command': 'sudo cat /etc/shadow',
            'event_type': 'sudo_abuse',
            'simulation': 'sudo_abuse'
        }]
    
    def test_rapid_logins(self):
        """VOSF4: Test rapid failed login detection (>10 in 1 minute)"""
        print("[VOSF4] Testing rapid failed login detection...")
        events = []
        for i in range(15):
            events.append({
                'timestamp': datetime.now().isoformat(),
                'source_ip': '10.0.0.123',
                'username': f'user{i}',
                'event_type': 'failed_login',
                'simulation': 'rapid_failed_logins'
            })
            time.sleep(2)  # 15 attempts in ~30 seconds
        return events
    
    def run_all(self):
        """Run all simulations"""
        print("="*50)
        print("CyberPulse Attack Simulations")
        print("="*50)
        
        all_events = []
        all_events.extend(self.simulate_hydra_attack())
        all_events.extend(self.simulate_nmap_scan())
        all_events.extend(self.simulate_powershell_attack())
        all_events.extend(self.simulate_sudo_abuse())
        all_events.extend(self.test_rapid_logins())
        
        # Save results
        with open('simulation_results.json', 'w') as f:
            json.dump(all_events, f, indent=2)
        
        print(f"\n✅ Generated {len(all_events)} simulation events")
        print("📁 Results saved to simulation_results.json")
        return all_events

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    simulator = AttackSimulator(target)
    simulator.run_all()

if __name__ == "__main__":
    main()
