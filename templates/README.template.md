# {{pkg}}

TODO: one paragraph. What it does, for whom, that it works offline, that it uses only the standard library (Python 3.9+), and what it never does (install, send, contact the network).

```
$ python -m {{pkg}} example-input
TODO: paste REAL output from running the tool on synthetic files. Never use real customer, visitor or server data.
```

Exit status: `0` nothing at or above the threshold, `1` findings, `2` a file could not be read. `--json` prints machine-readable output.

## What it checks

TODO: a table of every finding code, its severity and what it means.

## Limits

TODO: be specific and honest. What a clean result does NOT prove, what it cannot see, where it will be wrong (false positives, unknown formats), and anything you did not measure.

## How it was checked

TODO: how each claim above was verified: what the tests compare against (an independent implementation, the standard library's own writers, a published specification), which awkward cases are tests, and which parts are only heuristics.

```
python -m unittest discover -s tests -v
```

MIT licence.
