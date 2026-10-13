# translations.py
# Every piece of text the user sees, in English, French and Arabic.
# app.py never has display text in it, it asks for it here with t().

DEFAULT_LANGUAGE = "en"

# Names for the language picker, each written in its own language
LANGUAGES = {
    "en": "English",
    "fr": "Français",
    "ar": "العربية",
}

# These are written right to left, so the page layout gets flipped
RTL_LANGUAGES = {"ar"}

TEXTS = {
    "en": {
        "app_title": "Mizan",
        "app_tagline": "Credit scores for shops that run on cash",
        "app_subtitle": (
            "Mizan scores a shop from things it already has: how much cash "
            "comes in, how often it restocks, whether bills get paid on time "
            "and how long it has been open. No audited accounts needed."
        ),
        "sidebar_language": "Language",
        "currency": "DA",
        "form_title": "Shop details",
        "field_business_name": "Shop name or reference (optional)",
        "field_cash_flow": "Estimated monthly cash flow (DA)",
        "field_orders": "Supplier orders per month",
        "field_orders_help": (
            "How many times the shop restocks from its suppliers in a normal month."
        ),
        "field_no_utility": "No utility bill history",
        "field_utility_pct": "Utility bills paid on time, last 12 months (%)",
        "field_utility_help": (
            "Electricity, water, gas, phone or internet. "
            "The share of bills paid before the due date."
        ),
        "field_months": "How long the shop has been open (months)",
        "submit_button": "Calculate credit score",
        "results_title": "Result",
        "result_for": "Result for {name}",
        "metric_score": "Credit score",
        "metric_tier": "Tier",
        "metric_risk": "Risk level",
        "tier_value": "Tier {tier}",
        "risk_low": "Low",
        "risk_moderate": "Moderate",
        "risk_high": "High",
        "score_scale_caption": "Scale: 300 (highest risk) to 850 (best)",
        "decision_title": "Lending decision",
        "decision_A": (
            "Recommended for financing. The shop has a strong, steady record."
        ),
        "decision_B": (
            "Approve with conditions. Tie the credit to supplier purchases "
            "and review it when the term ends."
        ),
        "decision_C": (
            "Not ready for a standard loan. Offer a small credit-building loan "
            "and look again after a few months of repayments."
        ),
        "breakdown_title": "What the score is made of",
        "breakdown_caption": (
            "Each factor gets 0 to 100, then they are blended using the weights shown."
        ),
        "factor_cash_flow": "Cash flow",
        "factor_utility": "Utility bills",
        "factor_restocking": "Restocking",
        "factor_tenure": "Time open",
        "factor_weight": "{name} (counts for {weight}%)",
        "flags_title": "Things to check",
        "flag_no_utility_history": (
            "No bill history was given, so this factor got a middle score."
        ),
        "flag_late_utility_payments": "Utility bills are often paid late.",
        "flag_irregular_restocking": (
            "The shop rarely restocks, which can mean slow sales."
        ),
        "flag_short_history": (
            "The shop has been open under {months} months, "
            "so the score can't go above Tier B."
        ),
        "no_flags": "Nothing to flag.",
        "financing_title": "Suggested financing",
        "financing_product": "Product",
        "financing_amount": "Amount",
        "financing_term": "Term (months)",
        "product_working_capital_line": "Working capital line",
        "product_supplier_credit_advance": "Supplier credit advance",
        "product_credit_builder_loan": "Credit-builder loan",
        "method_title": "How the score works",
        "method_body": (
            "The score blends four factors: cash flow ({cash_flow}%), utility "
            "bills ({utility}%), restocking ({restocking}%) and time open "
            "({tenure}%). Cash flow is measured against the national minimum "
            "wage (SNMG, {snmg} DA a month). The result sits on a 300 to 850 "
            "scale: Tier A from {tier_a}, Tier B from {tier_b} to {tier_b_top}, "
            "Tier C below {tier_b}. It is a set of plain rules, not a trained "
            "model, so every weight can be checked and changed once real "
            "repayment data comes in."
        ),
        "privacy_note": (
            "What you type here is only used to work out this result. "
            "Nothing is saved."
        ),
    },
    "fr": {
        "app_title": "Mizan",
        "app_tagline": "Un score de crédit pour les commerces qui travaillent en espèces",
        "app_subtitle": (
            "Mizan note un commerce à partir de ce qu'il a déjà : l'argent qui "
            "entre, le rythme de réapprovisionnement, le paiement des factures "
            "et l'ancienneté. Aucun bilan audité n'est nécessaire."
        ),
        "sidebar_language": "Langue",
        "currency": "DA",
        "form_title": "Informations sur le commerce",
        "field_business_name": "Nom du commerce ou référence (facultatif)",
        "field_cash_flow": "Flux de trésorerie mensuel estimé (DA)",
        "field_orders": "Commandes aux fournisseurs par mois",
        "field_orders_help": (
            "Combien de fois le commerce se réapprovisionne auprès de ses "
            "fournisseurs dans un mois normal."
        ),
        "field_no_utility": "Pas d'historique de factures",
        "field_utility_pct": "Factures payées à temps, 12 derniers mois (%)",
        "field_utility_help": (
            "Électricité, eau, gaz, téléphone ou internet. "
            "La part des factures payées avant l'échéance."
        ),
        "field_months": "Depuis combien de temps le commerce est ouvert (mois)",
        "submit_button": "Calculer le score de crédit",
        "results_title": "Résultat",
        "result_for": "Résultat pour {name}",
        "metric_score": "Score de crédit",
        "metric_tier": "Catégorie",
        "metric_risk": "Niveau de risque",
        "tier_value": "Catégorie {tier}",
        "risk_low": "Faible",
        "risk_moderate": "Modéré",
        "risk_high": "Élevé",
        "score_scale_caption": "Échelle : 300 (risque le plus élevé) à 850 (le meilleur)",
        "decision_title": "Décision de prêt",
        "decision_A": (
            "Financement recommandé. Le commerce a un historique solide et régulier."
        ),
        "decision_B": (
            "Accord sous conditions. Lier le crédit aux achats chez les "
            "fournisseurs et le revoir à la fin de la durée."
        ),
        "decision_C": (
            "Pas prêt pour un prêt classique. Proposer un petit prêt pour "
            "construire un historique, puis réévaluer après quelques mois "
            "de remboursements."
        ),
        "breakdown_title": "De quoi le score est fait",
        "breakdown_caption": (
            "Chaque critère reçoit une note de 0 à 100, puis ils sont "
            "combinés selon les poids indiqués."
        ),
        "factor_cash_flow": "Flux de trésorerie",
        "factor_utility": "Factures",
        "factor_restocking": "Réapprovisionnement",
        "factor_tenure": "Ancienneté",
        "factor_weight": "{name} (compte pour {weight} %)",
        "flags_title": "À vérifier",
        "flag_no_utility_history": (
            "Aucun historique de factures n'a été donné : ce critère a "
            "reçu une note moyenne."
        ),
        "flag_late_utility_payments": "Les factures sont souvent payées en retard.",
        "flag_irregular_restocking": (
            "Le commerce se réapprovisionne rarement, ce qui peut "
            "indiquer des ventes lentes."
        ),
        "flag_short_history": (
            "Le commerce est ouvert depuis moins de {months} mois : "
            "le score ne peut pas dépasser la catégorie B."
        ),
        "no_flags": "Rien à signaler.",
        "financing_title": "Financement proposé",
        "financing_product": "Produit",
        "financing_amount": "Montant",
        "financing_term": "Durée (mois)",
        "product_working_capital_line": "Ligne de fonds de roulement",
        "product_supplier_credit_advance": "Avance de crédit fournisseur",
        "product_credit_builder_loan": "Prêt pour construire un historique",
        "method_title": "Comment le score fonctionne",
        "method_body": (
            "Le score combine quatre critères : flux de trésorerie "
            "({cash_flow} %), factures ({utility} %), réapprovisionnement "
            "({restocking} %) et ancienneté ({tenure} %). Le flux de "
            "trésorerie est comparé au salaire minimum national (SNMG, "
            "{snmg} DA par mois). Le résultat se place sur une échelle de "
            "300 à 850 : catégorie A à partir de {tier_a}, catégorie B de "
            "{tier_b} à {tier_b_top}, catégorie C en dessous de {tier_b}. "
            "Ce sont des règles simples, pas un modèle entraîné : chaque "
            "poids peut être vérifié et changé quand de vraies données de "
            "remboursement seront disponibles."
        ),
        "privacy_note": (
            "Ce que vous saisissez ici sert uniquement à calculer ce "
            "résultat. Rien n'est enregistré."
        ),
    },
    "ar": {
        "app_title": "ميزان",
        "app_tagline": "تقييم ائتماني للمحلات التي تعمل بالنقد",
        "app_subtitle": (
            "تقيّم ميزان المحل من معطيات يملكها أصلًا: كم من النقد يدخل، "
            "وكم مرة يتزوّد بالبضائع، وهل تُسدَّد الفواتير في وقتها، "
            "ومنذ متى فتح أبوابه. دون الحاجة إلى حسابات مدققة."
        ),
        "sidebar_language": "اللغة",
        "currency": "دج",
        "form_title": "معلومات المحل",
        "field_business_name": "اسم المحل أو مرجعه (اختياري)",
        "field_cash_flow": "التدفق النقدي الشهري المقدّر (دج)",
        "field_orders": "طلبات التزوّد من الموردين شهريًا",
        "field_orders_help": (
            "كم مرة يتزوّد المحل بالبضائع من الموردين في شهر عادي."
        ),
        "field_no_utility": "لا يوجد سجل لفواتير الخدمات",
        "field_utility_pct": "الفواتير المسددة في وقتها خلال آخر 12 شهرًا (%)",
        "field_utility_help": (
            "الكهرباء أو الماء أو الغاز أو الهاتف أو الإنترنت. "
            "نسبة الفواتير المسددة قبل تاريخ الاستحقاق."
        ),
        "field_months": "منذ متى فتح المحل (بالأشهر)",
        "submit_button": "احسب التقييم الائتماني",
        "results_title": "النتيجة",
        "result_for": "نتيجة {name}",
        "metric_score": "التقييم الائتماني",
        "metric_tier": "الفئة",
        "metric_risk": "مستوى المخاطر",
        "tier_value": "الفئة {tier}",
        "risk_low": "منخفض",
        "risk_moderate": "متوسط",
        "risk_high": "مرتفع",
        "score_scale_caption": "المقياس: من 300 (أعلى مخاطر) إلى 850 (الأفضل)",
        "decision_title": "قرار الإقراض",
        "decision_A": (
            "يُوصى بمنح التمويل. للمحل سجل قوي ومنتظم."
        ),
        "decision_B": (
            "موافقة بشروط. يُربط القرض بمشتريات الموردين "
            "ويُراجَع عند انتهاء المدة."
        ),
        "decision_C": (
            "غير جاهز لقرض عادي. يُقترح قرض صغير لبناء سجل ائتماني، "
            "ثم يُعاد التقييم بعد بضعة أشهر من السداد."
        ),
        "breakdown_title": "مما يتكوّن التقييم",
        "breakdown_caption": (
            "يأخذ كل عامل من 0 إلى 100، ثم تُجمع العوامل حسب الأوزان الموضحة."
        ),
        "factor_cash_flow": "التدفق النقدي",
        "factor_utility": "فواتير الخدمات",
        "factor_restocking": "التزوّد بالبضائع",
        "factor_tenure": "مدة العمل",
        "factor_weight": "{name} (يحتسب بنسبة {weight}%)",
        "flags_title": "نقاط للتحقق منها",
        "flag_no_utility_history": (
            "لم يُقدَّم سجل فواتير، لذلك أخذ هذا العامل تقييمًا متوسطًا."
        ),
        "flag_late_utility_payments": "كثيرًا ما تُسدَّد الفواتير بعد موعدها.",
        "flag_irregular_restocking": (
            "نادرًا ما يتزوّد المحل بالبضائع، وقد يعني ذلك بطء المبيعات."
        ),
        "flag_short_history": (
            "مضى على فتح المحل أقل من {months} أشهر، "
            "لذلك لا يمكن أن يتجاوز التقييم الفئة B."
        ),
        "no_flags": "لا شيء يستدعي التنبيه.",
        "financing_title": "التمويل المقترح",
        "financing_product": "المنتج",
        "financing_amount": "المبلغ",
        "financing_term": "المدة (بالأشهر)",
        "product_working_capital_line": "خط رأس المال العامل",
        "product_supplier_credit_advance": "سلفة ائتمان الموردين",
        "product_credit_builder_loan": "قرض لبناء السجل الائتماني",
        "method_title": "كيف يعمل التقييم",
        "method_body": (
            "يجمع التقييم أربعة عوامل: التدفق النقدي ({cash_flow}%)، "
            "وفواتير الخدمات ({utility}%)، والتزوّد بالبضائع ({restocking}%)، "
            "ومدة العمل ({tenure}%). يُقارَن التدفق النقدي بالأجر الوطني "
            "الأدنى المضمون (SNMG، {snmg} دج في الشهر). تقع النتيجة على "
            "مقياس من 300 إلى 850: الفئة A ابتداءً من {tier_a}، والفئة B من "
            "{tier_b} إلى {tier_b_top}، والفئة C أقل من {tier_b}. هذه "
            "قواعد بسيطة وليست نموذجًا مدرَّبًا، لذلك يمكن فحص كل وزن "
            "وتعديله عند توفر بيانات سداد حقيقية."
        ),
        "privacy_note": (
            "ما تكتبه هنا يُستخدم فقط لحساب هذه النتيجة. لا يتم حفظ أي شيء."
        ),
    },
}


def t(language, key, **values):
    """Get the text for `key` in `language`, filling in {placeholders}."""
    text = TEXTS.get(language, {}).get(key)
    if text is None:
        # missing in this language: use English instead of showing nothing
        text = TEXTS[DEFAULT_LANGUAGE][key]
    return text.format(**values)


def language_from_locale(locale):
    """Turn a browser locale like 'fr-FR' or 'ar-DZ' into 'fr' or 'ar'."""
    if not locale:
        return DEFAULT_LANGUAGE
    prefix = locale.replace("_", "-").split("-")[0].lower()
    return prefix if prefix in TEXTS else DEFAULT_LANGUAGE


def missing_keys():
    """Keys that English has but another language doesn't."""
    english = set(TEXTS[DEFAULT_LANGUAGE])
    problems = []
    for code, texts in TEXTS.items():
        for key in sorted(english - set(texts)):
            problems.append(f"{code}: {key}")
    return problems


if __name__ == "__main__":
    # Run this file on its own to check the translations: python translations.py
    for code in LANGUAGES:
        print(f"{code}: {len(TEXTS[code])} texts")
    print("Missing:", missing_keys() or "none")
    print(t("en", "flag_short_history", months=6))
    print(t("fr", "factor_weight", name="Ancienneté", weight=20))
    for locale in ("ar-DZ", "fr-FR", "en-US", "de-DE", None):
        print(f"{locale} -> {language_from_locale(locale)}")