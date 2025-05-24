from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI, OpenAIEmbeddings, ChatOpenAI
import re
from PyPDF2 import PdfReader
import arabic_reshaper
from bidi.algorithm import get_display
import os
from dotenv import load_dotenv
import tiktoken
from langchain.schema import Document
import unicodedata


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


# ==================== ENVIRONMENT SETUP ====================


def load_environment():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")
    return api_key


# ==================== UTILITIES ====================


def count_tokens(text: str, model: str = "cl100k_base") -> int:
    encoding = tiktoken.get_encoding(model)
    return len(encoding.encode(text))


def fix_arabic(text):
    """Fix Arabic text display issues."""
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


# ==================== LOADING AND SPLITTING ====================


def load_and_split_pdf(pdf_path: str, window_chars: int = 550, choice: str = "1"):
    """Load PDF and extract keyword matches with context.

    Args:
        pdf_path: Path to the PDF file
        window_chars: Number of characters to include around keyword matches
        choice: User's choice ('1' for revenue, '2' for IPO)

    Returns:
        List of Document objects containing keyword matches with context
    """
    # Load and extract text
    reader = PdfReader(pdf_path)
    text = ""
    for i, doc in enumerate(reader.pages):
        page_text = fix_arabic(doc.extract_text())
        text += page_text

    print(f"Total extracted text length: {len(text)} characters")

    # Normalize text for comparison
    text = unicodedata.normalize("NFC", text)
    text_lower = text.lower()

    # Select appropriate keywords based on choice
    keywords = (
        revenue_keywords
        if choice == "1"
        else {
            "ipo": {
                "English": [{"phrase": k} for k in ipo_keywords["English"]],
                "Arabic": [{"phrase": k} for k in ipo_keywords["Arabic"]],
            }
        }
    )

    # Pre-process keywords for consistent comparison
    processed_keywords = []
    for category, languages in keywords.items():
        for lang, keyword_list in languages.items():
            for keyword_entry in keyword_list:
                # Normalize and reshape each keyword
                normalized_key = unicodedata.normalize("NFC", keyword_entry["phrase"])
                processed_key = fix_arabic(normalized_key)
                processed_keywords.append(
                    (category, lang, keyword_entry["phrase"], processed_key.lower())
                )

    # Find keyword matches with context
    documents = []
    total_matches = 0
    for category, lang, original_key, processed_key in processed_keywords:
        matches = list(re.finditer(re.escape(processed_key), text_lower))
        if matches:
            print(
                f"Found {len(matches)} matches for keyword: {original_key} ({category} - {lang})"
            )
            total_matches += len(matches)

        for match in matches:
            start = max(0, match.start() - window_chars)
            end = min(len(text), match.end() + window_chars)
            context = (
                text[start:end].strip()
                + "\n\n"
                + f"Category: {category} | Language: {lang}"
            )
            # Create document for each match
            doc = Document(
                page_content=context,
                metadata={
                    "category": category,
                    "language": lang,
                    "keyword": original_key,
                    "match_position": match.start(),
                    "source": pdf_path,
                },
            )
            documents.append(doc)

    print(f"Total keyword matches found: {total_matches}")
    print(f"Created {len(documents)} documents with context")

    if not documents:
        print(
            "Warning: No keyword matches found in the PDF. Check if the keywords match the document content."
        )
        # Create a single document with the first 1000 characters as fallback
        doc = Document(page_content=text[:1000], metadata={"source": pdf_path})
        documents.append(doc)

    return documents


# ==================== INITIALIZERS ====================


def initialize_embeddings(api_key: str):
    return OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=api_key,
        base_url="https://api.openai.com/v1",
    )


def initialize_qa_chain():
    return load_qa_chain(ChatOpenAI(model="gpt-4.1", temperature=0), chain_type="stuff")


# ==================== QA FUNCTION ====================


def ask_question(docsearch, chain, query: str, max_docs: int = 5):
    try:
        docs = docsearch.similarity_search(query, k=max_docs * 3000)

        # Filter docs to fit in token budget
        MAX_MODEL_TOKENS = 25000
        RESERVED_FOR_RESPONSE = 512
        MAX_CONTEXT_TOKENS = MAX_MODEL_TOKENS - RESERVED_FOR_RESPONSE

        selected_docs = []
        total_tokens = 0

        for doc in docs:
            tokens = count_tokens(doc.page_content)
            if total_tokens + tokens > MAX_CONTEXT_TOKENS:
                break
            selected_docs.append(doc)
            total_tokens += tokens
            if len(selected_docs) >= max_docs:
                break

        if not selected_docs:
            return "Error: No suitable documents found within token limits."

        return chain.run(input_documents=selected_docs, question=query)

    except Exception as e:
        if "token" in str(e).lower():
            return "Error: Token limit exceeded. Try asking a more specific question."
        return f"Error: {str(e)}"


# ==================== MAIN ====================


def main():
    api_key = load_environment()

    # Use a Saudi IPO prospectus
    pdf_path = "./data/salama.pdf"  # Changed to a Saudi IPO prospectus
    print(f"Loading PDF from: {pdf_path}")

    # Ask user for their choice
    print("\nWhat would you like to extract?")
    print("1. Revenue Information")
    print("2. IPO Details")

    while True:
        try:
            choice = input("\nEnter your choice (1 or 2): ").strip()
            if choice not in ["1", "2"]:
                print("Please enter either 1 or 2")
                continue
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            return

    docs = load_and_split_pdf(pdf_path, choice=choice)
    print(f"Created {len(docs)} documents from PDF")

    if not docs:
        print("Error: No documents could be created from the PDF")
        return

    embeddings = initialize_embeddings(api_key)
    docsearch = FAISS.from_documents(docs, embeddings)
    chain = initialize_qa_chain()

    # Select appropriate query based on user choice
    if choice == "1":
        query = """
You are a financial data extraction assistant for Saudi Arabia financial reports, in both Arabic and English.  

CRITICAL PRIORITY: Always extract the NEWEST/MOST RECENT data available. Look for:
1. Latest fiscal year
2. Most recent period
3. Current year's data
4. Latest audited figures
5. Most recent financial statements

IMPORTANT: First look for and prioritize information from summary sections, which may be labeled as:
- Financial Summary
- Summary of Financial Information
- Selected Financial Data
- Financial Highlights
- Key Highlights
- ملخص المعلومات المالية
- البيانات المالية المختارة
- المعلومات المالية المختارة
- مؤشرات الأداء الرئيسية

If summary sections are found, use them as the primary source. If not, proceed with the following keyword groups:

1️⃣ **Latest audited annual revenue**  
   - **English** phrases: Revenue, Total revenue, Other revenue, Cost of revenue, Operating revenue, Consolidated revenue, Sales, Total Sales  
   - **Arabic** phrases: الإيرادات, إجمالي الإيرادات, صافي الإيرادات, الإيرادات التشغيلية, المبيعات, إجمالي المبيعات  
   - **Post-zakat logic**: if you see "Profit for the year before zakat" → "Zakat" → "Profit for the year" take that third line.  
   - If explicit "after zakat" exists, use that line.
   - ALWAYS prefer the most recent year's data when multiple years are present

✅ **Extract & normalize**:

**Revenue**  
- `revenue`: latest annual amount (Western digits)  
- `currency`: 3-letter code (SAR, USD)  
- `period`: fiscal year or "for the year ended YYYY-MM-DD"  
- `source_text`: exact snippet  
- `location`: page/section/table (if available)
- `data_freshness`: indicate if this is the most recent data available

---

**Normalization rules**:  
• Convert Arabic-Indic → Western numerals (١٢٣٤٥٦٧ → 1234567)  
• Expand "مليون"/"ألف" or "million"/"thousand" → full integer  
• Dates → ISO (YYYY-MM-DD)  
• Currency symbols → ISO codes  

---

IMPORTANT: Always prioritize and clearly indicate the newest/most recent data available. If multiple years are present, explicitly state which year's data you're using and why it's the most recent.
"""
    else:  # choice == '2'
        query = """
You are a financial data extraction assistant for Saudi Arabia IPO prospectuses (نشرات الإصدار) in Arabic and English.  
Use the following keywords to locate the company's **latest IPO details**:

English keywords:
{eng}

Arabic keywords:
{arb}

✅ Extract:
- Offer Price (with currency)
- Number of Shares Offered
- Total Offer Size (with currency)
- Offering / Subscription Period (start & end dates)
- Expected Listing Date
- Book-building details (process or dates)
- Lock-up Period (duration)
- Use of Proceeds (text summary)
- Receiving Agents (list, if any)
- CMA Approval (yes/no + date)

💡 Normalize:
- Convert Arabic-Indic numerals → Western digits
- Expand "مليون"/"ألف" or "million"/"thousand" → full integer
- Dates → ISO format YYYY-MM-DD
- Currency symbols → 3-letter ISO codes

🎯 Output format:

IPO Details:
------------
Offer Price: [amount] [currency]
Shares Offered: [number]
Total Offer Size: [amount] [currency]
Offering Period: [start] to [end]
Expected Listing Date: [date]
Book-building: [details]
Lock-up Period: [details]
Use of Proceeds: [text]
Receiving Agents: [list]
CMA Approval: [yes/no + date]

If any field is not found, return "Not found in document."
""".format(
            eng=", ".join(ipo_keywords["English"]),
            arb=", ".join(ipo_keywords["Arabic"]),
        )

    print("\nProcessing your request...")
    answer = ask_question(docsearch, chain, query)
    print(f"\nResults:\n{answer}")


if __name__ == "__main__":
    main()
