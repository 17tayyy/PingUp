#!/usr/bin/env python3

import argparse
import subprocess
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

def print_ascii():
    banner = '''

  ____  _             _   _       
 |  _ \(_)_ __   __ _| | | |_ __  
 | |_) | | '_ \ / _` | | | | '_ \ 
 |  __/| | | | | (_| | |_| | |_) |
 |_|   |_|_| |_|\__, |\___/| .__/ 
                |___/      |_|       

    Net host Scanner
    by tay

    '''
    print(colored(banner, 'blue'))

def def_handler(sig, frame):
    print(colored(f"\n[!] Exiting program...\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def get_arguments():
    parser = argparse.ArgumentParser(description="Tool for discovering active hosts in a network (ICMP)")
    parser.add_argument("-t", "--target", required=True, dest="target", help="Host or network range to scan")
    args = parser.parse_args()
    return args.target

def parse_target(target_str):
    target_str_splitted = target_str.split('.')
    first_three_octets = '.'.join(target_str_splitted[:3])

    if len(target_str_splitted) == 4:
        if "-" in target_str_splitted[3]:
            start, end = target_str_splitted[3].split('-')
            return [f"{first_three_octets}.{i}" for i in range(int(start), int(end) + 1)]
        else:
            return [target_str]
    else:
        print(colored(f"\n[!] Invalid IP or IP range format\n", 'red'))

def host_discovery(target):
    try:
        ping = subprocess.run(["ping", "-c", "1", target], timeout=1, stdout=subprocess.DEVNULL)
        if ping.returncode == 0:
            print(colored(f"    [+] IP {target} is active", 'green'))
    except subprocess.TimeoutExpired:
        pass

def main():
    target_str = get_arguments()
    targets = parse_target(target_str)

    max_threads = 100
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(host_discovery, targets)

if __name__ == '__main__':
    print_ascii()
    main()
