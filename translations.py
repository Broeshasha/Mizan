"""
All user-facing text for Mizan, in English, French and Arabic.

Keeping every sentence here means the rest of the code never contains
display text, and a translation can be corrected without touching any logic.

Use t(language, key, **values) to fetch a text. Placeholders such as
{currency} are filled from the keyword arguments.
"""

DEFAULT_LANGUAGE = "en"

# Shown in the language switcher, each in its own language.
LANGUAGES = {
    "en": "English",
    "fr": "Français",
    "ar": "العربية",
}

# Languages written right to left. The app flips the page layout for these.
RTL_LANGUAGES = {"ar"}

TRANSLATIONS = {
    "en": {
        "app_title": "Mizan",
        "app_tagline": "Credit scoring for cash-based merchants",
        "app_subtitle": (
            "Mizan builds a credit score from the signals a shop already produces: "
            "cash flow, restocking habits, bill payments and time in business. "
            "No audited accounts needed."
        ),
        "sidebar_language": "Language",
        "sidebar_rates_title": "Exchange rates",
        "sidebar_rates_help": (
            "Units of each currency per 1 US dollar. "
            "Update these to the latest rates."
        ),
        "rate_label": "{code} per 1 USD",
        "form_title": "Merchant details",
        "field_business_name": "Business name or reference (optional)",
        "field_country": "Country",
        "field_cash_flow": "Estimated monthly cash flow ({currency})",
        "field_orders": "Supplier orders per month",
        "field_orders_help": (
            "How many times the shop restocks from suppliers in a typical month."
        ),
        "field_no_utility": "No utility bill history",
        "field_utility_pct": "Utility bills paid on time, last 12 months (%)",
        "field_utility_help": (
            "Electricity, water, gas, phone or internet. "
            "Use the share of bills paid by the due date."
        ),
        "field_months": "Time in business (months)",
        "submit_button": "Calculate credit score",
        "country_DZ": "Algeria",
        "country_NG": "Nigeria",
        "country_ZA": "South Africa",
        "results_title": "Assessment",
        "result_for": "Result for {name}",
        "metric_score": "Credit score",
        "metric_tier": "Risk tier",
        "metric_risk": "Risk level",
        "tier_value": "Tier {tier}",
        "risk_low": "Low",
        "risk_moderate": "Moderate",
        "risk_high": "High",
        "score_scale_caption": "Scale: 300 (highest risk) to 850 (prime)",
        "decision_title": "Underwriting decision",
        "decision_A": (
            "Recommended for financing. The merchant shows a strong, "
            "consistent operating record."
        ),
        "decision_B": (
            "Conditional approval. Offer credit tied to supplier purchases "
            "and review at the end of the term."
        ),
        "decision_C": (
            "Not ready for standard credit. Offer a small credit-building loan "
            "and reassess after a few months of repayment history."
        ),
        "breakdown_title": "What drives the score",
        "breakdown_caption": (
            "Each factor is scored from 0 to 100 and weighted into the final score."
        ),
        "vector_cash_flow": "Cash flow",
        "vector_utility": "Utility payments",
        "vector_restocking": "Supplier restocking",
        "vector_tenure": "Time in business",
        "vector_weight": "{name} (weight {weight}%)",
        "flags_title": "Points to review",
        "flag_no_utility_history": (
            "No utility history was provided, so this factor is scored neutrally."
        ),
        "flag_late_utility_payments": "Utility bills are often paid late.",
        "flag_irregular_restocking": (
            "Restocking is infrequent, which can point to slow sales."
        ),
        "flag_short_history": (
            "The business is under {months} months old, "
            "so the score is capped below Tier A."
        ),
        "no_flags": "No warning signs found.",
        "financing_title": "Financing recommendation",
        "financing_product": "Product",
        "financing_amount": "Recommended amount",
        "financing_term": "Term",
        "term_months": "{months} months",
        "product_working_capital_line": "Working capital line",
        "product_supplier_credit_advance": "Supplier credit advance",
        "product_credit_builder_loan": "Credit-builder loan",
        "equivalents_title": "Cross-border view",
        "equivalents_caption": (
            "The same figures in each market currency, "
            "at the exchange rates in the sidebar."
        ),
        "row_cash_flow": "Monthly cash flow",
        "row_financing": "Recommended financing",
        "method_title": "How the score is calculated",
        "method_body": (
            "The score blends four factors: cash flow ({cash_flow}%), "
            "utility payments ({utility}%), supplier restocking ({restocking}%) "
            "and time in business ({tenure}%). The result is placed on a "
            "300 to 850 scale and sorted into Tier A ({tier_a} and above), "
            "Tier B ({tier_b} to {tier_b_top}) or Tier C (below {tier_b}). "
            "It is a transparent rule-based model, so every weight can be "
            "reviewed and adjusted as repayment data becomes available."
        ),
        "privacy_note": (
            "The figures entered here are used only to produce this result. "
            "Nothing is stored."
        ),
    },
    "fr": {
        "app_title": "Mizan",
        "app_tagline": "Notation de crédit pour les commerçants qui travaillent en espèces",
        "app_subtitle": (
            "Mizan établit un score de crédit à partir des signaux que produit "
            "déjà un commerce : flux de trésorerie, rythme de réapprovisionnement, "
            "paiement des factures et ancienneté. Aucun bilan audité n'est nécessaire."
        ),
        "sidebar_language": "Langue",
        "sidebar_rates_title": "Taux de change",
        "sidebar_rates_help": (
            "Unités de chaque devise pour 1 dollar américain. "
            "Mettez-les à jour avec les derniers taux."
        ),
        "rate_label": "{code} pour 1 USD",
        "form_title": "Informations sur le commerçant",
        "field_business_name": "Nom du commerce ou référence (facultatif)",
        "field_country": "Pays",
        "field_cash_flow": "Flux de trésorerie mensuel estimé ({currency})",
        "field_orders": "Commandes aux fournisseurs par mois",
        "field_orders_help": (
            "Nombre de fois où le commerce se réapprovisionne auprès de ses "
            "fournisseurs lors d'un mois ordinaire."
        ),
        "field_no_utility": "Aucun historique de factures",
        "field_utility_pct": "Factures payées à temps sur les 12 derniers mois (%)",
        "field_utility_help": (
            "Électricité, eau, gaz, téléphone ou internet. "
            "Indiquez la part des factures réglées avant l'échéance."
        ),
        "field_months": "Ancienneté du commerce (mois)",
        "submit_button": "Calculer le score de crédit",
        "country_DZ": "Algérie",
        "country_NG": "Nigéria",
        "country_ZA": "Afrique du Sud",
        "results_title": "Évaluation",
        "result_for": "Résultat pour {name}",
        "metric_score": "Score de crédit",
        "metric_tier": "Catégorie de risque",
        "metric_risk": "Niveau de risque",
        "tier_value": "Catégorie {tier}",
        "risk_low": "Faible",
        "risk_moderate": "Modéré",
        "risk_high": "Élevé",
        "score_scale_caption": "Échelle : 300 (risque le plus élevé) à 850 (excellent)",
        "decision_title": "Décision de crédit",
        "decision_A": (
            "Financement recommandé. Le commerçant présente un historique "
            "d'activité solide et régulier."
        ),
        "decision_B": (
            "Accord sous conditions. Proposez un crédit lié aux achats auprès "
            "des fournisseurs et réexaminez le dossier à l'échéance."
        ),
        "decision_C": (
            "Pas encore éligible au crédit standard. Proposez un petit prêt pour "
            "construire un historique et réévaluez après quelques mois de "
            "remboursement."
        ),
        "breakdown_title": "Ce qui détermine le score",
        "breakdown_caption": (
            "Chaque critère est noté de 0 à 100, puis pondéré dans le score final."
        ),
        "vector_cash_flow": "Flux de trésorerie",
        "vector_utility": "Paiement des factures",
        "vector_restocking": "Réapprovisionnement",
        "vector_tenure": "Ancienneté",
        "vector_weight": "{name} (poids {weight} %)",
        "flags_title": "Points à examiner",
        "flag_no_utility_history": (
            "Aucun historique de factures n'a été fourni : "
            "ce critère reçoit une note neutre."
        ),
        "flag_late_utility_payments": "Les factures sont souvent réglées en retard.",
        "flag_irregular_restocking": (
            "Le réapprovisionnement est peu fréquent, "
            "ce qui peut indiquer des ventes lentes."
        ),
        "flag_short_history": (
            "Le commerce a moins de {months} mois : "
            "le score est plafonné sous la catégorie A."
        ),
        "no_flags": "Aucun point d'alerte relevé.",
        "financing_title": "Recommandation de financement",
        "financing_product": "Produit",
        "financing_amount": "Montant recommandé",
        "financing_term": "Durée",
        "term_months": "{months} mois",
        "product_working_capital_line": "Ligne de fonds de roulement",
        "product_supplier_credit_advance": "Avance de crédit fournisseur",
        "product_credit_builder_loan": "Prêt pour construire un historique de crédit",
        "equivalents_title": "Vue transfrontalière",
        "equivalents_caption": (
            "Les mêmes montants dans chaque devise de marché, "
            "aux taux indiqués dans la barre latérale."
        ),
        "row_cash_flow": "Flux de trésorerie mensuel",
        "row_financing": "Financement recommandé",
        "method_title": "Comment le score est calculé",
        "method_body": (
            "Le score combine quatre critères : flux de trésorerie ({cash_flow} %), "
            "paiement des factures ({utility} %), réapprovisionnement "
            "({restocking} %) et ancienneté ({tenure} %). Le résultat est placé "
            "sur une échelle de 300 à 850, puis classé en catégorie A "
            "({tier_a} et plus), catégorie B (de {tier_b} à {tier_b_top}) ou "
            "catégorie C (moins de {tier_b}). Il s'agit d'un modèle transparent "
            "fondé sur des règles : chaque pondération peut être examinée et "
            "ajustée dès que des données de remboursement sont disponibles."
        ),
        "privacy_note": (
            "Les chiffres saisis ici servent uniquement à produire ce résultat. "
            "Rien n'est conservé."
        ),
    },
    "ar": {
        "app_title": "ميزان",
        "app_tagline": "تقييم ائتماني للتجار الذين يعتمدون على النقد",
        "app_subtitle": (
            "تُنشئ ميزان تقييمًا ائتمانيًا من المؤشرات التي ينتجها المحل أصلًا: "
            "التدفق النقدي، ووتيرة التزوّد بالبضائع، وسداد الفواتير، ومدة النشاط. "
            "دون الحاجة إلى حسابات مدققة."
        ),
        "sidebar_language": "اللغة",
        "sidebar_rates_title": "أسعار الصرف",
        "sidebar_rates_help": (
            "عدد وحدات كل عملة مقابل دولار أمريكي واحد. حدّثها وفق آخر الأسعار."
        ),
        "rate_label": "{code} مقابل 1 دولار",
        "form_title": "بيانات التاجر",
        "field_business_name": "اسم النشاط أو مرجعه (اختياري)",
        "field_country": "البلد",
        "field_cash_flow": "التدفق النقدي الشهري المقدّر ({currency})",
        "field_orders": "طلبات التزوّد من الموردين شهريًا",
        "field_orders_help": (
            "عدد مرات تزوّد المحل بالبضائع من الموردين في شهر عادي."
        ),
        "field_no_utility": "لا يوجد سجل لفواتير الخدمات",
        "field_utility_pct": "نسبة الفواتير المسددة في موعدها خلال آخر 12 شهرًا (%)",
        "field_utility_help": (
            "الكهرباء أو الماء أو الغاز أو الهاتف أو الإنترنت. "
            "أدخل نسبة الفواتير المسددة قبل تاريخ الاستحقاق."
        ),
        "field_months": "مدة النشاط (بالأشهر)",
        "submit_button": "احسب التقييم الائتماني",
        "country_DZ": "الجزائر",
        "country_NG": "نيجيريا",
        "country_ZA": "جنوب أفريقيا",
        "results_title": "نتيجة التقييم",
        "result_for": "نتيجة {name}",
        "metric_score": "التقييم الائتماني",
        "metric_tier": "فئة المخاطر",
        "metric_risk": "مستوى المخاطر",
        "tier_value": "الفئة {tier}",
        "risk_low": "منخفض",
        "risk_moderate": "متوسط",
        "risk_high": "مرتفع",
        "score_scale_caption": "المقياس: من 300 (أعلى مخاطر) إلى 850 (ممتاز)",
        "decision_title": "قرار منح التمويل",
        "decision_A": (
            "يُوصى بمنح التمويل. يُظهر التاجر سجل نشاط قويًا ومنتظمًا."
        ),
        "decision_B": (
            "موافقة مشروطة. يُقترح ائتمان مرتبط بمشتريات الموردين "
            "مع مراجعة الملف عند نهاية المدة."
        ),
        "decision_C": (
            "غير مؤهل بعد للائتمان العادي. يُقترح قرض صغير لبناء السجل الائتماني "
            "مع إعادة التقييم بعد بضعة أشهر من السداد."
        ),
        "breakdown_title": "ما الذي يحدد التقييم",
        "breakdown_caption": (
            "يُقيَّم كل عامل من 0 إلى 100 ثم يُوزَن ضمن التقييم النهائي."
        ),
        "vector_cash_flow": "التدفق النقدي",
        "vector_utility": "سداد الفواتير",
        "vector_restocking": "التزوّد من الموردين",
        "vector_tenure": "مدة النشاط",
        "vector_weight": "{name} (الوزن {weight}%)",
        "flags_title": "نقاط تستدعي المراجعة",
        "flag_no_utility_history": (
            "لم يُقدَّم سجل فواتير، لذلك يحصل هذا العامل على تقييم محايد."
        ),
        "flag_late_utility_payments": "تُسدَّد الفواتير في كثير من الأحيان بعد موعدها.",
        "flag_irregular_restocking": (
            "التزوّد بالبضائع قليل التكرار، وقد يدل ذلك على بطء المبيعات."
        ),
        "flag_short_history": (
            "عمر النشاط أقل من {months} أشهر، "
            "لذلك يُحدَّد سقف التقييم دون الفئة A."
        ),
        "no_flags": "لم يتم رصد أي مؤشرات تحذيرية.",
        "financing_title": "توصية التمويل",
        "financing_product": "المنتج",
        "financing_amount": "المبلغ الموصى به",
        "financing_term": "المدة",
        "term_months": "{months} شهر",
        "product_working_capital_line": "خط رأس المال العامل",
        "product_supplier_credit_advance": "سلفة ائتمان الموردين",
        "product_credit_builder_loan": "قرض بناء السجل الائتماني",
        "equivalents_title": "العرض عبر الحدود",
        "equivalents_caption": (
            "الأرقام نفسها بعملة كل سوق، وفق أسعار الصرف المحددة في الشريط الجانبي."
        ),
        "row_cash_flow": "التدفق النقدي الشهري",
        "row_financing": "التمويل الموصى به",
        "method_title": "كيف يُحسب التقييم",
        "method_body": (
            "يجمع التقييم بين أربعة عوامل: التدفق النقدي ({cash_flow}%)، "
            "وسداد الفواتير ({utility}%)، والتزوّد من الموردين ({restocking}%)، "
            "ومدة النشاط ({tenure}%). تُوضع النتيجة على مقياس من 300 إلى 850 "
            "ثم تُصنَّف في الفئة A ({tier_a} فما فوق)، أو الفئة B "
            "(من {tier_b} إلى {tier_b_top})، أو الفئة C (أقل من {tier_b}). "
            "النموذج شفاف ويقوم على قواعد واضحة، ويمكن مراجعة كل وزن وتعديله "
            "عند توفر بيانات السداد."
        ),
        "privacy_note": (
            "تُستخدم الأرقام المُدخلة هنا لإنتاج هذه النتيجة فقط، "
            "ولا يتم حفظ أي شيء."
        ),
    },
}


def t(language, key, **values):
    """
    Return the text for `key` in `language`, filling in any placeholders.
    If a language is missing a key we fall back to English rather than
    show a blank, and a key missing from English raises an error so the
    mistake is caught while developing.
    """
    text = TRANSLATIONS.get(language, {}).get(key)
    if text is None:
        text = TRANSLATIONS[DEFAULT_LANGUAGE][key]
    return text.format(**values)


def language_from_locale(locale):
    """
    Turn a browser locale such as 'fr-FR' or 'ar-DZ' into one of our
    language codes. Anything we do not support falls back to English.
    """
    if not locale:
        return DEFAULT_LANGUAGE
    prefix = locale.replace("_", "-").split("-")[0].lower()
    return prefix if prefix in TRANSLATIONS else DEFAULT_LANGUAGE


def missing_keys():
    """List every key that English has but another language lacks."""
    english_keys = set(TRANSLATIONS[DEFAULT_LANGUAGE])
    problems = []
    for code, texts in TRANSLATIONS.items():
        for key in sorted(english_keys - set(texts)):
            problems.append(f"{code}: {key}")
    return problems


if __name__ == "__main__":
    # Quick check you can run by hand: python translations.py
    for code in LANGUAGES:
        print(f"{code}: {len(TRANSLATIONS[code])} texts")
    print("Missing translations:", missing_keys() or "none")
    print(t("en", "term_months", months=12))
    print(t("fr", "term_months", months=6))
    for locale in ("ar-DZ", "fr-FR", "en-US", "de-DE", None):
        print(f"{locale} -> {language_from_locale(locale)}")