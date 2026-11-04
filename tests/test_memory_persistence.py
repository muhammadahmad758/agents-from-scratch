"""Tests for Memory persistence (save/load) added in this fork.

Run from the repo root:
    python -m unittest discover -s tests -v
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent.memory import Memory


class TestMemoryPersistence(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.file = str(Path(self.tmp.name) / "memory.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_save_load_round_trip(self):
        m = Memory()
        m.add("user likes tea")
        m.add("project codename is Falcon-27")
        m.save(self.file)

        fresh = Memory()
        loaded = fresh.load(self.file)

        self.assertEqual(loaded, 2)
        self.assertEqual(fresh.get_all(), ["user likes tea", "project codename is Falcon-27"])

    def test_saved_file_is_plain_json_list(self):
        m = Memory()
        m.add("hello")
        m.save(self.file)
        data = json.loads(Path(self.file).read_text(encoding="utf-8"))
        self.assertEqual(data, ["hello"])

    def test_load_missing_file_leaves_memory_unchanged(self):
        m = Memory()
        m.add("keep me")
        loaded = m.load(str(Path(self.tmp.name) / "does-not-exist.json"))
        self.assertEqual(loaded, 0)
        self.assertEqual(m.get_all(), ["keep me"])

    def test_load_replaces_and_deduplicates(self):
        Path(self.file).write_text(json.dumps(["a", "b", "a", 42]), encoding="utf-8")
        m = Memory()
        m.add("old item")
        loaded = m.load(self.file)
        self.assertEqual(loaded, 2)
        self.assertEqual(m.get_all(), ["a", "b"])

    def test_load_rejects_non_list_json(self):
        Path(self.file).write_text(json.dumps({"items": []}), encoding="utf-8")
        m = Memory()
        with self.assertRaises(ValueError):
            m.load(self.file)

    def test_existing_behaviour_unchanged(self):
        m = Memory()
        m.add("Tea is great")
        m.add("Tea is great")  # duplicate ignored by add()
        m.add("coffee too")
        self.assertEqual(len(m), 2)
        self.assertEqual(m.get_recent(1), ["coffee too"])
        self.assertEqual(m.search("tea"), ["Tea is great"])
        m.clear()
        self.assertEqual(len(m), 0)


if __name__ == "__main__":
    unittest.main()
