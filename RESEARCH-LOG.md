# Research log

One dated entry per research session: the queries, what was found, links, and what it changed in the backlog. Newest first. A claim with no source does not go in the backlog.

## 2026-09-26 (later): AI-crawler names and robots.txt behaviour

**Question:** which AI crawlers exist, what do they do, and which honour `robots.txt`? (Needed to build the `bots` command in `py-robotscheck`.)

**Queries run:** OpenAI crawlers and user agents; Anthropic ClaudeBot, Claude-User and Claude-SearchBot; Google-Extended, Applebot-Extended, PerplexityBot, Perplexity-User, CCBot, Bytespider, Amazonbot and Meta-ExternalAgent tokens.

**Primary sources read in full:**

- [OpenAI bots page](https://developers.openai.com/api/docs/bots): `GPTBot` (training), `OAI-SearchBot` (ChatGPT search), `ChatGPT-User` (user actions: "robots.txt rules may not apply"), and `OAI-AdsBot` (validates pages submitted as ads). `GPTBot` and `OAI-SearchBot` are governed by robots.txt.
- [Anthropic help-centre article](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler): `ClaudeBot` (training), `Claude-User` (user-initiated), `Claude-SearchBot` (search quality); all three explicitly honour robots.txt. It does **not** mention `anthropic-ai`.

**Secondary sources only** (independent 2026 crawler references, found by search): the categories and tokens for Perplexity, Google-Extended, Applebot-Extended, meta-externalagent, Bytespider, CCBot and Amazonbot, and the reports that `Perplexity-User` and `Bytespider` ignore robots.txt. Treated as reported, not confirmed, and worded that way in the tool.

**Lesson:** search-result summaries are not the source. The first draft of the README said the list was "checked against Anthropic's help-centre article" after reading only search snippets of it. Reading the pages found a bot that had been missed (`OAI-AdsBot`) and showed that `anthropic-ai` is not in the current documentation. Read the primary page before writing "checked against".

## 2026-09-26: first demand scan

**Question:** where do developers and site owners need small offline tools right now?

**Queries run:**

1. "most wanted developer tools pain points 2026 survey small CLI utilities developers wish existed"
2. "email deliverability tools demand 2026 Gmail Yahoo bulk sender requirements DMARC one-click unsubscribe checker"
3. "GitHub trending 2026 fastest growing open source categories AI agent security supply chain tools"
4. "creators affiliate marketers biggest compliance problems 2026 FTC disclosure link tracking tools needed"

**Findings:**

- **Cost and injection risk lead developer complaints.** A Q1 2026 analysis reports token-cost volatility (42%) and prompt-injection risk (31%) as the top two pain points, ahead of model reliability. Developers also report spending more time reviewing AI-generated code than writing new code, and struggle with configuration that YAML and JSON do not validate. Source: [Developer Pain Points in 2026: What the Complaint Data Actually Says](https://echosift.io/blog/developer-pain-points-2026/).
- **Supply-chain and agent security are trending.** GitHub's Octoverse figures show LLM-focused repositories up 178% year over year. Newly popular projects include agent harnesses, reusable skills, secure code-analysis skills, and read-only supply-chain scanners that check dependencies, MCP servers and editor extensions. Source: [Top AI GitHub Repositories in 2026](https://blog.bytebytego.com/p/top-ai-github-repositories-in-2026).
- **Bulk-sender rules are stricter and enforced.** Gmail and Yahoo require, for senders of more than about 5,000 messages a day, authentication (SPF or DKIM, and DMARC), spam complaints under 0.3%, and one-click unsubscribe via `List-Unsubscribe` and `List-Unsubscribe-Post`. Non-compliant mail can be rejected at SMTP time with a permanent 550. Sources: [Gmail's Bulk Sender Requirements in 2026](https://wpmailsmtp.com/gmail-bulk-sender-requirements/), [Bulk Email Sender Rules for Google, Yahoo, Microsoft & Apple (2026)](https://powerdmarc.com/bulk-email-sender-requirements/).
- **Affiliate and creator disclosure is a live legal risk.** The commonest failure is weak disclosure placement or vague wording, AI-generated endorsements now raise their own disclosure question, and brands share liability for creators' posts. Source: [Affiliate Marketing Compliance in 2026](https://www.tracknow.io/blog/affiliate-marketing-compliance/79).

**Conclusions and what they changed:**

| Finding | Response | Result |
| --- | --- | --- |
| Token-cost pain | Estimate context cost and flag wasteful files | `py-tokenbudget` published |
| Injection and agent-config risk | Lint agent configs and instruction files | `py-agentlint` published |
| Supply-chain trend | Audit dependency manifests offline | `py-depaudit` published |
| One-click unsubscribe enforcement | Exact RFC 8058 checker; `py-mailtrace` only noted the header | `py-unsubcheck` published |
| Affiliate disclosure | Partly covered by `py-rellint`; see backlog | backlog |

**Limits of this scan:** four searches, one day, US-centred results. Survey percentages come from one analysis and are not independently confirmed. Repeat and widen next month.
