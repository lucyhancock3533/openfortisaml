#!/usr/bin/env python3
 
# OpenFortiSAML v0.3
# Lucy Hancock <lucy@leh.dev> 2023, absolutely no copyrights
# Opens a firefox session and extracts the SVPNCOOKIE to use to authenticate with FortiVPN
# Functionality is derived from ****FortiClient with superfluous functionality removed
# ****FortiClient: https://gist.github.com/nonamed01/0961d8a79955206ebdc00abcaa56aefe
# One day I might also replicate finding the Firefox profile. Today is not that day.
 
# Licensed under CC0: https://creativecommons.org/publicdomain/zero/1.0/legalcode
# All code is dedicated to the public domain, where possible, and all liabilites are waived
 
import argparse
import os
import subprocess
import json
 
from pathlib import Path

if __name__ == "__main__":
    print('OpenFortiSAML v0.3')
    parser = argparse.ArgumentParser(prog='OpenFortiSAML')
    parser.add_argument('-f', '--firefox-profile', type=str, dest='fp', required=True)
    parser.add_argument('-s', '--server', type=str, dest='server', required=True)
    parser.add_argument('-p', '--port', type=int, dest='port', required=False, default=443)
    parser.add_argument('-a', '--openfortivpn-args', dest='ovpnargs', type=str, required=False, nargs='*', default=[])
    arg = parser.parse_args()
    print(arg)
    user = os.getlogin()
    Path('/tmp/.openfortisaml-cookie').unlink(missing_ok=True)
 
    if not Path(arg.fp).is_dir():
        print("Firefox profile doesn't seem to exist")
        exit(1)
 
    check_running_ff = subprocess.run(['pgrep', '-u', user, 'firefox'], capture_output=True)
    if check_running_ff.returncode != 1:
        print('Firefox seems to be running, please close it')
        exit(1)
 
    print('Opening firefox to VPN login, please login and then exit firefox')
    url = f'https://{arg.server}:{arg.port}/remote/saml/start'
 
    firefox_first = subprocess.run(['firefox', url], capture_output=True)
    if firefox_first.returncode:
        print("Hmm, that didn't work")
        exit(1)
 
    print('Opening firefox again, please just exit')
    firefox_second = subprocess.run(['firefox', 'https://1.1.1.1/help'], capture_output=True)
    if firefox_second.returncode:
        print("Hmm, that didn't work")
        exit(1)
 
    print('Looking for cookies backup')
    prev_path = Path(f'{arg.fp}/sessionstore-backups/previous.jsonlz4')
    if not prev_path.is_file():
        print("Huh, that doesn't exist")
        exit(1)
 
    print(f'Found at {prev_path.absolute()}, reading')
    jsonlz4cat = subprocess.run(['lz4jsoncat', prev_path.absolute()], capture_output=True, text=True)
    if jsonlz4cat.returncode:
        print("Hmm, that didn't work")
        exit(1)
    prev_dict = json.loads(jsonlz4cat.stdout) 
    cookie = None
    for i in prev_dict['cookies']:
        if i['host'] == arg.server:
            if i['name'] == 'SVPNCOOKIE':
                cookie = i['value']
 
    if cookie is None:
        print('SVPNCOOKIE not found')
        exit(1)

    Path('/tmp/.openfortisaml-cookie').touch()
    os.chmod('/tmp/.openfortisaml-cookie', 0o600)
    with open('/tmp/.openfortisaml-cookie', 'w') as f:
        f.write(f'SVPNCOOKIE={cookie}')
 
    ovpncmd = ['cat', '/tmp/.openfortisaml-cookie', '|', 'sudo',
               'openfortivpn', f'{arg.server}:{arg.port}', '--cookie-on-stdin']
    try:
        subprocess.run(['bash', '-c', ' '.join(ovpncmd)])
    except KeyboardInterrupt:
        Path('/tmp/.openfortisaml-cookie').unlink()
        print("That's all folks!")
        exit(0)
