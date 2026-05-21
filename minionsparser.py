#!/usr/bin/env python3
#
# Description: This script normalizes Binary Edge minions feeds into EDL files
# that can be consumed by Palo Alto NGFW.

import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

OUTPUT_DIR = Path("/tmp/minionsparser")
REQUEST_TIMEOUT_SECONDS = 30
FEEDS = {
    "https://api.binaryedge.io/v1/minions": "minions-v4.edl.txt",
    "https://api.binaryedge.io/v1/minions-ipv6": "minions-v6.edl.txt",
}


def fetch_scanners(url):
    with urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        payload = json.load(response)

    scanners = payload.get("scanners")
    if not isinstance(scanners, list):
        raise ValueError(f"Feed response from {url} did not include a scanners list")

    return scanners


def write_edl(url, filename):
    output_path = OUTPUT_DIR / filename
    scanners = sorted(set(fetch_scanners(url)), reverse=True)
    output_path.write_text("\n".join(scanners) + "\n", encoding="utf-8")
    print(f"Wrote {len(scanners)} entries to {output_path}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for url, filename in FEEDS.items():
        try:
            write_edl(url, filename)
        except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
            raise SystemExit(f"Failed to process {url}: {error}") from error


if __name__ == "__main__":
    main()
