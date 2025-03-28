"""Integration adapter for semantic chunking and document analysis components."""

import logging
from typing import List, Dict, Any, Optional, Tuple
from langchain.schema import Document

from src.data_processing.chunker import DocumentChunker
from src.data_processing.semantic_chunker import SemanticChunker
from src.data_processing.document_analyzer import DocumentAnalyzer

logger = logging.getLogger(__name__)

class SemanticDocumentChunker(DocumentChunker):
    """Enhanced chunker that implements DocumentChunker interface while providing semantic chunking.
    
    This adapter connects the new semantic chunking capabilities with the existing
    document processing pipeline by implementing the DocumentChunker interface.
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Initialize with compatible parameters to match the original DocumentChunker.
        
        Args:
            chunk_size: Default chunk size (will be adaptively adjusted)
            chunk_overlap: Default chunk overlap (will be adaptively adjusted)
        """
        super().__init__(chunk_size, chunk_overlap)
        self.semantic_chunker = SemanticChunker(
            min_chunk_size=chunk_size // 2,
            max_chunk_size=chunk_size * 2,
            chunk_overlap=chunk_overlap
        )
        self.document_analyzer = DocumentAnalyzer()
        logger.info(f"Initialized SemanticDocumentChunker with chunk_size={chunk_size}, "
                   f"chunk_overlap={chunk_overlap}")
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks using semantic chunking.
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of chunked documents with enhanced metadata
        """
        all_chunks = []
        
        for doc in documents:
            # Skip empty documents
            if not doc.page_content.strip():
                logger.warning(f"Skipping empty document with metadata: {doc.metadata}")
                continue
                
            logger.debug(f"Processing document with id: {doc.metadata.get('id', 'unknown')}")
            
            # Step 1: Use semantic chunker to split the document
            chunks = self.semantic_chunker.chunk_document(doc)
            
            # Step 2: Ensure chunk_id is added in the expected format
            for i, chunk in enumerate(chunks):
                # Check if chunk_id already exists from the semantic chunker
                if "chunk_id" not in chunk.metadata:
                    doc_id = doc.metadata.get("id", "doc")
                    chunk.metadata["chunk_id"] = f"{doc_id}_chunk_{i}"
                
                # Ensure backward compatibility by copying required metadata fields
                # in the format expected by the existing pipeline
                self._ensure_metadata_compatibility(doc.metadata, chunk.metadata)
            
            # Step 3: Analyze chunks to add entity and relationship metadata
            if chunks:
                chunks = self.document_analyzer.analyze_documents(chunks)
                
            all_chunks.extend(chunks)
            
        logger.info(f"Split {len(documents)} documents into {len(all_chunks)} chunks using semantic chunking")
        return all_chunks
    
    def split_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Document]:
        """Split text into chunks (maintains compatibility with original interface).
        
        Args:
            text: Text to split
            metadata: Optional metadata to associate with the document
            
        Returns:
            List of chunked documents
        """
        if not text.strip():
            logger.warning("Attempted to split empty text")
            return []
            
        # Create a Document object first
        doc = Document(page_content=text, metadata=metadata or {})
        
        # Then use split_documents to process it
        return self.split_documents([doc])
    
    def _ensure_metadata_compatibility(self, source_metadata: Dict[str, Any], 
                                     chunk_metadata: Dict[str, Any]) -> None:
        """Ensure chunk metadata is compatible with existing pipeline expectations.
        
        Args:
            source_metadata: Original document metadata
            chunk_metadata: Chunk metadata to be updated
        """
        # List of critical metadata fields that must be preserved
        critical_fields = [
            "doc_type", "content_type", "content_section", "source_path", 
            "id", "title", "vendor", "product", "mitre_tactics", "mitre_techniques"
        ]
        
        for field in critical_fields:
            if field in source_metadata and field not in chunk_metadata:
                chunk_metadata[field] = source_metadata[field]
                
        # Ensure chunk index is present
        if "chunk_index" not in chunk_metadata and "chunk_id" in chunk_metadata:
            # Try to extract index from chunk_id (format: doc_id_chunk_N)
            try:
                chunk_id = chunk_metadata["chunk_id"]
                if "_chunk_" in chunk_id:
                    index = int(chunk_id.split("_chunk_")[-1])
                    chunk_metadata["chunk_index"] = index
            except (ValueError, IndexError):
                # If extraction fails, assign a default index
                chunk_metadata["chunk_index"] = 0