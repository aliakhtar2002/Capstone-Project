# CyberPulse Project Overview
CyberPulse is a real-time virtual Security Operations Center (SOC) prototype designed to visualize, detect, and respond to cyber threats as they occur. The system integrates attack simulation, automated detection rules, and a centralized interactive dashboard to provide an end-to-end security monitoring experience.

## Architecture Flow 
1. **Victoria**: Victoria's Attack Simulation generates realistic threats using tools like Hydra, Nmap, and PowerShell.
2. **Waad**: Waad's Detection Rules analyze the traffic, identifying malicious patterns and anomalies.
3. **Aishat**: Aishat's Dashboard visualizes threats in real-time with interactive charts, geographic threat mapping, color-coded severity alerts, detailed security report generation (PDF/HTML/CSV), and IP blocking/unblocking capabilities.
4. **Ali and Grishab**: Ali & Grishab's Infrastructure connects all components via APIs and data pipelines, ensuring seamless communication between attack simulations, detection, visualization, reporting, response, and management systems.

### Team Roles
- Ali Akhtar: API infrastructure and system integration.
- Aishat Arawole: Dashboard frontend with complete visualization, reporting, and management interface.
- Waad Elkenin: Detection rule development and threat analysis logic.
- Grishab Mishra: Data pipeline architecture and database management.
- Victoria Omosowon: Attack simulation and penetration testing.

