"""
Alternative credit scoring for Mizan.

Banks in Algeria turn away cash-based shops because there are no audited
accounts to read. This module scores a merchant from the signals that
informal businesses do leave behind: how much cash moves through the shop,
how regularly the owner restocks, whether utility bills get paid on time,
and how long the business has been running.

It is a transparent rule engine, not a trained model. Every weight and
threshold is a named constant below, so a credit officer can read the
logic, question it, and change it without touching the code further down.

The engine works in Algerian Dinar. Values entered in Naira or Rand are
converted to dinar first (see currency.py).

The functions return codes such as "short_history" rather than sentences,
so the interface can show them in English, French or Arabic.
"""

import math
from dataclasses import dataclass, field

SCORE_MIN = 300
SCORE_MAX = 850

# How much each vector counts toward the final score. Must add up to 1.0.
WEIGHTS = {
    "cash_flow": 0.30,
    "utility": 0.30,
    "restocking": 0.20,
    "tenure": 0.20,
}

# Calibration points. A merchant at or above the "full marks" level on a
# vector gets 100 for it, and one at or below the floor gets 0.
CASH_FLOW_FLOOR_DZD = 40_000
CASH_FLOW_FULL_MARKS_DZD = 600_000
RESTOCKS_FOR_FULL_MARKS = 8        # orders to suppliers per month
MONTHS_FOR_FULL_MARKS = 60         # five years in business
NEUTRAL_UTILITY_SCORE = 50         # used when the merchant has no bill history

# Score boundaries for each tier.
TIER_A_MIN = 700
TIER_B_MIN = 580

# A business younger than this cannot be Tier A, whatever else it shows.
MIN_MONTHS_FOR_TIER_A = 6

# Flag thresholds
LATE_PAYER_BELOW_PCT = 70
IRREGULAR_RESTOCK_AT_OR_BELOW = 1

# What we offer each tier. The amount is a multiple of monthly cash flow.
FINANCING_RULES = {
    "A": {"product": "working_capital_line", "cash_flow_multiple": 3.0, "term_months": 12},
    "B": {"product": "supplier_credit_advance", "cash_flow_multiple": 1.5, "term_months": 6},
    "C": {"product": "credit_builder_loan", "cash_flow_multiple": 0.5, "term_months": 3},
}

RISK_LEVELS = {"A": "low", "B": "moderate", "C": "high"}


@dataclass
class MerchantProfile:
    """What we know about a merchant. All money is in Algerian Dinar."""
    monthly_cash_flow_dzd: float
    supplier_orders_per_month: float
    utility_on_time_pct: float | None   # None means no bill history
    months_in_operation: int


@dataclass
class Financing:
    product: str
    amount_dzd: float
    term_months: int


@dataclass
class Assessment:
    score: int
    tier: str
    risk_level: str
    vector_scores: dict
    flags: list = field(default_factory=list)
    financing: Financing | None = None


def _clamp(value, low=0.0, high=100.0):
    return max(low, min(high, value))


def _check_inputs(profile):
    """Stop early on values that make no sense instead of scoring them."""
    if profile.monthly_cash_flow_dzd < 0:
        raise ValueError("Monthly cash flow cannot be negative")
    if profile.supplier_orders_per_month < 0:
        raise ValueError("Supplier orders per month cannot be negative")
    if profile.months_in_operation < 0:
        raise ValueError("Months in operation cannot be negative")
    pct = profile.utility_on_time_pct
    if pct is not None and not 0 <= pct <= 100:
        raise ValueError("Utility on-time percentage must be between 0 and 100")


def score_cash_flow(monthly_cash_flow_dzd):
    """
    Cash flow differs enormously between shops, so we measure it on a log
    scale: going from 40,000 to 80,000 DZD matters about as much as going
    from 300,000 to 600,000.
    """
    if monthly_cash_flow_dzd <= CASH_FLOW_FLOOR_DZD:
        return 0.0
    position = math.log(monthly_cash_flow_dzd / CASH_FLOW_FLOOR_DZD) / math.log(
        CASH_FLOW_FULL_MARKS_DZD / CASH_FLOW_FLOOR_DZD
    )
    return _clamp(position * 100)


def score_utility(on_time_pct):
    """
    Squared on purpose: paying 80% of bills on time is noticeably worse than
    paying 90%, so the penalty grows as the record gets weaker.
    """
    if on_time_pct is None:
        return float(NEUTRAL_UTILITY_SCORE)
    return (on_time_pct / 100) ** 2 * 100


def score_restocking(orders_per_month):
    """
    Regular restocking means stock is selling. The square root means the
    first few orders count the most, and the gain flattens near the cap.
    """
    return _clamp(math.sqrt(orders_per_month / RESTOCKS_FOR_FULL_MARKS) * 100)


def score_tenure(months_in_operation):
    """Longer track record, lower risk, with gains slowing over time."""
    return _clamp(math.sqrt(months_in_operation / MONTHS_FOR_FULL_MARKS) * 100)


def classify(score):
    """Turn a 300-850 score into Tier A, B or C."""
    if score >= TIER_A_MIN:
        return "A"
    if score >= TIER_B_MIN:
        return "B"
    return "C"


def recommend_financing(tier, monthly_cash_flow_dzd):
    """Size an offer from the tier, rounded to the nearest 1,000 DZD."""
    rule = FINANCING_RULES[tier]
    raw_amount = monthly_cash_flow_dzd * rule["cash_flow_multiple"]
    return Financing(
        product=rule["product"],
        amount_dzd=round(raw_amount / 1000) * 1000,
        term_months=rule["term_months"],
    )


def _collect_flags(profile):
    flags = []
    if profile.utility_on_time_pct is None:
        flags.append("no_utility_history")
    elif profile.utility_on_time_pct < LATE_PAYER_BELOW_PCT:
        flags.append("late_utility_payments")
    if profile.supplier_orders_per_month <= IRREGULAR_RESTOCK_AT_OR_BELOW:
        flags.append("irregular_restocking")
    if profile.months_in_operation < MIN_MONTHS_FOR_TIER_A:
        flags.append("short_history")
    return flags


def assess(profile):
    """Run the full assessment: vectors, score, tier, flags and offer."""
    _check_inputs(profile)

    vector_scores = {
        "cash_flow": score_cash_flow(profile.monthly_cash_flow_dzd),
        "utility": score_utility(profile.utility_on_time_pct),
        "restocking": score_restocking(profile.supplier_orders_per_month),
        "tenure": score_tenure(profile.months_in_operation),
    }

    composite = sum(vector_scores[name] * WEIGHTS[name] for name in WEIGHTS)
    score = round(SCORE_MIN + composite / 100 * (SCORE_MAX - SCORE_MIN))

    flags = _collect_flags(profile)
    if "short_history" in flags:
        score = min(score, TIER_A_MIN - 1)

    tier = classify(score)
    return Assessment(
        score=score,
        tier=tier,
        risk_level=RISK_LEVELS[tier],
        vector_scores=vector_scores,
        flags=flags,
        financing=recommend_financing(tier, profile.monthly_cash_flow_dzd),
    )


if __name__ == "__main__":
    # Quick check you can run by hand: python scoring.py
    examples = [
        ("Established wholesaler", MerchantProfile(450_000, 8, 95, 60)),
        ("Steady neighbourhood shop", MerchantProfile(120_000, 3, 80, 24)),
        ("New small kiosk", MerchantProfile(50_000, 1, 40, 4)),
    ]
    for name, profile in examples:
        result = assess(profile)
        offer = result.financing
        print(f"{name}: {result.score} / Tier {result.tier} ({result.risk_level} risk)")
        print(f"  offer: {offer.product}, {offer.amount_dzd:,.0f} DZD over {offer.term_months} months")
        print(f"  flags: {', '.join(result.flags) or 'none'}")