# Research log

One dated entry per research session: the queries, what was found, links, and what it changed in the backlog. Newest first. A claim with no source does not go in the backlog.

## 2026-09-26 (sixth session): AI-content markers, with a real test corpus

**Question:** can the AI-content marker audit be built so that its claims can actually be verified?

**Primary sources read in full:** the [IPTC Digital Source Type vocabulary](https://cv.iptc.org/newscodes/digitalsourcetype/) (17 terms with exact URIs; four are AI-generated or AI-modified), the [Commission's page on the Code of Practice on marking and labelling AI-generated content](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content) (final version published 10 June 2026, confirmed as an adequate voluntary tool; it does not, on that page, say which marking techniques to use), and the text of Article 50 (unofficial reproduction). The C2PA specification page was truncated when fetched, so the PNG (`caBX`) and WebP (`C2PA`) embedding rules rest on secondary descriptions that agree with each other; they are tested on constructed files only.

**The verification problem was solved by looking for the standard body's own test corpus.** The C2PA project publishes sample files with a table of what each contains. Eleven real JPEGs (Adobe, Nikon, Truepic) were used as ground truth: the two listed as "No Content Credentials" give no manifest, and all others (including invalid-signature and hash-mismatch samples) give one. None of the real manifests names an IPTC source type, so that part remains constructed-only, and the README says so.

**A real bug was found by the generated tests, not the real files:** manifest text is length-prefixed CBOR, so reading letters after an IPTC URI swallowed the next byte. Terms are now matched against the known vocabulary.

**Real pages:** the page mode was run over eight blog articles from an estate site. The only AI wording in any of them is marketing text ("AI-powered"), which the tool correctly did not count as disclosure, confirmed by an independent `grep`. None contains disclosure or editorial wording. Whether those pages are AI-generated is for the owner to say; if they are, that is what the Act asks the owner to think about. Nothing about this is in any public repository.

## 2026-09-26 (fifth session): consent-before-tracking, validated on real pages

**Question:** can a tool show what a page loads before consent, and does it hold up on real pages?

**What was built and how it was checked:** `py-consentaudit` (HAR and saved-HTML modes). Constructed and generated HAR files for the rules; then, per the playbook, the HTML mode was run read-only over eight real public home pages (five small sites, three large news sites) and each finding was compared with a plain `grep` of the same page.

**What the real pages taught:** the first version could not tell a page that holds its Google tags behind Consent Mode defaults or a consent platform from one that does not, so consent-platform and Consent Mode detection were added. A test-only design would not have found that, and neither would a checker written from the tracker list alone.

**Estate observation (aggregate, kept out of every public repository):** of five estate home pages, one writes a Google tag (GA4) into its HTML and runs it on load, and none of the five contains any consent management script, Consent Mode default, or the words "cookie" or "consent" in its HTML. The estate's own analytics tables also record visitor IP addresses and countries, and its analytics show EU visitors. Static HTML cannot see scripts added at run time, so this needs a HAR from a clean browser to confirm. It is a compliance question for the owner, not a conclusion here; the fix is a live-site change that needs the owner's decision.

## 2026-09-26 (fourth session): new areas: llms.txt, AI-content rules, accessibility law, cookie consent

**Question:** the remaining backlog scored low, so which new areas have need, a gap, and something verifiable offline?

**Queries run:** llms.txt adoption, validators and common mistakes; EU AI Act Article 50 transparency obligations and website labelling; European Accessibility Act enforcement and common WCAG failures; GDPR cookie consent violations and enforcement in 2026.

**Primary sources read in full:** the [llmstxt.org specification](https://llmstxt.org/) and the text of [Article 50 of the AI Act](https://artificialintelligenceact.eu/article/50/) (an unofficial reproduction of the Regulation, not the Official Journal).

**Findings:**

- **llms.txt:** one study of 300,000 domains in early 2026 put adoption near 10%, mostly developer-facing sites. The specification requires only an H1; there is no official validator; common mistakes are HTML served instead of text, relative URLs, no summary, and dumping every URL. Sources: [State of llms.txt 2026](https://presenc.ai/research/state-of-llms-txt-2026), [llms.txt: The Complete 2026 Guide](https://llmpulse.ai/blog/llms-txt-guide/). That these files change how AI products behave is not established by anything read here.
- **AI Act Article 50** applies from 2 August 2026. Providers must mark AI outputs in a machine-readable way; deployers must disclose deepfakes and AI-generated text published to inform the public on matters of public interest, unless the text had human review or editorial control and a person holds editorial responsibility; information must be clear, distinguishable, given no later than first exposure, and accessible. Sources: the Article 50 text above, [Orrick's analysis](https://www.orrick.com/en/Insights/2026/08/EU-AI-Act-Transparency-Obligations-for-AI-Generated-Content-Article-50).
- **European Accessibility Act** enforceable since 28 June 2025, first inspections reported in January 2026; colour contrast, missing alt text and missing form labels are the commonest failures; automated checkers find only 30 to 57% of issues. Source: [European Accessibility Act 2026](https://www.levelaccess.com/compliance-overview/european-accessibility-act-eaa/). Existing free tools (axe, pa11y, Lighthouse) already cover this well.
- **Cookie consent:** the most frequent violation is placing advertising cookies or firing tags before the visitor interacts with the banner; a "reject" button that does not block cookies is treated as worse than none. Source: [Cookie Consent Fines 2025-2026](https://kukie.io/blog/cookie-consent-fines-2025-2026).

**Estate observations (aggregates only):** neither `earnifyhub.com` nor `earnifyhubmailer.com` serves an `llms.txt` (both answer 404); analytics show EU visitors (France, Spain, UK among the top countries).

**Result:** `py-llmstxtcheck` built and published. AI-content disclosure and consent-before-tracking scored 12 each and are in the backlog with their verification problems written down; accessibility was dropped as crowded.

**Limits:** the AI Act text was read from a reproduction, not the Official Journal; the legal significance for a specific site needs a lawyer, and no tool here decides it.

## 2026-09-26 (later still): DMARC aggregate reports

**Question:** is there a gap for reading DMARC aggregate (RUA) reports offline, and what do real reports look like?

**Findings:** no repository in the catalog reads reports (`py-emailauth` checks the DNS records, `py-mailtrace` one message). The format is specified in RFC 7489 appendix C. Real reports vary by reporter (namespaces, optional fields, zip or gzip or attached email), which is why the tool was validated against real ones.

**Validation on real data (read-only, nothing kept):** the parser was run once over 229 real reports in a working mailbox, from Yahoo, Google, Microsoft (consumer and enterprise), Zoho, Mail.ru and GMX: all 229 parsed, no failures. Only aggregate results were kept outside the mailbox; no report data, address or domain is in any repository.

**Result:** `py-dmarcreport` published.

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
