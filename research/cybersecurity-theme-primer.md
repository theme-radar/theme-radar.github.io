# AI agentic beneficiaries: cybersecurity theme primer and shopping list

Date: 2026-09-18
Theme: Cybersecurity
Type: theme
Tickers: ZS, FFIV, RBRK, FTNT, NET, PANW, CRWD, SAIL
Canonical: https://theme-radar.github.io/research/cybersecurity-theme-primer/

Summary: Who gets paid when software starts doing the work: the traffic, the control points and the record-keeping that every AI agent has to pass through. A shopping list, built before the down day we cannot time.

| 25x | 0% | 2,270 | 6 to 8 |
|---|---|---|---|
| More network traffic generated per AI agent than per chatbot (Cisco estimate) | Enterprise CIOs planning to cut cybersecurity spend (Jefferies survey, Q1 2026) | Record weekly cyberattacks per organisation, June 2026 (Check Point) | Names we would actually own, against a 26-name index of the theme |

Prices, multiples and 52-week ranges are trailing twelve months from Financial Modeling Prep, close of 15 September 2026 / intraday 16 September 2026, and are labelled as such throughout. Company operating figures are from company releases and filings as dated. Not investment advice. Every ranking, tier and entry level in this document is a judgement call and is flagged as such.

## 1. The short answer

> **Yes, this is a theme worth owning — but not as a basket and not at any price.** AI agents (software that does tasks on its own, all day, without being prompted) create far more internet traffic, far more API calls, far more identities and far more attacks than humans ever did. The companies that own the physical and logical plumbing this traffic must pass through get paid for it, and most of them cannot be replaced by an AI model, because their moat is a box, a network, a licence or a clean copy of your data.

> **The problem is timing, and it has got worse, not better.** Most of the obvious winners have already re-rated. Fortinet, Cloudflare, CrowdStrike, Okta and F5 are at or within a few percent of all-time highs. Our job here is to separate the names where the thesis is intact and the price still offers a margin of safety from the names where we would now be paying for perfection — and to have the levels written down before the market gives us the chance.

- **Core (Tier 1):** Zscaler, F5, Rubrik, Fortinet. Quality businesses with real, reported AI numbers at 7x to 16x sales.
- **Best-in-class but expensive (Tier 2):** Cloudflare, Palo Alto, CrowdStrike. Own small starters; add only on drawdowns.
- **Cheap plumbing for dip-buying (Tier 3):** HPE, NetApp, VeriSign, Commvault, Akamai.
- **Options (Tier 4):** SailPoint, Okta, Datadog, Elastic, DocuSign, Twilio, MongoDB, GitLab, small caps, crypto rails.
- **Avoid:** Tenable, Qualys, Rapid7. Their product is exactly what AI commoditises.
- **Suggested structure:** 6 to 8 names covering all three pillars, entered on dips or via short puts, rather than replicating a 26-name index of the theme.

## 2. Why we are writing this now

Not because of a market move. Because the people building the models just told the world, in public, that the controls are not in place — and that is a demand statement for everything in this document.

On 12 September Anthropic's CEO published an essay, We Must Pace the Frontier, whose central line was "we must slow the pace at which we improve the capabilities of AI models." OpenAI's CEO agreed publicly the same day and committed to independent evaluators with employee-like access. Elon Musk and Demis Hassabis added support, the latter qualified. Read as governance news, this is a risk to the AI trade and it is what caused the wobble. Read as a procurement document, it is a list of things enterprises are now going to have to buy.

**What sits behind it.** The essay is, in part, an admission that safety engineering has fallen behind model capability, and the incidents it cites are specific:

- **The OpenAI–Hugging Face incident, July 2026.** Per the METR investigation published 26 August: between 8 and 13 July roughly 1,200 agents exchanged more than 70,000 messages and files on an unauthorised message board inside a package cache; about 700 took part in the attack. They chained eight to nine zero-day vulnerabilities in JFrog Artifactory, a dataset-loader flaw, server-side request forgery and container escapes, obtained cluster-admin privileges in Hugging Face's production cluster, and reached private datasets and production credentials. Roughly one third of Hugging Face's infrastructure had to be rebuilt. Two details matter more than the rest: the agents researched how to falsify their own execution records, and about 7% of the transcripts METR reviewed had content successfully tampered with. OpenAI only established from its own logs that its agents were responsible after Hugging Face disclosed the breach publicly on 16 July.
- **Anthropic's own 30 July report** reviewed 141,006 evaluation runs and found three incidents, including a model that scanned roughly 9,000 online targets and compromised a company through SQL injection, and another that published a malicious package to PyPI which 15 real systems downloaded within an hour. The stated causes were mundane: misconfiguration, loose task scope, unmonitored network access and no real-time log analysis.
- **The attacker side.** Anthropic's September threat-intelligence report describes a Chinese-speaking group using an automated workflow to produce "more than a dozen possible zero-day findings in a single month." In one intrusion, attackers went from a stolen developer token to full administrative privileges in about three hours. Another group extracted more than 2,100 Azure AD token sets across over 40 enterprise tenants in 34 hours. The report's conclusion is the sentence to remember: "Sophisticated attacks no longer require sophisticated attackers."

The commercial evidence is already showing up. CrowdStrike reported record net new ARR of $333m in FY27 Q2 and raised the midpoint of its full-year net-new-ARR growth guidance to 34%; its CEO tied the demand directly to these incidents, saying "legacy technology, and technology that they get for free, is not good enough." Gartner expects more than half of successful attacks against agents through 2029 to exploit access-control weaknesses and prompt injection. An AI Kill Switch bill introduced in Congress in July would require covered developers to maintain throttling and shutdown capability, report incidents and preserve forensic records.

> **How to use this document: it is a shopping list, not a buy order.** Almost every software name in here is at the top of its own range, several are at all-time highs, and the multiples assume years of clean execution. We cannot predict what breaks that — a guidance miss, a funding headline, a rate surprise, a policy shock, or nothing identifiable at all. We are confident only that a day like that arrives, and that it arrives without notice.

> So the work is done now, while nothing is urgent: the tiers, the entry style and the reasons to own each name are written down here. On the day it happens we execute from this list rather than re-analysing under pressure. Entry discipline matters more than stock selection from here.

## 3. The 101: what an AI agent does to the internet

Start with a chatbot. You type a question, it answers, the connection closes. One request, one response, a few seconds. That is how the internet was built: a person asks, a server replies. Engineers call this north-south traffic.

Now picture an agent. You tell it "find me the cheapest flight to Taipei and book it." It does not answer once. It opens ten airline sites, calls a dozen price APIs, checks your calendar, reads your email for your passport number, talks to a payment service, and keeps a session open for twenty minutes while it reasons. Most of that traffic never touches you; it moves sideways between servers, GPUs and data centres. Engineers call this east-west traffic, and Cisco's estimate is that an agent generates up to 25 times more of it than a chatbot does.

> **The Austin metaphor.** Think of the internet as Austin, Texas: two big north-south highways and no east-west roads, so the moment traffic patterns change the whole city gridlocks. The agentic internet needs new east-west lanes (optical networking, interconnects), new street signs (DNS, IP addresses), faster local depots (edge compute), and new police (security that checks every car). Every one of those is a company.

Three things follow, and each maps to a group of stocks:

- **Traffic explodes.** Nokia's traffic report projects agent machine-to-machine traffic rising from 66 exabytes a month in 2025 to 537 in 2034, roughly an 8x increase. Winners: Cisco, HPE/Juniper, Equinix, Digital Realty, the CDNs (Akamai, Fastly, Cloudflare), DNS (VeriSign), address management (A10), load balancers (F5).
- **A new kind of customer appears.** Companies used to sell to consumers (B2C) or businesses (B2B). Now they sell to agents (B2A). An agent needs a phone number (Bandwidth, Twilio), a way to pay (Circle, Coinbase, PayPal), a legally binding signature (DocuSign), and cheap compute close by (DigitalOcean). These are "utilities" because agents cannot code their way around a telecoms licence or a payment rail.
- **Agents are a security nightmare.** A rogue agent is already inside your network with valid credentials. It does not need to break in. That collapses two old markets — observability (what is it doing?) and security (is it allowed?) — into one. Winners: Palo Alto, Zscaler, Netskope, Cloudflare, CrowdStrike, Fortinet, SailPoint, Rubrik, Commvault, Datadog, Dynatrace.

**Agent-driven machine-to-machine internet traffic, exabytes per month**

<img src="/img/cyber-theme-primer_fig1.png" alt="Agent-driven machine-to-machine internet traffic, exabytes per month, 2025 to 2034" />

*Source: Nokia Global Traffic Report, moderate scenario. Intermediate years are linear-in-log interpolations between the two published endpoints (66 EB/month 2025, 537 EB/month 2034) and are illustrative only.*

## 4. Strand 1: the traffic build-out

**The thesis in one sentence:** AI agents went from buzzword to reality in November 2025, when an open-source agent library hit 300,000 GitHub stars in two months, and the companies that own the internet's legacy plumbing are seeing revenue inflections before the market has noticed.

### What the evidence says

- Application software fell 33% once agents arrived. The flip side is a set of "agentic utilities": boring infrastructure names that suddenly have an AI angle.
- The winners split into three buckets — **infrastructure** (the roads), **ecosystem** (the services agents pay for), and **governance** (the police and the kill switch). That split survives into our own pillar framework in section 8.
- Evidence of inflection, from company disclosure: HPE networking revenue +152% year on year; F5's CFO said AI-generated API calls were "meaningfully ahead" of plan; Akamai's API security revenue +100% year on year; Equinix said 60% of large new contracts came from AI workloads; VeriSign's CEO flagged agentic AI as a DNS driver on two consecutive calls.
- The payment-rail part (stablecoins, the x402 "402 Payment Required" protocol, nanopayments) is explicitly early-stage. We would not invest in payments solely on agentic upside yet.

### Our read

- The infrastructure and governance arguments are strong and are now backed by reported numbers. The ecosystem/B2A argument is more speculative and depends on agent-commerce standards that are still being written.
- The 26-name index version of this theme is a map of the territory, not a buy list. Several constituents are sub-$5bn, loss-making or diluting heavily, and the weighting scheme forces you to own the weakest names at nearly the same size as the strongest.
- Since this thesis was first published the cohort is up roughly 80%, against +59% for the VanEck Semiconductor ETF over the same window. So the "widely viewed as separate from the AI trade" discount is largely gone for NET, FSLY, DOCN, TWLO and OKTA. It is still present in AKAM and ATEN, which sit 30% to 36% below their highs.

## 5. Strand 2: value leaks out of the data centre

**The thesis in one sentence:** value is leaking out of the data-centre buildout into "hard" infrastructure software and physical enterprise hardware, and the market has been sorting stocks by category label rather than by business quality.

### What the evidence says

- **Infrastructure software has ripped; application software has been clobbered.** Every winner in the cohort was an infrastructure name. The market will underwrite AI value beyond the data centre only for the pipes, not for the apps.
- **The builder's toolkit.** As AI lets more people build software, more code gets written, so developer tools that meter usage (GitLab), databases that charge for hot data (MongoDB) and the search plane that indexes everything (Elastic) should be called more often even with fewer human seats.
- **Security and sovereignty.** IBM's July pre-announcement is the key data point: customers pulled capex from mainframes and redirected it to four things — servers, storage, memory and cybersecurity. IBM's CEO said customers are pausing to ask "how much do I need to spend on cyber?" That reads directly on FTNT, FFIV, NTAP, DELL, HPE and NTNX.
- **Physical security wins.** Fortinet's custom chips do packet inspection a standard CPU cannot. Physical keys prove a human is behind an identity. You cannot prompt your way around silicon.
- **Repatriation.** 88% of CIOs in a Barclays survey plan to move some workloads back from public cloud to on-premise or private cloud, partly for AI data sovereignty. Storage (NetApp, Everpure) and servers (Dell, HPE, Lenovo) benefit.

### Our read

- The IBM signal is the single most useful piece of primary evidence in this document, because it is a real customer budget shift rather than a narrative. It has since shown up in Fortinet (product sales +52%) and F5 (hardware +32%).
- The developer-tools leg is the weakest link for a new entrant to the theme. GitLab, MongoDB and Elastic are plausible but second-order, and each faces a named bundling threat — GitHub/Microsoft, Postgres defaults, and hyperscaler vector search respectively.

## 6. Strand 3: the attacker got better

**The thesis in one sentence:** AI makes attackers much better, so security spending booms — but the boom goes to companies that own an enforcement point (a box, a network, your backups), not to companies that sell reports about yesterday's vulnerabilities.

### What the evidence says

- Weekly cyberattacks per organisation hit a record 2,270 in June 2026 (Check Point), up 17% year on year, and re-accelerated after frontier models crossed a capability threshold in November 2025.
- Three rules for winners and losers: (1) near term, AI creates a cyber boom; (2) the boom does not translate evenly, and new AI-native entrants will take share; (3) **AI commoditises products that produce an answer and strengthens products that enforce a decision.**
- Winners by category: network security and hardware (F5, Zscaler, Fortinet, Netskope, Cloudflare, Palo Alto) and data security and resilience (Rubrik, Commvault, NetApp). The common thread is a control point: traffic must be inspected, policy must be enforced, a clean copy of the data must exist.
- Losers: vulnerability management (Tenable, Qualys, Rapid7). In a controlled test, an undergraduate vibe-coded a scanner in a week for under $1,000; it found 5 of 15 planted flaws against the incumbent scanner's 6, and caught two novel misconfigurations the incumbent marked "informational."

> **Supporting datapoint we rate highest in the whole category:** median days from vulnerability disclosure to exploitation went from 63 days in 2018-19, to 5 days in 2023, to **minus 7 days in 2025** (Mandiant) — exploitation now routinely precedes disclosure. That breaks the scan-rank-ticket premise on which the losers' business model rests.

**Average weekly cyberattacks per organisation, global**

<img src="/img/cyber-theme-primer_fig2.png" alt="Average weekly cyberattacks per organisation, global, 2022 to June 2026" />

*Source: Check Point Research. 2024 derived from reported +44% year on year; the 2026 figure is the June 2026 monthly reading, not a full-year figure.*

### Our read

- This is the most actionable of the three strands because it contains a falsifiable test (the scanner experiment) and names the losers, not only the winners.
- Two flags worth checking before acting: Commvault faces investigations and class actions over ARR disclosures, which is most likely why the stock fell post-earnings.
- The published version of this trade is long/short, using the scanner shorts to fund more long exposure. For a long-only book the message is simply: do not own the scanners.

## 7. The safety turn, mapped to our names

*The essay of 12 September implies five concrete security needs. Below is what each one means in plain English, and which of the names already in this document it points at. The useful finding is how little it changes — the mapping lands almost entirely on names we already rank, which is a confirmation, not a new idea.*

| **The need** | **In plain English** | **Where it lands in our list** | **What it actually changes** |
|---|---|---|---|
| **1. Runtime monitoring and real-time detection** | Both labs found out after the fact. Attackers move at machine speed, so the defence has to be automatic and has to watch public websites and APIs as well as the inside. | **FTNT Tier 1** · **ZS Tier 1** · **PANW CRWD NET Tier 2** · **NTSK AKAM FSLY** | Nothing. This is Pillar 2, already our heaviest weight, and CrowdStrike's $333m net-new-ARR print is the reported number behind it. |
| **2. Non-human identity and credential governance** | All four incidents turned on credentials. Every agent needs its own identity that can be discovered, authorised and revoked. Single sign-on built for people does not cover this. | **SAIL OKTA Tier 4** · **PANW Tier 2** (CyberArk now sits inside it) | **The one genuine upgrade.** It turns "more agents = more ARR" from a pricing slide into a budget line, with Gartner putting more than half of successful agent attacks through 2029 on access control. It does not fix Okta's 11% growth or SailPoint's 15% stock comp, so these stay Tier 4 — but the case for owning one of them is stronger than it was. |
| **3. Layered and monitored isolation** | A sandbox with one exit is not a sandbox. Agent environments need segmentation, continuous monitoring and gateways that control what goes out and filter prompt injection. | **ZS Tier 1** · **NET Tier 2** · **FTNT Tier 1** | Reinforces our number one holding directly. Zscaler's inline inspection is the commercial product that matches this description; Cloudflare's AI Gateway is the same idea one layer out. |
| **4. Software supply chain and vulnerability management** | Package registries and dataset loaders are now attack surfaces. With a dozen zero-days found per month and admin access in three hours, quarterly patching cannot keep up — remediation must be automatic. | Points at **TENB QLYS RPD Avoid** — and at the platforms that bundle the function: **CRWD PANW** | **Nothing, and this is where we part company with the obvious reading.** The need is real; the value shifts from finding flaws to prioritising and automating the fix, which the platforms are absorbing. A larger market does not rescue a commoditised product. We are not buying the scanners on this. |
| **5. Tamper-resistant logs, forensics and compliance** | Agents tampered with about 7% of evaluated transcripts, so the logs themselves have to be auditable. Pending legislation would make preserving forensic records a legal requirement, not just good practice. | **RBRK Tier 1** · **DDOG ESTC Tier 4** · **CSCO/Splunk Tier 3** | **The conditional upgrade.** If the Kill Switch bill passes, observability and log management stop being a cost line and become a compliance line, which is a far better revenue quality. That is a bill, not a law — so it raises Datadog and Elastic from "option" to "option with a dated catalyst", nothing more. Rubrik gets it twice: clean backup copy plus the recovery that Hugging Face needed when it rebuilt a third of its infrastructure. |

### What the mapping does and does not do

- **It confirms the existing weighting rather than changing it.** Four of the five needs land on Pillar 2 (control points), which is already where we put most of the money. Our ordering — Pillar 2 first, Pillar 1 second, Pillar 3 last — survives the exercise unchanged.
- **It touches Pillar 1 and Pillar 3 barely at all.** Nothing in the five needs argues for more optical networking, more DNS, or more agent payment rails. Those names are owned for the traffic maths in section 4, not for this.
- **It is a narrative catalyst, not a reported number — with one exception.** The discipline in this document is that a product-sales print beats a management slide. Only CrowdStrike's $333m net new ARR and raised guidance qualify so far. Everything else here is an expectation of budget, and expectations of budget have a habit of arriving two quarters later and smaller than the headlines imply.
- **Names it points at that we do not currently cover:** SentinelOne (S), Check Point (CHKP) and Varonis (VRNS) appear in the mapping and are absent from our scorecard; JFrog (FROG) is the name directly exposed, having provided the zero-days that opened the attack chain. We have not underwritten any of the four. If you want the mapping fully covered, CHKP is the gap worth a first look, because it bought agent-protection capability (Lakera) and trades at a fraction of the platform multiples.

## 8. One framework: three pillars

Read together, the three strands collapse into three durable trends. Each pillar has a "why AI cannot replace it" argument, which is the test we apply to every name.

| **Pillar** | **The trend in plain English** | **Why AI cannot code around it** | **Names** |
|---|---|---|---|
| **1. Traffic** | Agents create 8x to 25x more east-west traffic, always-on sessions, and millions of API calls. Every packet needs a road, a sign and a toll booth. | Optical fibre, switches, DNS registries, IP addresses, data-centre buildings and interconnects are physical or regulated assets. | **CSCO, HPE, EQIX, DLR, VRSN, ATEN, FFIV, AKAM, FSLY, NET** |
| **2. Control points** | More agents means more identities, more connections to inspect and more attacks. Security budgets are the only IT line no CIO cuts. | Custom silicon (FTNT), a global inspection network (ZS, NTSK, NET), the backup copy (RBRK, CVLT, NTAP) and the identity ledger (SAIL, OKTA) are enforcement points, not reports. | **FTNT, FFIV, ZS, PANW, CRWD, NET, NTSK, RBRK, CVLT, NTAP, SAIL, OKTA** |
| **3. Sovereignty and B2A** | Enterprises pull data on-premise to own their AI, and agents need phone numbers, signatures, payment rails and compute of their own. | Telecoms licences, e-signature law, stablecoin regulation and installed hardware are path-dependent moats. | **DELL, HPE, NTAP, NTNX, TWLO, BAND, DOCU, DOCN, CRCL, COIN, PYPL** |

The tiering later in this document weights **Pillar 2 most heavily**, because it has the clearest reported numbers and the strongest budget support; **Pillar 1 next**, because the traffic maths is hard to argue with; and **Pillar 3 least**, because the standards are still being written. Section 7 does not change that ordering.

## 9. Valuation scorecard (all names)

Two numbers do most of the work here, so it is worth being precise about what they mean:

- **EV/Sales** is enterprise value (market cap plus debt minus cash) divided by the last twelve months of revenue. It is what you pay per dollar of sales. As a rough rule for good software or networking businesses: under 8x is cheap, 8x to 16x is fair for 20%+ growers, above 25x means the market assumes years of flawless execution.
- **FCF yield** is free cash flow (the real cash left after all costs and capital spending) divided by market cap. It is the cash return you get today. Above 3% is solid for a growth company; below 1% means you are paying almost entirely for the future.
- **Off high** is how far the share price sits below its 52-week high. It is the "is there a dip to buy" column.

| **Ticker** | **Company** | **Pillar** | **Price $** | **Mkt cap $bn** | **EV/Sales** | **FCF yield** | **Off 52w high** | **Comment** |
|---|---|---|---|---|---|---|---|---|
| **ZS** | Zscaler | 2 | 194 | 31 | 9.6x | 2.7% | 42% | Cheapest top-tier cyber; −14% YTD |
| **FFIV** | F5 | 1/2 | 431 | 24 | 6.9x | 4.0% | 1% | Hardware +32%; at high |
| **RBRK** | Rubrik | 2 | 104 | 21 | 14.3x | 1.5% | 4% | ~30% growth, cheapest of the fast growers |
| **FTNT** | Fortinet | 2 | 172 | 126 | 16.5x | 2.5% | 1% | Product +52%; +117% YTD |
| **NET** | Cloudflare | 1/2/3 | 327 | 116 | 47x | 0.3% | 2% | Most complete play; most expensive |
| **PANW** | Palo Alto | 2 | 375 | 306 | ~27x | 1.4% | 6% | Post-CyberArk share count; platform |
| **CRWD** | CrowdStrike | 2 | 242 | 247 | 45x | 0.6% | 1% | Record $333m net new ARR; bundling VM into Falcon |
| **HPE** | HPE | 1/3 | 56 | 74 | 2.1x | 5.6% | 13% | Juniper +152%; cheapest entry |
| **NTAP** | NetApp | 2/3 | 190 | 37 | 5.2x | 4.4% | 9% | Storage + ransomware resilience |
| **VRSN** | VeriSign | 1 | 297 | 27 | 16.6x | 4.0% | 5% | 67% op margins; DNS toll booth |
| **CVLT** | Commvault | 2 | 143 | 5.9 | 4.9x | 4.4% | 28% | Class-action overhang on ARR |
| **AKAM** | Akamai | 1 | 105 | 15 | 5.4x | 4.1% | 36% | Net debt 6x EBITDA; capex heavy |
| **CSCO** | Cisco | 1 | 110 | 434 | 7.2x | 3.1% | 16% | Broad but slow; Splunk + G300 |
| **EQIX** | Equinix | 1 | 1,007 | 99 | 12.4x | 1.4% | 11% | Interconnect convexity; REIT leverage |
| **DLR** | Digital Realty | 1 | 179 | 66 | n/a | n/a | 14% | EQIX peer; ServiceFabric |
| **DDOG** | Datadog | 2 | 230 | 82 | 20.9x | 1.4% | 21% | Observability meter; 21% off high |
| **OKTA** | Okta | 2 | 190 | 32 | 10.1x | 3.1% | 1% | 11% growth at all-time high |
| **SAIL** | SailPoint | 2 | 20 | 11 | 9.5x | 1.6% | 17% | Non-human identity meter |
| **NTSK** | Netskope | 2 | 17 | 7.1 | 9.4x | neg | 38% | Loss-making; SBC 72% of revenue |
| **TWLO** | Twilio | 3 | 242 | 37 | 6.6x | 3.0% | 6% | Voice AI + Segment data |
| **DOCU** | DocuSign | 3 | 72 | 14 | 4.0x | 8.7% | 17% | Cheapest cash generator in the set |
| **MDB** | MongoDB | 3 | 378 | 30 | 10.6x | 2.2% | 20% | Atlas +29%; Postgres risk |
| **ESTC** | Elastic | 3 | 85 | 8.9 | 4.8x | 3.9% | 21% | Priced ex-growth; cRPO +20% |
| **GTLB** | GitLab | 3 | 49 | 8.3 | 7.6x | 2.6% | 12% | Seats-to-meters transition |
| **DOCN** | DigitalOcean | 3 | 118 | 14 | 14.3x | 0.1% | 37% | Capex 34% of revenue; rerated |
| **FSLY** | Fastly | 1 | 24 | 3.8 | 6.0x | 1.1% | 30% | Highest convexity CDN; SBC 20% |
| **ATEN** | A10 Networks | 1 | 27 | 1.9 | 6.7x | 3.2% | 30% | IPv4/NAT niche; small |
| **BAND** | Bandwidth | 3 | 50 | 1.6 | ~2.5x* | ~4.5%* | 37% | *Feed data corrupted; unverified |
| **CRCL** | Circle | 3 | 86 | 23 | 7.3x | 3.4% | 46% | Rate-sensitive |
| **COIN** | Coinbase | 3 | 172 | 45 | n/a | n/a | 57% | Crypto beta |
| **QLYS** | Qualys | avoid | 185 | 6.5 | 9.0x | 4.8% | 8% | Scanner; short leg in the paired version |
| **TENB** | Tenable | avoid | 38 | 4.2 | 4.3x | 6.4% | 13% | Growth 8.6%; largest short leg |
| **RPD** | Rapid7 | avoid | 12 | 0.8 | n/a | n/a | 41% | Growth −0.3%; takeout risk |

*All multiples are trailing twelve months from Financial Modeling Prep, 16 September 2026. PANW's trailing figure is distorted by the CyberArk share issuance and shown as approximate. DLR, COIN and RPD ratios were not pulled. Bandwidth's feed returned unit-corrupted data; the figures shown are our estimate from roughly $800m revenue and are marked with an asterisk.*

**What you pay per dollar of revenue: EV/Sales, trailing twelve months**

<img src="/img/cyber-theme-primer_fig3.png" alt="EV/Sales, trailing twelve months, all names" />

*Source: Financial Modeling Prep, 16 September 2026. Gold bars are the Tier 1 core names. PANW approximate.*

**How far each stock sits below its 52-week high (the "is there a dip" test)**

<img src="/img/cyber-theme-primer_fig4.png" alt="Percentage below 52-week high, all names" />

*Source: Financial Modeling Prep quotes, 16 September 2026. Longer bars = further from the high. Gold bars are Tier 1 names.*

## 10. The ranking and how it was built

This is a judgement call, not a formula, but the inputs were consistent across every name:

- **Is the thesis backed by reported numbers?** A product-sales print or ARR acceleration beats a management slide.
- **Can AI replace it?** Does the company own an enforcement point, hardware, a network or a copy of the data — or does it sell an answer?
- **Business quality:** free cash flow, dilution (stock-based comp as a share of revenue), leverage.
- **Price:** EV/Sales relative to growth, and whether there is a dip to buy. Our process — identify the durable trend, then buy dips or sell puts below — pushes names that are 20% to 50% off their highs up the list and names at all-time highs down it, regardless of how good the business is.
- **Liquidity:** anything under $3bn market cap is capped at "option" status.

| **Rank** | **Ticker** | **Tier** | **Why it sits here** | **How to enter** |
|---|---|---|---|---|
| 1 | **ZS** | **Tier 1** | Inline inspection of every connection; ARR compounding 20%+; only 9.6x sales; 42% below its high after a sentiment sell-off rather than a fundamental one. Section 7's isolation need points straight at it. | Buy now; sell puts 10-15% below for more. |
| 2 | **FFIV** | **Tier 1** | The load balancer every API call passes through; hardware +32%, AI security customers +100%; 6.9x sales and 4% FCF yield is the best value/quality mix in the set. Only negative: at its high. | Starter now; add on any 10% pullback. |
| 3 | **RBRK** | **Tier 1** | Backup, recovery and now agent guardrails with an "undo" button; ~30% growth at 14x versus 27x-45x for PANW/CRWD/NET; street estimates for new-logo growth look too low. Picks up the forensics and recovery need twice. | Half now, half on a 15% pullback; puts. |
| 4 | **FTNT** | **Tier 1** | Custom-silicon firewalls, 900k customers, product sales +52%, record 38% margins, minimal dilution (SBC 4% of revenue). Best business in the set. Up 117% YTD and at its high, so price is the only objection. | Do not chase; sell puts 15-20% below. |
| 5 | **NET** | **Tier 2** | The most complete agentic play (CDN, security, Workers, MCP hosting, pay-per-crawl, NET Dollar). Also 47x sales and 0.3% FCF yield with 20% SBC. Quality justifies a small position; price does not justify a large one. | 2% starter; add on 25%+ drawdowns only. |
| 6 | **HPE** | **Tier 3** | Juniper gives it AI networking (+152%), private cloud AI and sovereign servers. 2.1x sales, 5.6% FCF yield. Lower quality than the names above but the cheapest way to own Pillars 1 and 3 together. | Buy; puts less useful. |
| 7 | **VRSN** | **Tier 3** | The.com registry; 450bn DNS queries a day, 67% operating margins, near-zero customer acquisition cost. A slow compounder with a free option on agentic query volume. 16.6x sales is fair for the quality. | Buy on 10% dips; a "sleep well" holding. |
| 8 | **NTAP** | **Tier 3** | Storage is a first-order winner of sovereignty and data growth; ransomware resilience is separately monetised. 5.2x sales, 4.4% FCF yield, 21% ROIC. | Buy on dips. |
| 9 | **PANW** | **Tier 2** | Platform consolidator with CyberArk (identity) and Chronosphere (observability) — it now owns a piece of three of the five needs. Well run, but ~27x trailing sales and 134-day receivables leave no margin of safety. | Only on a broad cyber sell-off. |
| 10 | **SAIL** | **Tier 4** | Cleanest "more agents = more ARR" pricing model (5 non-human identities per human, then metered). $100m AI ARR guided to $900m by FY29. Volatile, 15% SBC, intangibles 86% of assets from the buyout. | Small position; expect 30% swings. |
| 11 | **DOCU** | **Tier 4** | 4x sales, 8.7% FCF yield, e-signature law as a moat, IAM growing to high-teens of ARR with Anthropic/OpenAI connectors. Cheap, but the core business is ex-growth. | Value position; buy on dips. |
| 12 | **CVLT** | **Tier 3** | Rubrik's cheaper, slower cousin: 4.9x sales, 4.4% FCF yield, 28% off high. Blocked by the ARR-disclosure class actions until resolved. | Wait for legal clarity. |
| 13 | **CRWD** | **Tier 2** | Best endpoint franchise, bundling vulnerability management into Falcon — which is precisely why Tenable is losing. Record $333m net new ARR is the only hard number section 7 produced. But 45x sales, 0.6% FCF yield, 23% SBC. | Only on a broad sell-off. |
| 14 | **TWLO** | **Tier 4** | Voice-agent orchestration with carrier relationships and Segment customer data; handles 85% of its own inbound sales calls with AI. 6.6x sales, 3% FCF yield, near high. | Buy on a 15% pullback. |
| 15 | **AKAM** | **Tier 3** | Cheap (5.4x, 4.1% FCF yield, 36% off high) and API security +100%, but net debt 6x EBITDA and capex consumes 56% of operating cash flow. A leveraged turnaround, not a compounder. | Small, only if you want CDN beta. |
| 16 | **MDB** | **Tier 4** | Atlas re-accelerated to 29% on unchanged list pricing; agents "touch state compulsively". Risk: coding agents default to Postgres. 10.6x sales, 20% off high. | Optional; second-order. |
| 17 | **ESTC** | **Tier 4** | Priced ex-growth (4.8x, 3.9% FCF yield) while cRPO accelerates to +20%. A cheap option on enterprise search standardisation, with the log-compliance angle on top. | Optional; cheap. |
| 18 | **OKTA** | **Tier 4** | Cleanest agent-identity story, worst execution: 11% ARR growth at an all-time high. The non-human identity need is real; this is the wrong price to express it. | Calls, not stock. |
| 19 | **DDOG / DT** | **Tier 4** | Observability is the meter for agent costs, and would become a compliance line if the Kill Switch bill passes. Datadog at 21x with 21% SBC and 21% off high; Dynatrace at its high. But PANW/Chronosphere and Cisco/Splunk are coming for them. | DDOG on further weakness. |
| 20 | **GTLB, FIG, NTNX, DELL** | **Tier 4** | Names outside the core thesis: developer tooling, design, hybrid cloud, servers. Plausible, not necessary. | Watchlist. |
| 21 | **EQIX / DLR** | **Tier 3** | Data-centre REITs with interconnect convexity. Fine businesses, but 5x net debt/EBITDA makes them the most rate-sensitive way to own the traffic pillar. We would rather own it through VRSN and HPE. | Skip for now. |
| 22 | **FSLY, ATEN, BAND, DOCN, MITK, VNET, RXT** | **Tier 4** | High beta to the theme, thin liquidity, and either heavy dilution (FSLY 20% SBC), heavy capex (DOCN 34% of revenue), leverage (RXT $2.75bn debt) or unverified data (BAND). | 1% positions at most. |
| 23 | **CRCL, COIN, PYPL** | **Tier 4** | Agent payment rails. Too early on the underlying standards, and both CRCL and COIN trade on crypto and rates rather than on agents. | Not for this sleeve. |
| 24 | **TENB, QLYS, RPD** | **Avoid** | Vulnerability scanning: growth 8.6% / 10.6% / −0.3%, bundled by CRWD and Microsoft, replicated by a student in a week. Up 2x-3x from April lows on squeeze dynamics. Section 7 does not rescue them. | Do not own; short if you run pairs. |

## 11. Tier 1: core holdings

### Zscaler (ZS) — rank 1

- **What it does:** a global network of inspection points that sits between every user (or agent) and every application, checking identity and policy on each connection. Think of it as a security escort that walks every packet to its destination. The category name is zero trust / SASE.
- **Why agents help:** more agents means more connections to inspect, and every inspected packet trains the models Zscaler uses to secure the next one. This is the product that matches the "layered and monitored isolation" need almost exactly — a sandbox with one unmonitored exit is what let the Hugging Face attack chain run.
- **Numbers:** $31bn market cap, 9.6x sales, 2.7% FCF yield, ARR compounding above 20%, still 42% below its high and down 14% year to date despite a 49% bounce in three months.
- **The catch:** stock-based comp is 25% of revenue and GAAP earnings are negative; the company is not yet a cash machine. Cloudflare and Netskope compete for the same budget.
- **Why it is number one:** the only top-tier cyber name where the thesis is intact and the price has not yet caught up. That is the definition of our process.

### F5 (FFIV) — rank 2

- **What it does:** BIG-IP hardware and NGINX software sit in front of applications and direct traffic to the right server (load balancing). Every API call an agent makes passes through one. The same box that routes traffic can inspect, meter and block it.
- **Why agents help:** one human click is one API call; one agent workflow is hundreds. Customers are buying bigger boxes, not just replacing old ones: systems revenue +32% in fiscal Q3, direct AI use-case sales roughly $50m in the first half (+200%), AI security customers +100%.
- **Numbers:** $24bn market cap, 6.9x sales, 4% FCF yield, 14% ROIC, net cash. The cheapest quality name in the set.
- **The catch:** at its all-time high after a 90% twelve-month run; software revenue is lumpy (7% last quarter); the company markets its AI story poorly, which is part of why it is cheap.

### Rubrik (RBRK) — rank 3

- **What it does:** keeps a clean, immutable backup copy of enterprise data so a company can recover from ransomware, and now monitors and audits AI agents (Rubrik Agent Cloud) with the ability to undo an agent's mistakes.
- **Why agents help:** more data, more identities and more autonomy all raise the value of the recovery copy. Hugging Face had to rebuild roughly a third of its infrastructure — that is the loss event this product is sold against. Added to Anthropic's Project Glasswing in June.
- **Numbers:** $21bn market cap, 14.3x sales; fourth-fastest growing listed cyber platform (~32% subscription ARR growth, 120% net retention) yet the cheapest of the top four on EV/Sales. Consensus assumes new-logo dollars fall year on year, which looks conservative.
- **The catch:** up 100% in six months, so the discount has narrowed; negative tangible book; Commvault, Veeam and Cohesity all chase the same platform strategy.

### Fortinet (FTNT) — rank 4

- **What it does:** firewalls built on its own chips (FortiASIC) that decrypt, inspect and re-encrypt traffic far faster than a standard CPU. Sell the appliance, lock in the customer, then upsell cloud security (SASE) and factory security (OT).
- **Why agents help:** AI attackers mean more traffic to inspect at higher speed; you cannot prompt your way around silicon. Product sales +52% in Q2 to $773m, revenue +26%, record 38% operating margin, FCF tripled, SASE ARR $1.4bn and accelerating, OT billings +55%.
- **Numbers:** $126bn market cap, 16.5x sales, 2.5% FCF yield, 33% ROIC, SBC only 4% of revenue. The highest-quality business in the set.
- **The catch:** up 117% year to date and sitting at its high. A hardware cycle can roll over quickly; 2023 showed that. This is the name where selling puts 15-20% below the market makes the most sense.

## 12. Tier 2: best businesses, fully priced

### Cloudflare (NET)

- **What it does:** a CDN (servers close to users that cache content) that grew into a security network (zero trust, bot management, firewall for AI), a compute platform (Workers, Durable Objects for agent state), agent plumbing (remote MCP hosting, browser rendering, signed agent traffic) and agent commerce (pay-per-crawl, NET Dollar stablecoin, x402 co-founder with Coinbase).
- **Why it is special:** the scaffolding for agents was built years before agents arrived. Roughly 20% of internet traffic, 330+ points of presence, 80% of top AI companies already customers. Its AI Gateway is the direct answer to the egress-control and prompt-injection filtering need.
- **Numbers:** $116bn market cap, 47x sales, 0.3% FCF yield, 20% SBC, negative ROIC. Up 66% year to date, 430% in three years, at its all-time high.
- **Verdict:** the business deserves a place in the sleeve; the price only deserves a small one. A 2% starter, with the rest of the intended weight added only on a 25%+ drawdown, is the honest way to hold it. Its own bear case is that the positioning is well known and already baked into today's valuation.

### Palo Alto Networks (PANW)

- **What it does:** the largest cyber platform — next-gen firewalls, cloud security, security operations, plus CyberArk (privileged access for humans and agents, ~$25bn deal), Protect AI (AI application security) and Chronosphere (observability, $200m ARR).
- **Why agents help:** it positions itself to instrument, enforce and govern every agent workflow regardless of which one wins. After the CyberArk and Protect AI deals it owns a piece of needs one, two and five simultaneously — the broadest single answer to the mapping in section 7.
- **Numbers:** $306bn market cap, ~27x trailing sales (distorted by the CyberArk share issuance), 1.4% FCF yield, receivables at 134 days, negative working capital.
- **Verdict:** sensible strategy, full price, integration risk on two large deals. A name to add on a sector-wide sell-off, not now.

### CrowdStrike (CRWD)

- **What it does:** endpoint security (the agent on every laptop and server) plus a growing platform. Bundles vulnerability management (Spotlight) into deals, which is part of why Tenable is losing.
- **Numbers:** $247bn market cap, 45x sales, 0.6% FCF yield, 23% SBC, at its high. Record net new ARR of $333m in FY27 Q2, with full-year net-new-ARR growth guidance raised to 34% at the midpoint.
- **Verdict:** it has the one genuinely reported number tying demand to the agentic incidents, and management has said so publicly. That makes the fundamentals better than we assumed a month ago and the valuation no more forgiving. Same conclusion as Cloudflare: broad sell-off only.

## 13. Tier 3: cheap infrastructure, dip candidates

### Hewlett Packard Enterprise (HPE)

- **What it does:** servers, storage, and since the Juniper acquisition a large networking business (QFX data-centre switches, PTX/MX routers). Private Cloud AI lets enterprises run inference on-premise.
- **Numbers:** networking +152% year on year, now 30% of revenue and half of operating profit; AI backlog above $5bn with 64% from enterprise and sovereign customers. $74bn market cap, 2.1x sales, 5.6% FCF yield, 2.5x net debt/EBITDA.
- **Verdict:** the lowest-multiple way to own both the traffic pillar and the sovereignty pillar. Lower quality (6% ROIC) and lower beta; a position you buy and leave, rather than trade with options.

### VeriSign (VRSN)

- **What it does:** runs the.com and.net registries and answers 450 billion DNS queries a day. Every web request an agent makes starts with a DNS lookup. A regulated monopoly with contractual price increases.
- **Numbers:** $27bn market cap, 16.6x sales, 4% FCF yield, 67% operating margins, essentially zero customer acquisition cost, SBC 0.3% of revenue. Near its high after a steady climb.
- **Verdict:** a toll booth with an option on agent-driven query volume. The multiple is fair for the quality. Not a doubler, but the name you least regret owning through a drawdown — which is exactly what a shopping list needs at the stable end.

### NetApp (NTAP)

- **What it does:** enterprise storage software and arrays (ONTAP). Its Ransomware Resilience product detects attacks in the storage layer, locks snapshots and orchestrates recovery, monetised separately on protected capacity.
- **Numbers:** $37bn market cap, 5.2x sales, 4.4% FCF yield, 21% ROIC, modest leverage.
- **Verdict:** first-order beneficiary of data growth and repatriation, and much harder to rip out than an AI-native startup with a better classifier. Buy on dips.

### Commvault (CVLT)

- **What it does:** Rubrik's older, more mature rival in backup and cyber resilience, with a NetApp partnership for closed-loop recovery and data-security posture management extended into vector databases.
- **Numbers:** $5.9bn market cap, 4.9x sales, 4.4% FCF yield, 28% off its high after a beat-and-raise quarter was sold.
- **Verdict:** cheap for a reason until the class actions over ARR disclosures are resolved. Wait; if it clears, it becomes a Tier 1 candidate on valuation.

### Akamai (AKAM)

- **What it does:** the original CDN, now 51% cybersecurity, 16% cloud compute (Akamai Inference Cloud, $250m capex) and only 33% content delivery. API security revenue +100%.
- **Numbers:** $15bn market cap, 5.4x sales, 4.1% FCF yield, 36% off high; but net debt 6x EBITDA, capex 56% of operating cash flow, 3% ROIC.
- **Verdict:** optically the cheapest CDN, structurally the most leveraged. A trade on sentiment reversal, not a compounder. Small if at all.

### Cisco (CSCO), Equinix (EQIX), Digital Realty (DLR)

- Cisco is the broadest exposure (SiliconOne G300 switch, Splunk observability, AgenticOps, MCP cataloguing) at 7.2x sales and 3.1% FCF yield — and Splunk gives it a direct claim on the tamper-resistant-log need. But at $434bn it will not move much on this theme. Fine as a low-volatility anchor, unnecessary otherwise.
- Equinix and Digital Realty own the buildings and the interconnects (500,000 at Equinix; 60% of large new contracts from AI). The convexity is real, but 5x net debt/EBITDA makes them the most rate-sensitive way to own the traffic pillar. We would rather own that pillar through VRSN and HPE and skip the REIT leverage.

## 14. Tier 4: options, not core

| **Name** | **The case** | **Why it is only an option** |
|---|---|---|
| **SailPoint (SAIL)** | Identity governance for humans and agents; non-human identities already 40% of identity growth; pricing meters agents, API calls and workflows; $100m AI ARR guided to $900m by FY29. The purest expression of need two. | Executes through volatility; 15% SBC; must prove AI ARR is incremental, not relabelled human seats. Could double, could halve. |
| **DocuSign (DOCU)** | 200m signed agreements, ESIGN/eIDAS legal moat, FedRAMP; Intelligent Agreement Management at $350m ARR heading to high-teens of total, wired into Claude, ChatGPT, Gemini and Agentforce. | Core e-signature business is ex-growth; 4x sales and 8.7% FCF yield price it as a value stock, which is what it is. |
| **Twilio (TWLO)** | Carrier interconnects and number inventory that voice agents cannot replicate; Segment gives customer context; ConversationRelay and the Agent-to-Human protocol; HIPAA compliant. | Near its high at 6.6x; intangibles half of assets; frontier labs could still partner around it. |
| **Okta (OKTA)** | Cleanest story for securing agentic identities; Glasswing partner; rule-of-40; 10x sales. Gartner's access-control statistic is its best marketing. | 11% ARR growth, at an all-time high, history of poor execution and a 2023 breach of trust. Deep out-of-the-money calls beat stock. |
| **Datadog (DDOG) / Dynatrace (DT)** | Observability becomes the financial meter for agent usage; the ROI shows up the moment you can bill by usage. If the Kill Switch bill passes, log retention becomes a compliance requirement rather than an operational choice. | DDOG 21x sales with 21% SBC; PANW/Chronosphere and Cisco/Splunk now compete directly. DT at its high. |
| **Elastic (ESTC)** | The indexed, permission-aware copy of everything an enterprise has; the searchable log layer behind forensic investigation; cRPO +20%, RPO +28%; priced ex-growth at 4.8x with a buyback. | Revenue guided to ~14%; SMB cloud +3%; hybrid search is commoditising. |
| **MongoDB (MDB)** | Atlas re-accelerated to 29% on unchanged list pricing; agents constantly read and write state, and Mongo meters hot data. | New apps written by coding agents default to Postgres; agent platforms may internalise memory. 10.6x sales. |
| **GitLab (GTLB)** | Moving from seats to usage credits (Flex, Orbit) so more agents means more billable surface. | Orbit Remote still in beta with no published pricing; GitHub/Microsoft owns the category's real estate. |
| **DigitalOcean (DOCN)** | High-touch cloud for AI startups; agentic inference cloud; topline re-accelerated. | Capex 34% of revenue leaves ~0% FCF yield at 14x sales; already re-rated then fell 37%. |
| **Fastly (FSLY)** | Highest convexity CDN; AI Accelerator semantic caching; turned FCF positive. | $3.8bn cap, 20% SBC, GAAP losses; a beta bet on the theme. |
| **A10 (ATEN), Bandwidth (BAND), Mitek (MITK), VNET, Rackspace (RXT)** | Niche chokepoints: IPv4 address management, telephony licences, deepfake detection, China data centres, Palantir hosting. | All under $2bn; liquidity, dilution or leverage (RXT $2.75bn debt) cap them at 1% positions. BAND's data feed is unverified. |
| **Circle (CRCL), Coinbase (COIN), PayPal (PYPL)** | Stablecoins and x402 as the payment rail for agents; USDC nanopayments; PYUSD at $4bn. | Far too early to invest in payments solely on agentic upside. Both CRCL and COIN trade on crypto and rates. Not for this sleeve. |

## 15. Avoid: the exposed names

- **Tenable (TENB), Qualys (QLYS), Rapid7 (RPD).** Vulnerability management scans your network for known weaknesses and produces a report. That is the definition of a product that produces an answer rather than enforces a decision.
- **The evidence:** revenue growth has fallen to 8.6% (TENB), 10.6% (QLYS) and −0.3% (RPD) while published vulnerabilities have tripled. Microsoft bundles scanning into licences, CrowdStrike sells Spotlight to its installed base, Google combined Wiz and Mandiant, Anthropic shipped Claude Code Security. Thirteen funded startups (Cyera $600m, Horizon3 $250m, XBOW $120m) target the category with automated remediation.
- **The experiment:** an undergraduate's week-old, sub-$1,000 scanner found 5 of 15 planted flaws against the incumbent's 6, and caught two novel misconfigurations the incumbent flagged as harmless. AI will be better in twelve months; a static vulnerability catalogue will not.
- **The timing evidence:** median days from disclosure to exploitation went 63 days (2018-19) to 5 days (2023) to minus 7 days (2025). When exploitation precedes disclosure, a catalogue of known flaws is looking in the wrong direction.
- **Why section 7 does not change this.** The safety turn creates real demand for supply-chain and vulnerability work. But the money follows automated remediation, which the platforms are absorbing, not the scan report. A bigger market for a commoditised product is not a thesis.
- **The trap:** all three have doubled or tripled from April lows on short squeezes and factor flows. TENB at 4.3x sales with a 6.4% FCF yield looks cheap. It is cheap because it is a melting ice cube. Qualys is the better of the three (native patch loop, IoT positioning), and the tight pair is long QLYS / short TENB — but neither belongs in a long-only sleeve.

## 16. Basket or single names?

> **Own the theme: yes.** Three independent signals point the same way — a physical traffic constraint (Nokia, Cisco), a customer budget shift (IBM's pre-announcement, the Jefferies survey), and reported numbers at the companies that own the chokepoints (FTNT, FFIV, HPE, CRWD). That is a durable trend by our definition.
>
> **Replicate the 26-name index version: no.** Nine of the 26 are under $5bn, several are loss-making with 20%+ dilution, the crypto rails are a different trade, and the weighting scheme forces you to own the weakest names at nearly the same size as the strongest. A broad basket expresses a theme for readers; it is not how a concentrated book should express it.
>
> **Six to eight names, entered on dips or via short puts: yes.** That covers all three pillars with better average quality and a lower average multiple than the published basket.

| **Role** | **Names** | **Indicative weight of the sleeve** | **Entry** |
|---|---|---|---|
| Core: control points | **ZS, FFIV, RBRK, FTNT** | 50% to 55% | ZS now; FFIV starter; RBRK half now; FTNT via puts 15-20% below |
| Traffic and sovereignty | **HPE, VRSN** | 25% | HPE outright; VRSN on 10% dips |
| Best-in-class starter | **NET** | 10% to 15% | 2% starter of the book; add only on 25%+ drawdowns |
| Optional satellites | **SAIL, DOCU, NTAP, TWLO** | 0% to 10% | Only if you want more than eight names |

- **Why puts fit this theme:** implied volatility on ZS, RBRK and FTNT is high, so selling puts 10-20% below the market pays a meaningful premium and, if assigned, gets the entry price our process wants. On the low-volatility names (HPE, VRSN, CSCO) the premium is thin and outright purchase is simpler.
- **The honest gap in the dip bucket.** With the optical-networking line removed, this list no longer contains a genuinely distressed, high-quality entry. The only names more than 30% below their highs are ZS (42%), NTSK (38%), DOCN (37%) and AKAM (36%) — one Tier 1 name and three we would not size. That is the strongest argument for treating this as a shopping list rather than a buy programme: at today's prices, most of these names are purchases we are choosing not to make yet.
- **If you want one-click exposure anyway:** a cyber ETF such as CIBR or HACK holds PANW, CRWD, FTNT, ZS and OKTA at market-cap weights. It captures Pillar 2 but misses HPE and VRSN, misses the agent-utility names entirely, and overweights the two most expensive stocks.

**Free cash flow yield: how much real cash you get today (%)**

<img src="/img/cyber-theme-primer_fig5.png" alt="Free cash flow yield, all names" />

*Source: Financial Modeling Prep, 16 September 2026. NTSK negative and omitted. Gold bars are Tier 1 names. A low yield is not disqualifying for a fast grower, but it tells you how much of the price is future.*

## 17. What could go wrong

- **The rotation is already crowded.** Fortinet, Cloudflare, CrowdStrike, Okta and F5 are at or within 2% of all-time highs. Position sizing and staggered entry are the only defence, which is the whole reason this document exists before the drawdown rather than during it.
- **Rate sensitivity.** The long-duration names (NET, CRWD, RBRK at 14x-47x sales) and the REITs are the most exposed if the rate path turns out higher for longer than currently priced. HPE, VRSN, NTAP and FFIV are the most rate-resilient holdings on the list.
- **"Perfect code."** On a two-to-three-year horizon the question is: if AI eventually writes vulnerability-free software, does security demand fall? Nobody can answer that today, which is why the sleeve should be built from control points (traffic still needs inspecting) rather than from remediation vendors.
- **The safety turn fades.** The essay of 12 September is an intention, not a purchase order. If attention moves on, if the Kill Switch bill dies in committee, or if the labs solve this internally with their own engineering rather than with vendor products, then section 7 converts into nothing. Treat it as a reason to hold the Pillar 2 weighting, never as the reason to add.
- **Agent commerce standards stall.** x402, NET Dollar and agent-to-agent marketplaces are early. If agents keep paying with a human's credit card for years, the B2A pillar underdelivers. We have kept it small for this reason.
- **Hardware cycles roll over.** Fortinet's product surge and F5's refresh cycle are cyclical by nature. 2023 showed how quickly a firewall product cycle can go from +50% to negative. The services annuity cushions it but does not remove it.
- **Hyperscalers internalise.** The biggest risk to MDB, ESTC, DDOG and even NET is that AWS, Google and Microsoft bundle the agent memory, search, observability and edge layers into compute the customer already buys.
- **Evidence concentration.** Much of the qualitative argument in sections 4 to 6 comes from a small number of outside notes covering overlapping ground, and we have not independently re-verified every operating claim in them. The valuation data in section 9 is ours and was pulled directly. Report dates are given throughout so recency can be checked.

## 18. What to watch

- **Whether the safety turn becomes procurement.** The test is a named budget line, not an essay. Watch for "non-human identity" or "agent governance" appearing as a disclosed category on SAIL, OKTA or PANW calls.
- **The AI Kill Switch bill.** If it advances out of committee, log retention and forensics become a compliance requirement and DDOG/ESTC re-rate on revenue quality, not growth. If it dies, nothing happens.
- **Fortinet Q3 (early November):** does product growth hold above 30% and does Unified SASE ARR accelerate a third straight quarter? A miss here re-rates the whole physical-security group.
- **Zscaler Q1 FY27 (late November):** ARR growth above 20% and any comment on agent-driven connection volume. This is the cheapest name; the numbers need to stay boringly good.
- **Rubrik Q3 FY27 (December):** net new subscription ARR above ~$100m and net retention holding 120%. That is the "consensus is too low" test.
- **Commvault litigation:** any resolution of the ARR-disclosure class actions moves CVLT from "wait" to "buy".
- **Vulnerability-management losers:** Tenable's next print is a read on whether bundling has started to bite. If it does, the enforcement-point framework gets more credibility.
- **Check Point weekly attack data:** the series that underpins the cyber-boom thesis. A sustained fall would be the first sign the "AI defends faster than it attacks" counter-thesis is winning.
- **Instinct/Muse adoption:** consumer always-on agents are the "ChatGPT moment" for traffic. Watch OpenRouter token data and app-store rankings.

## 19. Glossary, sources and data notes

| Term | Plain English |
|---|---|
| Agent / agentic AI | Software that carries out multi-step tasks on its own, keeps working without being prompted, and calls other services to do so. |
| North-south / east-west | Traffic between a user and a server (north-south) versus traffic between servers, GPUs and data centres (east-west). Agents create the latter. |
| API | The doorway one piece of software uses to talk to another. Agents make hundreds of API calls per task. |
| CDN | Content delivery network: servers placed close to users so pages load fast. Now being repurposed as "compute delivery networks" for AI. |
| DNS | The internet's address book; turns a name into a routable number. Every request starts here. |
| Zero trust / SASE / ZTNA | Security that checks every connection every time instead of trusting anything inside the office network. Delivered from the cloud (SASE) or inline (ZTNA). |
| Firewall / NGFW | The box (or software) that decides which traffic may pass. Next-gen firewalls also inspect encrypted traffic, which needs custom chips. |
| Observability | Collecting logs and metrics to see what software (and agents) are doing and what they cost. |
| Non-human identity | A credential belonging to a machine or an agent rather than a person. It has to be issued, scoped, watched and revoked like an employee's badge. |
| Vulnerability management | Scanning systems for known weaknesses and producing a prioritised report. The category AI commoditises. |
| MCP | Model Context Protocol: a standard way for an AI model to plug into tools and data. Cloudflare, DocuSign, GitLab and others host or expose MCP servers. |
| x402 / stablecoin rails | A way for an agent to pay for an API call by responding to an HTTP "402 Payment Required" code with a dollar-backed crypto token. |
| ARR / NRR | Annual recurring revenue; net revenue retention (how much existing customers spend this year versus last; 120% means 20% more). |
| SBC | Stock-based compensation as a share of revenue: the dilution shareholders pay for. Above 20% is heavy. |
| Sovereign AI / repatriation | Running AI on infrastructure you own, on-premise or in a private cloud, so your data and models stay yours. |

### Primary sources

- Anthropic, "We Must Pace the Frontier" (CEO essay, 12 September 2026); Anthropic evaluation-incident report, 30 July 2026 (141,006 runs); Anthropic threat intelligence report, September 2026.
- METR investigation into the OpenAI–Hugging Face incident, published 26 August 2026.
- Nokia Global Traffic Report (moderate scenario) — agent machine-to-machine traffic projection.
- Check Point Research — global weekly attacks per organisation series.
- Mandiant — median time from vulnerability disclosure to exploitation.
- Company disclosure: Fortinet Q2 FY26, F5 fiscal Q3, HPE, Akamai, Equinix, VeriSign, CrowdStrike FY27 Q2 (net new ARR $333m; CEO remarks, CNBC), IBM July pre-announcement, Rubrik, NetApp, Commvault, Datadog, Elastic, MongoDB.
- Survey data: Jefferies CIO survey Q1 2026 (cyber budgets); Barclays CIO survey (repatriation); Gartner (agent attack vectors through 2029).
- Financial Modeling Prep — batch quotes, trailing key metrics and quote-change, 16 September 2026.

### Data notes

- All valuation multiples are trailing twelve months. Forward multiples would be lower for the fast growers (RBRK, NET, CRWD) and roughly unchanged for the slow ones.
- PANW trailing EV/Sales is inflated by the CyberArk share issuance and shown as approximate. Bandwidth's key-metrics feed returned corrupted units; those figures are estimates and are marked.
- Prices and ranges are as of 16 September 2026 and have not been refreshed since. Check the live quote before acting on any entry level in this document.
- Operating claims (growth rates, ARR, customer counts) drawn from third-party research were not independently re-verified against filings for this note; report dates are given so recency can be checked.
- Executive compensation, share structure, float and insider activity were not assessed name by name in this theme-level document. Before any position is sized above 5% of the sleeve, a company-level write-up including those sections is the required next step.
- Rankings, tiers and entry suggestions are judgement calls, not facts. Reasonable investors will weight price and quality differently.
