# Backlog

Ranked candidates. Score with the rubric in [`PLAYBOOK.md`](PLAYBOOK.md) section 3.2 (need, gap, offline and verifiable, estate fit, size; each 0-3). A gate line scoring 0 drops the idea. Statuses: `idea`, `building`, `published`, `dropped`.

| Idea | Need | Gap | Verif. | Fit | Size | Total | Status | Evidence / notes |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | --- | --- |
| Token-cost and wasted-context finder | 3 | 2 | 2 | 2 | 3 | 12 | published: `py-tokenbudget` | 2026-09-26 log: token-cost pain 42% |
| Agent config and instruction-file linter | 3 | 3 | 3 | 2 | 2 | 13 | published: `py-agentlint` | prompt-injection risk 31%; agent tooling trending |
| Dependency manifest supply-chain audit | 3 | 2 | 3 | 2 | 2 | 12 | published: `py-depaudit` | supply-chain scanners trending |
| One-click unsubscribe (RFC 8058) checker | 3 | 2 | 3 | 3 | 3 | 14 | published: `py-unsubcheck` | Gmail/Yahoo enforcement; `py-mailtrace` gap |
| File-type-by-content and extension mismatch | 2 | 2 | 3 | 2 | 3 | 12 | published: `py-magicfile` | upload validation |
| `pyproject.toml` and Pipfile support in `py-depaudit` | 2 | 2 | 3 | 2 | 2 | 11 | published: `py-depaudit` 0.2.0 (extension) | needed a fallback TOML reader for Python 3.9/3.10 (`tomllib` is 3.11+); verified by round-trip generation, comparison with `tomllib` and real files. Poetry/uv/Pipfile tables covered; Hatch, PDM dependency tables and lockfile contents still not read |
| AI-disclosure and endorsement wording checker for affiliate content | 2 | 2 | 2 | 3 | 2 | 11 | idea | FTC risk finding; overlaps `py-rellint`, check first; wording rules are judgement calls, be explicit about that |
| DMARC aggregate report (XML) summariser | 2 | 2 | 3 | 3 | 2 | 12 | published: `py-dmarcreport` | estate receives DMARC reports daily; validated on 229 real reports from 8 reporters (0 parse failures), none committed |
| MCP server config diff between two versions | 1 | 2 | 3 | 1 | 2 | 9 | idea | would extend `py-agentlint`; wait for demand |
| Robots.txt AI-crawler policy checker (GPTBot, ClaudeBot and similar) | 2 | 2 | 3 | 3 | 3 | 13 | published: `py-robotscheck` 0.2.0 (`bots` command, an extension, not a new repo) | estate logs show heavy AI-crawler traffic; crawler list verified against OpenAI's and Anthropic's own pages on 2026-09-26; other vendors from secondary sources, so re-verify monthly |
| Structured-data (schema.org) required-field checker for articles | 2 | 1 | 2 | 3 | 2 | 10 | idea | overlaps `py-jsonldcheck`; probably an extension |
| Public-status page generator | 1 | 1 | 1 | 1 | 1 | 5 | dropped | needs the network and a server; not an offline tool |

## How to add an entry

1. Find evidence and log it in `RESEARCH-LOG.md`.
2. Check `CATALOG.md` for overlap.
3. Score it. Add a row. Keep the table sorted by total within each status when you review.
4. When you start, set `building`. When it ships, set `published: repo-name` and note the repo in the log entry.
5. If you drop it, keep the row and say why.
