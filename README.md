# OpenFortiSAML

Lucy Hancock <lucy@leh.dev> 2023, absolutely no copyrights

Opens a firefox session and extracts the SVPNCOOKIE to use to authenticate with FortiVPN

Functionality is derived from ****FortiClient with superfluous functionality removed

****FortiClient: https://gist.github.com/nonamed01/0961d8a79955206ebdc00abcaa56aefe

One day I might also replicate finding the Firefox profile. Today is not that day.

## License
 
Licensed under CC0: https://creativecommons.org/publicdomain/zero/1.0/legalcode

All code is dedicated to the public domain, where possible, and all liabilites are waived

## Requirements

Requires lz4json for lz4jsoncat to read the cookies file, and openfortivpn with support for the --cookies flag.
