"""Document ingestion pipeline for Exabeam content."""

import logging
import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from tqdm import tqdm

from langchain.schema import Document

from src.config import CHROMA_DB_PATH, CHROMA_SERVER_HOST, CHROMA_SERVER_PORT
from src.data_processing.embeddings import MultiModalEmbeddingProvider
from src.data_processing.exabeam_loader import ExabeamDocumentLoader
from src.data_processing.exabeam_preprocessor import ExabeamPreprocessor
from src.data_processing.exabeam_chunker import ExabeamChunker
from src.data_processing.exabeam_processor import ExabeamContentProcessor
from src.data_processing.vector_store import VectorDatabase

logger = logging.getLogger(__name__)


class ExabeamIngestionPipeline:
    """Pipeline for ingesting Exabeam content into the vector database."""

    def __init__(
        self,
        content_dir: str,
        db_path: str = CHROMA_DB_PATH,
        collection_name: str = "exabeam_docs",
        use_server: bool = True,
        server_host: str = CHROMA_SERVER_HOST,
        server_port: int = CHROMA_SERVER_PORT,
        batch_size: int = 50,
        max_threads: int = 4,
    ):
        """Initialize the ingestion pipeline.

        Args:
            content_dir: Directory containing Exabeam content
            db_path: Path to ChromaDB database
            collection_name: Name of the collection in ChromaDB
            use_server: Whether to use ChromaDB server mode
            server_host: ChromaDB server host
            server_port: ChromaDB server port
            batch_size: Number of documents to process in each batch
            max_threads: Maximum number of threads for concurrent processing
        """
        self.content_dir = Path(content_dir)
        if not self.content_dir.exists() or not self.content_dir.is_dir():
            raise ValueError(f"Invalid content directory: {content_dir}")

        self.db_path = db_path
        self.collection_name = collection_name
        self.use_server = use_server
        self.server_host = server_host
        self.server_port = server_port
        self.batch_size = batch_size
        self.max_threads = max_threads

        # Initialize components
        self.document_loader = ExabeamDocumentLoader(content_dir=content_dir)
        self.preprocessor = ExabeamPreprocessor()
        self.chunker = ExabeamChunker()
        self.embedding_provider = MultiModalEmbeddingProvider(max_workers=max_threads)
        
        # Initialize processor with our specialized components
        self.content_processor = ExabeamContentProcessor(
            content_dir=content_dir,
            document_loader=self.document_loader,
            document_chunker=self.chunker,
        )
        
        # Initialize vector database
        self.vector_db = VectorDatabase(
            embedding_provider=self.embedding_provider,
            db_path=self.db_path,
            collection_name=self.collection_name,
            use_server=self.use_server,
            server_host=self.server_host,
            server_port=self.server_port,
        )
        
        # Statistics tracking
        self.stats = {
            "total_documents": 0,
            "total_chunks": 0,
            "successful_chunks": 0,
            "failed_chunks": 0,
            "embedding_errors": 0,
            "start_time": None,
            "end_time": None,
            "processing_time": None,
        }

    def run(self, reset_db: bool = False) -> Dict[str, Any]:
        """Run the ingestion pipeline.

        Args:
            reset_db: Whether to reset the database before ingestion

        Returns:
            Statistics about the ingestion process
        """
        self.stats["start_time"] = time.time()
        logger.info(f"Starting Exabeam content ingestion from {self.content_dir}")
        
        try:
            # Reset the database if requested
            if reset_db:
                logger.warning("Resetting vector database")
                self.vector_db.delete_collection()
                logger.info("Vector database reset completed")
            
            # Process content to get document chunks
            logger.info("Processing Exabeam content")
            documents = self.content_processor.process_content()
            self.stats["total_documents"] = len(documents)
            logger.info(f"Processed {len(documents)} document chunks")
            
            if not documents:
                logger.warning("No documents to ingest")
                return self.stats
            
            # Ingest documents in batches
            logger.info(f"Ingesting documents in batches of {self.batch_size}")
            self._ingest_documents_in_batches(documents)
            
            self.stats["end_time"] = time.time()
            self.stats["processing_time"] = self.stats["end_time"] - self.stats["start_time"]
            
            logger.info(f"Ingestion complete. Processed {self.stats['successful_chunks']} chunks successfully " +
                         f"({self.stats['failed_chunks']} failed) in {self.stats['processing_time']:.2f} seconds")
            
            return self.stats
            
        except Exception as e:
            logger.error(f"Error during ingestion: {str(e)}", exc_info=True)
            self.stats["end_time"] = time.time()
            self.stats["processing_time"] = self.stats["end_time"] - self.stats["start_time"]
            raise

    def _ingest_documents_in_batches(self, documents: List[Document]) -> None:
        """Ingest documents in batches to avoid overwhelming the system.

        Args:
            documents: List of documents to ingest
        """
        total_batches = (len(documents) + self.batch_size - 1) // self.batch_size
        
        with tqdm(total=len(documents), desc="Ingesting documents") as pbar:
            for i in range(0, len(documents), self.batch_size):
                batch = documents[i:i+self.batch_size]
                batch_num = (i // self.batch_size) + 1
                
                logger.info(f"Processing batch {batch_num}/{total_batches} with {len(batch)} documents")
                
                try:
                    # Add batch to vector database
                    self.vector_db.add_documents(batch)
                    self.stats["successful_chunks"] += len(batch)
                    logger.info(f"Successfully added batch {batch_num}/{total_batches}")
                except Exception as e:
                    self.stats["failed_chunks"] += len(batch)
                    self.stats["embedding_errors"] += 1
                    logger.error(f"Error processing batch {batch_num}/{total_batches}: {str(e)}", exc_info=True)
                    
                    # If a batch fails, try processing documents individually
                    logger.info("Attempting to process failed batch documents individually")
                    for doc in batch:
                        try:
                            self.vector_db.add_documents([doc])
                            self.stats["successful_chunks"] += 1
                            self.stats["failed_chunks"] -= 1  # Correct the count
                            logger.info(f"Successfully added individual document")
                        except Exception as e2:
                            logger.error(f"Error processing individual document: {str(e2)}")
                
                pbar.update(len(batch))

    def verify_ingestion(self, query: str = "Exabeam") -> List[Document]:
        """Verify that documents were ingested correctly.

        Args:
            query: Query to use for verification

        Returns:
            List of retrieved documents
        """
        logger.info(f"Verifying ingestion with query: {query}")
        results = self.vector_db.similarity_search(query, k=5)
        logger.info(f"Retrieved {len(results)} documents")
        
        for i, doc in enumerate(results):
            logger.info(f"Result {i+1}: {doc.page_content[:100]}... [Metadata: {doc.metadata}]")
        
        return results