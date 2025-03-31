#!/usr/bin/env python3
"""Script to ingest product documentation from a JSON file into ChromaDB."""

import json
import logging
import os
import sys
import time
import uuid
import re
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

from langchain.schema import Document

# Add the root directory to sys.path for proper imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "../.."))
sys.path.insert(0, project_root)

from src.config import CHROMA_DB_PATH, CHROMA_SERVER_HOST, CHROMA_SERVER_PORT
from src.data_processing.embeddings import MultiModalEmbeddingProvider
from src.data_processing.vector_store import VectorDatabase
from src.data_processing.chunker import DocumentChunker
from src.data_processing.semantic_document_chunker import SemanticDocumentChunker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def load_json_data(json_file: str) -> List[Dict[str, Any]]:
    """Load documentation data from JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, dict):
            # If the JSON is a dictionary, convert to list of entries
            if "entries" in data:
                data = data["entries"]
            else:
                # Wrap the entire object in a list
                data = [data]
        
        logger.info(f"Loaded {len(data)} entries from {json_file}")
        return data
    except Exception as e:
        logger.error(f"Error loading JSON data from {json_file}: {str(e)}")
        raise


def convert_to_documents(json_data: List[Dict[str, Any]]) -> List[Document]:
    """Convert JSON data to Document objects."""
    documents = []
    skipped = 0
    
    for i, entry in enumerate(json_data):
        # Extract content and metadata fields based on common JSON patterns
        content = (
            entry.get('content', '') or 
            entry.get('text', '') or 
            entry.get('body', '') or
            entry.get('description', '')
        )
        
        # Skip empty content
        if not content or not content.strip():
            skipped += 1
            continue
        
        # Get document title for the ID
        title = entry.get('title', '')
        if title:
            # Clean the title to make it safe for use in IDs
            clean_title = re.sub(r'[^a-zA-Z0-9]+', '_', title).lower()
            # Truncate if too long
            if len(clean_title) > 40:
                clean_title = clean_title[:40]
        else:
            clean_title = f"doc_{i}"
        
        # Build metadata with a meaningful ID
        metadata = {
            "source": "product_documentation",
            "doc_type": "product_doc",
            "content_type": "documentation",
            "id": f"{clean_title}_{i}_{uuid.uuid4().hex[:8]}",
            "original_title": title,
        }
        
        # Add other fields if they exist
        for field in [
            "title", "url", "product", "category", "section", 
            "vendor", "version", "author", "date", "tags"
        ]:
            if field in entry and entry[field]:
                metadata[field] = entry[field]
        
        # Handle nested fields
        if "metadata" in entry and isinstance(entry["metadata"], dict):
            # Merge nested metadata
            for k, v in entry["metadata"].items():
                if v:  # Only add non-empty values
                    metadata[k] = v
        
        # Create document
        doc = Document(
            page_content=content,
            metadata=metadata
        )
        
        documents.append(doc)
    
    logger.info(f"Created {len(documents)} Document objects (skipped {skipped} empty entries)")
    return documents


def sanitize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize metadata to ensure compatibility with ChromaDB.
    
    Args:
        metadata: Document metadata
            
    Returns:
        Sanitized metadata compatible with ChromaDB
    """
    sanitized = {}
    for key, value in metadata.items():
        # Skip None values
        if value is None:
            continue
            
        # Convert lists to comma-separated strings
        if isinstance(value, (list, tuple)):
            sanitized[key] = ", ".join(str(item) for item in value)
        # Convert dicts to JSON-like strings
        elif isinstance(value, dict):
            sanitized[key] = str(value)
        # Pass through scalar types supported by ChromaDB
        elif isinstance(value, (str, int, float, bool)):
            sanitized[key] = value
        # Convert anything else to string
        else:
            sanitized[key] = str(value)
                
    return sanitized


def chunk_documents(documents: List[Document], use_semantic_chunking: bool = True, chunk_batch_size: int = 50) -> List[Document]:
    """Split documents into chunks for better retrieval, processing in batches."""
    if use_semantic_chunking:
        logger.info("Using semantic chunking for documents")
        chunker = SemanticDocumentChunker()
    else:
        logger.info("Using standard chunking for documents")
        chunker = DocumentChunker()
    
    # Process documents in batches to avoid memory issues
    chunked_docs = []
    total_batches = (len(documents) + chunk_batch_size - 1) // chunk_batch_size
    
    # Use a set to track used IDs and ensure uniqueness
    used_ids = set()
    
    try:
        from tqdm import tqdm
        use_progress_bar = True
        pbar = tqdm(total=len(documents), desc="Chunking documents")
    except ImportError:
        use_progress_bar = False
    
    for i in range(0, len(documents), chunk_batch_size):
        batch = documents[i:i+chunk_batch_size]
        batch_num = (i // chunk_batch_size) + 1
        
        logger.info(f"Chunking batch {batch_num}/{total_batches} with {len(batch)} documents")
        batch_chunks = chunker.split_documents(batch)
        
        # Ensure unique IDs and sanitize metadata
        for j, chunk in enumerate(batch_chunks):
            # Extract the original document title/ID base
            original_id = chunk.metadata.get("id", "")
            if original_id:
                # Get the base part before the UUID
                base_id = original_id.rsplit('_', 1)[0] if '_' in original_id else original_id
            else:
                base_id = f"chunk_{i}_{j}"
            
            # Create a unique ID using the base plus chunk number
            unique_id = f"{base_id}_chunk_{j}_{uuid.uuid4().hex[:8]}"
            
            # Check if ID exists, generate new one if needed
            while unique_id in used_ids:
                unique_id = f"{base_id}_chunk_{j}_{uuid.uuid4().hex[:12]}"
            
            # Add to tracking set
            used_ids.add(unique_id)
            
            # Update metadata
            chunk.metadata["id"] = unique_id
            chunk.metadata["chunk_id"] = unique_id
            
            # Preserve original document ID for reference
            if original_id and "original_doc_id" not in chunk.metadata:
                chunk.metadata["original_doc_id"] = original_id
            
            # Sanitize metadata
            chunk.metadata = sanitize_metadata(chunk.metadata)
        
        chunked_docs.extend(batch_chunks)
        logger.info(f"Batch {batch_num} yielded {len(batch_chunks)} chunks")
        
        # Update progress bar
        if use_progress_bar:
            pbar.update(len(batch))
    
    # Close progress bar
    if use_progress_bar:
        pbar.close()
    
    logger.info(f"Split {len(documents)} documents into {len(chunked_docs)} chunks")
    return chunked_docs


def ingest_documents(
    documents: List[Document], 
    collection_name: str = "exabeam_docs",
    batch_size: int = 20,
    use_server: bool = True,
    server_host: str = CHROMA_SERVER_HOST,
    server_port: int = CHROMA_SERVER_PORT,
    max_workers: int = 4
) -> Dict[str, Any]:
    """Ingest documents into the vector database."""
    # Initialize embedding provider and vector database
    embedding_provider = MultiModalEmbeddingProvider(max_workers=max_workers)
    vector_db = VectorDatabase(
        embedding_provider=embedding_provider,
        collection_name=collection_name,
        use_server=use_server,
        server_host=server_host,
        server_port=server_port
    )
    
    # Statistics
    stats = {
        "total_documents": len(documents),
        "successful_chunks": 0,
        "failed_chunks": 0,
        "start_time": time.time(),
        "end_time": None,
        "processing_time": None,
    }
    
    # Process in batches
    total_docs = len(documents)
    
    try:
        from tqdm import tqdm
        use_progress_bar = True
        pbar = tqdm(total=total_docs, desc="Ingesting documents")
    except ImportError:
        use_progress_bar = False
    
    for i in range(0, total_docs, batch_size):
        batch = documents[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total_docs + batch_size - 1) // batch_size
        
        logger.info(f"Processing batch {batch_num}/{total_batches} with {len(batch)} documents")
        
        try:
            # For each document in the batch, ensure it has a unique ID in its metadata
            for j, doc in enumerate(batch):
                # Generate a unique ID if not already present
                if "id" not in doc.metadata or not doc.metadata["id"]:
                    doc.metadata["id"] = f"chunk_{i}_{j}_{uuid.uuid4().hex[:8]}"
                
                # Ensure all metadata is in the correct format
                doc.metadata = sanitize_metadata(doc.metadata)
            
            # Add batch to vector database
            vector_db.add_documents(batch)
            stats["successful_chunks"] += len(batch)
            logger.info(f"Successfully added batch {batch_num}/{total_batches}")
        except Exception as e:
            stats["failed_chunks"] += len(batch)
            logger.error(f"Error processing batch {batch_num}/{total_batches}: {str(e)}")
            
            # Try processing documents individually if batch fails
            logger.info("Attempting to process failed batch documents individually")
            for doc in batch:
                try:
                    # Ensure metadata is sanitized and has unique ID
                    doc.metadata = sanitize_metadata(doc.metadata)
                    if "id" not in doc.metadata or not doc.metadata["id"]:
                        doc.metadata["id"] = f"single_{uuid.uuid4().hex}"
                    
                    # Add individual document
                    vector_db.add_documents([doc])
                    stats["successful_chunks"] += 1
                    stats["failed_chunks"] -= 1  # Correct the count
                    logger.info(f"Successfully added individual document")
                except Exception as e2:
                    logger.error(f"Error processing individual document: {str(e2)}")
        
        # Update progress bar
        if use_progress_bar:
            pbar.update(len(batch))
    
    # Close progress bar
    if use_progress_bar:
        pbar.close()
    
    # Update stats
    stats["end_time"] = time.time()
    stats["processing_time"] = stats["end_time"] - stats["start_time"]
    
    logger.info(f"Ingestion complete. Processed {stats['successful_chunks']} chunks successfully " +
                 f"({stats['failed_chunks']} failed) in {stats['processing_time']:.2f} seconds")
    
    return stats

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Ingest product documentation from JSON")
    parser.add_argument(
        "--json-file", 
        type=str, 
        required=True,
        help="Path to the JSON file with documentation"
    )
    parser.add_argument(
        "--collection-name", 
        type=str, 
        default="exabeam_docs",
        help="Name of the ChromaDB collection"
    )
    parser.add_argument(
        "--batch-size", 
        type=int, 
        default=20,
        help="Number of documents to process in each batch"
    )
    parser.add_argument(
        "--chunk-batch-size", 
        type=int, 
        default=50,
        help="Number of documents to process in each chunking batch"
    )
    parser.add_argument(
        "--no-semantic-chunking",
        action="store_true",
        help="Disable semantic chunking (use standard chunking instead)"
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=4,
        help="Maximum number of parallel workers for embedding"
    )
    parser.add_argument(
        "--server-host",
        type=str,
        default=CHROMA_SERVER_HOST,
        help="ChromaDB server host"
    )
    parser.add_argument(
        "--server-port",
        type=int,
        default=CHROMA_SERVER_PORT,
        help="ChromaDB server port"
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()
    
    logger.info(f"Starting ingestion of product documentation from {args.json_file}")
    logger.info(f"Using collection: {args.collection_name}")
    logger.info(f"Batch size: {args.batch_size}")
    logger.info(f"Chunk batch size: {args.chunk_batch_size}")
    logger.info(f"Semantic chunking: {not args.no_semantic_chunking}")
    
    try:
        # Load data from JSON file
        json_data = load_json_data(args.json_file)
        
        # Convert to Document objects
        documents = convert_to_documents(json_data)
        
        # Chunk documents in batches
        chunked_docs = chunk_documents(
            documents, 
            use_semantic_chunking=not args.no_semantic_chunking,
            chunk_batch_size=args.chunk_batch_size
        )
        
        # Ingest documents
        stats = ingest_documents(
            documents=chunked_docs,
            collection_name=args.collection_name,
            batch_size=args.batch_size,
            server_host=args.server_host,
            server_port=args.server_port,
            max_workers=args.max_workers
        )
        
        # Write stats to file
        with open("product_docs_ingestion_stats.json", "w") as f:
            json.dump(stats, f, indent=2)
        
        logger.info("Ingestion complete. Stats written to product_docs_ingestion_stats.json")
        
        return 0
    except Exception as e:
        logger.error(f"Error during ingestion: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
