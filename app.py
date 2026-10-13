# app.py
# The Streamlit page. The scoring rules are in scoring.py and all the text
# is in translations.py. This file only collects the answers and shows the
# result. Nothing is saved: the answers live in the browser session and
# disappear when the tab is closed.

import streamlit as st

from scoring import (
    MONTHS_NEEDED_FOR_A,
    SCORE_MAX,
    SCORE_MIN,
    SNMG,
    TIER_A_FROM,
    TIER_B_FROM,
    WEIGHTS,
    Shop,
    assess,
)
from translations import LANGUAGES, RTL_LANGUAGES, language_from_locale, t

# Colours for the decision card. The accent is the heading and the bar on
# the side, the background is the box itself.
TIER_COLOURS = {
    "A": {"accent": "#1b7f4c", "background": "#e7f5ec"},
    "B": {"accent": "#b7791f", "background": "#fdf3dc"},
    "C": {"accent": "#c0392b", "background": "#fbe9e7"},
}


def get_language():
    # First visit: use the language the browser is set to.
    # After that the picker in the sidebar decides.
    if "language" not in st.session_state:
        try:
            locale = st.context.locale
        except Exception:
            locale = None
        st.session_state["language"] = language_from_locale(locale)
    return st.session_state["language"]


def flip_for_arabic(language):
    # Arabic reads right to left. Number boxes stay left to right so the
    # digits don't get jumbled.
    if language not in RTL_LANGUAGES:
        return
    st.markdown(
        "<style>"
        ".stApp, [data-testid='stSidebar'] { direction: rtl; }"
        "[data-testid='stNumberInput'] input { direction: ltr; text-align: left; }"
        "</style>",
        unsafe_allow_html=True,
    )


def language_picker(language):
    # at the top of the page instead of the sidebar, so it is easy to find on a phone
    _, picker_column = st.columns([3, 1])
    with picker_column:
        st.selectbox(
            t(language, "sidebar_language"),
            options=list(LANGUAGES),
            format_func=LANGUAGES.get,
            key="language",
        )


def da(amount, language):
    """Write an amount like '1,350,000 DA'."""
    return f"{amount:,.0f} {t(language, 'currency')}"


def show_form(language):
    st.subheader(t(language, "form_title"))

    with st.container(border=True):
        name = st.text_input(t(language, "field_business_name"), key="name")

        left, right = st.columns(2)
        with left:
            cash_flow = st.number_input(
                t(language, "field_cash_flow"),
                min_value=0,
                value=300_000,
                step=10_000,
                key="cash_flow",
            )
            orders = st.number_input(
                t(language, "field_orders"),
                min_value=0,
                max_value=60,
                value=4,
                help=t(language, "field_orders_help"),
                key="orders",
            )
            months = st.number_input(
                t(language, "field_months"),
                min_value=0,
                max_value=600,
                value=18,
                key="months",
            )
        with right:
            no_bills = st.checkbox(t(language, "field_no_utility"), key="no_bills")
            bills_pct = st.slider(
                t(language, "field_utility_pct"),
                min_value=0,
                max_value=100,
                value=85,
                help=t(language, "field_utility_help"),
                disabled=no_bills,
                key="bills_pct",
            )

        pressed = st.button(t(language, "submit_button"), type="primary")

    if pressed:
        # Keep the answers, not the result. That way switching language
        # redraws the result without asking for everything again.
        st.session_state["answers"] = {
            "name": name.strip(),
            "cash_flow": cash_flow,
            "orders": orders,
            "no_bills": no_bills,
            "bills_pct": bills_pct,
            "months": months,
        }


def decision_card(colours, heading, body):
    return (
        f'<div style="border-inline-start: 8px solid {colours["accent"]}; '
        f'background: {colours["background"]}; color: #1f2933; '
        'padding: 1rem 1.25rem; border-radius: 8px; margin-bottom: 1rem;">'
        f'<div style="font-size: 1.4rem; font-weight: 700; '
        f'color: {colours["accent"]};">{heading}</div>'
        f'<div style="margin-top: 0.4rem;">{body}</div>'
        "</div>"
    )


def show_result(language, answers):
    shop = Shop(
        monthly_cash_flow=answers["cash_flow"],
        supplier_orders_per_month=answers["orders"],
        bills_paid_on_time_pct=None if answers["no_bills"] else answers["bills_pct"],
        months_open=answers["months"],
    )
    result = assess(shop)

    st.divider()
    st.header(t(language, "results_title"))
    if answers["name"]:
        st.caption(t(language, "result_for", name=answers["name"]))

    # the three big numbers
    col_score, col_tier, col_risk = st.columns(3)
    col_score.metric(t(language, "metric_score"), result.score)
    col_tier.metric(
        t(language, "metric_tier"), t(language, "tier_value", tier=result.tier)
    )
    col_risk.metric(
        t(language, "metric_risk"), t(language, f"risk_{result.risk_level}")
    )

    # where the score sits between 300 and 850
    st.progress((result.score - SCORE_MIN) / (SCORE_MAX - SCORE_MIN))
    st.caption(t(language, "score_scale_caption"))

    st.subheader(t(language, "decision_title"))
    st.markdown(
        decision_card(
            TIER_COLOURS[result.tier],
            t(language, "tier_value", tier=result.tier),
            t(language, f"decision_{result.tier}"),
        ),
        unsafe_allow_html=True,
    )

    st.subheader(t(language, "breakdown_title"))
    st.caption(t(language, "breakdown_caption"))
    for factor, value in result.factor_scores.items():
        label = t(
            language,
            "factor_weight",
            name=t(language, f"factor_{factor}"),
            weight=round(WEIGHTS[factor] * 100),
        )
        st.progress(value / 100, text=f"{label}: {value:.0f}/100")

    st.subheader(t(language, "flags_title"))
    if result.flags:
        for flag in result.flags:
            st.warning(t(language, f"flag_{flag}", months=MONTHS_NEEDED_FOR_A))
    else:
        st.success(t(language, "no_flags"))

    offer = result.offer
    st.subheader(t(language, "financing_title"))
    col_product, col_amount, col_term = st.columns(3)
    col_product.metric(
        t(language, "financing_product"), t(language, f"product_{offer.product}")
    )
    col_amount.metric(t(language, "financing_amount"), da(offer.amount, language))
    col_term.metric(t(language, "financing_term"), offer.months)

    with st.expander(t(language, "method_title")):
        st.write(
            t(
                language,
                "method_body",
                cash_flow=round(WEIGHTS["cash_flow"] * 100),
                utility=round(WEIGHTS["utility"] * 100),
                restocking=round(WEIGHTS["restocking"] * 100),
                tenure=round(WEIGHTS["tenure"] * 100),
                snmg=f"{SNMG:,}",
                tier_a=TIER_A_FROM,
                tier_b=TIER_B_FROM,
                tier_b_top=TIER_A_FROM - 1,
            )
        )


def main():
    language = get_language()

    # has to be the first thing that draws on the page
    st.set_page_config(
        page_title=f"{t(language, 'app_title')} | {t(language, 'app_tagline')}",
        page_icon="⚖️",
        layout="wide",
    )
    flip_for_arabic(language)
    language_picker(language)

    st.title(f"⚖️ {t(language, 'app_title')}")
    st.markdown(f"**{t(language, 'app_tagline')}**")
    st.write(t(language, "app_subtitle"))

    show_form(language)

    answers = st.session_state.get("answers")
    if answers:
        show_result(language, answers)

    st.caption(t(language, "privacy_note"))


main()