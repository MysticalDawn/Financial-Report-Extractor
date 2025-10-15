# 📊 Financial Report Extractor

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)

**A powerful AI-driven tool for extracting and analyzing financial data from PDF reports, with specialized support for Saudi Arabian financial documents and IPO prospectuses.**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Examples](#-examples)

</div>

---

## 🌟 Overview

The Financial Report Extractor is an advanced Python application that leverages cutting-edge AI technologies to automatically extract, process, and analyze financial information from PDF documents. Built with a focus on Saudi Arabian financial markets, it supports both Arabic and English documents and provides specialized extraction for revenue data and IPO prospectuses.

### 🎯 Key Capabilities

- **🔍 Intelligent PDF Processing**: Advanced text extraction with Arabic language support
- **🤖 AI-Powered Analysis**: Uses Claude Opus and HuggingFace embeddings for accurate data extraction
- **📈 Financial Data Focus**: Specialized for revenue extraction and IPO prospectus analysis
- **🌐 Bilingual Support**: Native support for both Arabic and English financial documents
- **⚡ High Performance**: Optimized for Apple Silicon with MPS acceleration support
- **🔧 Modular Architecture**: Clean, maintainable codebase with separation of concerns

---

## ✨ Features

### 📋 Core Functionality

- **Revenue Data Extraction**: Automatically identify and extract revenue figures, growth rates, and financial metrics
- **IPO Analysis**: Comprehensive extraction of IPO details including offer prices, timing, and financial information
- **Language Detection**: Automatic detection of Arabic vs English content
- **Context-Aware Processing**: Intelligent keyword matching with surrounding context
- **Token Management**: Smart token budgeting to handle large documents efficiently

### 🛠️ Technical Features

- **Vector Search**: FAISS-powered similarity search for relevant document sections
- **Arabic Text Processing**: Proper handling of Arabic text with reshaping and bidirectional display
- **PDF Processing**: Robust PDF text extraction using PyPDF2
- **Environment Management**: Secure API key handling with dotenv
- **Error Handling**: Comprehensive error handling and user feedback

### 🎨 User Experience

- **Interactive CLI**: User-friendly command-line interface
- **Progress Feedback**: Real-time processing updates and status messages
- **Flexible Input**: Support for various PDF formats and file paths
- **Detailed Output**: Structured results with metadata and source information

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for Claude integration)
- Git (for cloning the repository)

### Step-by-Step Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/MysticalDawn/Financial-Report-Extractor.git
   cd Financial-Report-Extractor
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r config/requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create a .env file in the project root
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

---

## 🏃‍♂️ Quick Start

### Basic Usage

```python
from src.financial_extractor import FinancialReportExtractor

# Initialize the extractor
extractor = FinancialReportExtractor()

# Extract revenue data from a PDF
result = extractor.extract_financial_data(
    pdf_path="path/to/your/financial_report.pdf",
    task="1"  # '1' for revenue, '2' for IPO
)

print(result['result'])
```

### Command Line Usage

```bash
# Run the interactive CLI
python -m src.financial_extractor.main

# Or run directly
python src/financial_extractor/main.py
```

### Example Workflow

1. **Start the application**

   ```bash
   python -m src.financial_extractor.main
   ```

2. **Choose your PDF file**

   - Enter the path to your PDF file
   - Or press Enter to use the default sample file

3. **Select extraction type**

   - Choose `1` for Revenue Information
   - Choose `2` for IPO Details

4. **View results**
   - The AI will process your document and extract relevant financial data
   - Results will be displayed in a structured format

---

## 📁 Project Structure

```
Financial-Report-Extractor/
├── 📁 src/
│   └── 📁 financial_extractor/
│       ├── 📄 __init__.py              # Package initialization
│       ├── 📄 main.py                  # Main application entry point
│       ├── 📁 core/                    # Core functionality modules
│       │   ├── 📄 pdf_processor.py     # PDF processing and text extraction
│       │   └── 📄 llm_handler.py       # LLM operations and embeddings
│       ├── 📁 utils/                   # Utility functions
│       │   └── 📄 helpers.py           # Common helper functions
│       ├── 📁 queries/                 # Query templates
│       │   └── 📄 query_templates.py   # AI query templates for different tasks
│       └── 📁 keywords/                # Keyword extraction
│           └── 📄 keyword_extractor.py # Keyword definitions and extraction logic
├── 📁 examples/                        # Sample files and examples
│   └── 📁 sample_reports/              # Sample PDF reports for testing
├── 📁 config/                          # Configuration files
│   └── 📄 requirements.txt             # Python dependencies
├── 📁 tests/                           # Test files
├── 📁 docs/                            # Documentation
├── 📄 README.md                        # This file
└── 📄 .env.example                     # Environment variables template
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
TOKENIZERS_PARALLELISM=false
```

### Customization Options

You can customize the extraction behavior by modifying parameters:

```python
# Customize extraction parameters
result = extractor.extract_financial_data(
    pdf_path="your_file.pdf",
    task="1",                    # '1' for revenue, '2' for IPO
    window_chars=2000           # Increase context window around keywords
)
```

---

## 📚 Documentation

### API Reference

#### `FinancialReportExtractor`

The main class for financial data extraction.

**Methods:**

- `__init__(api_key=None)`: Initialize the extractor
- `extract_financial_data(pdf_path, task="1", window_chars=1500)`: Extract financial data

**Parameters:**

- `pdf_path` (str): Path to the PDF file
- `task` (str): Extraction task type ('1' for revenue, '2' for IPO)
- `window_chars` (int): Context window size around keyword matches

**Returns:**

- `dict`: Dictionary containing extracted data and metadata

### Supported File Formats

- **PDF**: Primary format supported
- **Text Encoding**: UTF-8 with Arabic and English support
- **File Size**: Optimized for documents up to 50MB

### Language Support

- **Arabic**: Full support with proper text reshaping and bidirectional display
- **English**: Native support with standard processing
- **Mixed Content**: Automatic language detection and appropriate processing

---

## 🎯 Use Cases

### Financial Analysis

- **Revenue Analysis**: Extract revenue figures, growth rates, and trends
- **IPO Research**: Analyze IPO prospectuses for investment decisions
- **Compliance**: Ensure financial data accuracy and completeness
- **Due Diligence**: Support investment and acquisition processes

### Business Intelligence

- **Market Research**: Analyze competitor financial performance
- **Risk Assessment**: Identify financial risks and opportunities
- **Reporting**: Generate structured financial reports
- **Data Integration**: Feed extracted data into business systems

### Academic Research

- **Financial Studies**: Support academic research on financial markets
- **Case Studies**: Analyze specific companies or market segments
- **Trend Analysis**: Study financial trends over time
- **Comparative Analysis**: Compare financial performance across companies

---

## 🧪 Examples

### Example 1: Revenue Extraction

```python
from src.financial_extractor import FinancialReportExtractor

# Initialize extractor
extractor = FinancialReportExtractor()

# Extract revenue data
result = extractor.extract_financial_data(
    pdf_path="examples/sample_reports/company_annual_report.pdf",
    task="1"  # Revenue extraction
)

# Display results
print(f"Language: {result['language']}")
print(f"Documents processed: {result['document_count']}")
print(f"Revenue data: {result['result']}")
```

### Example 2: IPO Analysis

```python
# Extract IPO details
result = extractor.extract_financial_data(
    pdf_path="examples/sample_reports/ipo_prospectus.pdf",
    task="2"  # IPO analysis
)

# Process IPO information
ipo_data = result['result']
print(f"IPO Details: {ipo_data}")
```

---

## 🛠️ Development

### Setting up Development Environment

1. **Clone and setup**

   ```bash
   git clone https://github.com/MysticalDawn/Financial-Report-Extractor.git
   cd Financial-Report-Extractor
   python -m venv venv
   source venv/bin/activate
   pip install -r config/requirements.txt
   ```

2. **Install development dependencies**

   ```bash
   pip install -r config/requirements-dev.txt  # If available
   ```

3. **Run tests**
   ```bash
   python -m pytest tests/
   ```

### Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 🐛 Troubleshooting

### Common Issues

**Q: "Please set the OPENAI_API_KEY environment variable" error**
A: Make sure you have created a `.env` file with your OpenAI API key.

**Q: Arabic text not displaying correctly**
A: The application handles Arabic text reshaping automatically. If issues persist, check your terminal's Unicode support.

**Q: "No keyword matches found" warning**
A: This usually means the PDF doesn't contain the expected financial keywords. Try using a different PDF or check the document content.

**Q: Memory issues with large PDFs**
A: Try reducing the `window_chars` parameter or processing smaller sections of the document.

### Performance Tips

- **Use SSD storage** for faster PDF processing
- **Close other applications** to free up memory
- **Use smaller context windows** for very large documents
- **Process documents in batches** for multiple files

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Support

- **Documentation**: [Full Documentation](docs/)
- **Issues**: [GitHub Issues](https://github.com/MysticalDawn/Financial-Report-Extractor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MysticalDawn/Financial-Report-Extractor/discussions)
- **Email**: contact@financial-extractor.com

---

## 🙏 Acknowledgments

- **OpenAI** for providing the Claude API
- **HuggingFace** for the sentence transformers
- **LangChain** for the LLM framework
- **FAISS** for vector similarity search
- **PyPDF2** for PDF processing
- **Arabic Reshaper** for Arabic text processing

---

<div align="center">

**Made with ❤️ for the financial community**

[⭐ Star this repo](https://github.com/MysticalDawn/Financial-Report-Extractor) • [🐛 Report Bug](https://github.com/MysticalDawn/Financial-Report-Extractor/issues) • [💡 Request Feature](https://github.com/MysticalDawn/Financial-Report-Extractor/issues)

</div>
