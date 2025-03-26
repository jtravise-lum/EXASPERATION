"""Document chunking strategies for Exabeam Content-Library-CIM2 repository."""

import logging
import re
from typing import Dict, List, Any, Optional, Callable, Union

from langchain.schema import Document
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)

logger = logging.getLogger(__name__)


class ExabeamChunker:
    """Advanced document chunking for Exabeam Content-Library-CIM2 documents."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        keep_separator: bool = True,
    ):
        """Initialize the Exabeam document chunker.

        Args:
            chunk_size: The size of each text chunk
            chunk_overlap: The amount of overlap between chunks
            keep_separator: Whether to keep the separator in the chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.keep_separator = keep_separator
        
        # Create a markdown splitter for structured content
        self.md_header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "heading1"),
                ("##", "heading2"),
                ("###", "heading3"),
                ("####", "heading4"),
            ],
            strip_headers=False,
            return_each_line=False,
        )
        
        # Create a recursive splitter for fallback chunking
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
            keep_separator=self.keep_separator,
        )
        
        # Create specialized chunkers for different document types
        self.doc_type_chunkers = {
            "use_case_detail": self._chunk_by_vendor_sections,
            "data_source": self._chunk_by_use_case_sections,
            "parser": self._chunk_as_single_document,
            "rules_models": self._chunk_by_event_type,
            # Default to markdown header chunking
            "default": self._chunk_by_markdown_headers,
        }

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Chunk documents using the appropriate strategy based on document type.

        Args:
            documents: List of documents to chunk

        Returns:
            List of chunked documents
        """
        all_chunks = []
        
        for document in documents:
            try:
                doc_type = document.metadata.get("doc_type", "default")
                chunker = self.doc_type_chunkers.get(doc_type, self.doc_type_chunkers["default"])
                
                chunks = chunker(document)
                logger.debug(f"Created {len(chunks)} chunks for document {document.metadata.get('source', 'unknown')}")
                
                all_chunks.extend(chunks)
            except Exception as e:
                logger.error(f"Error chunking document {document.metadata.get('source', 'unknown')}: {str(e)}")
                # Add the original document as a single chunk if chunking fails
                all_chunks.append(document)
        
        # Add chunk IDs and positions
        for i, chunk in enumerate(all_chunks):
            chunk.metadata["chunk_id"] = i
            chunk.metadata["total_chunks"] = len(all_chunks)
        
        logger.info(f"Created a total of {len(all_chunks)} chunks from {len(documents)} documents")
        return all_chunks

    def _chunk_by_markdown_headers(self, document: Document) -> List[Document]:
        """Chunk a document by markdown headers.

        Args:
            document: Document to chunk

        Returns:
            List of chunked documents
        """
        try:
            # First try to split by markdown headers
            md_chunks = self.md_header_splitter.split_text(document.page_content)
            
            # Create documents with metadata
            chunks = []
            for md_chunk in md_chunks:
                # Extract headers from the metadata
                headers = {k: v for k, v in md_chunk.metadata.items() if k.startswith("heading")}
                
                # Create a new document with combined metadata
                chunk_doc = Document(
                    page_content=md_chunk.page_content,
                    metadata={
                        **document.metadata,
                        **headers,
                    }
                )
                chunks.append(chunk_doc)
            
            # If chunks are still too large, apply recursive splitting
            final_chunks = []
            for chunk in chunks:
                if len(chunk.page_content) > self.chunk_size:
                    smaller_chunks = self.recursive_splitter.split_text(chunk.page_content)
                    for smaller_chunk in smaller_chunks:
                        final_chunks.append(
                            Document(
                                page_content=smaller_chunk,
                                metadata=chunk.metadata.copy()
                            )
                        )
                else:
                    final_chunks.append(chunk)
            
            return final_chunks
        except Exception as e:
            logger.warning(f"Error in markdown header chunking: {str(e)}. Falling back to recursive chunking.")
            # Fall back to recursive chunking
            return self._chunk_recursively(document)

    def _chunk_recursively(self, document: Document) -> List[Document]:
        """Chunk a document using recursive character splitting.

        Args:
            document: Document to chunk

        Returns:
            List of chunked documents
        """
        chunks = self.recursive_splitter.split_text(document.page_content)
        
        # Create documents with metadata
        return [
            Document(
                page_content=chunk,
                metadata=document.metadata.copy()
            )
            for chunk in chunks
        ]

    def _chunk_by_vendor_sections(self, document: Document) -> List[Document]:
        """Chunk a use case document by vendor sections.

        Args:
            document: Document to chunk

        Returns:
            List of chunked documents
        """
        # Use case documents have sections for each vendor
        # Try to identify vendor heading patterns
        vendor_pattern = re.compile(r"### Vendor: ([^\n]+)")
        
        # Find all vendor sections
        content = document.page_content
        vendor_matches = list(vendor_pattern.finditer(content))
        
        if not vendor_matches:
            # If no vendor sections found, fall back to markdown headers
            return self._chunk_by_markdown_headers(document)
        
        chunks = []
        
        # Process each vendor section
        for i, match in enumerate(vendor_matches):
            start_pos = match.start()
            # If it's the last match, go to the end of the document
            end_pos = len(content) if i == len(vendor_matches) - 1 else vendor_matches[i+1].start()
            
            vendor_name = match.group(1).strip()
            vendor_content = content[start_pos:end_pos]
            
            # Create a document for the vendor section
            vendor_doc = Document(
                page_content=vendor_content,
                metadata={
                    **document.metadata.copy(),
                    "section_type": "vendor",
                    "vendor": vendor_name,
                }
            )
            
            # If the vendor section is still too large, recursively split it
            if len(vendor_content) > self.chunk_size:
                vendor_chunks = self._chunk_recursively(vendor_doc)
                chunks.extend(vendor_chunks)
            else:
                chunks.append(vendor_doc)
        
        return chunks

    def _chunk_by_use_case_sections(self, document: Document) -> List[Document]:
        """Chunk a data source document by use case sections.

        Args:
            document: Document to chunk

        Returns:
            List of chunked documents
        """
        # Data source documents are structured with use case sections
        use_case_pattern = re.compile(r"\|\s*\[([^]]+)\]\([^)]+\)\s*\|")
        
        content = document.page_content
        chunks = []
        
        # First, add the vendor and product information as a separate chunk
        header_match = re.search(r"Vendor:.*?Product:.*?\n\n", content, re.DOTALL)
        if header_match:
            header_content = header_match.group(0)
            chunks.append(
                Document(
                    page_content=header_content,
                    metadata={
                        **document.metadata.copy(),
                        "section_type": "header",
                    }
                )
            )
        
        # Try to find use case sections
        use_case_matches = list(use_case_pattern.finditer(content))
        
        if not use_case_matches:
            # If no use case sections found, fall back to markdown headers
            return self._chunk_by_markdown_headers(document)
        
        # Extract each use case section
        for match in use_case_matches:
            use_case_name = match.group(1).strip()
            
            # Find the surrounding context (the row of the table)
            line_start = content.rfind("\n", 0, match.start()) + 1
            line_end = content.find("\n", match.end())
            if line_end == -1:
                line_end = len(content)
                
            use_case_row = content[line_start:line_end]
            
            # Create a document for the use case reference
            use_case_doc = Document(
                page_content=use_case_row,
                metadata={
                    **document.metadata.copy(),
                    "section_type": "use_case_reference",
                    "use_case": use_case_name,
                }
            )
            
            chunks.append(use_case_doc)
        
        # If we identified use cases but didn't create enough chunks,
        # also add chunks based on markdown headers
        if len(chunks) < 2:
            md_chunks = self._chunk_by_markdown_headers(document)
            chunks.extend(md_chunks)
        
        return chunks

    def _chunk_as_single_document(self, document: Document) -> List[Document]:
        """Keep a document as a single chunk if it's small enough.

        Args:
            document: Document to potentially chunk

        Returns:
            List of chunked documents
        """
        # For some document types like parsers, it's better to keep them whole
        # if they're already small enough
        if len(document.page_content) <= self.chunk_size:
            return [document]
        else:
            # If it's too large, use recursive chunking
            return self._chunk_recursively(document)

    def _chunk_by_event_type(self, document: Document) -> List[Document]:
        """Chunk a rules and models document by event type sections.

        Args:
            document: Document to chunk

        Returns:
            List of chunked documents
        """
        # Rules and models documents are organized by event types
        event_type_pattern = re.compile(r"\| Event Type\s*\|\s*Rules\s*\|\s*Models\s*\|")
        event_row_pattern = re.compile(r"\| ([^|]+)\s*\|(.*?)\|(.*?)\|")
        
        content = document.page_content
        chunks = []
        
        # First, extract the header information
        header_end = content.find("| Event Type")
        if header_end > 0:
            header_content = content[:header_end].strip()
            chunks.append(
                Document(
                    page_content=header_content,
                    metadata={
                        **document.metadata.copy(),
                        "section_type": "header",
                    }
                )
            )
        
        # Find all event type rows
        event_rows = event_row_pattern.finditer(content)
        
        for match in event_rows:
            event_type = match.group(1).strip()
            rules = match.group(2).strip()
            models = match.group(3).strip()
            
            # Create a document for the event type
            event_doc = Document(
                page_content=f"Event Type: {event_type}\nRules: {rules}\nModels: {models}",
                metadata={
                    **document.metadata.copy(),
                    "section_type": "event_type",
                    "event_type": event_type,
                }
            )
            
            chunks.append(event_doc)
        
        # If no event types found, fall back to markdown headers
        if not chunks:
            return self._chunk_by_markdown_headers(document)
        
        return chunks