"""Retrieval module for finding relevant documents for a query."""

import logging
from typing import List, Dict, Any, Optional, Tuple

from langchain.schema import Document

from src.config import TOP_K_RETRIEVAL, RERAPQUNK_THRESHOLD
from src.data_processing.vector_store import VectorDatabase
from src.retrieval.query_processor import QueryProcessor
from src.retrieval.reranker import Reranker

logger = logging.getLogger(__name__)


class Retriever:
    """Handles retrieval of relevant documents for a query."""

    def __init__(
        self,
        vector_db: VectorDatabase,
        query_processor: Optional[QueryProcessor] = None,
        reranker: Optional[Reranker] = None,
        top_k: int = TOP_K_RETRIEVAL,
        rerank_threshold: float = RERAPQUNK_THRESHOLD,
    ):
        """Initialize the retriever.

        Args:
            vector_db: Vector database for similarity search
            query_processor: Optional query processor for query enhancement
            reranker: Optional reranker for improving search results
            top_k: Number of documents to retrieve
            rerank_threshold: Threshold for reranker relevance
        """
        self.vector_db = vector_db
        self.query_processor = query_processor or QueryProcessor()
        self.reranker = reranker
        self.top_k = top_k
        self.rerank_threshold = rerank_threshold

    def retrieve(self, query: str, filter: Optional[Dict[str, Any]] = None) -> List[Document]:
        """Retrieve relevant documents for a query.

        Args:
            query: The search query
            filter: Optional metadata filters

        Returns:
            List of relevant documents
        """
        if not query or not query.strip():
            logger.warning("Empty query received")
            return []

        # Process the query
        processed_query = self.query_processor.process_query(query)
        logger.info(f"Processed query: {processed_query}")

        # Retrieve documents from vector database
        # We retrieve more documents than needed if reranking is enabled
        k = self.top_k * 3 if self.reranker else self.top_k
        retrieved_docs = self.vector_db.similarity_search(processed_query, k=k, filter=filter)

        if not retrieved_docs:
            logger.warning("No documents retrieved for query")
            return []

        logger.info(f"Retrieved {len(retrieved_docs)} documents from vector database")

        # Rerank if a reranker is available
        if self.reranker and len(retrieved_docs) > 1:
            reranked_docs = self.reranker.rerank(query, retrieved_docs, threshold=self.rerank_threshold)
            logger.info(f"Reranked documents, kept {len(reranked_docs)} above threshold")
            
            # If we have enough reranked documents, use them; otherwise use vector search results
            if len(reranked_docs) >= min(3, self.top_k):
                return reranked_docs[:self.top_k]

        # Return top_k documents
        return retrieved_docs[:self.top_k]

    def retrieve_with_scores(
        self, query: str, filter: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Document, float]]:
        """Retrieve relevant documents with similarity scores.

        Args:
            query: The search query
            filter: Optional metadata filters

        Returns:
            List of (document, score) tuples
        """
        processed_query = self.query_processor.process_query(query)
        retrieved_docs = self.vector_db.similarity_search_with_score(
            processed_query, k=self.top_k, filter=filter
        )

        logger.info(f"Retrieved {len(retrieved_docs)} scored documents from vector database")
        return retrieved_docs

    def assemble_context(self, documents: List[Document]) -> str:
        """Assemble retrieved documents into a context string for the LLM.

        Args:
            documents: List of retrieved documents

        Returns:
            Assembled context string
        """
        if not documents:
            return ""

        # Basic assembly - concatenate document contents with citations
        context_parts = []

        for i, doc in enumerate(documents, 1):
            # Extract source information for citation
            source = doc.metadata.get("source", f"Document {i}")
            
            # Format the document with a citation
            content = f"Document {i} (Source: {source}):\n{doc.page_content}\n"
            context_parts.append(content)

        return "\n\n".join(context_parts)
