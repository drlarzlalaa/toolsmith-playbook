import contextlib
import io
import os
import tempfile
import unittest

from {{pkg}} import check
from {{pkg}}.__main__ import main


class Rules(unittest.TestCase):
    # One test per rule: a matching input AND a near-miss that must NOT match.
    def test_example_rule(self):
        self.assertEqual([f.code for f in check("nothing to see")], [])
        self.assertEqual([f.code for f in check("a TODO here")], ["EXAMPLE"])


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "a.txt")
            with open(p, "w") as fh:
                fh.write("all good\n")
            self.assertEqual(self.run_cli(p)[0], 0)
            with open(p, "w") as fh:
                fh.write("a TODO\n")
            self.assertEqual(self.run_cli(p, "--fail-on", "low")[0], 1)
            self.assertEqual(self.run_cli(os.path.join(d, "missing.txt"))[0], 2)


if __name__ == "__main__":
    unittest.main()
