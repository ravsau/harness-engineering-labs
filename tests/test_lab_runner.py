import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def runner(*args):
    return subprocess.run(["python3", str(ROOT / "lab.py"), *args], cwd=ROOT, text=True, capture_output=True)


def workspace_snapshot(workspace):
    return {
        p.relative_to(workspace).as_posix(): (p.read_bytes(), p.stat().st_mode, p.stat().st_mtime_ns)
        for p in workspace.rglob("*") if p.is_file()
    }


class RunnerTests(unittest.TestCase):
    def test_relative_workspace_works_from_checkout_and_workspace(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            workspace = Path(tmp) / 'work'
            relative = str(workspace.relative_to(ROOT))
            runner('start', '02', '--workspace', relative)
            shutil.copytree(ROOT / 'labs/02-baseline/solution', workspace, dirs_exist_ok=True)
            checked = runner('check', '02', '--workspace', relative)
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            inside = subprocess.run(['python3', str(ROOT / 'lab.py'), 'check', '02', '--workspace', '.'],
                                    cwd=workspace, text=True, capture_output=True)
            self.assertEqual(inside.returncode, 0, inside.stdout + inside.stderr)

    def test_map_accepts_readable_link_labels_and_import_only_bridge(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / 'work'
            runner('start', '03', '--workspace', str(workspace))
            shutil.copytree(ROOT / 'labs/03-map/solution', workspace, dirs_exist_ok=True)
            (workspace / 'AGENTS.md').write_text('[Run commands](docs/runbook.md)\n[App structure](architecture.md)\n[What must work](acceptance.md)\n')
            (workspace / 'CLAUDE.md').write_text('@AGENTS.md\n')
            checked = runner('check', '03', '--workspace', str(workspace))
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_baseline_starter_has_a_real_failing_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "work"
            self.assertEqual(runner("start", "02", "--workspace", str(workspace)).returncode, 0)
            result = runner("check", "02", "--workspace", str(workspace))
            self.assertEqual(result.returncode, 1)
            self.assertIn("feature-count sanity check", result.stdout)

    def test_start_does_not_overwrite_existing_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "work"
            first = runner("start", "02", "--workspace", str(workspace))
            self.assertEqual(first.returncode, 0, first.stderr)
            taskboard = workspace / "taskboard.py"
            taskboard.write_text(taskboard.read_text(encoding="utf-8") + "# learner marker\n", encoding="utf-8")
            second = runner("start", "02", "--workspace", str(workspace))
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("learner marker", taskboard.read_text(encoding="utf-8"))

    def test_independent_start_seeds_prior_solutions_then_current_starter(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "fresh"
            result = runner("start", "07", "--workspace", str(workspace))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((workspace / "taskboard.py").is_file())
            self.assertTrue((workspace / "router.py").is_file())
            self.assertEqual(runner("check", "07", "--workspace", str(workspace)).returncode, 1)

    def test_check_and_show_are_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "work"
            self.assertEqual(runner("start", "02", "--workspace", str(workspace)).returncode, 0)
            shutil.copytree(ROOT / "labs" / "02-baseline" / "solution", workspace, dirs_exist_ok=True)
            before = workspace_snapshot(workspace)
            self.assertEqual(runner("check", "02", "--workspace", str(workspace)).returncode, 0)
            self.assertEqual(runner("show", "02", "--workspace", str(workspace)).returncode, 0)
            after = workspace_snapshot(workspace)
            self.assertEqual(before, after)

    def test_all_finished_lesson_examples_pass(self):
        lesson_names = {
            "02": "02-baseline", "03": "03-map", "04": "04-guides", "05": "05-sensors",
            "06": "06-verifier", "07": "07-boundaries", "08": "08-handoff", "09": "09-shapes", "10": "10-evals",
        }
        with tempfile.TemporaryDirectory() as tmp:
            for number, name in lesson_names.items():
                workspace = Path(tmp) / number
                shutil.copytree(ROOT / "labs" / "02-baseline" / "solution", workspace)
                shutil.copytree(ROOT / "labs" / name / "solution", workspace, dirs_exist_ok=True)
                result = runner("check", number, "--workspace", str(workspace))
                self.assertEqual(result.returncode, 0, f"{number}: {result.stdout}{result.stderr}")

    def test_cumulative_solution_overlay_passes_check_all(self):
        lesson_names = {
            "02": "02-baseline", "03": "03-map", "04": "04-guides", "05": "05-sensors",
            "06": "06-verifier", "07": "07-boundaries", "08": "08-handoff", "09": "09-shapes", "10": "10-evals",
        }
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "cumulative"
            for number, name in lesson_names.items():
                started = runner("start", number, "--workspace", str(workspace))
                self.assertEqual(started.returncode, 0, f"{number}: {started.stdout}{started.stderr}")
                shutil.copytree(ROOT / "labs" / name / "solution", workspace, dirs_exist_ok=True)
            result = runner("check-all", "--workspace", str(workspace))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for name in lesson_names.values():
                self.assertIn(f"PASS {name}:", result.stdout)


if __name__ == "__main__":
    unittest.main()
