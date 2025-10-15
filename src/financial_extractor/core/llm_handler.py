"""
LLM Handler Module

Handles language model initialization, embeddings, and question-answering chains.
"""

import os
import tiktoken
import torch
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_anthropic import ChatAnthropic
from langchain.schema import Document


class LLMHandler:
    """Handles LLM operations and embeddings."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Please set the OPENAI_API_KEY environment variable.")

    def count_tokens(self, text: str, model: str = "cl100k_base") -> int:
        """Count tokens in text for a given model.

        Args:
            text: Text to count tokens for
            model: Tokenizer model to use

        Returns:
            Number of tokens
        """
        encoding = tiktoken.get_encoding(model)
        return len(encoding.encode(text))

    def initialize_embeddings(self) -> HuggingFaceEmbeddings:
        """Initialize HuggingFace embeddings.

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

    def initialize_qa_chain(self) -> object:
        """Initialize the question-answering chain.

        Returns:
            QA chain instance
        """
        return load_qa_chain(
            ChatAnthropic(
                model_name="claude-opus-4-20250514", temperature=0, verbose=True
            ),
            chain_type="stuff",
        )

    def create_vector_store(self, documents: List[Document], embeddings) -> FAISS:
        """Create FAISS vector store from documents.

        Args:
            documents: List of Document objects
            embeddings: Embeddings instance

        Returns:
            FAISS vector store
        """
        return FAISS.from_documents(documents, embeddings)

    def ask_question(
        self, docsearch: FAISS, chain: object, query: str, max_docs: int = 5
    ) -> str:
        """Ask a question using the vector store and QA chain.

        Args:
            docsearch: FAISS vector store
            chain: QA chain instance
            query: Question to ask
            max_docs: Maximum number of documents to retrieve

        Returns:
            Answer from the LLM
        """
        try:
            docs = docsearch.similarity_search(query, k=max_docs)

            # Filter docs to fit in token budget
            MAX_MODEL_TOKENS = 25000
            RESERVED_FOR_RESPONSE = 512
            MAX_CONTEXT_TOKENS = MAX_MODEL_TOKENS - RESERVED_FOR_RESPONSE

            selected_docs = []
            total_tokens = 0

            for doc in docs:
                tokens = self.count_tokens(doc.page_content)
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
                return (
                    "Error: Token limit exceeded. Try asking a more specific question."
                )
            return f"Error: {str(e)}"
