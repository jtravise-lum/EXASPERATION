#!/usr/bin/env python3
"""Initialize the vector database with Exabeam content."""

import argparse
import logging
import os
import sys
from pathlib import Path

from src.config import CHROMA_DB_PATH
from src.data_processing.embeddings import EmbeddingProvider
from src.data_processing.exabeam_processor import ExabeamContentProcessor
from src.data_processing.vector_store import VectorDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Initialize the vector database with Exabeam content.")
    parser.add_argument(
        "--content-dir",
        type=str,
        default=os.path.join(Path(__file__).parent.parent, "data", "content-library-cim2"),
        help="Path to the Exabeam Content-Library-CIM2 repository",
    )
    parser.add_argument(
        "--db-path",
        type=str,
        default=CHROMA_DB_PATH,
        help=f"Path to the vector database (default: {CHROMA_DB_PATH})",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset the database before initialization",
    )
    return parser.parse_args()


def main():
    """Initialize the database with Exabeam content."""
    args = parse_args()

    logger.info(f"Initializing database at {args.db_path}")
    logger.info(f"Using content from {args.content_dir}")

    try:
        # Initialize embedding provider
        embedding_provider = EmbeddingProvider()
        logger.info(f"Initialized embedding provider using {embedding_provider.model_name}")

        # Initialize vector database
        vector_db = VectorDatabase(
            embedding_provider=embedding_provider,
            db_path=args.db_path,
        )
        logger.info(f"Initialized vector database at {args.db_path}")

        # Reset database if requested
        if args.reset:
            logger.warning("Resetting vector database")
            vector_db.delete_collection()
            logger.info("Vector database reset completed")

        # Process and ingest Exabeam content
        content_processor = ExabeamContentProcessor(
            content_dir=args.content_dir,
        )
        logger.info("Beginning content processing")
        
        # Process content and get document chunks
        documents = content_processor.process_content()
        logger.info(f"Processed {len(documents)} document chunks")

        # Add documents to vector database
        if documents:
            logger.info(f"Adding {len(documents)} documents to vector database")
            vector_db.add_documents(documents)
            logger.info("Content ingestion completed successfully")
        else:
            logger.warning("No documents to add to the vector database")

        logger.info("Database initialization completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())