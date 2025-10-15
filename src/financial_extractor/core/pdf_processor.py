"""
PDF Processing Module

Handles PDF loading, text extraction, and document preparation for analysis.
"""

import re
import unicodedata
from typing import List, Tuple
from PyPDF2 import PdfReader
import arabic_reshaper
from bidi.algorithm import get_display
from langchain.schema import Document
from langdetect import detect, LangDetectException


class PDFProcessor:
    """Handles PDF processing and text extraction."""

    def __init__(self):
        self.supported_languages = ["Arabic", "English"]

    def detect_language(self, text: str) -> str:
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

    def fix_arabic(self, text: str) -> str:
        """Fix Arabic text display issues."""
        if not text:
            return ""
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text content
        """
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = self.fix_arabic(page.extract_text())
            text += page_text
        return text

    def normalize_text(self, text: str) -> Tuple[str, str]:
        """Normalize text for consistent processing.

        Args:
            text: Raw text to normalize

        Returns:
            Tuple of (normalized_text, normalized_lowercase_text)
        """
        # Normalize text for comparison
        normalized_text = unicodedata.normalize("NFC", text)
        normalized_lower = normalized_text.lower()
        return normalized_text, normalized_lower

    def find_keyword_matches(
        self,
        text: str,
        text_lower: str,
        keywords: List[Tuple],
        window_chars: int = 1500,
    ) -> List[Document]:
        """Find keyword matches with context in the text.

        Args:
            text: Original text
            text_lower: Lowercase version of text
            keywords: List of keyword tuples (category, lang, original_key, processed_key)
            window_chars: Number of characters to include around matches

        Returns:
            List of Document objects with keyword matches and context
        """
        documents = []
        total_matches = 0

        for category, lang, original_key, processed_key in keywords:
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

                doc = Document(
                    page_content=context,
                    metadata={
                        "category": category,
                        "language": lang,
                        "keyword": original_key,
                        "match_position": match.start(),
                    },
                )
                documents.append(doc)

        print(f"Total keyword matches found: {total_matches}")
        print(f"Created {len(documents)} documents with context")

        return documents
