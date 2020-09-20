#!/bin/python3

import os
import sys
import subprocess
import re

if os.geteuid()==0:
    if len(sys.argv)!=2:
        print(f" [!] Syntax error.")
        sys.exit(" [!] Example: sudo quickmap 192.168.1.1")
else:
    sys.exit(" [!] Syntax error: Rerun as root.")


target_ip = sys.argv[1]
# ports = []
ports = ["21","445"]
nse_ports = ["21","135", "445"]
args = ["-sS", "-T4"]

def port_scan():
    global ports
    pattern = re.compile('[0-9]+(?=/tcp)|[0-9]+(?=/udp)')
    
    # Checking if ports varible is empty
    args.append("-p-")

    print(f" [+] Starting QuickMap")
    print(f" [+] Determining open ports...")
    # print(" [!] TEST: nmap "+" ".join(args)+" "+target_ip)
    output = subprocess.getoutput("nmap "+" ".join(args)+" "+target_ip)
    ports = pattern.findall(output)
    print(f" [+] Ports found: {ports}")
    args.pop()

def full_scan():
    stuff= ["-p "+",".join(ports),"-oA "+target_ip,"-A"]
    if any(item in nse_ports for item in ports):
        nse_script(args)
    n = 0
    while n < len(stuff):
        args.append(stuff[n])
        n = n + 1

    print(f"\n [+] Starting full scan now...")
    print(f" [+] Args: {args}")
    output = subprocess.getoutput("nmap "+" ".join(args)+" "+target_ip)
    print(" [D] nmap "+" ".join(args)+" "+target_ip)

def nse_script(args):
    script_args = "--script "
    if "21" in ports:
        script_args = script_args + "ftp-* "
    if "445" in ports:
        script_args = script_args + "smb-enum* "
        if "135" in ports:
            script_args = script_args + "msrpc-enum "

    print(f"{script_args}")
    args.append(script_args)
    print(f"{args}")

def test():
    print(f"Target: {target_ip}")
    print(f"Ports found: {ports}")
    print(f"Aurguments: {args}")

if not ports:
    port_scan()
full_scan()
# test()
               
