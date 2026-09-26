# Research log

One dated entry per research session: the queries, what was found, links, and what it changed in the backlog. Newest first. A claim with no source does not go in the backlog.

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
