# AI Prompts Used — DeepThought Target Company Research

This file documents the **exact prompts** I wrote when using AI tools (Claude / Gemini) during this assignment, plus the negative prompts used as anti-hallucination guardrails. Prompts are reproduced verbatim so they can be audited.

---

## Prompt 1 — Discovery (broad name generation)

> "List Indian privately-held specialty manufacturing companies headquartered in Hyderabad, with revenue between Rs.50Cr and Rs.500Cr, in (a) specialty biotech (probiotics, enzymes, recombinant proteins, fermentation services), (b) custom synthesis & specialty chemicals (pharma intermediates, agrochem intermediates, catalysts), (c) hybrid seeds & specialty agri-inputs, (d) specialty diagnostics. **Do not include** Bharat Biotech, Granules India, Aragen, Suven Pharma, Sai Life Sciences, Divi's Labs, Laurus Labs, Optimus Drugs, or any other company that is (i) listed with revenue >Rs.500Cr, (ii) PE-controlled, (iii) a subsidiary, or (iv) primarily a CRO. For each candidate, give: company name, website, founder name, one-line product description, and the source URL where you read about them. **If you cannot point to a source URL, do NOT include the company.**"

## Prompt 2 — Per-company qualification (the core scoring prompt)

> "You are scoring an Indian manufacturing company against DeepThought's 6-criterion Federer rubric. Read the supplied evidence pack (website text, LinkedIn page, Tracxn / Tofler page, regulatory filings).
>
> Output JSON with C1..C6 each as `{level, evidence, source_url}` plus `auto_disqualifier_flags` and `personalization_hook`.
>
> Hard rules (override everything else):
> 1. No source URL → level MUST be 'Weak'. Do NOT invent URLs.
> 2. If revenue >Rs.500Cr OR subsidiary OR PE-controlled OR CRO/testing-lab/trader → tag in `auto_disqualifier_flags` and mark all six 'Weak'.
> 3. Personalization hook MUST be a single specific recent fact traceable to a source URL. Generic 'innovative company' phrases are forbidden.
> 4. If founder credentials (PhD/IIT/ex-ISRO) are not on the company's About page or LinkedIn, mark C4 'Moderate' and note 'verify in pre-call'.
>
> Respond with JSON only, no prose."

## Prompt 3 — Personalization hook (after qualification passes)

> "Given this company's website + LinkedIn + last 12 months of press, give me ONE specific, true, recent fact (capacity addition, certification, founder quote, technology partnership, fundraise) that could be the first line of an outreach email. The fact must be (a) verifiable from the supplied URLs, (b) more recent than 18 months, and (c) specific enough that the recipient cannot mistake it for a generic compliment. If you can't find such a fact, say 'NO HOOK' — do not invent one."

## Prompt 4 — Cross-check (run with a different LLM provider)

> "Below is a Federer score and evidence pack produced by another AI for [Company X]. Re-score independently using the same rubric. Flag any criterion where the original evidence is (a) missing, (b) outdated (>24 months), or (c) cannot be confirmed from the cited URL. Output: 'AGREE' or 'DISAGREE on Cn because <reason>'."

---

## Negative prompts (the most important part)

These are appended to every prompt above:

```
EXCLUDE if any of the following are true:
  - Listed entity with revenue > Rs.500Cr (FY24 or FY25 whichever is later)
  - Acquired by a larger group / PE in the last 24 months
  - PE majority shareholding (>50%)
  - Primarily a CRO, CDMO services or analytical-testing company
  - Generic pharma / bulk API only
  - Subsidiary of a Tata/Reliance/Mahindra/Murugappa-class group
  - No working website or a single-page placeholder
  - Zero visible activity in the last 24 months

NEVER:
  - Invent revenue figures — only return what is in MCA / Tofler / Tracxn / investor presentations.
  - Claim 'DSIR-recognized', 'USFDA-approved', 'IIT-alumni' without a source URL on the company's own website or a regulator's site.
  - Generate a 'personalization hook' that says 'growing fast' or 'innovative' — that is a generic claim, not a hook.
  - Include a company on the basis of website language alone — every claim needs a second confirming source.
```

---

## What I caught the AI doing wrong

Documenting these because the assignment specifically asks where I disagreed with AI:

1. **AI proposed Bharat Biotech as a 'perfect Federer'.** It is listed, revenue Rs.1,463Cr (FY25), and primarily a vaccine manufacturer (auto-disqualified per ICP). Rejected and added to fail list.
2. **AI confidently cited 'Sapala Organics revenue Rs.75.6Cr (FY24)'**. The latest filing was Rs.54.7Cr (FY25) — a 28% YoY *decline*. AI was reading a stale snapshot. I corrected the record and dropped C6 from Strong to Moderate.
3. **AI claimed 'Suven Pharma is founder-led, technical decision-maker, growing'.** Suven Pharma was acquired by Advent in 2022 — PE-controlled. The brief itself uses Suven as the FAIL example. AI ignored the auto-disqualifier rule. Rejected.
4. **AI fabricated 'IIT Delhi alumnus' tag for two founders** (whose actual education was Osmania / JNTU per their LinkedIn). C4 score forced to Moderate, flagged 'verify in pre-call'.
5. **AI wrote a personalization hook that said 'building India's biotech future'.** Generic, forbidden. Replaced with a specific fact (Plant 1 capacity 980 Kg) from the company's own LinkedIn.
6. **AI included two companies that are CROs with manufacturing-style websites** (Aragen, Aurigene). Both auto-disqualified — services, not products.
7. **AI suggested Megafine Pharma as a Hyderabad firm.** It is primarily Mumbai/Nashik with limited Hyderabad presence; it was also acquired by Motilal Oswal Alternates in 2025 (PE). Rejected.
