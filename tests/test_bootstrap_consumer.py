from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = REPOSITORY_ROOT / "tools" / "bootstrap_consumer.py"
START_MARKER = "<!-- classlib-consumer-contract:start -->"


def run(
    *arguments: str,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        list(arguments),
        cwd=cwd,
        env=env,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if check and result.returncode:
        raise AssertionError(
            f"command failed: {' '.join(arguments)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def initialize_git_repository(path: Path) -> None:
    path.mkdir()
    run("git", "init", "-q", cwd=path)
    run("git", "config", "user.name", "Bootstrap Test", cwd=path)
    run("git", "config", "user.email", "bootstrap@example.invalid", cwd=path)


class ConsumerBootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.source = self.root / "classlib-source"
        initialize_git_repository(self.source)
        (self.source / "AGENTS.md").write_text(
            "# Shared test guidance\n", encoding="utf-8"
        )
        (self.source / "bootstrap").mkdir()
        (self.source / "tools").mkdir()
        shutil.copy2(
            REPOSITORY_ROOT / "bootstrap" / "consumer-agents-block.md",
            self.source / "bootstrap" / "consumer-agents-block.md",
        )
        shutil.copy2(
            BOOTSTRAP,
            self.source / "tools" / "bootstrap_consumer.py",
        )
        run("git", "add", "AGENTS.md", "bootstrap", "tools", cwd=self.source)
        run("git", "commit", "-q", "-m", "Initial classlib", cwd=self.source)

        self.consumer = self.root / "consumer"
        initialize_git_repository(self.consumer)
        self.environment = os.environ.copy()
        self.environment["GIT_ALLOW_PROTOCOL"] = "file"

    def bootstrap(
        self, operation: str, *, check: bool = True
    ) -> subprocess.CompletedProcess[str]:
        arguments = [
            sys.executable,
            str(BOOTSTRAP),
            operation,
            str(self.consumer),
        ]
        if operation == "init":
            arguments.extend(["--classlib-url", str(self.source)])
        return run(*arguments, env=self.environment, check=check)

    def pinned_check(self) -> subprocess.CompletedProcess[str]:
        return run(
            sys.executable,
            str(self.consumer / "classlib" / "tools" / "bootstrap_consumer.py"),
            "check",
            str(self.consumer),
            env=self.environment,
        )

    def test_init_is_idempotent_and_check_succeeds(self) -> None:
        first = self.bootstrap("init")
        agents_after_first = (self.consumer / "AGENTS.md").read_text(
            encoding="utf-8"
        )
        status_after_first = run(
            "git", "status", "--short", cwd=self.consumer
        ).stdout

        second = self.bootstrap("init")
        agents_after_second = (self.consumer / "AGENTS.md").read_text(
            encoding="utf-8"
        )
        status_after_second = run(
            "git", "status", "--short", cwd=self.consumer
        ).stdout
        checked = self.pinned_check()
        status_after_check = run(
            "git", "status", "--short", cwd=self.consumer
        ).stdout

        self.assertIn("bootstrap is valid", first.stdout)
        self.assertIn("AGENTS contract: already current", second.stdout)
        self.assertEqual(agents_after_first, agents_after_second)
        self.assertEqual(status_after_first, status_after_second)
        self.assertEqual(status_after_second, status_after_check)
        self.assertEqual(agents_after_first.count(START_MARKER), 1)
        self.assertIn("bootstrap is valid", checked.stdout)

    def test_init_preserves_existing_agents_content(self) -> None:
        local_guidance = (
            "# Local repository instructions\n\n"
            "## Explicit local exceptions\n\n"
            "Use the event-specific title layout because the venue requires it.\n"
        )
        (self.consumer / "AGENTS.md").write_text(
            local_guidance, encoding="utf-8"
        )

        self.bootstrap("init")
        updated = (self.consumer / "AGENTS.md").read_text(encoding="utf-8")

        self.assertTrue(updated.startswith(local_guidance))
        self.assertEqual(updated.count(START_MARKER), 1)

    def test_init_updates_only_the_managed_contract(self) -> None:
        local_prefix = "# Local repository instructions\n\nLocal prefix.\n"
        (self.consumer / "AGENTS.md").write_text(
            local_prefix, encoding="utf-8"
        )
        self.bootstrap("init")
        agents = self.consumer / "AGENTS.md"
        local_suffix = "\n## Explicit local exceptions\n\nLocal suffix.\n"
        modified = agents.read_text(encoding="utf-8").replace(
            "Keep universal guidance", "Copy universal guidance"
        )
        agents.write_text(modified + local_suffix, encoding="utf-8")

        self.bootstrap("init")
        updated = agents.read_text(encoding="utf-8")

        self.assertTrue(updated.startswith(local_prefix))
        self.assertTrue(updated.endswith(local_suffix))
        self.assertIn("Keep universal guidance", updated)
        self.assertNotIn("Copy universal guidance", updated)

    def test_check_reports_missing_bootstrap(self) -> None:
        result = self.bootstrap("check", check=False)

        self.assertEqual(result.returncode, 1)
        self.assertIn(".gitmodules", result.stderr)
        self.assertIn("root AGENTS.md is missing", result.stderr)

    def test_check_reports_modified_contract(self) -> None:
        self.bootstrap("init")
        agents = self.consumer / "AGENTS.md"
        agents.write_text(
            agents.read_text(encoding="utf-8").replace(
                "Keep universal guidance", "Copy universal guidance"
            ),
            encoding="utf-8",
        )

        result = self.bootstrap("check", check=False)

        self.assertEqual(result.returncode, 1)
        self.assertIn("outdated or modified", result.stderr)

    def test_init_rejects_out_of_order_contract_markers(self) -> None:
        (self.consumer / "AGENTS.md").write_text(
            "<!-- classlib-consumer-contract:end -->\n"
            "Local instructions\n"
            "<!-- classlib-consumer-contract:start -->\n",
            encoding="utf-8",
        )

        result = self.bootstrap("init", check=False)

        self.assertEqual(result.returncode, 1)
        self.assertIn("out-of-order", result.stderr)
        self.assertFalse((self.consumer / ".gitmodules").exists())

    def test_init_refuses_to_change_a_different_submodule_checkout(self) -> None:
        self.bootstrap("init")
        (self.source / "second.txt").write_text("second\n", encoding="utf-8")
        run("git", "add", "second.txt", cwd=self.source)
        run("git", "commit", "-q", "-m", "Second classlib", cwd=self.source)
        run("git", "fetch", cwd=self.consumer / "classlib")
        run("git", "checkout", "-q", "FETCH_HEAD", cwd=self.consumer / "classlib")

        result = self.bootstrap("init", check=False)

        self.assertEqual(result.returncode, 1)
        self.assertIn("refusing to change either pointer", result.stderr)


if __name__ == "__main__":
    unittest.main()
