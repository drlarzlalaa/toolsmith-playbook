import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import catalog  # noqa: E402
import checkrepo  # noqa: E402
import scaffold  # noqa: E402


def run(main, *args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(args))
    return code, out.getvalue(), err.getvalue()


class Catalog(unittest.TestCase):
    def setUp(self):
        self.rules, self.fallback = catalog.load_rules(os.path.join(ROOT, "categories.json"))

    def cat(self, name, desc=""):
        return catalog.categorise({"name": name, "description": desc}, self.rules, self.fallback)

    def test_prefix_rules_come_first(self):
        self.assertEqual(self.cat("larzscript-sat", "A DPLL SAT solver; every verdict checked against brute force"), "Larzscript: simulations, algorithms and science")
        self.assertEqual(self.cat("larz-encode", "Base64 and URL encoding in Larzscript"), "Larzscript: utilities")
        self.assertEqual(self.cat("larz-meter", "usage meter"), "LarzOS money tools and showcases")
        self.assertEqual(self.cat("larzos-showcase", "Showcase of LarzOS"), "LarzOS money tools and showcases")

    def test_keyword_rules_and_order(self):
        self.assertEqual(self.cat("py-agentlint", "Lint MCP configs and CLAUDE.md"), "AI agents and LLM tooling")
        self.assertEqual(self.cat("py-depaudit", "Audit requirements.txt for supply-chain risks"), "Security and supply chain")
        self.assertEqual(self.cat("py-unsubcheck", "Check one-click unsubscribe in .eml files"), "Email and deliverability")
        self.assertEqual(self.cat("py-sitemapcheck", "Check sitemap.xml"), "Web, SEO and content")
        self.assertEqual(self.cat("py-csvdiff", "Compare two CSV files"), "Data and files")
        self.assertEqual(self.cat("py-cronnext", "Next run times of a cron expression"), "DevOps and infrastructure")
        self.assertEqual(self.cat("py-zzz", "Something entirely different"), "Other")
        self.assertEqual(self.cat("py-zzz", None), "Other")
        for word in ["different", "profile", "credit", "login", "curl", "catalogue", "voltage"]:       # substrings of keywords must not match
            self.assertEqual(self.cat("py-zzz", "About %s things" % word), "Other", word)
        self.assertEqual(self.cat("py-envcheck", "Lint .env files"), "DevOps and infrastructure")
        self.assertEqual(self.cat("py-linkaudit", "Audit outbound links"), "Web, SEO and content")

    def test_overrides_win_over_rules(self):
        repo = {"name": "py-csvdoctor", "description": "Diagnose CSV files: duplicate headers, page breaks and links"}
        self.assertEqual(catalog.categorise(repo, self.rules, self.fallback), "Web, SEO and content")
        self.assertEqual(catalog.categorise(repo, self.rules, self.fallback, {"py-csvdoctor": "Data and files"}), "Data and files")
        self.assertEqual(catalog.categorise(repo, self.rules, self.fallback, {"py-other": "X"}), "Web, SEO and content")

    def test_override_to_a_category_without_a_rule_is_still_listed(self):
        md = catalog.build([{"name": "py-q", "description": "x", "url": "u"}], self.rules, self.fallback, overrides={"py-q": "Brand new area"})
        self.assertIn("## Brand new area", md)
        self.assertIn("| Brand new area | 1 |", md)

    def test_every_rule_regex_compiles_and_categories_are_unique(self):
        with open(os.path.join(ROOT, "categories.json")) as fh:
            data = json.load(fh)
        names = [r["category"] for r in data["rules"]]
        self.assertEqual(len(names), len(set(names)))

    def test_build_output(self):
        repos = [{"name": "py-b", "description": "Lint MCP configs", "url": "https://x/py-b"},
                 {"name": "py-a", "description": "Compare two CSV files | with a pipe", "url": "https://x/py-a"},
                 {"name": "py-c", "description": "", "url": "https://x/py-c"},
                 {"name": "larzscript-q", "description": "queues", "url": "https://x/larzscript-q"}]
        md = catalog.build(repos, self.rules, self.fallback)
        self.assertIn("**4 repositories** in 4 categories.", md)
        self.assertLess(md.index("## Larzscript: simulations"), md.index("## AI agents"))
        self.assertLess(md.index("## AI agents"), md.index("## Data and files"))
        self.assertIn("| [py-a](https://x/py-a) | Compare two CSV files \\| with a pipe |", md)
        self.assertIn("(no description: add one)", md)
        self.assertIn("matched no rule", md)
        self.assertTrue(md.endswith("\n"))

    def test_cli_reads_a_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "r.json")
            with open(p, "w") as fh:
                json.dump([{"name": "py-x", "description": "Compare CSV files", "url": "https://x"}], fh)
            code, out, _ = run(catalog.main, p)
            self.assertEqual(code, 0)
            self.assertIn("## Data and files", out)


class Scaffold(unittest.TestCase):
    def test_creates_project_that_fails_only_on_todos_then_passes(self):
        with tempfile.TemporaryDirectory() as d:
            folder = scaffold.scaffold("demo", "Check demo things offline", "demo, example", d)
            self.assertEqual(os.path.basename(folder), "py-demo")
            for rel in ["LICENSE", ".gitignore", "README.md", "pyproject.toml", ".github/workflows/test.yml", "demo/__init__.py", "demo/__main__.py", "tests/test_demo.py"]:
                self.assertTrue(os.path.isfile(os.path.join(folder, rel)), rel)
            with open(os.path.join(folder, "pyproject.toml")) as fh:
                py = fh.read()
            self.assertIn('name = "demo"', py)
            self.assertIn('keywords = ["demo", "example"]', py)
            self.assertNotIn("{{", py)
            results = checkrepo.check(folder, run_tests=True)
            failed = [m for ok, m in results if not ok]
            self.assertEqual(failed, ["README has no TODO markers left"])
            readme = os.path.join(folder, "README.md")
            with open(readme) as fh:
                text = fh.read()
            with open(readme, "w") as fh:
                fh.write(text.replace("TODO", "Done"))
            self.assertEqual([m for ok, m in checkrepo.check(folder, run_tests=True) if not ok], [])

    def test_scaffolded_tool_actually_runs(self):
        with tempfile.TemporaryDirectory() as d:
            folder = scaffold.scaffold("demo", "Check demo things", "", d)
            sample = os.path.join(d, "s.txt")
            with open(sample, "w") as fh:
                fh.write("a TODO here\n")
            r = subprocess.run([sys.executable, "-m", "demo", sample], cwd=folder, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)                     # low severity, default threshold is medium
            r = subprocess.run([sys.executable, "-m", "demo", sample, "--fail-on", "low"], cwd=folder, capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertIn("[LOW] EXAMPLE", r.stdout)

    def test_rejects_bad_names_and_existing_folders(self):
        with tempfile.TemporaryDirectory() as d:
            for bad in ["Demo", "1demo", "de-mo", ""]:
                with self.assertRaises(ValueError):
                    scaffold.scaffold(bad, "x", "", d)
            with self.assertRaises(ValueError):
                scaffold.scaffold("demo", 'has "quotes"', "", d)
            scaffold.scaffold("demo", "x", "", d)
            with self.assertRaises(FileExistsError):
                scaffold.scaffold("demo", "x", "", d)
            self.assertEqual(run(scaffold.main, "demo", "x", "--dest", d)[0], 2)


class CheckRepo(unittest.TestCase):
    def make_good(self, d):
        folder = scaffold.scaffold("demo", "Check demo things", "", d)
        readme = os.path.join(folder, "README.md")
        with open(readme) as fh:
            text = fh.read()
        with open(readme, "w") as fh:
            fh.write(text.replace("TODO", "Done"))
        return folder

    def failures(self, folder):
        return [m for ok, m in checkrepo.check(folder) if not ok]

    def test_each_rule_fails_on_its_own(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_good(d)
            self.assertEqual(self.failures(folder), [])
            os.remove(os.path.join(folder, "LICENSE"))
            self.assertEqual(self.failures(folder), ["has LICENSE"])
            with open(os.path.join(folder, "LICENSE"), "w") as fh:
                fh.write("MIT")
            readme = os.path.join(folder, "README.md")
            with open(readme) as fh:
                text = fh.read()
            with open(readme, "w") as fh:
                fh.write(text.replace("## Limits", "## Notes"))
            self.assertEqual(self.failures(folder), ["README has a Limits section"])
            with open(readme, "w") as fh:
                fh.write(text.replace("## How it was checked", "## Testing"))
            self.assertEqual(self.failures(folder), ["README has a 'How it was checked' section"])
            with open(readme, "w") as fh:
                fh.write(text)
            pj = os.path.join(folder, "pyproject.toml")
            with open(pj) as fh:
                p = fh.read()
            with open(pj, "w") as fh:
                fh.write(p.replace("dependencies = []", 'dependencies = ["requests"]'))
            self.assertEqual(self.failures(folder), ["pyproject declares no dependencies (dependencies = [])"])

    def test_secret_shapes_and_env_files_are_caught(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_good(d)
            fake = "gh" + "p_" + "A1b2C3d4" * 5                     # assembled so this file holds no token-shaped string
            with open(os.path.join(folder, "tests", "test_demo.py"), "a") as fh:
                fh.write("\nTOKEN = %r\n" % fake)
            bad = [m for m in self.failures(folder)]
            self.assertEqual(len(bad), 1)
            self.assertIn("test_demo.py", bad[0])
            self.assertNotIn(fake, bad[0])                           # the report must not echo the secret
            with open(os.path.join(folder, "tests", "test_demo.py")) as fh:
                lines = fh.read().splitlines()
            with open(os.path.join(folder, "tests", "test_demo.py"), "w") as fh:
                fh.write("\n".join(l for l in lines if "TOKEN" not in l) + "\n")
            self.assertEqual(self.failures(folder), [])
            with open(os.path.join(folder, ".env"), "w") as fh:
                fh.write("A=1\n")
            self.assertIn(".env", self.failures(folder)[0])

    def test_failing_tests_are_reported(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_good(d)
            with open(os.path.join(folder, "tests", "test_demo.py"), "a") as fh:
                fh.write("\n\nclass Broken(unittest.TestCase):\n    def test_x(self):\n        self.assertEqual(1, 2)\n")
            results = checkrepo.check(folder, run_tests=True)
            self.assertTrue(any(not ok and m.startswith("tests pass") for ok, m in results))
            self.assertEqual(run(checkrepo.main, folder, "--run-tests")[0], 1)

    def test_cli(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_good(d)
            code, out, _ = run(checkrepo.main, folder, "--run-tests")
            self.assertEqual(code, 0)
            self.assertIn("0 failed", out)
            self.assertEqual(run(checkrepo.main, os.path.join(d, "nope"))[0], 2)

    def test_this_repository_passes_its_own_template_rules_for_the_files_it_has(self):
        results = dict((m, ok) for ok, m in checkrepo.check(ROOT))
        for rel in ["LICENSE", ".gitignore", ".github/workflows/test.yml"]:
            self.assertTrue(results["has %s" % rel], rel)


if __name__ == "__main__":
    unittest.main()
