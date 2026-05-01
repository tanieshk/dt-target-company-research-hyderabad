# Part B — Sourcing Strategy + 1000-Company Scale-Up Proposal
**For:** DeepThought Business Analytics Internship  
**Author:** [Your Name]

---

## QUESTION 1 — Sourcing Methods

**Goal:** find Federer-profile companies (specialty manufacturer, Rs.50-500Cr, technical promoter, growing) across India, beyond what surface-level Google search can yield.

### Method 1 — MCA / Tofler / ZaubaCorp programmatic queries
**Why it works for this ICP:** Every Indian company files with the MCA. Filters on (a) NIC code (24 — chemicals, 21 — pharma, 20 — fertilisers/agrochem, 32.5 — medical devices), (b) revenue band (Rs.50-500Cr), (c) ownership pattern (paid-up capital + promoter share >50%), produce a clean shortlist that already filters out subsidiaries, PE-controlled and traders.  
**Limitation:** Stale by 6-12 months; doesn't show the founder's pedigree — that requires layering.

### Method 2 — DSIR SIRO / In-house R&D directory
**Why it works:** DSIR-recognized R&D status is one of DeepThought's exact C3 signals. The annual PDF directory lists every recognized in-house R&D unit by company, location and date of recognition.  
**Limitation:** PDF format — needs OCR + parsing. Doesn't capture firms with informal R&D.

### Method 3 — USFDA / EU-GMP / WHO-PQ inspection databases + DCGI manufacturing licences
**Why it works:** Filters for *regulated* manufacturers — auto-cleans CROs, traders, formulation-only repackers. Every firm here makes something physical that has cleared a regulator. Strongest single proxy for C1 + C3 in pharma/biotech.  
**Limitation:** Misses non-regulated specialty (agrochem, performance chemicals).

### Method 4 — IndiaMART / TradeIndia / ExportersIndia category pages, treated as discovery (not as truth)
**Why it works:** Long-tail discovery; surfaces founder-led MSMEs the trade press never covers.  
**Limitation:** ~80% of "manufacturers" listed are traders. Use only for **name discovery**; verify everything downstream.

### Method 5 — Industry association member directories
- **CII Pharma Council, IDMA, IPA** — bulk drug + intermediates makers
- **Pesticides Manufacturers & Formulators Association of India (PMFAI), CCFI** — agrochem
- **ABLE (Association of Biotechnology-Led Enterprises)** — biotech
- **Federation of Indian Export Organisations (FIEO)** — chapters by state
- **CHEMEXCIL** — specialty chemicals export council

**Why it works:** Members opt-in, pay dues, and report manufacturing capacity → already pre-filters traders. Each member entry usually carries one named promoter contact.  
**Limitation:** Membership is voluntary — a real Federer may not be listed.

### Method 6 — Industry events + expos as concentrated lead pools
- **CPHI India** (pharma + intermediates) — exhibitor list is published with stand details
- **Chemspec India / Chemexpo / Pharmac India**
- **BioAsia (Hyderabad), BIOTECH Expo, India Animal Health Summit**
- **AGROCHEM Summit, Indian Agrochem Conclave**
- **MEDFAIR, India Medical Device Show**

**Why it works:** Exhibitor lists are downloadable. Companies that pay for a stand at CPHI India are by definition *not stagnant.* Booth size correlates loosely with revenue band.  
**Limitation:** Same exhibitor universe across years — diminishing marginal yield after one cycle.

### Method 7 — PLI scheme beneficiary lists + state government incentive rolls
- **PLI for bulk drugs, medical devices, specialty steel** — DoP and DoCA publish beneficiary lists
- **Telangana / Gujarat / Karnataka / TN incentive rolls** publish capex announcements

**Why it works:** Direct C5 (sector tailwind) + C6 (active growth — capex announced) signal in one source.  
**Limitation:** Skews toward larger companies that can absorb the compliance cost.

### Method 8 — IIT / IISc / NIT / BITS / IICT alumni founder networks
**Why it works:** Direct C4 (technical decision-maker) signal; many alumni networks publish entrepreneur lists.  
**Limitation:** Manual; small per-search yield, but extremely high quality per hit.

### Method 9 — Patent + paper authorship lookups
USPTO and Indian patent office assignee searches by Indian addresses for relevant CPC codes (C07 organic chemistry, C12N microbiology, A01N agrochem) surface companies that *demonstrably* invent — the strongest possible C3 evidence.  
**Limitation:** Patent dataset cleaning is non-trivial.

### Method 10 — Banker / CA / IPO-DRHP secondary networks
DRHPs of mid-cap specialty firms (e.g., Anthem Biosciences, Aether Industries, Laxmi Organic) include detailed peer-set tables — competitor analysis published in DRHPs is the single best curated map of an industry.  
**Limitation:** DRHPs are episodic; not a continuous feed.

### Method 11 (creative) — Google Maps "industrial estate" sweeps
Hyderabad's IDA Bollaram, IDA Mallapur, IDA Uppal, Choutuppal SEZ; Pune's Ranjangaon and Chakan; Ahmedabad's GIDC Ankleshwar/Dahej — Maps lists every plant in these zones with the company name. A scripted sweep finds promoters running plants who don't show up online elsewhere.  
**Limitation:** Maps data is messy; needs cleanup.

### Method 12 (creative) — LinkedIn structured-search via Sales Navigator + headcount-deltas
Filter for company size 51-500 + headquarters India + industry "Pharmaceutical Manufacturing" / "Chemical Manufacturing" / "Biotechnology Research" + headcount growth >10% YoY → instant C6 + scale-band match. Deeper: people-search for "PhD" + "founder" + city.  
**Limitation:** Sales Navigator licence cost; LinkedIn's anti-scraping enforcement.

### Method 13 (creative) — Shipping-bill / DGFT export-data pulls
Subscriptions like Volza, ExportGenius, Connect2India publish HS-code-level export records by exporter. Filtering for HS 29 (organic chemistry), 30 (pharma), 38 (misc chemical) by Indian exporter, with shipment count growth → confirms the manufacturer is real, exporting, and growing.  
**Limitation:** Paid; data quality varies.

### Method 14 (creative) — Hiring-platform reverse-search
Naukri / LinkedIn job posts for "Production Chemist", "QC Manager — API", "Fermentation Scientist" → click through to the posting company → cross-check against the rest of the funnel. This is the cleanest single C6 (active hiring) confirmation step.  
**Limitation:** Surfaces only currently-hiring firms.

---

## QUESTION 2 — The 1000-Company Proposal

### TL;DR

> **Build the 1000-company list as a 4-stage funnel: Source → Auto-qualify → Human verify → Personalise. Source 6,000-8,000 candidate names from 6 structured databases. AI-qualify down to ~3,000 ICP-aligned candidates. Human-verify ~1,800 in batches of 200/day. Final 1,000 with personalisation hooks. Yield: 12-17% from raw discovery, ~33% from human-verify stage. Cost: 4 weeks, 1 analyst (me) + 1 AI agent stack (Claude/Gemini + Antigravity + scraping infrastructure).**

### Architecture

```
   ┌─────────────────────────────────────────────────────────┐
   │ STAGE 0  | Define ICP rules + scoring schema (Day 1-2) │
   └─────────────────────────────────────────────────────────┘
                              │
   ┌──────────────────────────▼──────────────────────────────┐
   │ STAGE 1  | SOURCE: 6,000-8,000 raw company names         │
   │  • MCA + Tofler scrape (NIC 20, 21, 24, 32) — 3,500     │
   │  • DSIR SIRO directory parse — 1,200                    │
   │  • CPHI/Chemspec/BioAsia exhibitor lists — 800          │
   │  • Industry assoc directories (IDMA, ABLE, PMFAI) — 1,000│
   │  • Google Maps industrial-estate sweep — 700            │
   │  • DGFT export shipping data — 600                      │
   └──────────────────────────┬──────────────────────────────┘
                              │
   ┌──────────────────────────▼──────────────────────────────┐
   │ STAGE 2  | AUTO-DEDUP + AUTO-DISQUALIFY  → ~5,000        │
   │  • Fuzzy-match on PAN/CIN to dedup                      │
   │  • Auto-reject:                                         │
   │     - listed mega-caps (revenue > Rs.500Cr)             │
   │     - PE/MNC-controlled (M&A press signals)             │
   │     - subsidiary keywords ("a XYZ Group company")       │
   │     - CRO / testing-lab keywords                        │
   │     - traders (no manufacturing licence)                │
   └──────────────────────────┬──────────────────────────────┘
                              │
   ┌──────────────────────────▼──────────────────────────────┐
   │ STAGE 3  | AI-QUALIFY (Claude/Gemini) → ~3,000           │
   │  • Per company: pull website + LinkedIn + Tracxn page   │
   │  • LLM prompt scores against C1-C6 with evidence req'd  │
   │  • Hallucination guardrail: "no answer if no source URL"│
   │  • Output: structured JSON with score + evidence URLs   │
   └──────────────────────────┬──────────────────────────────┘
                              │
   ┌──────────────────────────▼──────────────────────────────┐
   │ STAGE 4  | HUMAN VERIFY (the analyst — me) → ~1,800     │
   │  • Spot-check 100% of A-band, 30% of B-band             │
   │  • Reject any score with hallucinated/missing evidence   │
   │  • Add personalization hook (one specific recent fact)  │
   │  • 200 verifies/day × 9 days = 1,800                    │
   └──────────────────────────┬──────────────────────────────┘
                              │
   ┌──────────────────────────▼──────────────────────────────┐
   │ STAGE 5  | RANK + DELIVER 1,000                          │
   │  • Sort by Federer Score; top 1,000 → CRM-ready CSV     │
   │  • 200-300 backup B/C companies as buffer               │
   └─────────────────────────────────────────────────────────┘
```

### Yield assumptions

| Stage | In | Out | Yield | Justification |
|-------|----|-----|-------|---------------|
| Source | 0 | 7,000 | — | Empirical: each source gives 600-3,500 names (overlap accepted) |
| Auto-dedup + auto-disqualify | 7,000 | 5,000 | 71% | ~30% lost to dedup + obvious disqualifiers |
| AI-qualify | 5,000 | 3,000 | 60% | Conservative — many MCA-listed firms turn out to be traders |
| Human verify | 3,000 | 1,800 | 60% | DeepThought's own observed yield is ~30% from raw discovery; I expect higher from AI-pre-scored pool |
| Final selection | 1,800 | 1,000 | 56% | Pick top 1,000 by score, hold 800 as backup |
| **End-to-end** | **0** | **1,000** | **14% of raw** | Aligns with DT's published 30% yield from "investigated" |

### Week-by-week plan

**Week 1 — Foundations (the hardest week)**
- Day 1-2: Lock the ICP scoring rubric, write 3 LLM prompt templates (qualify, score, hook) with hallucination guardrails. Set up the data warehouse (Postgres or Notion-as-DB or Airtable).
- Day 3-4: Build the MCA/Tofler/Tracxn scraper (or use Surepass/Probe42 APIs if licensed). Parse the DSIR SIRO directory PDF (OCR + regex).
- Day 5-6: Pull CPHI/BioAsia/Chemspec exhibitor lists; pull industry-association member rolls.
- Day 7: First raw list of ~3,000 names assembled. Auto-dedup pass.
- **Week 1 deliverable:** 3,000 deduped names with raw-source attribution.

**Week 2 — Source + AI-qualify**
- Day 8-9: Add Google Maps industrial-estate sweep, DGFT export-bill names → list grows to ~7,000.
- Day 10-11: Auto-disqualify pass (listed mega-caps, PE/MNC keywords, subsidiary phrases, CRO/trader keywords). List drops to ~5,000.
- Day 12-14: Run AI-qualify on all 5,000. Each company gets website + LinkedIn + Tracxn URL + filing data fed into a Claude/Gemini scoring prompt that outputs JSON with C1-C6 scores AND a source URL per criterion. **No source URL = no score (forced by prompt).** List drops to ~3,000 ICP-aligned.
- **Week 2 deliverable:** 3,000 AI-scored candidates with evidence URLs.

**Week 3 — Human verify (the part that matters)**
- Day 15-23: Verify 200/day. Workflow per company:
  1. Open the AI's evidence URLs — confirm they actually say what the AI claims (this catches ~10-15% hallucination).
  2. Re-score any criterion where evidence is weak; downgrade or auto-reject.
  3. Confirm promoter is still in seat (search recent M&A news).
  4. Confirm at least one C6 signal (hiring post / capex press / certification).
  5. Add a one-line personalisation hook from public sources.
- Run a daily 30-min loop with the AI: "here are the 20 I rejected today, why? — adjust the scoring prompt."
- **Week 3 deliverable:** 1,800 human-verified companies in the funnel.

**Week 4 — Rank, polish, deliver**
- Day 24-26: Re-score the top 1,800 with the final-version prompt; select top 1,000 by Federer Score.
- Day 27-28: Stratify deliverable by city (top 8 manufacturing hubs) and segment so the sales team can attack horizontally or vertically.
- Day 29: QA pass — random spot-check 50 of the 1,000; if hallucination rate >5%, push 100 fixes through.
- Day 30: Hand-off CSV + methodology + the residual 800 (B-band buffer) + the 200-company "research deeper" bucket.
- **Week 4 deliverable:** 1,000 ICP-qualified companies + 800 backup + ops handover doc.

### Quality control mechanisms

1. **Mandatory evidence URL per criterion.** No URL → score reverts to "Weak". This single rule kills ~80% of LLM hallucination.
2. **Negative-prompt checklist.** Every AI scoring call appends: "DO NOT include if (i) listed entity revenue > Rs.500Cr, (ii) acquired by larger group in last 24 months, (iii) PE majority holding, (iv) primarily a CRO/CDMO services without own product, (v) no website or single-page placeholder."
3. **20%-spot-check audit.** A separate AI agent re-scores a random 20% sample using a different prompt and provider (Claude vs Gemini). Mismatch >15% triggers a rubric review.
4. **Cross-source confirmation rule.** A company can only be A-band if at least 2 independent sources confirm the headline claim (e.g., revenue from Tofler + revenue from Tracxn; or DSIR + USFDA; or MCA + LinkedIn employee count delta).
5. **Promoter-still-in-seat check.** A scripted M&A news lookup runs nightly on the in-funnel list — anyone acquired in the previous 24 months gets auto-flagged for re-review.
6. **Recency window for C6.** Any growth signal older than 18 months (per the rubric) is automatically discounted to "weak" regardless of the strength of the original signal.

### Tooling I would use

| Layer | Tool |
|-------|------|
| Discovery (semi-structured scrape) | Antigravity / Playwright / ScrapingBee |
| Data store + dedup | Postgres + a CIN-based primary key |
| LLM qualification | Claude (rubric scoring) + Gemini (cross-check sample) |
| Document parsing (DSIR PDF, DRHPs) | LlamaIndex + Tesseract OCR |
| Workflow orchestration | n8n or Airflow (each stage as a DAG) |
| Human review UI | Airtable or Retool — the analyst sees one company at a time with all evidence URLs prefilled |
| News & event monitoring | Google Alerts + a custom RSS aggregator on Hindi BusinessLine + Telugu Eenadu industrial sections |

### What can go wrong

- **Source overlap.** 7,000 raw names probably has only ~5,000 unique CINs. Build dedup robustly from day one.
- **AI confidently scoring stale data.** Mitigated by forcing source URLs and date filters in the prompt.
- **Promoter exits during the project.** The PE-rollup of Indian specialty manufacturers is fast (5+ deals in 18 months I tracked for Part A). The nightly M&A scan is non-optional.
- **Recruiter spot-check finding a fabricated bio.** Mitigated by the cross-source rule and the rubric's evidence requirement.
- **Yield falls below 1,000.** Backup plan: drop to 800 A-band + 200 best B-band; or expand to a 7th source (sector-specific patent searches).

### Realistic delivery

Net of holidays, sick days, and one full week of build / debug / scrap-and-redo, **30 working days** is achievable for **1,000 verified ICP-qualified companies + 800 buffer.** The hard constraint is not the volume — AI handles that — but the *human verification throughput.* 200/day is the realistic peak rate before quality drops.

---

*The hand-drawn diagram is sent separately on Internshala chat.*
