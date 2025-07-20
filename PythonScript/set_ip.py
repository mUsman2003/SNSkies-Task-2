#!/usr/bin/env python3

import argparse
import subprocess
from datetime import datetime

LOG_FILE = "/var/log/ip-config.log"
NETPLAN_FILE = "/etc/netplan/01-netcfg.yaml"

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} {message}\n")
    print(f"{timestamp} {message}")

def write_netplan(iface, ip, gw):
    config = f"""
network:
  version: 2
  renderer: networkd
  ethernets:
    {iface}:
      dhcp4: no
      addresses: [{ip}]
      gateway4: {gw}
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
"""
    try:
        with open(NETPLAN_FILE, "w") as f:
            f.write(config.strip())
        log(f"Netplan config written to {NETPLAN_FILE}")
    except Exception as e:
        log(f"ERROR writing netplan config: {e}")
        return False
    return True

def apply_netplan():
    try:
        subprocess.run(["netplan", "apply"], check=True)
        log("Netplan applied successfully")
        return True
    except subprocess.CalledProcessError as e:
        log(f"ERROR applying netplan: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Apply static IP using Netplan.")
    parser.add_argument("--ip", required=True, help="Static IP address with CIDR (e.g. 192.168.56.10/24)")
    parser.add_argument("--gw", required=True, help="Default gateway IP")
    parser.add_argument("--iface", required=True, help="Network interface name (e.g. enp0s3)")
    args = parser.parse_args()

    log(f"Applying static IP {args.ip} on {args.iface} with gateway {args.gw}")
    
    if write_netplan(args.iface, args.ip, args.gw):
        apply_netplan()

if __name__ == "__main__":
    main()
