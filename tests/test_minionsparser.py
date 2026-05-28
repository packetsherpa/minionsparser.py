import importlib.util
import io
import json
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "minionsparser.py"


def load_parser_module():
    spec = importlib.util.spec_from_file_location("minionsparser", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeResponse(io.StringIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False


class MinionsParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = load_parser_module()

    def test_normalize_scanners_deduplicates_and_sorts_descending(self):
        scanners = ["192.0.2.1", "198.51.100.2", "192.0.2.1"]

        self.assertEqual(
            self.parser.normalize_scanners(scanners),
            ["198.51.100.2", "192.0.2.1"],
        )

    def test_process_feeds_writes_each_edl_file(self):
        feeds = {
            "https://example.invalid/minions": "minions-v4.edl.txt",
            "https://example.invalid/minions-ipv6": "minions-v6.edl.txt",
        }
        payloads = {
            "https://example.invalid/minions": {"scanners": ["192.0.2.1", "198.51.100.2"]},
            "https://example.invalid/minions-ipv6": {"scanners": ["2001:db8::2", "2001:db8::1"]},
        }

        def opener(url, timeout):
            self.assertEqual(timeout, self.parser.REQUEST_TIMEOUT_SECONDS)
            return FakeResponse(json.dumps(payloads[url]))

        output_dir = PROJECT_ROOT / ".test-output"
        try:
            self.parser.process_feeds(feeds=feeds, output_dir=output_dir, opener=opener)

            self.assertEqual(
                (output_dir / "minions-v4.edl.txt").read_text(encoding="utf-8"),
                "198.51.100.2\n192.0.2.1\n",
            )
            self.assertEqual(
                (output_dir / "minions-v6.edl.txt").read_text(encoding="utf-8"),
                "2001:db8::2\n2001:db8::1\n",
            )
        finally:
            for path in output_dir.glob("*"):
                path.unlink()
            output_dir.rmdir()

    def test_fetch_scanners_rejects_missing_scanner_list(self):
        def opener(url, timeout):
            return FakeResponse(json.dumps({"not_scanners": []}))

        with self.assertRaisesRegex(ValueError, "scanners list"):
            self.parser.fetch_scanners("https://example.invalid/minions", opener=opener)


if __name__ == "__main__":
    unittest.main()
