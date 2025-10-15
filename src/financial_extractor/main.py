"""
Financial Report Extractor - Main Module

A comprehensive tool for extracting financial data from PDF reports,
with special focus on Saudi Arabian financial documents and IPO prospectuses.
"""

import os
from typing import List, Dict, Any
from PyPDF2 import PdfReader

from .core.pdf_processor import PDFProcessor
from .core.llm_handler import LLMHandler
from .utils.helpers import load_environment, setup_environment
from .queries.query_templates import get_query
from .keywords.keyword_extractor import get_keywords


class FinancialReportExtractor:
    """Main class for extracting financial data from PDF reports."""

    def __init__(self, api_key: str = None):
        """Initialize the Financial Report Extractor.

        Args:
            api_key: OpenAI API key (optional, will use environment variable if not provided)
        """
        setup_environment()
        self.api_key = api_key or load_environment()
        self.pdf_processor = PDFProcessor()
        self.llm_handler = LLMHandler(self.api_key)

    def extract_financial_data(
        self, pdf_path: str, task: str = "1", window_chars: int = 1500
    ) -> Dict[str, Any]:
        """Extract financial data from a PDF report.

        Args:
            pdf_path: Path to the PDF file
            task: Task type ('1' for revenue, '2' for IPO)
            window_chars: Number of characters to include around keyword matches

        Returns:
            Dictionary containing extracted financial data
        """
        print(f"Loading PDF from: {pdf_path}")

        # Load the PDF and get a sample of text for language detection
        reader = PdfReader(pdf_path)
        sample_text = ""
        for i, page in enumerate(reader.pages):
            if i < 2:  # Check first two pages
                sample_text += self.pdf_processor.fix_arabic(page.extract_text())
            else:
                break

        # Detect language
        language = self.pdf_processor.detect_language(sample_text)
        print(f"Detected language: {language}")

        # Select appropriate query based on choice and language
        query = get_query(language=language, task=task)

        # Load and process the PDF
        docs = self._load_and_split_pdf(pdf_path, window_chars, task)
        print(f"Created {len(docs)} documents from PDF")

        if not docs:
            print("Error: No documents could be created from the PDF")
            return {"error": "No documents could be created from the PDF"}

        # Initialize embeddings and create vector store
        embeddings = self.llm_handler.initialize_embeddings()
        docsearch = self.llm_handler.create_vector_store(docs, embeddings)
        chain = self.llm_handler.initialize_qa_chain()

        print("Processing your request...")
        answer = self.llm_handler.ask_question(docsearch, chain, query)

        return {
            "language": language,
            "task": task,
            "document_count": len(docs),
            "result": answer,
            "source_file": pdf_path,
        }

    def _load_and_split_pdf(self, pdf_path: str, window_chars: int, task: str) -> List:
        """Load PDF and extract keyword matches with context.

        Args:
            pdf_path: Path to the PDF file
            window_chars: Number of characters to include around keyword matches
            task: User's choice ('1' for revenue, '2' for IPO)

        Returns:
            List of Document objects containing keyword matches with context
        """
        # Extract text from PDF
        text = self.pdf_processor.extract_text_from_pdf(pdf_path)
        print(f"Total extracted text length: {len(text)} characters")

        # Normalize text for comparison
        text, text_lower = self.pdf_processor.normalize_text(text)

        # Select appropriate keywords based on task
        keywords = get_keywords(task=task)

        # Pre-process keywords for consistent comparison
        processed_keywords = []
        for category, languages in keywords.items():
            for lang, keyword_list in languages.items():
                for keyword_entry in keyword_list:
                    # Normalize and reshape each keyword
                    normalized_key = self.pdf_processor.fix_arabic(
                        keyword_entry["phrase"]
                    )
                    processed_keywords.append(
                        (
                            category,
                            lang,
                            keyword_entry["phrase"],
                            normalized_key.lower(),
                        )
                    )

        # Find keyword matches with context
        documents = self.pdf_processor.find_keyword_matches(
            text, text_lower, processed_keywords, window_chars
        )

        if not documents:
            print(
                "Warning: No keyword matches found in the PDF. Check if the keywords match the document content."
            )
            # Create a single document with the first 1000 characters as fallback
            from langchain.schema import Document

            doc = Document(page_content=text[:1000], metadata={"source": pdf_path})
            documents.append(doc)

        return documents


def main():
    """Main function for command-line usage."""
    print("Financial Report Extractor")
    print("=" * 50)

    # Initialize extractor
    try:
        extractor = FinancialReportExtractor()
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Get PDF path
    pdf_path = input("Enter path to PDF file (or press Enter for default): ").strip()
    if not pdf_path:
        pdf_path = "./examples/sample_reports/pru.pdf"

    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
        return

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

    # Extract financial data
    result = extractor.extract_financial_data(pdf_path, task=choice)

    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print(f"\nResults:\n{result['result']}")


if __name__ == "__main__":
    main()
