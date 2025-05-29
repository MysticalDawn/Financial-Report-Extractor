# ==================== IMPORTS ====================

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI, ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
import re
from PyPDF2 import PdfReader
import arabic_reshaper
from bidi.algorithm import get_display
import os
from dotenv import load_dotenv
import tiktoken
from langchain.schema import Document
import unicodedata
from queries import get_query
from keywords import get_keywords
from langdetect import detect, LangDetectException
from langchain_anthropic import ChatAnthropic
import torch

# ==================== LANGUAGE DETECTION ====================
load_dotenv()

os.environ["TOKENIZERS_PARALLELISM"] = "false"


# Add this new function for language detection
def detect_language(text: str) -> str:
    """Detect if the text is primarily Arabic or English.

    Args:
        text: The text to analyze

    Returns:
        'Arabic' if the text is primarily Arabic, 'English' otherwise
    """
    try:
        return "Arabic" if detect(text) == "ar" else "English"
    except LangDetectException:
        return "Unknown"


# ==================== ENVIRONMENT SETUP ====================


def load_environment():
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


def load_and_split_pdf(pdf_path: str, window_chars: int = 1500, choice: str = "1"):
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
    keywords = get_keywords(task=choice)

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
    """Initialize HuggingFace embeddings.

    Args:
        api_key: Not used for HuggingFace embeddings, kept for compatibility

    Returns:
        HuggingFaceEmbeddings instance
    """
    # Check if MPS is available (for Apple Silicon Macs)

    device = "mps" if torch.backends.mps.is_available() else "cpu"

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": True},
    )


def initialize_qa_chain():
    return load_qa_chain(
        ChatAnthropic(model_name="claude-opus-4-20250514", temperature=0, verbose=True),
        chain_type="stuff",
    )


# ==================== QA FUNCTION ====================


def ask_question(docsearch, chain, query: str, max_docs: int = 5):
    try:
        docs = docsearch.similarity_search(query, k=max_docs)

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
    pdf_path = "./data/pru.pdf"  # Changed to a Saudi IPO prospectus
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

    # Load the PDF and get a sample of text for language detection
    reader = PdfReader(pdf_path)
    sample_text = ""
    for i, page in enumerate(reader.pages):
        if i < 2:  # Check first two pages
            sample_text += fix_arabic(page.extract_text())
        else:
            break

    # Detect language
    language = detect_language(sample_text)
    print(f"\nDetected language: {language}")

    # Select appropriate query based on choice and language
    query = get_query(language=language, task=choice)

    docs = load_and_split_pdf(pdf_path, choice=choice)
    print(f"Created {len(docs)} documents from PDF")

    if not docs:
        print("Error: No documents could be created from the PDF")
        return

    embeddings = initialize_embeddings(api_key)
    docsearch = FAISS.from_documents(docs, embeddings)
    chain = initialize_qa_chain()

    print("\nProcessing your request...")
    answer = ask_question(docsearch, chain, query)
    print(f"\nResults:\n{answer}")


if __name__ == "__main__":
    main()
