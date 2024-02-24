#!/bin/python3

import subprocess
import json
import ipaddress
import re
import os

# Let's check if the user has sudo priveleges
id_output = subprocess.check_output(["id"]).decode("utf-8")
id_result = re.search(r"uid=(\d*)",id_output)
if id_result.group(1) != "0":
    print("You need to have sudo priveleges to run this script.")
    exit()

# Load config file
with open('config.json') as f:
    config = json.load(f)

# Pull required parameters from config file
ctf_player_name = config["ctf_player_name"]
gobuster_wordlist_directory = config["gobuster_wordlist_directory"]
password_wordlist = config["password_wordlist"]

print("CTFSetup by Mehmet Akif VARDAR. See https://github.com/devmehmetakifv/ctfsetup for more information.")
print(f"Welcome, {ctf_player_name}.")

# Ask for the challenge name
challenge_name = input("Challenge Name: ")

# Format the input to be a valid directory name
challenge_name = challenge_name.replace(" ", "-").lower()

# Ask for the target machine IP
target_ip = input("Target Machine IP: ")
try:
    ipaddress.ip_address(target_ip)
except ValueError:
    print(f"IP Address {target_ip} seems invalid. Are you sure you entered it correctly?")
    exit()

# Let's create the directory
print("Looking good! Let's create the directory for the challenge.")
subprocess.call(["mkdir", challenge_name])
if os.path.exists(challenge_name) == False:
    print(f"Failed to create the directory {challenge_name}.")
    exit()
else:
    print(f"Directory {challenge_name} created successfully.")

