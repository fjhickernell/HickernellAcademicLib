#!/usr/bin/env python3
"""Initialize or audit classlib adoption in a consumer Git repository."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


DEFAULT_CLASSLIB_URL = "git@github.com:fjhickernell/HickernellAcademicLib.git"
CLASSLIB_PATH = Path("classlib")
AGENTS_PATH = Path("AGENTS.md")
CONTRACT_PATH = (
    Path(__file__).resolve().parents[1]
    / "bootstrap"
    / "consumer-agents-block.md"
)
START_MARKER = "<!-- classlib-consumer-contract:start -->"
END_MARKER = "<!-- classlib-consumer-contract:end -->"


class BootstrapError(RuntimeError):
    """A consumer does not satisfy the bootstrap contract."""


def run_git(
    repository: Path,
    *arguments: str,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run Git in *repository* and capture its text output."""

    result = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if check and result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise BootstrapError(f"git {' '.join(arguments)} failed: {detail}")
    return result


def repository_root(target: Path) -> Path:
    """Return the target Git worktree root, requiring the target to be it."""

    target = target.expanduser().resolve()
    if not target.is_dir():
        raise BootstrapError(f"consumer path is not a directory: {target}")
    result = run_git(target, "rev-parse", "--show-toplevel")
    root = Path(result.stdout.strip()).resolve()
    if target != root:
        raise BootstrapError(f"consumer path must be the repository root: {root}")
    return root


def canonical_contract() -> str:
    """Read and validate the authoritative managed AGENTS block."""

    try:
        contract = CONTRACT_PATH.read_text(encoding="utf-8").strip()
    except OSError as error:
        raise BootstrapError(f"cannot read canonical contract: {error}") from error
    if contract.count(START_MARKER) != 1 or contract.count(END_MARKER) != 1:
        raise BootstrapError("canonical contract has invalid managed markers")
    if contract.index(START_MARKER) > contract.index(END_MARKER):
        raise BootstrapError("canonical contract markers are out of order")
    return contract


def gitmodule_value(root: Path, key: str) -> str | None:
    """Read one value from the consumer's .gitmodules file."""

    modules = root / ".gitmodules"
    if not modules.is_file():
        return None
    result = run_git(
        root,
        "config",
        "-f",
        str(modules),
        "--get",
        key,
        check=False,
    )
    if result.returncode:
        return None
    return result.stdout.strip()


def recorded_gitlink(root: Path) -> str | None:
    """Return the recorded classlib commit when its index entry is a gitlink."""

    result = run_git(root, "ls-files", "--stage", "--", str(CLASSLIB_PATH))
    line = result.stdout.strip()
    if not line:
        return None
    fields = line.split()
    if len(fields) < 4 or fields[0] != "160000":
        return None
    return fields[1]


def initialized_submodule_head(root: Path) -> str | None:
    """Return the initialized classlib HEAD, or None when unavailable."""

    classlib = root / CLASSLIB_PATH
    result = run_git(classlib, "rev-parse", "HEAD", check=False)
    if result.returncode:
        return None
    return result.stdout.strip()


def verify_submodule(root: Path, *, require_initialized: bool = True) -> list[str]:
    """Return contract violations for the consumer's classlib submodule."""

    errors: list[str] = []
    path = gitmodule_value(root, "submodule.classlib.path")
    url = gitmodule_value(root, "submodule.classlib.url")
    if path != str(CLASSLIB_PATH):
        errors.append(".gitmodules must define submodule.classlib.path = classlib")
    if not url:
        errors.append(".gitmodules must define submodule.classlib.url")

    recorded = recorded_gitlink(root)
    if not recorded:
        errors.append("classlib must be tracked as a Git submodule gitlink")
        return errors

    if require_initialized:
        head = initialized_submodule_head(root)
        if not head:
            errors.append("classlib submodule is not initialized")
        elif head != recorded:
            errors.append(
                "initialized classlib HEAD does not match the recorded gitlink "
                f"({head[:12]} != {recorded[:12]})"
            )
        elif not (root / CLASSLIB_PATH / "AGENTS.md").is_file():
            errors.append("the pinned classlib commit does not contain AGENTS.md")
    return errors


def add_or_initialize_submodule(root: Path, classlib_url: str) -> None:
    """Add a missing submodule or initialize the already recorded commit."""

    path = gitmodule_value(root, "submodule.classlib.path")
    url = gitmodule_value(root, "submodule.classlib.url")
    recorded = recorded_gitlink(root)

    if path is None and url is None and recorded is None:
        destination = root / CLASSLIB_PATH
        if destination.exists():
            raise BootstrapError(
                "classlib path already exists but is not a recorded submodule"
            )
        run_git(root, "submodule", "add", "--", classlib_url, str(CLASSLIB_PATH))
    else:
        structural_errors = verify_submodule(root, require_initialized=False)
        if structural_errors:
            raise BootstrapError("; ".join(structural_errors))

        head = initialized_submodule_head(root)
        if head and head != recorded:
            raise BootstrapError(
                "existing classlib checkout differs from the recorded gitlink; "
                "refusing to change either pointer"
            )
        if not head:
            run_git(
                root,
                "submodule",
                "update",
                "--init",
                "--recursive",
                "--",
                str(CLASSLIB_PATH),
            )

    errors = verify_submodule(root)
    if errors:
        raise BootstrapError("; ".join(errors))


def contract_bounds(content: str) -> tuple[int, int] | None:
    """Locate one well-formed managed contract, rejecting ambiguous markers."""

    starts = content.count(START_MARKER)
    ends = content.count(END_MARKER)
    if starts == 0 and ends == 0:
        return None
    if starts != 1 or ends != 1:
        raise BootstrapError(
            "AGENTS.md has malformed classlib contract markers; review manually"
        )
    start = content.index(START_MARKER)
    end_start = content.index(END_MARKER)
    if end_start < start:
        raise BootstrapError(
            "AGENTS.md has out-of-order classlib contract markers; review manually"
        )
    end = end_start + len(END_MARKER)
    return start, end


def install_contract(root: Path) -> bool:
    """Install or update the managed AGENTS contract; return whether it changed."""

    contract = canonical_contract()
    agents = root / AGENTS_PATH
    try:
        content = agents.read_text(encoding="utf-8") if agents.exists() else ""
    except OSError as error:
        raise BootstrapError(f"cannot read {agents}: {error}") from error

    bounds = contract_bounds(content)
    if bounds:
        start, end = bounds
        updated = content[:start] + contract + content[end:]
    elif content:
        if content.endswith("\n\n"):
            separator = ""
        elif content.endswith("\n"):
            separator = "\n"
        else:
            separator = "\n\n"
        updated = content + separator + contract + "\n"
    else:
        updated = contract + "\n"

    if updated == content:
        return False
    try:
        agents.write_text(updated, encoding="utf-8")
    except OSError as error:
        raise BootstrapError(f"cannot write {agents}: {error}") from error
    return True


def preflight_contract(root: Path) -> None:
    """Reject an unreadable or structurally ambiguous AGENTS contract."""

    canonical_contract()
    agents = root / AGENTS_PATH
    if not agents.exists():
        return
    try:
        content = agents.read_text(encoding="utf-8")
    except OSError as error:
        raise BootstrapError(f"cannot read {agents}: {error}") from error
    contract_bounds(content)


def verify_contract(root: Path) -> list[str]:
    """Return violations of the root AGENTS managed contract."""

    agents = root / AGENTS_PATH
    if not agents.is_file():
        return ["root AGENTS.md is missing"]
    try:
        content = agents.read_text(encoding="utf-8")
        bounds = contract_bounds(content)
    except (OSError, BootstrapError) as error:
        return [str(error)]
    if bounds is None:
        return ["root AGENTS.md does not contain the classlib consumer contract"]
    start, end = bounds
    if content[start:end] != canonical_contract():
        return ["root AGENTS.md contains an outdated or modified consumer contract"]
    return []


def check_consumer(root: Path) -> list[str]:
    """Return every minimal consumer-contract violation."""

    return verify_submodule(root) + verify_contract(root)


def command_init(args: argparse.Namespace) -> int:
    """Initialize one consumer repository."""

    root = repository_root(args.consumer)
    preflight_contract(root)
    add_or_initialize_submodule(root, args.classlib_url)
    changed = install_contract(root)
    errors = check_consumer(root)
    if errors:
        raise BootstrapError("; ".join(errors))
    action = "installed or updated" if changed else "already current"
    print(f"classlib consumer bootstrap is valid: {root}")
    print(f"AGENTS contract: {action}")
    return 0


def command_check(args: argparse.Namespace) -> int:
    """Audit one consumer repository without changing it."""

    root = repository_root(args.consumer)
    errors = check_consumer(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"classlib consumer bootstrap is valid: {root}")
    return 0


def parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    result = argparse.ArgumentParser(
        description="Initialize or audit classlib consumer adoption."
    )
    subparsers = result.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init", help="add or verify classlib and install the AGENTS contract"
    )
    init_parser.add_argument("consumer", type=Path)
    init_parser.add_argument(
        "--classlib-url",
        default=DEFAULT_CLASSLIB_URL,
        help="submodule URL used only when classlib is not already recorded",
    )
    init_parser.set_defaults(handler=command_init)

    check_parser = subparsers.add_parser(
        "check", help="read-only audit of the classlib consumer contract"
    )
    check_parser.add_argument("consumer", type=Path)
    check_parser.set_defaults(handler=command_check)
    return result


def main() -> int:
    """Run the requested bootstrap operation."""

    args = parser().parse_args()
    try:
        return args.handler(args)
    except BootstrapError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
