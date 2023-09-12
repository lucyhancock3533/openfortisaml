#!/usr/bin/env python3
 
# OpenFortiSAML v0.2
# Lucy Hancock <lucy@leh.dev> 2023, absolutely no copyrights
# Opens a Webkit2GTK window and extracts the SVPNCOOKIE to use to authenticate with FortiVPN
# Functionality is derived from ****FortiClient
# ****FortiClient: https://gist.github.com/nonamed01/0961d8a79955206ebdc00abcaa56aefe

# Licensed under CC0: https://creativecommons.org/publicdomain/zero/1.0/legalcode
# All code is dedicated to the public domain, where possible, and all liabilities are waived
 
import argparse
import subprocess
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.1')

from tempfile import NamedTemporaryFile
from gi.repository import Gtk, WebKit2, Soup


def check_cookie(cookies):
    for c in cookies:
        if c[5] == 'SVPNCOOKIE':
            return c[6]

    return None


def do_login(server, port):
    url = f'https://{server}:{port}/remote/saml/start'

    with NamedTemporaryFile(prefix='.openfortisaml-', dir='/tmp/', delete=True) as f:
        window = Gtk.Window()
        window.set_default_size(1024, 768)
        window.connect("destroy", Gtk.main_quit)
        webview = WebKit2.WebView()
        wdm = webview.get_website_data_manager()
        ckm = wdm.get_cookie_manager()
        ckm.set_persistent_storage(f.name, WebKit2.CookiePersistentStorage.TEXT)
        ckm.set_accept_policy(Soup.CookieJarAcceptPolicy.ALWAYS)
        webview.load_uri(url)
        window.add(webview)
        window.show_all()
        Gtk.main()

        cookies = f.read().decode()

    return [x.split('\t') for x in cookies.strip().split('\n')]


def start_vpn(server, port, cookie, ovpnargs):
    with NamedTemporaryFile(prefix='.openfortisaml-', dir='/tmp/', delete=True) as f:
        f.write(f'SVPNCOOKIE={cookie}')
        ovpncmd = ['cat', f.name, '|', 'sudo', 'openfortivpn', f'{server}:{port}',
                   '--cookie-on-stdin'] + ovpnargs
        try:
            subprocess.run(['bash', '-c', ' '.join(ovpncmd)])
        except KeyboardInterrupt:
            print("That's all folks!")


def run():
    print('OpenFortiSAML')
    parser = argparse.ArgumentParser(prog='OpenFortiSAML')
    parser.add_argument('-s', '--server', type=str, dest='server', required=True)
    parser.add_argument('-p', '--port', type=int, dest='port', required=False, default=443)
    parser.add_argument('-a', '--openfortivpn-args', dest='ovpnargs', type=str, required=False, nargs='*', default=[])
    arg = parser.parse_args()
    print(arg)

    cookies = do_login(arg.server, arg.port)
    #print(cookies)
    cookie = check_cookie(cookies)

    if cookie is None:
        print('SVPNCOOKIE not found')
        exit(1)

    start_vpn(arg.server, arg.port, cookie, arg.ovpnargs)


if __name__ == "__main__":
    run()
