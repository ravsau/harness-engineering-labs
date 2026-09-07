import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "labs" / "02-baseline" / "solution" / "taskboard.py"


class TaskboardTests(unittest.TestCase):
    def test_add_then_list_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            task_file = Path(tmp) / "tasks.json"
            add = subprocess.run(["python3", str(SCRIPT), "add", "record evidence", "--file", str(task_file)], text=True, capture_output=True)
            listing = subprocess.run(["python3", str(SCRIPT), "list", "--file", str(task_file)], text=True, capture_output=True)
            self.assertEqual(add.stdout.strip(), "added 1: record evidence")
            self.assertIn("1: [ ] record evidence", listing.stdout)
            self.assertEqual(json.loads(task_file.read_text(encoding="utf-8"))[0]["done"], False)


if __name__ == "__main__":
    unittest.main()
