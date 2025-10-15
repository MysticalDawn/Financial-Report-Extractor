"""
Basic tests for Financial Report Extractor

These tests verify the basic functionality of the extractor.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from financial_extractor import FinancialReportExtractor
from financial_extractor.core.pdf_processor import PDFProcessor
from financial_extractor.core.llm_handler import LLMHandler


class TestPDFProcessor(unittest.TestCase):
    """Test cases for PDFProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = PDFProcessor()

    def test_detect_language_english(self):
        """Test English language detection."""
        text = "This is an English financial report with revenue data."
        result = self.processor.detect_language(text)
        self.assertEqual(result, "English")

    def test_detect_language_arabic(self):
        """Test Arabic language detection."""
        text = "هذا تقرير مالي باللغة العربية يحتوي على بيانات الإيرادات."
        result = self.processor.detect_language(text)
        self.assertEqual(result, "Arabic")

    def test_fix_arabic_text(self):
        """Test Arabic text fixing."""
        text = "مرحبا"
        result = self.processor.fix_arabic(text)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_normalize_text(self):
        """Test text normalization."""
        text = "Test text with numbers 123"
        normalized, normalized_lower = self.processor.normalize_text(text)
        self.assertEqual(normalized, text)
        self.assertEqual(normalized_lower, text.lower())


class TestLLMHandler(unittest.TestCase):
    """Test cases for LLMHandler class."""

    def setUp(self):
        """Set up test fixtures."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
            self.handler = LLMHandler()

    def test_count_tokens(self):
        """Test token counting."""
        text = "This is a test text for token counting."
        tokens = self.handler.count_tokens(text)
        self.assertIsInstance(tokens, int)
        self.assertGreater(tokens, 0)

    @patch("torch.backends.mps.is_available")
    def test_initialize_embeddings(self, mock_mps):
        """Test embeddings initialization."""
        mock_mps.return_value = False
        embeddings = self.handler.initialize_embeddings()
        self.assertIsNotNone(embeddings)


class TestFinancialReportExtractor(unittest.TestCase):
    """Test cases for FinancialReportExtractor class."""

    def setUp(self):
        """Set up test fixtures."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
            self.extractor = FinancialReportExtractor()

    def test_initialization(self):
        """Test extractor initialization."""
        self.assertIsNotNone(self.extractor.pdf_processor)
        self.assertIsNotNone(self.extractor.llm_handler)
        self.assertEqual(self.extractor.api_key, "test_key")

    def test_initialization_without_api_key(self):
        """Test initialization without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                FinancialReportExtractor()


class TestIntegration(unittest.TestCase):
    """Integration tests."""

    def test_module_imports(self):
        """Test that all modules can be imported."""
        try:
            from financial_extractor import FinancialReportExtractor
            from financial_extractor.core.pdf_processor import PDFProcessor
            from financial_extractor.core.llm_handler import LLMHandler
            from financial_extractor.utils.helpers import load_environment
            from financial_extractor.queries.query_templates import get_query
            from financial_extractor.keywords.keyword_extractor import get_keywords
        except ImportError as e:
            self.fail(f"Failed to import module: {e}")


if __name__ == "__main__":
    # Set up environment for testing
    os.environ["OPENAI_API_KEY"] = "test_key"
    unittest.main()
