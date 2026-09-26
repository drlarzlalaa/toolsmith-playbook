# Toolsmith Playbook

The working method behind a growing collection of small, offline, standard-library tools: how to find a real need, build a tool that meets it, prove it works, publish it, and keep the collection organised as it grows.

| File | What it is |
| --- | --- |
| [`PLAYBOOK.md`](PLAYBOOK.md) | The method, start to finish: principles, research, scoring, building, verifying, documenting, publishing, growing, safety, checklist. |
| [`RESEARCH-LOG.md`](RESEARCH-LOG.md) | Dated research sessions with queries, sources and what each changed. |
| [`BACKLOG.md`](BACKLOG.md) | Ranked candidate tools with evidence and status. |
| [`CATALOG.md`](CATALOG.md) | Every published repository by category. Generated. |
| [`categories.json`](categories.json) | The rules and overrides that decide the catalog's categories. |
| [`templates/`](templates) | README, `pyproject.toml`, CI workflow and code skeletons. |
| [`scripts/`](scripts) | `scaffold.py` (new project), `checkrepo.py` (definition of done), `catalog.py` (regenerate the catalog). |

```
$ python scripts/scaffold.py depaudit2 "Audit dependency manifests offline" --keywords "supply chain,security" --dest ~/python-space
created ~/python-space/py-depaudit2
next: replace the TODOs, then  python scripts/checkrepo.py ~/python-space/py-depaudit2 --run-tests

$ python scripts/checkrepo.py ~/python-space/py-depaudit2 --run-tests
ok    has LICENSE
ok    has README.md
ok    has pyproject.toml
ok    has .gitignore
ok    has .github/workflows/test.yml
ok    has tests/test_*.py
ok    README has a Limits section
ok    README has a 'How it was checked' section
ok    README shows real output in a code block
FAIL  README has no TODO markers left
ok    pyproject declares no dependencies (dependencies = [])
ok    CI runs the tests
ok    CI also runs the tool once
ok    no secret-shaped strings or .env files
ok    tests pass
15 check(s), 1 failed
```

(A freshly scaffolded project fails `checkrepo.py` on purpose until its README TODOs are replaced with real output, limits and verification notes.)

## Using it

1. Read section 1 (principles) and section 3 (research) of the playbook.
2. Add research to `RESEARCH-LOG.md`, ideas to `BACKLOG.md`.
3. Build with `scripts/scaffold.py`, finish with `scripts/checkrepo.py --run-tests`.
4. Publish, wait for CI, then regenerate the catalog: `python scripts/catalog.py --from-gh OWNER > CATALOG.md`.

Standard library only, Python 3.9+. Tests: `python -m unittest discover -s tests -v`.

## How it was checked

The scripts have tests: categorisation order and the near-miss keywords that a naive rule gets wrong ("different" is not "diff", "profile" is not "file"), overrides, catalog output, scaffolding a project and running its generated tests, that a fresh scaffold fails only on the README TODOs and passes once they are replaced, that each `checkrepo.py` rule fails on its own, that secret-shaped strings and `.env` files are caught without the report echoing the secret, and the command-line exit codes. The playbook's prose describes practice, not a measurement: its claims about what worked are from building the first repositories, not from a controlled comparison.

MIT licence.
