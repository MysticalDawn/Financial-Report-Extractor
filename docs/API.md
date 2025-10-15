# API Documentation

## FinancialReportExtractor

The main class for extracting financial data from PDF reports.

### Constructor

```python
FinancialReportExtractor(api_key: str = None)
```

**Parameters:**

- `api_key` (str, optional): OpenAI API key. If not provided, will use the `OPENAI_API_KEY` environment variable.

**Raises:**

- `ValueError`: If no API key is provided and `OPENAI_API_KEY` environment variable is not set.

### Methods

#### extract_financial_data

```python
extract_financial_data(pdf_path: str, task: str = "1", window_chars: int = 1500) -> Dict[str, Any]
```

Extract financial data from a PDF report.

**Parameters:**

- `pdf_path` (str): Path to the PDF file to process
- `task` (str, optional): Type of extraction task. Defaults to "1".
  - "1": Revenue information extraction
  - "2": IPO details extraction
- `window_chars` (int, optional): Number of characters to include around keyword matches for context. Defaults to 1500.

**Returns:**

- `Dict[str, Any]`: Dictionary containing:
  - `language` (str): Detected language ("Arabic" or "English")
  - `task` (str): The extraction task performed
  - `document_count` (int): Number of documents created from the PDF
  - `result` (str): Extracted financial data as text
  - `source_file` (str): Path to the source PDF file
  - `error` (str, optional): Error message if extraction failed

**Raises:**

- `FileNotFoundError`: If the PDF file doesn't exist
- `ValueError`: If the task parameter is invalid

### Example Usage

```python
from src.financial_extractor import FinancialReportExtractor

# Initialize the extractor
extractor = FinancialReportExtractor()

# Extract revenue data
result = extractor.extract_financial_data(
    pdf_path="path/to/financial_report.pdf",
    task="1"
)

# Check for errors
if "error" in result:
    print(f"Error: {result['error']}")
else:
    print(f"Language: {result['language']}")
    print(f"Documents processed: {result['document_count']}")
    print(f"Extracted data: {result['result']}")
```

## PDFProcessor

Handles PDF processing and text extraction.

### Methods

#### detect_language

```python
detect_language(text: str) -> str
```

Detect the primary language of the text.

**Parameters:**

- `text` (str): Text to analyze

**Returns:**

- `str`: "Arabic", "English", or "Unknown"

#### extract_text_from_pdf

```python
extract_text_from_pdf(pdf_path: str) -> str
```

Extract text content from a PDF file.

**Parameters:**

- `pdf_path` (str): Path to the PDF file

**Returns:**

- `str`: Extracted text content

## LLMHandler

Handles language model operations and embeddings.

### Methods

#### initialize_embeddings

```python
initialize_embeddings() -> HuggingFaceEmbeddings
```

Initialize HuggingFace embeddings for vector search.

**Returns:**

- `HuggingFaceEmbeddings`: Configured embeddings instance

#### ask_question

```python
ask_question(docsearch: FAISS, chain: object, query: str, max_docs: int = 5) -> str
```

Ask a question using the vector store and QA chain.

**Parameters:**

- `docsearch` (FAISS): Vector store containing document embeddings
- `chain` (object): QA chain instance
- `query` (str): Question to ask
- `max_docs` (int, optional): Maximum number of documents to retrieve. Defaults to 5.

**Returns:**

- `str`: Answer from the language model

## Error Handling

The application includes comprehensive error handling:

- **API Key Errors**: Clear messages when API keys are missing or invalid
- **File Errors**: Proper handling of missing or corrupted PDF files
- **Token Limit Errors**: Automatic handling of token limit exceeded scenarios
- **Language Detection Errors**: Fallback handling for unsupported languages
- **Processing Errors**: Graceful handling of PDF processing failures

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Required. Your OpenAI API key for Claude integration
- `TOKENIZERS_PARALLELISM`: Optional. Set to "false" to avoid warnings
- `LOG_LEVEL`: Optional. Logging level (DEBUG, INFO, WARNING, ERROR)
- `MAX_FILE_SIZE_MB`: Optional. Maximum file size in MB (default: 50)
- `DEFAULT_WINDOW_CHARS`: Optional. Default context window size (default: 1500)

### Customization

You can customize the extraction behavior by:

1. **Modifying keyword lists** in `src/financial_extractor/keywords/keyword_extractor.py`
2. **Updating query templates** in `src/financial_extractor/queries/query_templates.py`
3. **Adjusting processing parameters** in the main extraction method
4. **Adding new extraction tasks** by extending the existing framework
