#!/bin/python3

###################################################################
#                                                                 #
# Quick Nmap script - By Boakill                                  #
# Run basic scan to gather ports, then run -A against open ports. # 
#                                                                 #
# Need to add:                                                    #
# - function for script engine. ie --script smb-enum-*            #
# - make it cooler                                                #
#                                                                 #
###################################################################

import os
import sys
import subprocess
import re

target_ip = sys.argv[1]
ports = []
nse_ports = [ "21" , "443" ]

def nmap_scan():
    global target_ip
    global ports
    print(" [#] Determining open ports... ")
    pattern = re.compile('[0-9]+(?=/tcp)|[0-9]+(?=/udp)')
    output = subprocess.getoutput('nmap -sS -T4 -p- ' + target_ip)
    ports = pattern.findall(output)
    print(" [#] Ports found: " + ','.join(ports) + "\n")

    print(" [#] Running full nmap scan now...")
    output = subprocess.getoutput('nmap -sS -T4 -A -p ' + ','.join(ports) + ' ' + target_ip)
    print(" [#] Scan complete!")
    print(output)

def nse_scripts():                                                                                                                                                                                 
    global target_ip                                                                                                                                                                               
    global ports                                                                                                                                                                                   
    print("\n [#] Running NSE Module... ")                                                                                                                                                         
    if "443" in ports:                                                                                                                                                                             
        print(" [#] Starting SMB Enumeration...")                                                                                                                                                  
        output = subprocess.getoutput("nmap -sS -T4 --script smb-enum-* " + target_ip)                                                                                                             
        print(output)
        print(" [#] End of SMB Enumeration.")

    if "21" in ports:
        print(" [#] Starting FTP Anon script...")
        output = subprocess.getoutput("nmap -sS -T4 --script ftp-anon " + target_ip)
        print(output)
        print(" [#] End of FTP Anon check.")

print("\n [#] Runing QuickMAP!!!")
print(" [#] Running SYN Scan against " + target_ip + "\n")
nmap_scan()
nse_check = any(item in nse_ports for item in ports)
if nse_check is True:
    nse_scripts()
