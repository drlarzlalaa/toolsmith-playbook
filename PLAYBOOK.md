# The Toolsmith Playbook

How to find a real need, build a small tool that meets it, prove it works, publish it, and keep the whole collection growing without it turning into a pile. Written from what worked, and what went wrong, while building the first 120 repositories.

The loop:

```
research -> shortlist -> build -> verify -> publish -> review -> (back to research)
```

Every stage has a rule below, a script where a script helps, and a file where the result is recorded.

## 1. Principles

These decide arguments. When two rules conflict, the earlier one wins.

1. **Never claim what you did not verify.** A README states what was checked and what was not. If a number cannot be measured (for example a token estimate with no real tokenizer to compare against), say that, and say how the reader can calibrate it. A tool that overstates itself is worse than no tool.
2. **Real data never goes into a repository.** Fixtures are synthetic or built with the standard library's own writers. No customer, visitor, subscriber or server data, no addresses, no IPs, no credentials, not even "just as an example". Output shown in a README comes from running the tool on made-up files.
3. **Zero dependencies, offline, read-only by default.** Standard library only. A tool reads what it is given and reports. It does not install, send, delete or call the network unless that is its whole purpose and the README says so up front.
4. **Small and sharp.** One job, one command, a few hundred lines. If a second job appears, it is a second tool.
5. **A clean result is not a proof.** Heuristic tools say so in a `Limits` section, and name what a pass does not prove.
6. **Check before you assert, including about your own work.** Verify a file, a folder or a service is what you think it is before you delete it, describe it, or build on it.

## 2. Language choice

- **Larzscript** is the default for new code on LarzOS and is used for the `larzscript-*` simulations and `larz-*` utilities. Those are verified by comparing against an independent Python reference or a published sequence.
- **Python (standard library only)** is used for the `py-*` real-world tools, where the audience expects `python -m tool file`. Use it when the user asks for it, or when the tool needs an ecosystem Larzscript does not have (email parsing, JSON, archives, the `email`, `zipfile`, `sqlite3` modules).
- Pick one per tool and do not mix. Do not add a third-party dependency to either.

## 3. Research: finding what people need

**Goal:** a ranked list of problems that are real, current, not already solved well, and solvable offline in a small tool.

### 3.1 Where to look

| Source | What it tells you | How |
| --- | --- | --- |
| Developer surveys and "pain point" analyses | What people complain about, with numbers | Search "developer pain points 2026 survey", "state of code developer survey" |
| Platform rule changes | Hard deadlines people must meet | Gmail/Yahoo/Microsoft bulk-sender rules, FTC endorsement rules, browser and package-registry policy changes |
| GitHub trending and "awesome" lists | Which categories are growing, and which are crowded | Search "GitHub trending 2026 fastest growing", then read the top repos' issues |
| Issue trackers of popular tools | Recurring unmet requests | Search issues sorted by reactions for "feature request" and "wish" |
| Q&A sites and forums | Repeated "how do I check whether..." questions | Search the question, count how many near-duplicates exist |
| The estate itself | Problems this business actually has (EarnifyHub, the Mailer, the affiliate and creator audience) | The server's own logs and tickets, **never copied into a repo** |

Record every research session in [`RESEARCH-LOG.md`](RESEARCH-LOG.md): date, queries, what was found, and links. A conclusion with no source does not go in the backlog.

**Read the primary source before you write "checked against".** Search results and summaries are leads, not sources. Open the vendor's or standard's own page, and record in the log which sources you read in full and which you only saw summarised. Say the same in the tool's README. (Reading the actual vendor pages for the crawler list found a missing bot and a token the vendor no longer documents.)

### 3.2 Scoring an opportunity

Score each candidate 0 to 3 on each line, then add. Build the highest scores first. Anything scoring 0 on a line marked **gate** is dropped or reshaped.

| Line | 0 | 3 |
| --- | --- | --- |
| **Evidence of need** (gate) | One person's guess | Several independent sources, with numbers or deadlines |
| **Gap** | Excellent free tools already exist | Nothing focused, or only paid or online-only tools |
| **Offline and verifiable** (gate) | Needs the network, or has no ground truth to test against | Every claim can be tested against a spec, a standard-library implementation or constructed fixtures |
| **Estate fit** | No link to the audience | Directly helps the estate's sites, mail or users |
| **Size** | Weeks of work | One sitting |

Also ask two questions before starting: *is a tool the right answer, or is it really a guide?* and *does this overlap a repository we already have?* Check [`CATALOG.md`](CATALOG.md) first. If overlap exists, extend the old tool or write a sharper one for the gap (`py-unsubcheck` exists because `py-mailtrace` only notes whether the `-Post` header is present, and does not check its exact value, the HTTPS rule or DKIM coverage).

### 3.3 Where results go

`BACKLOG.md` holds the ranked candidates with their evidence and status. Move an entry to *building*, then *published* with the repo name, or to *dropped* with the reason. Dropped ideas stay in the file so they are not researched twice.

## 4. Building

### 4.1 Layout

Use `scripts/scaffold.py` to create the standard layout:

```
python scripts/scaffold.py NAME "One-line description" --keywords "a,b,c" --dest ~/python-space
```

```
py-NAME/
  NAME/__init__.py      the library: pure functions, no printing
  NAME/__main__.py      the command line: argparse, printing, exit codes
  tests/test_NAME.py    unittest, no other test framework
  README.md
  pyproject.toml        dependencies = []
  .github/workflows/test.yml
  LICENSE  .gitignore
```

Keep the library and the command line apart: the library returns findings, the command line prints them. That makes the tests easy.

### 4.2 Command-line conventions

Follow these so every tool feels the same.

- Exit status: `0` nothing at or above the threshold, `1` findings, `2` an input could not be read or parsed.
- `--json` for machine-readable output. Print JSON with `ensure_ascii` so hidden characters are visible in it.
- `--fail-on low|medium|high|never` (default `medium`) for tools that grade findings. Severities are `low`, `medium`, `high`.
- Findings print one per line: `where: [SEVERITY] CODE subject: message`. Codes are stable, upper-case, and listed in the README.
- Read files with `errors="replace"`. Never crash on odd input; report it.
- Walk folders skipping `.git`, `node_modules`, virtual environments and build output.

### 4.3 Writing rules that do not cry wolf

False positives kill a tool faster than missed detections. Rules of thumb learned the hard way:

- **Write the near-miss test first.** For every rule, write one input that must match and one that looks similar but must not. Real examples that a first draft got wrong: `Bash(python -m unittest:*)` is not a blanket "run any Python" permission; "Do not tell users their passwords" is not an instruction to hide something from the user; the word "different" is not the word "diff"; a first draft of a pattern that stopped at the dot in `~/.ssh`.
- **Anchor keywords.** Match whole words or specific suffixes, not substrings.
- **Say "one edit away from a popular name, check it" not "typosquat".** Report what the tool observed, not a verdict it cannot support.
- **Grade severity by consequence.** High means "act now", medium means "should be looked at", low means "worth knowing".

## 5. Verifying

A test suite is the tool's proof. It must check the tool against something the tool did not produce.

| Ground truth | Use it when | Example |
| --- | --- | --- |
| A published specification or worked examples | A standard exists | RFC 8058 header rules; the semver.org examples |
| The standard library | It implements the same thing | Compare against `ipaddress`, `hashlib`, `zlib`, `datetime` |
| Constructed fixtures made by the standard library's writers | Formats (zip, tar, gzip, sqlite, wav, email) | `zipfile` builds the test archive, not hand-typed bytes |
| An independent reference implementation | Algorithms | A second implementation, or brute force on small inputs |
| Properties | No single right answer | Never decreases when text is added; repeating input N times gives N times the result; sorting is stable |

**Calibrate severities against real files, not only the specification.** A strict reading of a format flags things every real file does. Run the first version over real samples, look at each kind of finding, and ask "is this the file's fault or the tool's?" Then set levels by consequence: **error** for what the format requires or what makes the file unusable, **warn** for departures an agent or parser may mishandle, **info** for style. In the `llms.txt` checker this turned two wrong errors into warnings and found three genuine parser bugs (underlined headings, URLs containing parentheses, nested bullets). Cap repeated findings in the output (five per kind, with `--all`) so one habit repeated 121 times does not bury everything else.

**Test the safe pattern, not only the unsafe one.** For any checker that reports a problem, also build the case where the problem is legitimately handled (a consent platform, a fixed pin, a signed header) and make sure the tool says so or stays quiet. A first version of `py-consentaudit` reported "tracker present" on a page that gates it behind a consent banner; running on real pages exposed that. Also keep findings about **your own systems out of public repositories**: a README shows synthetic examples and says how the tool was validated, while what it found on real systems goes to the owner and, in aggregate, the private research log.

**Then run it on real data, without keeping the data.** Fixtures prove the tool does what you think the format is; real files show what the format actually is. For tools that read files a working system produces (mail reports, logs, headers), run the tool once, read-only, over real samples: copy the tool (not the data) to where the data lives, run it, print only aggregate results (counts, failure kinds), and delete the temporary copy. Record the sample size and the outcome in the README and the research log ("229 real reports from eight reporters, all parsed"), and never commit the samples, addresses or domains. Anything that fails on real data becomes a new fixture built from the standard library's writers.

Also test: empty input, truncated input, huge input, odd encodings, and every exit code through the real command line. Tools that read untrusted files (reports, archives, XML) must also be defensive, and tested that way: refuse DOCTYPE and entity declarations, cap decompressed size for gzip and zip members, and report corrupt input as an error rather than a crash. Tests that build secrets must assemble them at run time (`"gh" + "p_" + ...`) so the repository never contains a token-shaped string.

**When a standard-library module is missing on an older Python, write a fallback and verify it three ways.** (Example: `tomllib` exists only on 3.11+, so `py-depaudit` carries a small TOML reader for 3.9 and 3.10.) First, generate random inputs from known data, write them out in the format, and check the parser returns the original data: the ground truth is the data, not another parser. Second, where the real module exists, compare results with it on a corpus and on real files, and check that both reject the same bad inputs. Third, run the tool's own tests a second time with the fallback forced on, so the older-Python path is exercised on every version. Have the fallback refuse what it does not support instead of guessing. Generated tests found two real bugs in the first version of that reader.

**When a test fails, decide which side is wrong.** In the first five tools built with this method, the first test failures were a mix: some were mistakes in the test (a wrong expected sort order, a mis-counted edit distance, a helper that silently wrapped the value being tested) and some exposed a real weakness in the tool (a pattern that stopped at a dot, a permission rule that was too broad, a keyword that matched inside another word). Read the failure. Do not weaken the assertion until it passes.

## 6. Documenting

The README follows the same shape in every repository (the template is `templates/README.template.md`):

1. One paragraph: what it does, that it is offline and standard-library only, what it never does.
2. A real run, pasted from actual output on synthetic files.
3. Options and exit status.
4. A table of every finding code with severity and meaning.
5. **Limits**: what a pass does not prove, what it cannot see, known false positives, anything unmeasured.
6. **How it was checked**: what each claim was tested against and which parts are only heuristics.
7. The test command and the licence.

Counts and sizes quoted in a README must be measured, not remembered (a README once said "about 130 names" for a list of 140; it was fixed by counting).

## 7. Publishing

Definition of done: `python scripts/checkrepo.py PATH --run-tests` passes. It checks for the required files, the two README sections, no leftover TODOs, real output in a code block, `dependencies = []`, a CI workflow that runs the tests and the tool, no secret-shaped strings, no `.env` files, and that the tests pass.

Then:

```
git init -b main && git config core.createObject rename        # the second line is needed in the proot environment
git add -A && git commit -m "py-NAME: what it does"
gh repo create OWNER/py-NAME --public --source . --push --description "One line (Python, stdlib only)"
gh run list -R OWNER/py-NAME --limit 3                          # wait for green on 3.9-3.13
```

Never finish at the push: look at the CI result. Add topics with `gh repo edit OWNER/py-NAME --add-topic ...` (a few specific ones). Then regenerate the catalog (section 9).

## 8. Environment notes

- `gh` lives at `~/.local/bin/gh`; add it to `PATH`.
- In the LarzOS proot environment, hard-linked files cannot be opened, so `git add` fails unless `git config core.createObject rename` is set **before the first add**. If a failed add already happened, delete `.git` and start again.
- `pip` and `sudo` are not available; that is one more reason for standard library only.
- Larzscript numeric traps: `sqrt` is wrong outside about 1e-32..1e32, `%` truncates floats, `print` shows six significant digits locally but full precision in CI (format every printed float explicitly), there are no exponent literals, and `wait`, `from`, `at` cannot be identifiers.

## 9. Growing the collection

- **Catalog.** `python scripts/catalog.py --from-gh OWNER > CATALOG.md`. Categories come from `categories.json`: add a rule for a new area, or an override for an exception. Anything in *Other* needs a category.
- **New area.** Add a category to `categories.json`, three to five backlog entries to `BACKLOG.md` with evidence, and build the highest-scoring first.
- **Review cadence.** Once a month: rerun the research queries in `RESEARCH-LOG.md`, add a dated entry, re-score the backlog, retire tools that a better one has replaced (say so in the old README and archive the repository, do not delete it), and check that CI is still green.
- **Cross-linking.** When a new tool overlaps an old one, each README links to the other and says which to use when.
- **Extending a tool** is preferred to a near-duplicate. Bump the version in `pyproject.toml` and note the change in the README.

## 10. Safety rules for dual-use tools

Some tools (security scanners, injection detectors) could help an attacker as well as a defender. Build them to **find and report problems in your own files**, not to generate attacks: detect hidden instructions rather than write them, flag risky permissions rather than exploit them. Do not build anything whose main use is harm, and do not publish working exploits or evasion techniques.

## 11. Checklist

Copy into the tracking issue or the commit for each new tool.

- [ ] Evidence of need recorded in `RESEARCH-LOG.md`; overlap with `CATALOG.md` checked
- [ ] Scaffolded from the templates; library and command line separated
- [ ] Every rule has a matching and a near-miss test; ground truth is independent of the code
- [ ] All README TODOs replaced with real output, a Limits section and a How it was checked section
- [ ] Counts in the README measured
- [ ] `checkrepo.py --run-tests` passes
- [ ] Pushed, CI green on every Python version, topics added
- [ ] `BACKLOG.md` updated, `CATALOG.md` regenerated
