#!/bin/python3

import subprocess
import json
import ipaddress
import re
import os
import optparse
import threading
import time

def run_gobuster():
    subprocess.call(["gobuster","dir","-u",f"http://{target_ip}","-w",gobuster_wordlist_directory,"-o",f"{challenge_name}/gobuster/initial"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def print_directories():
    known_dirs = set()
    while gobuster_thread.is_alive() or not known_dirs:
        # Wait until the output file exists
        while not os.path.exists(f"{challenge_name}/gobuster/initial"):
            time.sleep(1)
        with open(f"{challenge_name}/gobuster/initial", 'r') as file:
            gobuster_result = file.read()
        gobuster_dirs = set(re.findall(r"\/\S+\s+\(Status: \d+\)", gobuster_result))
        new_dirs = gobuster_dirs - known_dirs
        for dir in new_dirs:
            print(f"{GREEN}{BOLD}[+][+]{WHITE} Here's a directory you might want to take a look: {GREEN}{dir}{RESET}")
        known_dirs = gobuster_dirs
        time.sleep(1)  # Wait a bit before checking for new directories

# Define some colors and styles
RED = "\033[31m"
GREEN = "\033[32m"
WHITE = "\033[37m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Let's check if the user has sudo priveleges
id_output = subprocess.check_output(["id"]).decode("utf-8")
id_result = re.search(r"uid=(\d*)",id_output)
if id_result.group(1) != "0":
    print(f"{RED}{BOLD}[-]{WHITE} Run it as root, pal.{RESET}")
    exit()

# Parse the arguments given from the command line
parser = optparse.OptionParser()
parser.add_option("-n", "--name", dest="ctf_name", help="CTF Name")
parser.add_option("-i", "--ip", dest="target_ip", help="Target IP")
(options, arguments) = parser.parse_args()
if not options.ctf_name or not options.target_ip:
    parser.error(f"{RED}{BOLD}[-]{WHITE} Specify a CTF Name and a Target IP. Use --help for more info.{RESET}")

# Load config file
with open('config.jsonc') as f:
    config = json.load(f)

# Pull required parameters from config file
ctf_player_name = config["ctf_player_name"]
gobuster_wordlist_directory = config["gobuster_wordlist_directory"]
password_wordlist = config["password_wordlist"]
nmap_scan_command = config["nmap_scan_command"]

# Clear the terminal
subprocess.call("clear")

# Print the welcome message
print(f'''
   █████████  ███████████ ███████████  █████████            █████                        
  ███░░░░░███░█░░░███░░░█░░███░░░░░░█ ███░░░░░███          ░░███                         
 ███     ░░░ ░   ░███  ░  ░███   █ ░ ░███    ░░░   ██████  ███████   █████ ████ ████████ 
░███             ░███     ░███████   ░░█████████  ███░░███░░░███░   ░░███ ░███ ░░███░░███
░███             ░███     ░███░░░█    ░░░░░░░░███░███████   ░███     ░███ ░███  ░███ ░███
░░███     ███    ░███     ░███  ░     ███    ░███░███░░░    ░███ ███ ░███ ░███  ░███ ░███
 ░░█████████     █████    █████      ░░█████████ ░░██████   ░░█████  ░░████████ ░███████ 
  ░░░░░░░░░     ░░░░░    ░░░░░        ░░░░░░░░░   ░░░░░░     ░░░░░    ░░░░░░░░  ░███░░░  
                                                                                ░███     
{GREEN}{BOLD}CTFSetup by Mehmet Akif VARDAR.{RESET}                                                 █████    
{GREEN}{BOLD}See https://github.com/devmehmetakifv/ctfsetup for more information.{RESET}           ░░░░░     
''')
print(f"{GREEN}{BOLD}[+]{WHITE} Wassup, {ctf_player_name}.{RESET}")
print(f"{GREEN}{BOLD}[+]{WHITE} If you just started the machine, make sure to wait 3-5 minutes for machine to boot up.{RESET}")

# Parse the challenge name from the input
challenge_name = options.ctf_name

# Format the input to be a valid directory name
challenge_name = challenge_name.replace(" ", "-").lower()

# Parse the target IP from the input
target_ip = options.target_ip
try:
    ipaddress.ip_address(target_ip)
except ValueError:
    print(f"{RED}{BOLD}[-]{WHITE} IP Address {target_ip} seems invalid. Come on, you gotta have some networking knowledge right?{RESET}")
    exit()

# Check if the machine is up
print(f"{GREEN}{BOLD}[+]{WHITE} Let me check if the target is up and running...{RESET}")
ping_result = subprocess.check_output(["ping","-c","1",target_ip]).decode("utf-8")
if "1 packets transmitted, 1 received, 0% packet loss" in ping_result:
    print(f"{GREEN}{BOLD}[+]{WHITE} Target {target_ip} is up. Bells are ringing! Let's start the setup...{RESET}")
else:
    print(f"{RED}{BOLD}[-]{WHITE} Looks like target is dead. Are you sure you entered the correct IP?{RESET}")
    exit()

# Let's create the CTF directory
print(f"{GREEN}{BOLD}[+]{WHITE} A'ight looks good. Let me create the directory for the challenge...{RESET}")
subprocess.call(["mkdir", challenge_name])
if os.path.exists(challenge_name) == False:
    print(f"{RED}{BOLD}[-]{WHITE} Woops, failed to create the directory {challenge_name}.{RESET}")
    exit()
else:
    print(f"{GREEN}{BOLD}[+]{WHITE} Directory {challenge_name} created successfully. Let the war begin, eh?{RESET}")

print(f"{GREEN}{BOLD}PHASE #1: Information Gathering With Nmap.{RESET}")

# Creating nmap directory
print(f"{GREEN}{BOLD}[+]{WHITE} Let me create an nmap directory for the challenge...{RESET}")
subprocess.call(["mkdir", f"{challenge_name}/nmap"])
if os.path.exists(f"{challenge_name}/nmap") == False:
    print(f"{RED}{BOLD}[-]{WHITE} Woops, failed to create the directory {challenge_name}/nmap.{RESET}")
    exit()
else:
    print(f"{GREEN}{BOLD}[+]{WHITE} Directory {challenge_name}/nmap created successfully.{RESET}")


# Initiating nmap scan
web_server_found = 0
print(f"{GREEN}{BOLD}[+]{WHITE} Firing up the good old friend nmap...")
subprocess.call(f"nmap -sC -sV {target_ip} > {challenge_name}/nmap/initial", shell=True) # Potential lack of security here. An arbitrary bash code can be executed in between the command. Need to fix this.
with open(f"{challenge_name}/nmap/initial", 'r') as file:
    nmap_result = file.read()
open_ports = re.findall(r"(\d+\/\w*)", nmap_result)
for port in open_ports:
    print(f"{GREEN}{BOLD}[+][+]{WHITE} I got a port: {GREEN}{port}{RESET}")
    if "80" in port or "8080" in port:
        print(f"{GREEN}{BOLD}[+]{WHITE} Well, well, well, looks like we have a potential web server running on port {port.split('/')[0]}. Will run gobuster on it after the nmap scan.{RESET}")
        web_server_found = 1
if os.path.exists(f"{challenge_name}/nmap/initial") == True:
    print(f"{GREEN}{BOLD}[+]{WHITE} nmap scan is done! You can check {challenge_name}/nmap/initial for the detailed results.{RESET}")
else:
    print(f"{RED}{BOLD}[-]{WHITE} nmap scan is failed. Something seems off. Check your nmap command in config.jsonc and try again.{RESET}")
    exit()

# Check if gobuster is needed
if web_server_found == 1:
    print(f"{GREEN}{BOLD}PHASE #2: Hidden Directory Enumeration With Gobuster.{RESET}")
    print(f"{GREEN}{BOLD}[+]{WHITE} Remember the web server I found during the nmap scan? Let's run our good friend gobuster to find hidden directories on the website.{RESET}")
    print(f"{GREEN}{BOLD}[+]{WHITE} I'm creating a gobuster directory for the challenge...{RESET}")
    subprocess.call(["mkdir", f"{challenge_name}/gobuster"])
    if os.path.exists(f"{challenge_name}/gobuster") == False:
        print(f"{RED}{BOLD}[-]{WHITE} Woops, failed to create the directory {challenge_name}/gobuster.{RESET}")
        exit()
    print(f"{GREEN}{BOLD}[+]{WHITE} Directory {challenge_name}/gobuster created successfully.{RESET}")
    print(f"{GREEN}{BOLD}[+]{WHITE} Show us what you got gobuster...{RESET}")
    gobuster_thread = threading.Thread(target=run_gobuster)
    gobuster_thread.start()
    print_directories()
    if os.path.exists(f"{challenge_name}/gobuster/initial") == True:
        print(f"{GREEN}{BOLD}[+]{WHITE} gobuster nailed it! Check {challenge_name}/gobuster/initial for the detailed results.{RESET}")
    else:
        print(f"{RED}{BOLD}[-]{WHITE} gobuster failed somehow. Something seems off. Check the gobuster command in config.jsonc and try again.{RESET}") # Add GoBuster command to config.jsonc later.
        exit()

