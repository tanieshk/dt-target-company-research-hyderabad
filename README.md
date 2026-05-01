# DeepThought — Business Analytics Internship Assignment
**Submission: Target Company Research (Hyderabad — Specialty Biotech + Custom Synthesis & Specialty Chemicals)**

> *48-hour assignment.  Submission deadline: 02 May 2026.*

---

## What's in this repository

```
dt_assignment/
├── README.md                                ← this file (start here)
├── data/
│   ├── 25_target_companies_hyderabad.csv    ← Part A deliverable (the 25 PASS companies)
│   └── fail_list.csv                        ← 30+ companies researched and rejected, with reasons
├── docs/
│   ├── methodology.md                       ← how I did the research (Part A)
│   └── PartB_1000_company_proposal.md       ← Part B — sourcing methods + 1000-company plan
└── code/
    ├── research_pipeline.py                 ← illustrative pipeline + ICP rubric in code
    └── ai_prompts.md                        ← exact AI prompts + negative prompts used
```

---

## Quick read order for the recruiter

1. **`data/25_target_companies_hyderabad.csv`** — the headline deliverable. 25 Federer-profile companies in Hyderabad, scored on all 6 criteria with one line of evidence per criterion, banded A/B/C, with a personalization hook per company.
2. **`docs/methodology.md`** — why Hyderabad, why these two segments, the funnel I ran, the sources I used, the borderline calls I made, and where I disagreed with the AI.
3. **`data/fail_list.csv`** — the 30+ companies I researched and rejected, with the disqualifier called out for each. This is where the recruiter can stress-test ICP judgment.
4. **`docs/PartB_1000_company_proposal.md`** — sourcing methods + the 4-week plan to build 1,000 ICP-qualified companies.
5. **`code/`** — the rubric expressed as code, plus the exact AI prompts and negative prompts I used as anti-hallucination guardrails.

---
## 🧠 Thought Process (Hand-drawn Sketch)

![Thought Process](./THOUGHT PROCESS HAND DRAWN.pdf)
---

## Headline numbers

| | Final 25 |
|---|---|
| A-band (80-100) | 11 |
| B-band (60-79) | 13 |
| C-band (40-59) | 1 |
| Median revenue band | Rs.30-100Cr |
| % with promoter still in seat | 100% (auto-disqualified otherwise) |
| % with technical (PhD / IIT / IICT / ex-ICRISAT) decision-maker | 76% |
| % with at least 2 of 5 C6 growth signals | 100% |

## Headline observations (full version in methodology.md)

1. **The Federer band in Hyderabad is shrinking, not growing.** PE money has rolled up the Rs.300-500Cr cohort in the last 4 years (Suven → Advent, Optimus → PAG, Sai Life → TPG, Vasant → ICIG, Novopor → Bain). DeepThought's window is *before* the PE call. Over-index on Rs.50-200Cr.
2. **Specialty biotech in Hyderabad is bimodal.** Either listed mega-caps or scientist-founder <Rs.50Cr — very little in between. The Federer pool here looks like "scientist-founder, sub-Rs.50Cr, deep IP."
3. **Strongest 2nd-gen transitions are in Rs.50-300Cr custom synthesis** (Bhagiradha, Synergene, Vasudha) — the most receptive prospects right now.

---

## Submission checklist (per the brief)

| # | Item | Where | Status |
|---|------|-------|--------|
| 1 | CSV with 25 companies (scored, with evidence) | GitHub / Google Drive → link on Internshala | ✅ this repo |
| 2 | Methodology document | Same repo | ✅ `docs/methodology.md` |
| 3 | Code (and AI prompts) | Same repo | ✅ `code/` |
| 4 | Sourcing methods (Question 1) | Internshala chat window | ✅ — also in `docs/PartB_1000_company_proposal.md` (paste from there) |
| 5 | 1000-company proposal (full write-up) | GitHub → link on Internshala | ✅ `docs/PartB_1000_company_proposal.md` |
| 6 | **Hand-drawn diagram of the 1000-company plan** | **Photo in Internshala chat** | **⚠️ TO DO BY APPLICANT — see below** |


## Author's note

I used AI extensively (Claude / Gemini) but applied four guardrails against hallucination:

1. **Mandatory source URL per criterion** — no URL = score reverts to "Weak".
2. **Negative prompts** — explicit `EXCLUDE if listed >Rs.500Cr / PE-controlled / subsidiary / CRO / etc.`
3. **Cross-source rule** — A-band requires 2 independent confirming sources for the headline claim.
4. **Manual override on every score** — every row in the CSV was hand-verified against company website + LinkedIn + Tofler/Tracxn before inclusion.

Where I disagreed with the AI is documented at the end of `code/ai_prompts.md`.
