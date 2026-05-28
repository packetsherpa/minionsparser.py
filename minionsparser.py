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


def fetch_scanners(url, opener=urlopen):
    with opener(url, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        payload = json.load(response)

    scanners = payload.get("scanners")
    if not isinstance(scanners, list):
        raise ValueError(f"Feed response from {url} did not include a scanners list")

    return scanners


def normalize_scanners(scanners):
    return sorted(set(scanners), reverse=True)


def write_edl(url, filename, output_dir=OUTPUT_DIR, opener=urlopen):
    output_path = output_dir / filename
    scanners = normalize_scanners(fetch_scanners(url, opener=opener))
    output_path.write_text("\n".join(scanners) + "\n", encoding="utf-8")
    print(f"Wrote {len(scanners)} entries to {output_path}")


def process_feeds(feeds=FEEDS, output_dir=OUTPUT_DIR, opener=urlopen):
    output_dir.mkdir(parents=True, exist_ok=True)

    for url, filename in feeds.items():
        write_edl(url, filename, output_dir=output_dir, opener=opener)


def main():
    try:
        process_feeds()
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"Failed to process feeds: {error}") from error


if __name__ == "__main__":
    main()
