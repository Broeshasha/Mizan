# scoring.py
# Gives an Algerian shop a score from 300 to 850.
#
# We use four things the owner can tell us: how much cash comes in each
# month, how often they restock, how many utility bills they pay on time,
# and how long the shop has been open. All money is in dinars (DA).
#
# The weights and cut-offs are all up here at the top so they are easy to
# find and change.

import math
from dataclasses import dataclass, field

SCORE_MIN = 300
SCORE_MAX = 850

# How much each factor counts. These add up to 1.
WEIGHTS = {
    "cash_flow": 0.30,
    "utility": 0.30,
    "restocking": 0.20,
    "tenure": 0.20,
}

# The minimum wage (SNMG) has been 24,000 DA a month since January 2026.
# A shop bringing in less than two minimum wages a month has nothing left
# over to repay a loan, so that is where the cash flow score starts.
# 25 times the minimum wage (600,000 DA) is full marks.
SNMG = 24_000
CASH_FLOW_START = 2 * SNMG
CASH_FLOW_FULL = 25 * SNMG

RESTOCKS_FOR_FULL_SCORE = 8    # orders to suppliers in a month
MONTHS_FOR_FULL_SCORE = 60     # five years open
NO_BILLS_SCORE = 50            # middle score for shops with no bill history

# Where each tier starts
TIER_A_FROM = 700
TIER_B_FROM = 580

# A shop open for less than this can't be Tier A, however good it looks
MONTHS_NEEDED_FOR_A = 6

# Used for the warning flags
LATE_PAYER_BELOW = 70          # % of bills paid on time
RARE_RESTOCKING = 1            # orders a month or fewer

# What we offer each tier. The amount is a multiple of monthly cash flow,
# held down by a ceiling. The ceilings for B and C match what ANGEM
# lends (1,000,000 DA for small projects, 100,000 DA for raw materials).
# The ceiling for A is just our own choice.
OFFERS = {
    "A": {"product": "working_capital_line", "times_cash_flow": 3.0,
          "months": 12, "ceiling": 3_000_000},
    "B": {"product": "supplier_credit_advance", "times_cash_flow": 1.5,
          "months": 6, "ceiling": 1_000_000},
    "C": {"product": "credit_builder_loan", "times_cash_flow": 0.5,
          "months": 3, "ceiling": 100_000},
}

RISK_LEVELS = {"A": "low", "B": "moderate", "C": "high"}


@dataclass
class Shop:
    monthly_cash_flow: float          # DA
    supplier_orders_per_month: float
    bills_paid_on_time_pct: float | None   # None = no bill history
    months_open: int


@dataclass
class Offer:
    product: str
    amount: float                     # DA
    months: int


@dataclass
class Result:
    score: int
    tier: str
    risk_level: str
    factor_scores: dict
    flags: list = field(default_factory=list)
    offer: Offer | None = None


def check_inputs(shop):
    if shop.monthly_cash_flow < 0:
        raise ValueError("Monthly cash flow can't be negative")
    if shop.supplier_orders_per_month < 0:
        raise ValueError("Supplier orders can't be negative")
    if shop.months_open < 0:
        raise ValueError("Months open can't be negative")
    pct = shop.bills_paid_on_time_pct
    if pct is not None and not 0 <= pct <= 100:
        raise ValueError("Bills paid on time must be between 0 and 100")


def cap(value):
    """Keep a factor score between 0 and 100."""
    return max(0.0, min(100.0, value))


def cash_flow_score(monthly_cash_flow):
    # Log scale: going from 50,000 to 100,000 DA should count about the
    # same as going from 300,000 to 600,000 DA.
    if monthly_cash_flow <= CASH_FLOW_START:
        return 0.0
    how_far = math.log(monthly_cash_flow / CASH_FLOW_START) / math.log(
        CASH_FLOW_FULL / CASH_FLOW_START
    )
    return cap(how_far * 100)


def utility_score(on_time_pct):
    if on_time_pct is None:
        return float(NO_BILLS_SCORE)
    # Squared so missing bills hurts more and more: 90% on time scores
    # 81, 80% scores 64, 50% scores 25.
    return (on_time_pct / 100) ** 2 * 100


def restocking_score(orders_per_month):
    # Square root: the first few orders matter most, after that it levels off
    return cap(math.sqrt(orders_per_month / RESTOCKS_FOR_FULL_SCORE) * 100)


def tenure_score(months_open):
    return cap(math.sqrt(months_open / MONTHS_FOR_FULL_SCORE) * 100)


def tier_for(score):
    if score >= TIER_A_FROM:
        return "A"
    if score >= TIER_B_FROM:
        return "B"
    return "C"


def make_offer(tier, monthly_cash_flow):
    rules = OFFERS[tier]
    amount = min(monthly_cash_flow * rules["times_cash_flow"], rules["ceiling"])
    # round to the nearest 1,000 DA
    return Offer(rules["product"], round(amount / 1000) * 1000, rules["months"])


def find_flags(shop):
    flags = []
    if shop.bills_paid_on_time_pct is None:
        flags.append("no_utility_history")
    elif shop.bills_paid_on_time_pct < LATE_PAYER_BELOW:
        flags.append("late_utility_payments")
    if shop.supplier_orders_per_month <= RARE_RESTOCKING:
        flags.append("irregular_restocking")
    if shop.months_open < MONTHS_NEEDED_FOR_A:
        flags.append("short_history")
    return flags


def assess(shop):
    check_inputs(shop)

    factor_scores = {
        "cash_flow": cash_flow_score(shop.monthly_cash_flow),
        "utility": utility_score(shop.bills_paid_on_time_pct),
        "restocking": restocking_score(shop.supplier_orders_per_month),
        "tenure": tenure_score(shop.months_open),
    }

    blended = sum(factor_scores[name] * WEIGHTS[name] for name in WEIGHTS)
    score = round(SCORE_MIN + blended / 100 * (SCORE_MAX - SCORE_MIN))

    flags = find_flags(shop)
    if "short_history" in flags:
        score = min(score, TIER_A_FROM - 1)

    tier = tier_for(score)
    return Result(
        score=score,
        tier=tier,
        risk_level=RISK_LEVELS[tier],
        factor_scores=factor_scores,
        flags=flags,
        offer=make_offer(tier, shop.monthly_cash_flow),
    )


if __name__ == "__main__":
    # Run this file on its own to try three sample shops: python scoring.py
    samples = [
        ("Old wholesaler", Shop(450_000, 8, 95, 60)),
        ("Steady corner shop", Shop(120_000, 3, 80, 24)),
        ("New kiosk", Shop(50_000, 1, 40, 4)),
    ]
    for name, shop in samples:
        result = assess(shop)
        offer = result.offer
        print(f"{name}: {result.score}, Tier {result.tier} ({result.risk_level} risk)")
        print(f"  offer: {offer.product}, {offer.amount:,.0f} DA over {offer.months} months")
        print(f"  flags: {', '.join(result.flags) or 'none'}")