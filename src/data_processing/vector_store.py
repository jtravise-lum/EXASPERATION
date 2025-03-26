"""Vector database integration for storing and retrieving document embeddings."""

import logging
import os
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple

from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain.vectorstores.base import VectorStore

from src.config import CHROMA_DB_PATH
from src.data_processing.embeddings import MultiModalEmbeddingProvider, EmbeddingProvider

logger = logging.getLogger(__name__)


class CustomEmbeddingFunction:
    """Custom embedding function that works with the multi-modal embedding provider."""
    
    def __init__(self, embedding_provider: MultiModalEmbeddingProvider):
        """Initialize with a multi-modal embedding provider.
        
        Args:
            embedding_provider: The embedding provider to use
        """
        self.embedding_provider = embedding_provider
        
    def embed_documents(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> List[List[float]]:
        """Embed documents with appropriate model based on metadata.
        
        Args:
            texts: List of texts to embed
            metadatas: Optional list of metadata dictionaries
            
        Returns:
            List of embedding vectors
        """
        # Create document objects from texts and metadata
        documents = []
        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
            documents.append(Document(page_content=text, metadata=metadata))
        
        # Get embeddings with the most appropriate model for each document
        embedding_results = self.embedding_provider.embed_documents(documents)
        
        # Extract just the embedding vectors
        return [embedding for embedding, _ in embedding_results]
        
    def embed_query(self, text: str) -> List[float]:
        """Embed a query using the default text model.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector
        """
        return self.embedding_provider.embed_query(text, query_type="text")


class VectorDatabase:
    """Interface for interacting with the vector database."""

    def __init__(
        self,
        embedding_provider: Union[EmbeddingProvider, MultiModalEmbeddingProvider],
        db_path: str = CHROMA_DB_PATH,
        collection_name: str = "exabeam_docs",
    ):
        """Initialize the vector database.

        Args:
            embedding_provider: The embedding provider to use
            db_path: Path to the database
            collection_name: Name of the collection
        """
        self.embedding_provider = embedding_provider
        self.db_path = db_path
        self.collection_name = collection_name
        self.vectorstore = None

        # Create a custom embedding function that works with our multi-modal provider
        self.embedding_function = CustomEmbeddingFunction(embedding_provider)

        # Ensure the database directory exists
        os.makedirs(db_path, exist_ok=True)

        # Initialize or load the database
        self._init_vectorstore()

    def _init_vectorstore(self) -> None:
        """Initialize or load the vector store."""
        try:
            logger.info(f"Initializing vector database at {self.db_path}")
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embedding_function,
                persist_directory=self.db_path,
            )
            count = self.vectorstore._collection.count()
            logger.info(f"Vector database initialized with {count} documents")
        except Exception as e:
            logger.error(f"Error initializing vector database: {str(e)}")
            raise

    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to the vector database.

        Args:
            documents: List of documents to add

        Returns:
            List of document IDs
        """
        if not documents:
            logger.warning("Attempting to add empty document list")
            return []

        logger.info(f"Adding {len(documents)} documents to vector database")
        
        try:
            # Generate IDs if not present
            ids = []
            for doc in documents:
                if "id" not in doc.metadata:
                    doc.metadata["id"] = str(uuid.uuid4())
                ids.append(doc.metadata["id"])
            
            # Add documents using custom add method
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            
            self.vectorstore._collection.add(
                documents=texts,
                embeddings=self.embedding_function.embed_documents(texts, metadatas),
                metadatas=metadatas,
                ids=ids
            )
            
            self.vectorstore.persist()
            logger.info(f"Added {len(ids)} documents to vector database")
            return ids
        except Exception as e:
            logger.error(f"Error adding documents to vector database: {str(e)}")
            raise

    def similarity_search(
        self, query: str, k: int = 5, filter: Optional[Dict[str, Any]] = None,
        query_type: str = "text"
    ) -> List[Document]:
        """Search for similar documents.

        Args:
            query: The query string
            k: Number of results to return
            filter: Optional metadata filters
            query_type: Type of query ("text" or "code")

        Returns:
            List of similar documents
        """
        logger.info(f"Searching for documents similar to: {query[:50]}...")
        try:
            # Get the embedding for the query
            query_embedding = self.embedding_provider.embed_query(query, query_type=query_type)
            
            # Perform the search
            results = self.vectorstore.similarity_search_by_vector(
                query_embedding, k=k, filter=filter
            )
            
            logger.info(f"Found {len(results)} results for query")
            return results
        except Exception as e:
            logger.error(f"Error searching vector database: {str(e)}")
            raise

    def similarity_search_with_score(
        self, query: str, k: int = 5, filter: Optional[Dict[str, Any]] = None,
        query_type: str = "text"
    ) -> List[Tuple[Document, float]]:
        """Search for similar documents and return scores.

        Args:
            query: The query string
            k: Number of results to return
            filter: Optional metadata filters
            query_type: Type of query ("text" or "code")

        Returns:
            List of (document, score) tuples
        """
        logger.info(f"Searching with scores for documents similar to: {query[:50]}...")
        try:
            # Get the embedding for the query
            query_embedding = self.embedding_provider.embed_query(query, query_type=query_type)
            
            # Perform the search
            results = self.vectorstore.similarity_search_by_vector_with_relevance_scores(
                query_embedding, k=k, filter=filter
            )
            
            logger.info(f"Found {len(results)} scored results for query")
            return results
        except Exception as e:
            logger.error(f"Error searching vector database with scores: {str(e)}")
            raise

    def delete_collection(self) -> None:
        """Delete the entire collection from the database."""
        logger.warning(f"Deleting collection {self.collection_name}")
        try:
            self.vectorstore.delete_collection()
            self._init_vectorstore()
            logger.info("Collection deleted and reinitialized")
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            raise
