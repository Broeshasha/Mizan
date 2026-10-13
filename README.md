# Mizan

A credit score for shops in Algeria that run on cash.

Banks turn most of these shops away because there are no audited accounts to look at. Mizan scores a shop from things it does have: how much cash comes in each month, how often it restocks from suppliers, how many utility bills it pays on time, and how long it has been open.

## What it does

- Takes a few details about a shop through a simple form.
- Gives a score from 300 (highest risk) to 850 (best).
- Puts the shop in Tier A, B or C and suggests a loan product, an amount and a term.
- Shows which factors pushed the score up or down, plus warnings worth a second look.
- Works in French, Arabic (right to left) and English. It starts in the browser's language and there is a picker at the top of the page.
- Saves nothing. Whatever is typed stays in the browser session.

## How the score works

Four factors each get 0 to 100, then are blended: cash flow 30%, utility bills 30%, restocking 20%, time open 20%.

Cash flow is measured against the national minimum wage (SNMG), which has been 24,000 DA a month since January 2026. A shop bringing in less than two minimum wages a month scores zero on cash flow, and 25 times the minimum wage is full marks.

Loan sizes follow what Algerian micro-credit looks like. The Tier C offer is capped at 100,000 DA and the Tier B offer at 1,000,000 DA, which match the ceilings ANGEM uses for raw-material loans and small projects. The Tier A cap of 3,000,000 DA is our own choice.

Two rules worth knowing:

- A shop open for under six months cannot reach Tier A.
- A shop with no utility bill history gets a middle score on that factor instead of a bad one, because many small shops have no bills in their own name.

This is a set of plain rules, not a trained model. Every weight and cut-off sits at the top of scoring.py so it can be checked and changed once real repayment data exists.

## Files

- app.py: the Streamlit page
- scoring.py: the scoring rules, tiers and loan offers
- translations.py: all the text, in three languages

## Run it on your own computer

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python -m streamlit run app.py
