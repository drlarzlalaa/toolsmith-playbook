import argparse
import json
import sys

from . import SEVERITY, check


def main(argv=None):
    p = argparse.ArgumentParser(prog="{{pkg}}", description="{{description}}")
    p.add_argument("files", nargs="+")
    p.add_argument("--fail-on", choices=["low", "medium", "high", "never"], default="medium", help="lowest severity that makes the exit status 1 (default: medium)")
    p.add_argument("--json", action="store_true", help="print findings as JSON")
    a = p.parse_args(argv)
    results, errors = {}, []
    for path in a.files:
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                results[path] = check(fh.read())
        except OSError as e:
            errors.append("%s: cannot read (%s)" % (path, e.__class__.__name__))
    if a.json:
        print(json.dumps({"results": {k: [f.as_dict() for f in v] for k, v in results.items()}, "errors": errors}, indent=2))
    else:
        for path, findings in results.items():
            for f in findings:
                print("%s: %s" % (path, f))
        for e in errors:
            print(e, file=sys.stderr)
    if errors:
        return 2
    if a.fail_on != "never" and any(SEVERITY[f.severity] >= SEVERITY[a.fail_on] for v in results.values() for f in v):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
