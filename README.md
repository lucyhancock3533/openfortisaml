# OpenFortiSAML

Lucy Hancock <lucy@leh.dev> 2023, absolutely no copyrights

Opens a Webkit2GTK window and extracts the SVPNCOOKIE to use to authenticate with FortiVPN

Functionality is derived from ****FortiClient

****FortiClient: https://gist.github.com/nonamed01/0961d8a79955206ebdc00abcaa56aefe

Once logged into the VPN exit the GTK window and login will proceed.

## License
 
Licensed under CC0: https://creativecommons.org/publicdomain/zero/1.0/legalcode

All code is dedicated to the public domain, where possible, and all liabilities are waived

## Requirements

Requires GTK3 and Webkit2GTK to read the cookies, and openfortivpn with support for the --cookies flag.
