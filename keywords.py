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
            {"phrase": "ملخص المعلومات المالية"},  # arab.pdf, pru.pdf
        ],
    },
}

# IPO‐only keyword list
ipo_keywords = {
    "English": [
        "IPO",
        "Initial Public Offering",
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
