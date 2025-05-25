revenue_keywords = {
    "revenue": {
        "English": [
            {"phrase": "Revenue"},
            {"phrase": "Total revenue"},
            {"phrase": "Net revenue"},
            {"phrase": "Gross revenue"},
            {"phrase": "Sales"},
            {"phrase": "Cost of revenue"},
            {"phrase": "Revenue from operations"},
        ],
        "Arabic": [
            {"phrase": "الإيرادات"},
            {"phrase": "إجمالي الإيرادات"},
            {"phrase": "صافي الإيرادات"},
            {"phrase": "الإيرادات التشغيلية"},
            {"phrase": "المبيعات"},
            {"phrase": "تكلفة الإيرادات"},
            {"phrase": "أرباح"},
        ],
    },
    "summary": {
        "English": [
            {"phrase": "Financial Summary"},
            {"phrase": "Summary of Financial Statements"},
            {"phrase": "Selected Financial Data"},
            {"phrase": "Financial Highlights"},
            {"phrase": "Key Highlights"},
            # Embedded exact section names found in each PDF:
            {
                "phrase": "Summary of Statement of Financial Position Data"
            },  # ara_mills.pdf
            {
                "phrase": "Consolidated income statement for the year ended December 31, 2024"
            },  # nestle.pdf
        ],
        "Arabic": [
            {"phrase": "ملخص المعلومات المالية"},
            {"phrase": "ملخص القوائم المالية"},
            {"phrase": "البيانات المالية المختارة"},
            {"phrase": "أبرز المعلومات المالية"},
            {"phrase": "مؤشرات الأداء الرئيسية"},
            # Embedded exact section names found in each PDF:
            {
                "phrase": "ملخص المعلومات المالية ومؤشرات الأداء الرئيسية للسنوات المالية المنتهية في 31 ديسمبر 2023م"
            },  # almoosa.pdf, salama.pdf, alkuzama.pdf
            {"phrase": "ملخص المعلومات المالية"},  # arab.pdf, pru.pdf
        ],
    },
}

# IPO‐only keyword list
ipo_keywords = {
    "English": [
        "IPO",
        "Initial Public Offering",
        "Prospectus",
        "Red Herring Prospectus",
        "Supplementary Prospectus",
        "Offer Price",
        "Offer Shares",
        "Total Offer Size",
        "Offering Proceeds",
        "Net Offering Proceeds",
        "Use of Proceeds",
        "Book-building",
        "Lock-up Period",
        "CMA approval",
    ],
    "Arabic": [
        "نشرة الإصدار",
        "النشرة الأولية",
        "النشرة النهائية",
        "نشرة الإصدار التكميلية",
        "سعر الطرح",
        "أسهم الطرح",
        "إجمالي العرض",
        "متحصلات الطرح",
        "استخدام متحصلات الطرح",
        "بناء سجل الأوامر",
        "فترة الحظر",
        "موافقة الهيئة",
    ],
}


def get_keywords(task: str):
    if task == "1":
        return revenue_keywords
    else:
        return ipo_keywords
