README.txt  
-----------

Project Title: Week 2 – Virtualization, Containerization & Python Scripting  
Student Name: Muhammad Usman  
Roll Number: [22i-0900]  

---------------------------------------
📁 Submission Folder Structure
---------------------------------------

Week2_Submission/
├─ Week2_Lab_Report.pdf            → Final PDF report with diagrams, screenshots, and analysis
├─ Diagrams/
│   └─ network_topology.png        → Visual representation of VM/container network
├─ Screenshots/
├─ Python_Scripts/
│   ├─ set_ip.py                   → Script to set static IP via Netplan
│   └─ monitor.py                  → Health monitoring + email alert
├─ Output_Logs/
│   ├─ ip-config.png               → Output from `set_ip.py`
│   └─ healthcheck.png             → Log entries from `monitor.py`
└─ README.txt                      → You are here :)

---------------------------------------
🛠 Tools & Technologies Used
---------------------------------------
• VirtualBox (for virtualization)
• Ubuntu 22.04 Server & Desktop (as VMs)
• Docker Engine + Docker Compose
• Python 3.x (for scripting and automation)
• Wireshark & tcpdump (for packet-level inspection)
• VS Code (for editing scripts and YAML files)

---------------------------------------
📌 Summary of Tasks
---------------------------------------

✅ Task 1 – Virtualization  
• Two Ubuntu VMs created: `infra-server` and `admin-tools`  
• Static IPs assigned:  
  - infra-server → 192.168.56.10  
  - admin-tools → 192.168.56.20  
• Cross-VM ping successful  

✅ Task 2 – Containerization  
• Nginx container running on infra-server with host port 8080  
• Syslog-NG container running on admin-tools with UDP port 514  
• Docker bridge networks created for isolation  
• Nginx successfully accessed via browser from admin-tools

✅ Task 3 – Python Automation  
• `set_ip.py`: applies static IP using Netplan  
• `monitor.py`:  
  - Pings Nginx host  
  - Sends HTTP request to Nginx  
  - Sends syslog message and verifies log  
  - Logs status with timestamps  
  - Sends email if any test fails


---------------------------------------
📬 Notes
---------------------------------------
• Email alert from `monitor.py` works using a containerized SMTP relay (`namshi/smtp`)
• Static IPs were set on boot via Netplan
• Host-only network ensures isolated lab environment while allowing host↔VM access

---------------------------------------
📧 Contact
---------------------------------------
If there are any issues running the scripts or containers, please contact me at:  
📨 [usman2003.fb@gmail.com]

#   S N S k i e s - T a s k - 2 
 
 