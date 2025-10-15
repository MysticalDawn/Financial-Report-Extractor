# Project Structure Overview

## 📁 Financial Report Extractor

```
Financial-Report-Extractor/
├── 📁 src/                              # Source code directory
│   └── 📁 financial_extractor/          # Main package
│       ├── 📄 __init__.py              # Package initialization & exports
│       ├── 📄 main.py                  # Main application & FinancialReportExtractor class
│       ├── 📁 core/                    # Core functionality modules
│       │   ├── 📄 pdf_processor.py     # PDF processing & text extraction
│       │   └── 📄 llm_handler.py       # LLM operations & embeddings
│       ├── 📁 utils/                   # Utility functions
│       │   └── 📄 helpers.py           # Common helper functions
│       ├── 📁 queries/                 # Query templates
│       │   └── 📄 query_templates.py   # AI query templates for different tasks
│       └── 📁 keywords/                # Keyword extraction
│           └── 📄 keyword_extractor.py # Keyword definitions & extraction logic
├── 📁 examples/                        # Examples and sample files
│   ├── 📁 sample_reports/              # Sample PDF reports for testing
│   └── 📄 basic_usage.py              # Basic usage example
├── 📁 tests/                           # Test files
│   └── 📄 test_basic.py               # Basic unit tests
├── 📁 docs/                            # Documentation
│   └── 📄 API.md                      # API documentation
├── 📁 config/                          # Configuration files
│   └── 📄 requirements.txt             # Python dependencies
├── 📄 README.md                        # Main project documentation
├── 📄 setup.py                         # Package setup script
├── 📄 run.py                          # CLI entry point
├── 📄 env.example                     # Environment variables template
├── 📄 .gitignore                      # Git ignore rules
└── 📄 PROJECT_STRUCTURE.md            # This file
```

## 🏗️ Architecture Overview

### Core Components

1. **FinancialReportExtractor** (`main.py`)

   - Main application class
   - Orchestrates the entire extraction process
   - Provides public API for external use

2. **PDFProcessor** (`core/pdf_processor.py`)

   - Handles PDF loading and text extraction
   - Language detection (Arabic/English)
   - Arabic text processing and normalization
   - Keyword matching with context

3. **LLMHandler** (`core/llm_handler.py`)

   - Manages language model operations
   - Handles embeddings and vector stores
   - Question-answering chain management
   - Token counting and budget management

4. **Query Templates** (`queries/query_templates.py`)

   - Pre-defined AI prompts for different tasks
   - Revenue extraction queries (Arabic/English)
   - IPO analysis queries (Arabic/English)
   - Language-specific optimization

5. **Keyword Extractor** (`keywords/keyword_extractor.py`)

   - Keyword definitions for different tasks
   - Revenue-related keywords
   - IPO-related keywords
   - Multi-language support

6. **Utilities** (`utils/helpers.py`)
   - Environment variable management
   - Common helper functions
   - Configuration setup

## 🔄 Data Flow

```
PDF Input → PDFProcessor → Text Extraction → Language Detection
    ↓
Keyword Matching → Context Extraction → Document Creation
    ↓
LLMHandler → Embeddings → Vector Store → Query Processing
    ↓
AI Analysis → Structured Output → Results
```

## 🎯 Key Features

- **Modular Design**: Clean separation of concerns
- **Extensible**: Easy to add new extraction tasks
- **Bilingual**: Native Arabic and English support
- **AI-Powered**: Advanced language model integration
- **Production-Ready**: Comprehensive error handling and logging
- **Well-Tested**: Unit tests and examples included

## 🚀 Usage Patterns

### As a Library

```python
from src.financial_extractor import FinancialReportExtractor

extractor = FinancialReportExtractor()
result = extractor.extract_financial_data("report.pdf", task="1")
```

### As a CLI Tool

```bash
python run.py
# or
python -m src.financial_extractor.main
```

### As a Package

```bash
pip install -e .
financial-extractor
```

## 🔧 Development

- **Testing**: Run `python -m pytest tests/`
- **Linting**: Code follows PEP 8 standards
- **Documentation**: Comprehensive API docs and examples
- **Configuration**: Environment-based configuration
- **Dependencies**: Managed via requirements.txt

## 📈 Future Enhancements

- Additional file format support (Excel, Word)
- More extraction task types
- Web interface
- Batch processing capabilities
- Advanced analytics and reporting
- Integration with financial databases
