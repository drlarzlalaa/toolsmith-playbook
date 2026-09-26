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
| llms.txt validator | 2 | 2 | 3 | 3 | 3 | 13 | published: `py-llmstxtcheck` | 10% adoption in a 300k-domain study; no official validator; checked against the spec read in full and six real public files. Neither estate site has a `/llms.txt` (both return 404); creating one is a live-site change for the owner to approve |
| AI-content disclosure audit (Article 50 of the EU AI Act, applies from 2026-08-02) | 3 | 3 | 2 | 3 | 2 | 13 | published: `py-aiprovenance` | the earlier verification worry was resolved by finding the C2PA project's public test files (11 real JPEGs, ground truth from its own table). Still only constructed data for IPTC terms inside manifests, PNG and WebP manifests, and XMP DigitalSourceType. Reports markers and wording present; never sufficiency. Invisible watermarks are not detected |
| Consent-before-tracking audit from a browser HAR file (trackers and cookies that fire before consent) | 3 | 2 | 2 | 3 | 2 | 12 | published: `py-consentaudit` | most common cookie-consent violation is tags firing before consent; supports a saved-HTML mode too (curl output). Tracker list is a dated starter list (52 entries); consent state depends on how the HAR was recorded; validated on 8 real public pages by comparing every finding with grep |
| HTML accessibility linter (alt text, labels, lang, headings) | 3 | 1 | 2 | 2 | 1 | 9 | dropped | European Accessibility Act enforceable since 2025-06-28 and automated tools find only 30-57% of issues, but axe, pa11y and Lighthouse already do this well; `py-wcag` covers contrast. Revisit only for a narrow gap |
| Public-status page generator | 1 | 1 | 1 | 1 | 1 | 5 | dropped | needs the network and a server; not an offline tool |

## How to add an entry

1. Find evidence and log it in `RESEARCH-LOG.md`.
2. Check `CATALOG.md` for overlap.
3. Score it. Add a row. Keep the table sorted by total within each status when you review.
4. When you start, set `building`. When it ships, set `published: repo-name` and note the repo in the log entry.
5. If you drop it, keep the row and say why.
