"""
DeepThought — Target Company Research
Research pipeline used to build the 25-company shortlist for Hyderabad
specialty biotech + custom synthesis & specialty chemicals.

This script is illustrative — it documents the *exact process* I followed,
including the AI guardrails. It is not a one-click automation; the human
verification step is deliberate (see README and methodology.md).

Author: [Your Name]
"""

import csv
import json
import re
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional


# ──────────────────────────────────────────────────────────────────────────
#  1. ICP RUBRIC (single source of truth for all scoring)
# ──────────────────────────────────────────────────────────────────────────

CRITERIA = {
    "C1_Manufacturer":  {"weight": 10},
    "C2_India":         {"weight":  5},
    "C3_Differentiated":{"weight": 25},
    "C4_TechnicalDM":   {"weight": 20},
    "C5_GrowingSector": {"weight": 20},
    "C6_GrowthSignals": {"weight": 20},
}

LEVELS = {"Strong": 1.0, "Moderate": 0.5, "Weak": 0.0}

AUTO_DISQUALIFIERS = [
    "trader", "distributor", "importer",
    "cro", "contract research organization", "testing lab", "analytical service",
    "generic pharma", "bulk api", "branded generic",
    "subsidiary of", "a tata", "a reliance",
    "acquired by", "now part of",
    "pe-controlled", "private equity majority",
    "no website", "single-page placeholder",
]

REVENUE_CEILING_CR = 500   # Rs.500Cr — DT's stated upper bound
REVENUE_FLOOR_CR   = 30    # informal lower bound; smaller firms allowed if C3 strong


# ──────────────────────────────────────────────────────────────────────────
#  2. DATA MODEL
# ──────────────────────────────────────────────────────────────────────────

@dataclass
class CriterionScore:
    level: str               # "Weak" | "Moderate" | "Strong"
    evidence: str            # one-line evidence
    source_url: str = ""     # MANDATORY for AI-generated scores

    def points(self, weight: int) -> float:
        return weight * LEVELS[self.level]


@dataclass
class Company:
    name: str
    website: str
    location: str
    segment: str
    products: str
    revenue_cr: Optional[float]   # in INR Crore
    revenue_band: str
    decision_maker: Dict[str, str]  # {name, title, background}
    scores: Dict[str, CriterionScore] = field(default_factory=dict)
    auto_disqualifier_flags: List[str] = field(default_factory=list)
    personalization_hook: str = ""
    confidence: str = "medium"    # high | medium | low

    def federer_score(self) -> int:
        if self.auto_disqualifier_flags:
            return 0
        total = sum(
            self.scores[k].points(CRITERIA[k]["weight"])
            for k in CRITERIA
            if k in self.scores
        )
        return round(total)

    def band(self) -> str:
        s = self.federer_score()
        if s >= 80:  return "A"
        if s >= 60:  return "B"
        if s >= 40:  return "C"
        return "D"

    def revenue_in_band(self) -> bool:
        if self.revenue_cr is None:
            return True   # unknown — don't auto-fail
        return self.revenue_cr <= REVENUE_CEILING_CR


# ──────────────────────────────────────────────────────────────────────────
#  3. ANTI-HALLUCINATION GUARDRAIL FOR AI-ASSISTED SCORING
# ──────────────────────────────────────────────────────────────────────────

SCORING_PROMPT_TEMPLATE = """\
You are scoring an Indian manufacturing company against DeepThought's
6-criterion Federer rubric.  Read the supplied evidence (website text,
LinkedIn page, Tracxn / Tofler page, regulatory filings).

Output a single JSON object with this schema:
{
  "C1_Manufacturer":   {"level": "...", "evidence": "...", "source_url": "..."},
  "C2_India":          {"level": "...", "evidence": "...", "source_url": "..."},
  "C3_Differentiated": {"level": "...", "evidence": "...", "source_url": "..."},
  "C4_TechnicalDM":    {"level": "...", "evidence": "...", "source_url": "..."},
  "C5_GrowingSector":  {"level": "...", "evidence": "...", "source_url": "..."},
  "C6_GrowthSignals":  {"level": "...", "evidence": "...", "source_url": "..."},
  "auto_disqualifier_flags": ["..."],
  "personalization_hook": "one specific true recent fact"
}

HARD RULES — these override everything else:
1. If you cannot point to a specific source URL for a criterion, the level
   MUST be "Weak".  No URL → no score.  Do NOT invent URLs.
2. If revenue exceeds Rs.500Cr, OR the company is a subsidiary, OR PE-controlled,
   OR a CRO / testing lab / pure-trader → add the matching tag to
   auto_disqualifier_flags and mark all six criteria "Weak".
3. The personalization_hook MUST be a single specific recent fact (capacity
   addition, certification, founding-team member quote, etc.) traceable to a
   source URL.  Generic claims like "growing fast" or "innovative company"
   are forbidden.
4. If founder credentials (PhD, IIT, ex-ISRO etc.) are not on the company's
   own About page or LinkedIn, mark C4 as "Moderate" and note "verify in
   pre-call" in the evidence.

Evidence pack is below.  Respond with JSON only, no prose.
"""

NEGATIVE_PROMPT_CHECKLIST = """\
EXCLUDE if any of the following are true:
  - Listed entity with revenue > Rs.500Cr (FY24 or FY25 whichever is later)
  - Acquired by a larger group / PE in the last 24 months
  - PE majority shareholding (>50%)
  - Primarily a CRO, CDMO services or analytical-testing company
  - Generic pharma / bulk API only
  - Subsidiary of a Tata/Reliance/Mahindra/Murugappa-class group
  - No working website or a single-page placeholder
  - Zero visible activity in the last 24 months
"""


# ──────────────────────────────────────────────────────────────────────────
#  4. SOURCE PIPELINE — what was queried, in order
# ──────────────────────────────────────────────────────────────────────────

SOURCES_USED = [
    # name, type, what it gave us
    ("Tracxn",            "DB",   "revenue, founders, incorporation, ownership"),
    ("Tofler",            "DB",   "MCA filings, revenue range, EBITDA trend"),
    ("ZaubaCorp",         "DB",   "directors, CIN, paid-up capital"),
    ("RocketReach",       "DB",   "employee count, headquarters"),
    ("DSIR SIRO PDF",     "Reg",  "DSIR-recognized R&D status"),
    ("USFDA UFFDM",       "Reg",  "USFDA-registered manufacturing facilities"),
    ("LinkedIn",          "Web",  "founder bio, employee count delta, hiring posts"),
    ("Company website",   "Web",  "products, plant locations, certifications"),
    ("BioSpectrum India", "News", "biotech press releases, capacity additions"),
    ("Indian Chemical News","News","chemicals press releases, M&A"),
    ("Economic Times",    "News", "M&A, acquisitions, PE rounds"),
    ("VCCircle",          "News", "PE / VC deal flow"),
    ("Investor pitches",  "Doc",  "DRHPs, annual reports for revenue cross-check"),
]


# ──────────────────────────────────────────────────────────────────────────
#  5. POST-AI VERIFICATION CHECKLIST (the human step)
# ──────────────────────────────────────────────────────────────────────────

VERIFICATION_CHECKLIST = [
    "Revenue confirmed from at least 2 independent sources",
    "Promoter still in seat (no M&A news in last 24 months)",
    "C6 growth signal cleared — at least 2 of 5 thresholds verified",
    "C4 founder credential traceable to company About page or LinkedIn",
    "Personalization hook is specific, recent, and source-cited",
    "No auto-disqualifier triggered",
]


# ──────────────────────────────────────────────────────────────────────────
#  6. FINAL 25 — DATA-LOADER (the actual research output)
# ──────────────────────────────────────────────────────────────────────────

def load_final_25(csv_path: str) -> List[Dict]:
    """Load the final 25 PASS companies from the deliverable CSV."""
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def summary_stats(rows: List[Dict]) -> Dict:
    """Compute stats over the final 25 for the methodology doc."""
    bands = {}
    segments = {}
    revenue_bands = {}
    for r in rows:
        bands[r["Band"]]               = bands.get(r["Band"], 0) + 1
        segments[r["Segment"]]         = segments.get(r["Segment"], 0) + 1
        revenue_bands[r["Revenue Band"]] = revenue_bands.get(r["Revenue Band"], 0) + 1
    return {
        "n_companies": len(rows),
        "by_band": bands,
        "by_segment": segments,
        "by_revenue_band": revenue_bands,
    }


# ──────────────────────────────────────────────────────────────────────────
#  7. (Illustrative) Auto-disqualify pre-screen
# ──────────────────────────────────────────────────────────────────────────

def pre_screen_text(name: str, blob: str) -> List[str]:
    """Return list of disqualifier tags found in a free-text blob."""
    blob_lc = blob.lower()
    flags = []
    for kw in AUTO_DISQUALIFIERS:
        if kw in blob_lc:
            flags.append(kw)
    # crude revenue check
    m = re.search(r"revenue[^0-9]*?(\d{2,5})\s*(cr|crore)", blob_lc)
    if m:
        try:
            cr = float(m.group(1))
            if cr > REVENUE_CEILING_CR:
                flags.append(f"revenue >Rs.{REVENUE_CEILING_CR}Cr (~Rs.{cr}Cr)")
        except ValueError:
            pass
    return flags


# ──────────────────────────────────────────────────────────────────────────
#  8. Entry point — produces the methodology summary block
# ──────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    csv_path = sys.argv[1] if len(sys.argv) > 1 else \
        "../data/25_target_companies_hyderabad.csv"
    rows = load_final_25(csv_path)
    stats = summary_stats(rows)
    print(json.dumps(stats, indent=2))
    print("\nVerification checklist applied to every row:")
    for c in VERIFICATION_CHECKLIST:
        print(f"  [x] {c}")
