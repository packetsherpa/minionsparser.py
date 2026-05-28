# Description

Python script to normalize the data contained in the file published by Binary Edge at https://api.binaryedge.io/v1/minions and https://api.binaryedge.io/v1/minions-v6 into a format that can be consumed as an EDL by the Palo Alto NGFW. The output is written to /tmp/minionsparser/minions-v4.edl.txt and /tmp/minionsparser/minions-v6.edl.txt.

# Updates

- 06-30-2023 - Added Support for IPv4 and IPv6 and fixed broken sort function
- 06-29-2023 - Added rudamentary support for v6 feed
- 06-29-2023 - Initial Commit

# Supported OS

- Currently supported on *nix based systems (linux, mac, bsd and sysV variant Unix systems)

# To Do

- Add Support for Windows Systems

# Requirements

- python3

# Usage

1. Install Python 3 (hhttps://www.python.org/downloads/)
2. Run `./minionsparser.py`
3. Output will be in /tmp/minionsparser
    - minions-v4.edl.txt = IPv4 List
    - minions-v6.edl.txt = IPv6 List

# Docker Usage

This repository also contains the Docker wrappers that were previously maintained
in separate repositories.

The standalone `minionsparser.py` script is the source of truth. Both Docker
images copy that local script at build time, so parser fixes only need to land in
one place.

## Alpine cron container

The Alpine image installs the parser into the daily cron directory and keeps cron
running in the foreground.

```sh
docker/alpine-cron/build-image.sh
```

## Python one-shot container

The Python image runs the parser once and exits.

```sh
docker/python-once/build-image.sh
```

Both images write output to `/tmp/minionsparser` inside the container. The build
scripts bind mount `/tmp/minionsparser` from the host.

# Development

Run the unit tests with:

```sh
python3 -m unittest discover -s tests
```

When changing parser behavior, update `minionsparser.py` first and keep the
Docker wrappers as thin runtime variants:

- `docker/alpine-cron/` builds the scheduled Alpine container.
- `docker/python-once/` builds the run-once Python container.

# Support Policy

This script is provided under an **as-is, best effort,** support policy. This  code should be seen as community supported.  We will contribute our expertise as and when possible.

Palo Alto Networks **does not** provide technical support or help in using or troubleshooting the components of this project through its normal support options such as Palo Alto Networks support teams, or ASC (Authorized Support Centers) partners and backline support options. The underlying product(s) and product feature(s) used in conjunction with this container (Palo Alto Networks NGFW and EDLs) is supported by Palo Alto Networks according to support entitlements, but the support is only for the product functionality and not for help in deploying or using this container itself.
