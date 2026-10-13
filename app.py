"""
Mizan: the Streamlit screen.

Scoring logic lives in scoring.py, currency conversion in currency.py and
every piece of display text in translations.py. This file only collects
the merchant's details, calls those modules and lays out the result.

Nothing is written to disk or to a database. The details a user types
stay in their own browser session and disappear when they close the tab.
"""

import pandas as pd
import streamlit as st

from currency import (
    DEFAULT_RATES_PER_USD,
    SUPPORTED_CURRENCIES,
    convert,
    convert_to_all,
)
from scoring import (
    MIN_MONTHS_FOR_TIER_A,
    TIER_A_MIN,
    TIER_B_MIN,
    WEIGHTS,
    MerchantProfile,
    assess,
)
from translations import (
    DEFAULT_LANGUAGE,
    LANGUAGES,
    RTL_LANGUAGES,
    language_from_locale,
    t,
)

COUNTRY_CURRENCY = {"DZ": "DZD", "NG": "NGN", "ZA": "ZAR"}

# Colours for each tier. The accent is used for text and the left edge of
# the decision card, the background for the card itself.
TIER_STYLES = {
    "A": {"accent": "#1b7f4c", "background": "#e7f5ec"},
    "B": {"accent": "#b7791f", "background": "#fdf3dc"},
    "C": {"accent": "#c0392b", "background": "#fbe9e7"},
}

# Step sizes for the number boxes, so the + and - buttons make sense for
# each currency (a Naira amount is far bigger than a Rand amount).
RATE_STEPS = {"DZD": 1.0, "NGN": 10.0, "ZAR": 0.1}
CASH_FLOW_STEPS = {"DZD": 10_000.0, "NGN": 100_000.0, "ZAR": 5_000.0}

# A starting cash-flow figure for each currency, worth about the same
# amount in all three (300,000 DZD at the default rates).
DEFAULT_CASH_FLOW = {
    code: float(round(convert(300_000, "DZD", code), -3))
    for code in SUPPORTED_CURRENCIES
}


def money(amount, currency):
    """Format an amount without decimals, e.g. '1,350,000 DZD'."""
    return f"{amount:,.0f} {currency}"


def current_language():
    """
    Return the language to use. On the first visit we read the browser's
    language setting; after that the sidebar switcher is in charge.
    """
    if "language" not in st.session_state:
        try:
            browser_locale = st.context.locale
        except Exception:
            browser_locale = None
        st.session_state["language"] = language_from_locale(browser_locale)
    return st.session_state["language"]


def apply_text_direction(language):
    """Flip the page to right-to-left for Arabic, keeping numbers readable."""
    if language not in RTL_LANGUAGES:
        return
    st.markdown(
        "<style>"
        ".stApp, [data-testid='stSidebar'] { direction: rtl; }"
        "[data-testid='stNumberInput'] input { direction: ltr; text-align: left; }"
        "</style>",
        unsafe_allow_html=True,
    )


def render_sidebar(language):
    """Language switcher and editable exchange rates. Returns the rates."""
    with st.sidebar:
        st.selectbox(
            t(language, "sidebar_language"),
            options=list(LANGUAGES),
            format_func=LANGUAGES.get,
            key="language",
        )
        st.divider()
        st.subheader(t(language, "sidebar_rates_title"))
        st.caption(t(language, "sidebar_rates_help"))

        rates = {}
        for code in SUPPORTED_CURRENCIES:
            rates[code] = st.number_input(
                t(language, "rate_label", code=code),
                min_value=0.01,
                value=DEFAULT_RATES_PER_USD[code],
                step=RATE_STEPS[code],
                format="%.2f",
                key=f"rate_{code}",
            )
    return rates


def render_form(language):
    """Collect the merchant's details. Saves them when the button is pressed."""
    st.subheader(t(language, "form_title"))

    with st.container(border=True):
        business_name = st.text_input(
            t(language, "field_business_name"), key="business_name"
        )
        country = st.selectbox(
            t(language, "field_country"),
            options=list(COUNTRY_CURRENCY),
            format_func=lambda code: t(language, f"country_{code}"),
            key="country",
        )
        currency = COUNTRY_CURRENCY[country]

        left, right = st.columns(2)
        with left:
            cash_flow = st.number_input(
                t(language, "field_cash_flow", currency=currency),
                min_value=0.0,
                value=DEFAULT_CASH_FLOW[currency],
                step=CASH_FLOW_STEPS[currency],
                format="%.0f",
                key=f"cash_flow_{currency}",
            )
            orders = st.number_input(
                t(language, "field_orders"),
                min_value=0,
                max_value=60,
                value=4,
                help=t(language, "field_orders_help"),
                key="orders",
            )
        with right:
            no_utility = st.checkbox(t(language, "field_no_utility"), key="no_utility")
            utility_pct = st.slider(
                t(language, "field_utility_pct"),
                min_value=0,
                max_value=100,
                value=85,
                help=t(language, "field_utility_help"),
                disabled=no_utility,
                key="utility_pct",
            )
            months = st.number_input(
                t(language, "field_months"),
                min_value=0,
                max_value=600,
                value=18,
                key="months",
            )

        submitted = st.button(t(language, "submit_button"), type="primary")

    if submitted:
        # We keep the raw inputs, not the result, so that changing the
        # language or an exchange rate re-calculates everything.
        st.session_state["last_run"] = {
            "name": business_name.strip(),
            "country": country,
            "cash_flow": cash_flow,
            "orders": orders,
            "no_utility": no_utility,
            "utility_pct": utility_pct,
            "months": months,
        }


def decision_card(accent, background, heading, body):
    """The coloured box that states the underwriting decision."""
    return (
        f'<div style="border-inline-start: 8px solid {accent}; '
        f"background: {background}; color: #1f2933; padding: 1rem 1.25rem; "
        'border-radius: 8px; margin-bottom: 1rem;">'
        f'<div style="font-size: 1.4rem; font-weight: 700; color: {accent};">{heading}</div>'
        f'<div style="margin-top: 0.4rem;">{body}</div>'
        "</div>"
    )


def render_results(language, rates, run):
    """Score the saved inputs and show the full assessment."""
    currency = COUNTRY_CURRENCY[run["country"]]

    # The scoring engine works in dinar, so convert whatever was typed.
    cash_flow_dzd = convert(run["cash_flow"], currency, "DZD", rates)
    profile = MerchantProfile(
        monthly_cash_flow_dzd=cash_flow_dzd,
        supplier_orders_per_month=run["orders"],
        utility_on_time_pct=None if run["no_utility"] else run["utility_pct"],
        months_in_operation=run["months"],
    )
    result = assess(profile)
    style = TIER_STYLES[result.tier]

    st.divider()
    st.header(t(language, "results_title"))
    if run["name"]:
        st.caption(t(language, "result_for", name=run["name"]))

    # Headline numbers
    score_col, tier_col, risk_col = st.columns(3)
    score_col.metric(t(language, "metric_score"), result.score)
    tier_col.metric(t(language, "metric_tier"), t(language, "tier_value", tier=result.tier))
    risk_col.metric(
        t(language, "metric_risk"), t(language, f"risk_{result.risk_level}")
    )

    # Where the score sits on the 300 to 850 scale
    position = (result.score - 300) / (850 - 300)
    st.progress(min(1.0, max(0.0, position)))
    st.caption(t(language, "score_scale_caption"))

    # Underwriting decision, coloured by tier
    st.subheader(t(language, "decision_title"))
    st.markdown(
        decision_card(
            style["accent"],
            style["background"],
            t(language, "tier_value", tier=result.tier),
            t(language, f"decision_{result.tier}"),
        ),
        unsafe_allow_html=True,
    )

    # What drove the score
    st.subheader(t(language, "breakdown_title"))
    st.caption(t(language, "breakdown_caption"))
    for name, value in result.vector_scores.items():
        label = t(
            language,
            "vector_weight",
            name=t(language, f"vector_{name}"),
            weight=int(WEIGHTS[name] * 100),
        )
        st.progress(min(1.0, value / 100), text=f"{label}: {value:.0f}/100")

    # Warning signs
    st.subheader(t(language, "flags_title"))
    if result.flags:
        for flag in result.flags:
            st.warning(t(language, f"flag_{flag}", months=MIN_MONTHS_FOR_TIER_A))
    else:
        st.success(t(language, "no_flags"))

    # Financing offer, shown in the merchant's own currency
    offer = result.financing
    offer_in_local = convert(offer.amount_dzd, "DZD", currency, rates)
    st.subheader(t(language, "financing_title"))
    product_col, amount_col, term_col = st.columns(3)
    product_col.metric(
        t(language, "financing_product"), t(language, f"product_{offer.product}")
    )
    amount_col.metric(t(language, "financing_amount"), money(offer_in_local, currency))
    term_col.metric(
        t(language, "financing_term"),
        t(language, "term_months", months=offer.term_months),
    )

    # The same figures in all three market currencies
    st.subheader(t(language, "equivalents_title"))
    st.caption(t(language, "equivalents_caption"))
    cash_flow_all = convert_to_all(cash_flow_dzd, "DZD", rates)
    financing_all = convert_to_all(offer.amount_dzd, "DZD", rates)
    table = pd.DataFrame(
        {
            code: [money(cash_flow_all[code], code), money(financing_all[code], code)]
            for code in SUPPORTED_CURRENCIES
        },
        index=[t(language, "row_cash_flow"), t(language, "row_financing")],
    )
    st.table(table)

    with st.expander(t(language, "method_title")):
        st.write(
            t(
                language,
                "method_body",
                cash_flow=int(WEIGHTS["cash_flow"] * 100),
                utility=int(WEIGHTS["utility"] * 100),
                restocking=int(WEIGHTS["restocking"] * 100),
                tenure=int(WEIGHTS["tenure"] * 100),
                tier_a=TIER_A_MIN,
                tier_b=TIER_B_MIN,
                tier_b_top=TIER_A_MIN - 1,
            )
        )


def main():
    language = current_language()

    # This must be the first Streamlit call that draws anything.
    st.set_page_config(
        page_title=f"{t(language, 'app_title')} | {t(language, 'app_tagline')}",
        page_icon="⚖️",
        layout="wide",
    )
    apply_text_direction(language)
    rates = render_sidebar(language)

    st.title(f"⚖️ {t(language, 'app_title')}")
    st.markdown(f"**{t(language, 'app_tagline')}**")
    st.write(t(language, "app_subtitle"))

    render_form(language)

    last_run = st.session_state.get("last_run")
    if last_run:
        render_results(language, rates, last_run)

    st.caption(t(language, "privacy_note"))


main()