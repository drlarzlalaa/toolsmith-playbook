#!/usr/bin/env python3
"""Create a new project folder from the playbook templates.

    python scripts/scaffold.py depaudit "Audit dependency manifests offline" --keywords "supply chain,security" --dest ~/python-space

Creates DEST/py-depaudit with the package, tests, README skeleton (full of TODO markers that
scripts/checkrepo.py refuses until they are replaced), pyproject, CI workflow, LICENSE and .gitignore.
"""
import argparse
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def scaffold(pkg, description, keywords, dest, prefix="py-"):
    if not re.fullmatch(r"[a-z][a-z0-9_]*", pkg):
        raise ValueError("package name must be lower-case letters, digits and underscores, starting with a letter: %r" % pkg)
    if '"' in description or "\n" in description:
        raise ValueError("description must be one line without double quotes")
    folder = os.path.join(dest, prefix + pkg)
    if os.path.exists(folder):
        raise FileExistsError(folder)
    kw = ", ".join('"%s"' % k.strip() for k in keywords.split(",") if k.strip())
    fill = lambda s: s.replace("{{pkg}}", pkg).replace("{{description}}", description).replace("{{keywords}}", kw)
    _write(os.path.join(folder, "LICENSE"), _read("LICENSE"))
    _write(os.path.join(folder, ".gitignore"), _read(".gitignore"))
    _write(os.path.join(folder, "README.md"), fill(_read("templates/README.template.md")))
    _write(os.path.join(folder, "pyproject.toml"), fill(_read("templates/pyproject.template.toml")))
    _write(os.path.join(folder, ".github", "workflows", "test.yml"), fill(_read("templates/test.yml.template")))
    _write(os.path.join(folder, pkg, "__init__.py"), fill(_read("templates/module.template.py")))
    _write(os.path.join(folder, pkg, "__main__.py"), fill(_read("templates/main.template.py")))
    _write(os.path.join(folder, "tests", "test_%s.py" % pkg), fill(_read("templates/test.template.py")))
    return folder


def main(argv=None):
    p = argparse.ArgumentParser(description="Create a new project from the playbook templates.")
    p.add_argument("name", help="package name, e.g. depaudit (the folder becomes py-depaudit)")
    p.add_argument("description", help="one-line description")
    p.add_argument("--keywords", default="", help="comma-separated keywords for pyproject.toml")
    p.add_argument("--dest", default=".", help="folder to create the project in")
    p.add_argument("--prefix", default="py-", help="folder name prefix (default py-)")
    a = p.parse_args(argv)
    try:
        folder = scaffold(a.name, a.description, a.keywords, a.dest, a.prefix)
    except (ValueError, FileExistsError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    print("created %s" % folder)
    print("next: replace the TODOs, then  python %s %s --run-tests" % (os.path.join("scripts", "checkrepo.py"), folder))
    return 0


if __name__ == "__main__":
    sys.exit(main())
