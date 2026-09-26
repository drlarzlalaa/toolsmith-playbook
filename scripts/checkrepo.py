#!/usr/bin/env python3
"""Check a project folder against the playbook's definition of done.

    python scripts/checkrepo.py ../py-something [--run-tests]

Exit status 0 when every check passes, 1 when something fails, 2 when the folder does not exist.
"""
import argparse
import os
import re
import subprocess
import sys

SECRET_SHAPES = re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}|github_pat_\w{30,}|AKIA[0-9A-Z]{16}|sk-ant-[\w-]{20,}|sk-[A-Za-z0-9_-]{24,}|xox[baprs]-[\w-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----")
SKIP = {".git", "__pycache__", "node_modules", ".venv", "build", "dist"}
REQUIRED_FILES = ["LICENSE", "README.md", "pyproject.toml", ".gitignore", ".github/workflows/test.yml"]
REQUIRED_SECTIONS = [("a Limits section", re.compile(r"^#{2,3}\s+(Limits?|What it does not do)\b", re.M | re.I)),
                     ("a 'How it was checked' section", re.compile(r"^#{2,3}\s+How it was checked\b", re.M | re.I))]


def _files(root):
    for base, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for n in names:
            yield os.path.join(base, n)


def check(root, run_tests=False):
    """Return a list of (ok, message)."""
    results = []
    ok = lambda cond, msg: results.append((bool(cond), msg))
    for rel in REQUIRED_FILES:
        ok(os.path.isfile(os.path.join(root, rel)), "has %s" % rel)
    tests = os.path.join(root, "tests")
    ok(os.path.isdir(tests) and any(n.startswith("test_") and n.endswith(".py") for n in os.listdir(tests)), "has tests/test_*.py")
    readme = ""
    if os.path.isfile(os.path.join(root, "README.md")):
        with open(os.path.join(root, "README.md"), encoding="utf-8") as fh:
            readme = fh.read()
    for name, rx in REQUIRED_SECTIONS:
        ok(rx.search(readme), "README has %s" % name)
    ok("```" in readme, "README shows real output in a code block")
    ok(not re.search(r"\bTODO\b", readme), "README has no TODO markers left")
    pyproject = ""
    if os.path.isfile(os.path.join(root, "pyproject.toml")):
        with open(os.path.join(root, "pyproject.toml"), encoding="utf-8") as fh:
            pyproject = fh.read()
    ok(re.search(r"^dependencies\s*=\s*\[\s*\]", pyproject, re.M), "pyproject declares no dependencies (dependencies = [])")
    workflow = os.path.join(root, ".github", "workflows", "test.yml")
    if os.path.isfile(workflow):
        with open(workflow, encoding="utf-8") as fh:
            wf = fh.read()
        ok("unittest" in wf, "CI runs the tests")
        ok(re.search(r"run the example|run: python -m", wf), "CI also runs the tool once")
    leaks = []
    for path in _files(root):
        if os.path.basename(path).startswith(".env"):
            leaks.append(os.path.relpath(path, root) + " (an .env file)")
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except (UnicodeDecodeError, OSError):
            continue
        if SECRET_SHAPES.search(text):
            leaks.append(os.path.relpath(path, root))
    ok(not leaks, "no secret-shaped strings or .env files%s" % ((": " + ", ".join(leaks)) if leaks else ""))
    if run_tests:
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=root, capture_output=True, text=True)
        ok(r.returncode == 0, "tests pass" + ("" if r.returncode == 0 else ": " + r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ""))
    return results


def main(argv=None):
    p = argparse.ArgumentParser(description="Check a project against the playbook's definition of done.")
    p.add_argument("folder")
    p.add_argument("--run-tests", action="store_true")
    a = p.parse_args(argv)
    if not os.path.isdir(a.folder):
        print("%s: not a folder" % a.folder, file=sys.stderr)
        return 2
    results = check(a.folder, a.run_tests)
    for good, msg in results:
        print("%s  %s" % ("ok  " if good else "FAIL", msg))
    failed = sum(1 for good, _ in results if not good)
    print("%d check(s), %d failed" % (len(results), failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
