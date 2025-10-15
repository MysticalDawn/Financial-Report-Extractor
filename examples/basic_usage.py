"""
Basic Usage Example for Financial Report Extractor

This example demonstrates how to use the Financial Report Extractor
to extract financial data from PDF reports.
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from financial_extractor import FinancialReportExtractor


def main():
    """Demonstrate basic usage of the Financial Report Extractor."""

    print("Financial Report Extractor - Basic Usage Example")
    print("=" * 50)

    try:
        # Initialize the extractor
        print("Initializing Financial Report Extractor...")
        extractor = FinancialReportExtractor()
        print("✅ Extractor initialized successfully!")

        # Example 1: Revenue extraction
        print("\n📊 Example 1: Revenue Data Extraction")
        print("-" * 40)

        # Check if sample file exists
        sample_file = "../examples/sample_reports/pru.pdf"
        if os.path.exists(sample_file):
            result = extractor.extract_financial_data(
                pdf_path=sample_file, task="1"  # Revenue extraction
            )

            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Language detected: {result['language']}")
                print(f"✅ Documents processed: {result['document_count']}")
                print(f"✅ Source file: {result['source_file']}")
                print(f"\n📋 Extracted Revenue Data:")
                print("-" * 30)
                print(result["result"])
        else:
            print(f"⚠️  Sample file not found: {sample_file}")
            print(
                "Please ensure you have sample PDF files in the examples/sample_reports/ directory"
            )

        # Example 2: IPO extraction
        print("\n\n🏢 Example 2: IPO Details Extraction")
        print("-" * 40)

        if os.path.exists(sample_file):
            result = extractor.extract_financial_data(
                pdf_path=sample_file, task="2"  # IPO extraction
            )

            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Language detected: {result['language']}")
                print(f"✅ Documents processed: {result['document_count']}")
                print(f"✅ Source file: {result['source_file']}")
                print(f"\n📋 Extracted IPO Data:")
                print("-" * 30)
                print(result["result"])
        else:
            print(f"⚠️  Sample file not found: {sample_file}")

        print("\n🎉 Example completed successfully!")

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please ensure you have set the OPENAI_API_KEY environment variable.")
        print("You can do this by creating a .env file with your API key.")

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print("Please check your setup and try again.")


if __name__ == "__main__":
    main()
