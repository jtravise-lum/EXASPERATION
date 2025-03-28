"""Enhanced semantic chunking for Exabeam documentation."""

import logging
import re
from typing import List, Dict, Any, Optional, Tuple, Union
from collections import defaultdict
import nltk
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

class SemanticChunker:
    """Enhanced chunker with semantic awareness for optimal document splitting."""
    
    def __init__(self, min_chunk_size=200, max_chunk_size=1500, chunk_overlap=150):
        """Initialize the semantic chunker.
        
        Args:
            min_chunk_size: Minimum chunk size in characters
            max_chunk_size: Maximum chunk size in characters
            chunk_overlap: Overlap between chunks in characters
        """
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize NLP tools
        self.nlp = self._initialize_nlp()
        
        # Define content type patterns
        self._init_content_patterns()
        
        logger.info(f"Initialized SemanticChunker with min_size={min_chunk_size}, "
                   f"max_size={max_chunk_size}, overlap={chunk_overlap}")
    
    def _initialize_nlp(self):
        """Initialize NLP tools for content analysis."""
        try:
            # Download required NLTK resources if not already available
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('maxent_ne_chunker', quiet=True)
            nltk.download('words', quiet=True)
            return nltk
        except Exception as e:
            logger.warning(f"Error initializing NLP tools: {str(e)}. "
                         "Falling back to basic chunking.")
            return None
    
    def _init_content_patterns(self):
        """Initialize patterns for identifying content types and boundaries."""
        # Patterns for detecting section headings with hierarchy levels
        self.section_patterns = [
            # Header level 1 (# Title)
            (r'^\s*#\s+(.+?)\s*$', 1),
            # Header level 2 (## Title)
            (r'^\s*##\s+(.+?)\s*$', 2),
            # Header level 3 (### Title)
            (r'^\s*###\s+(.+?)\s*$', 3),
            # Header level 4 (#### Title)
            (r'^\s*####\s+(.+?)\s*$', 4),
            # Underlined headers (Title\n===== or Title\n-----)
            (r'^(.+?)\s*\n\s*=+\s*$', 1),
            (r'^(.+?)\s*\n\s*-+\s*$', 2)
        ]
        
        # Patterns for detecting content types
        self.content_type_patterns = {
            "code_block": r'```[\s\S]*?```',  # Code blocks
            "table": r'\|[^\n]*\|[^\n]*\n(\|[:\-]+\|[:\-]+[^\n]*\n)+([^\n]*\|[^\n]*\n)+',  # Markdown tables
            "list": r'(^\s*[-*+]\s+.+?$(\n^\s*[-*+]\s+.+?$)+)',  # Bullet lists
            "numbered_list": r'(^\s*\d+\.\s+.+?$(\n^\s*\d+\.\s+.+?$)+)',  # Numbered lists
            "definition": r'(^\s*.+?:\s*$\n^\s{2,}.+?$)',  # Definition lines
            "url": r'(https?:\/\/[^\s\)]+)',  # URLs
            "exabeam_entity": r'\b(parser|data source|use case|rule|model|technique)\b',  # Exabeam entities
            "mitre": r'T\d{4}(?:\.\d{1,3})?'  # MITRE ATT&CK techniques
        }
        
        # Patterns for detecting security entities
        self.security_entity_patterns = {
            "attack_technique": r'\b(T\d{4}(?:\.\d{1,3})?)\b',  # MITRE ATT&CK technique IDs
            "attack_tactic": r'\b(reconnaissance|resource development|initial access|execution|persistence|privilege escalation|defense evasion|credential access|discovery|lateral movement|collection|command and control|exfiltration|impact)\b',  # MITRE tactics
            "security_product": r'\b(firewall|WAF|IDS|IPS|EDR|SIEM|SOAR|DLP|IAM|UEBA)\b',  # Security products
            "credential": r'\b(credential|password|token|key|access|authentication|authorization)\b',  # Credential terms
            "threat_actor": r'\b(threat actor|APT|campaign|malware|trojan|ransomware|backdoor)\b'  # Threat actor terms
        }
        
        # Exabeam-specific terminology for metadata extraction
        self.exabeam_terms = {
            "product": ["Advanced Analytics", "Data Lake", "Case Management", "Cloud Security", "Entity Analytics", "Threat Hunter"],
            "component": ["Data Sources", "Parsers", "Use Cases", "Rules", "Models", "Content"],
            "event_types": ["Authentication", "Network", "Process", "File", "Registry", "Database", "Email", "DLP", "IAM"]
        }
    
    def _analyze_content_density(self, text: str) -> float:
        """Analyze information density of text segment.
        
        Args:
            text: Text segment to analyze
            
        Returns:
            Density score (0-1) where higher means more information-dense
        """
        if not text or not self.nlp:
            return 0.5  # Default medium density
        
        # Tokenize text
        tokens = self.nlp.word_tokenize(text)
        if not tokens:
            return 0.5
        
        # Calculate metrics
        sentence_count = len(self.nlp.sent_tokenize(text))
        token_count = len(tokens)
        if sentence_count == 0:
            return 0.5
            
        avg_sentence_length = token_count / sentence_count
        
        # Count entities as a proxy for information density
        try:
            pos_tags = self.nlp.pos_tag(tokens)
            entities = self.nlp.ne_chunk(pos_tags)
            entity_count = sum(1 for chunk in entities if hasattr(chunk, 'label'))
        except Exception:
            entity_count = 0
            
        # Count security and exabeam-specific terms
        security_term_count = 0
        for pattern in self.security_entity_patterns.values():
            security_term_count += len(re.findall(pattern, text, re.IGNORECASE))
            
        # Count structured content markers
        structured_count = 0
        for pattern in self.content_type_patterns.values():
            structured_count += len(re.findall(pattern, text))
        
        # Combine factors to calculate density
        weighted_score = (
            0.3 * min(1.0, avg_sentence_length / 20)  # Sentence complexity
            + 0.3 * min(1.0, entity_count / max(1, sentence_count))  # Entity density
            + 0.2 * min(1.0, security_term_count / max(1, token_count / 10))  # Security relevance
            + 0.2 * min(1.0, structured_count / max(1, sentence_count))  # Structured content
        )
        
        return min(1.0, max(0.1, weighted_score))
    
    def _find_semantic_boundaries(self, text: str) -> List[int]:
        """Find natural semantic boundaries in text.
        
        Args:
            text: Text to analyze for boundaries
            
        Returns:
            List of character indices representing optimal split points
        """
        if not text or not self.nlp:
            return []  # No boundaries in empty text
            
        boundaries = []
        
        # Split text into sentences
        try:
            sentences = self.nlp.sent_tokenize(text)
        except Exception:
            # Fallback to simple splits if NLTK fails
            sentences = re.split(r'(?<=[.!?])\s+', text)
        
        if not sentences:
            return []
        
        # Track the character index as we process sentences
        char_index = 0
        
        # First, add explicit section headings as definite boundaries
        lines = text.split('\n')
        line_start_indices = [0]
        current_index = 0
        
        # Calculate the starting character index of each line
        for line in lines[:-1]:
            current_index += len(line) + 1  # +1 for the newline character
            line_start_indices.append(current_index)
        
        # Find section heading boundaries
        for i, line in enumerate(lines):
            for pattern, level in self.section_patterns:
                if re.match(pattern, line, re.MULTILINE):
                    # Add the start of this line as a boundary
                    boundaries.append(line_start_indices[i])
                    break
        
        # Now add sentence boundaries in dense areas
        char_index = 0
        for i, sentence in enumerate(sentences):
            sentence_start = text.find(sentence, char_index)
            if sentence_start == -1:  # Skip if we can't find the exact position
                char_index += len(sentence)
                continue
                
            char_index = sentence_start + len(sentence)
            
            # Skip adding boundaries for headings (already added)
            if any(re.match(pattern[0], sentence) for pattern in self.section_patterns):
                continue
                
            # Calculate local density around this sentence
            context_start = max(0, i - 2)
            context_end = min(len(sentences), i + 3)
            context = ' '.join(sentences[context_start:context_end])
            density = self._analyze_content_density(context)
            
            # Only add sentence boundaries in high-density areas or for long sentences
            if density > 0.7 or len(sentence) > 200:
                boundaries.append(char_index)
                
        # Sort and deduplicate boundaries
        boundaries = sorted(set(boundaries))
        
        return boundaries
    
    def _extract_content_features(self, text: str) -> Dict[str, Any]:
        """Extract content features for metadata enrichment.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of extracted features and entities
        """
        features = {
            "content_type": [],
            "entities": [],
            "security_entities": [],
            "exabeam_entities": [],
            "complexity": 0.0,
            "information_density": 0.0
        }
        
        # Detect content type
        for content_type, pattern in self.content_type_patterns.items():
            if re.search(pattern, text, re.MULTILINE | re.IGNORECASE):
                features["content_type"].append(content_type)
        
        # Extract security entities
        for entity_type, pattern in self.security_entity_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                for match in matches:
                    features["security_entities"].append({
                        "type": entity_type,
                        "value": match
                    })
        
        # Extract Exabeam-specific entities
        for category, terms in self.exabeam_terms.items():
            for term in terms:
                if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
                    features["exabeam_entities"].append({
                        "type": category,
                        "value": term
                    })
        
        # Calculate information density
        features["information_density"] = self._analyze_content_density(text)
        
        # Use NLTK for entity extraction if available
        if self.nlp:
            try:
                tokens = self.nlp.word_tokenize(text)
                pos_tags = self.nlp.pos_tag(tokens)
                named_entities = self.nlp.ne_chunk(pos_tags)
                
                for chunk in named_entities:
                    if hasattr(chunk, 'label'):
                        entity_text = ' '.join(c[0] for c in chunk)
                        features["entities"].append({
                            "type": chunk.label(),
                            "value": entity_text
                        })
            except Exception as e:
                logger.debug(f"Error in NLTK entity extraction: {str(e)}")
        
        return features
    
    def chunk_document(self, document: Document) -> List[Document]:
        """Split document into semantically meaningful chunks with rich metadata.
        
        Args:
            document: Document to split into chunks
            
        Returns:
            List of semantically meaningful document chunks with enhanced metadata
        """
        if not document.page_content.strip():
            return []  # Skip empty documents
            
        text = document.page_content
        base_metadata = document.metadata.copy()
        doc_type = base_metadata.get("doc_type", "")
        
        # Use different chunking strategies based on document type
        if doc_type == "parser" or "parser" in base_metadata.get("content_type", ""):
            return self._chunk_parser_document(document)
        elif doc_type == "use_case" or "use_case" in base_metadata.get("content_type", ""):
            return self._chunk_use_case_document(document)
        elif doc_type == "data_source" or "data_source" in base_metadata.get("content_type", ""):
            return self._chunk_data_source_document(document)
        else:
            # Default to semantic chunking
            return self._chunk_by_semantic_boundaries(document)
    
    def _adjust_chunk_size(self, text: str) -> Tuple[int, int]:
        """Adaptively adjust chunk size based on content complexity.
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (chunk_size, chunk_overlap)
        """
        # Analyze content density
        density = self._analyze_content_density(text)
        
        # Adjust chunk size based on density
        # More dense content gets smaller chunks to ensure each chunk has coherent information
        # Less dense content gets larger chunks to ensure enough context
        adjusted_size = int(self.max_chunk_size - (density * (self.max_chunk_size - self.min_chunk_size)))
        
        # Also adjust overlap based on density
        # More dense content gets more overlap to maintain context between chunks
        adjusted_overlap = int(self.chunk_overlap + (density * self.chunk_overlap))
        
        return adjusted_size, adjusted_overlap
    
    def _chunk_by_semantic_boundaries(self, document: Document) -> List[Document]:
        """Chunk document using semantic boundary detection.
        
        Args:
            document: Document to chunk
            
        Returns:
            List of document chunks
        """
        text = document.page_content
        base_metadata = document.metadata.copy()
        
        # Find semantic boundaries
        boundaries = self._find_semantic_boundaries(text)
        
        # If no semantic boundaries found, fall back to adjusted size chunking
        if not boundaries:
            chunk_size, chunk_overlap = self._adjust_chunk_size(text)
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            chunks = splitter.split_text(text)
            
            result_docs = []
            for i, chunk in enumerate(chunks):
                chunk_metadata = base_metadata.copy()
                chunk_metadata["chunk_index"] = i
                chunk_metadata["chunk_id"] = f"{base_metadata.get('id', 'doc')}_chunk_{i}"
                
                # Extract content features
                content_features = self._extract_content_features(chunk)
                for key, value in content_features.items():
                    chunk_metadata[key] = value
                
                result_docs.append(Document(
                    page_content=chunk,
                    metadata=chunk_metadata
                ))
                
            return result_docs
        
        # Use the boundaries to create chunks
        chunks = []
        for i in range(len(boundaries)):
            start = boundaries[i]
            end = boundaries[i+1] if i < len(boundaries) - 1 else len(text)
            
            # Only create chunks for non-empty segments
            segment = text[start:end].strip()
            if segment:
                chunks.append(segment)
                
        # Post-process chunks to ensure they meet size constraints
        final_chunks = []
        current_chunk = ""
        
        for chunk in chunks:
            # If adding this chunk would exceed max size, finalize current chunk
            if current_chunk and len(current_chunk) + len(chunk) > self.max_chunk_size:
                final_chunks.append(current_chunk)
                current_chunk = chunk
            else:
                # Add to current chunk with a separator if needed
                if current_chunk:
                    current_chunk += "\n\n" + chunk
                else:
                    current_chunk = chunk
        
        # Add the last chunk if non-empty
        if current_chunk:
            final_chunks.append(current_chunk)
            
        # Create documents from chunks with enhanced metadata
        result_docs = []
        for i, chunk in enumerate(final_chunks):
            chunk_metadata = base_metadata.copy()
            chunk_metadata["chunk_index"] = i
            chunk_metadata["chunk_id"] = f"{base_metadata.get('id', 'doc')}_chunk_{i}"
            
            # Extract content features
            content_features = self._extract_content_features(chunk)
            for key, value in content_features.items():
                chunk_metadata[key] = value
            
            result_docs.append(Document(
                page_content=chunk,
                metadata=chunk_metadata
            ))
            
        return result_docs
    
    def _chunk_parser_document(self, document: Document) -> List[Document]:
        """Chunk parser document with awareness of parser structure.
        
        Args:
            document: Parser document to chunk
            
        Returns:
            List of document chunks
        """
        text = document.page_content
        base_metadata = document.metadata.copy()
        
        # Parsers should generally be kept intact if possible
        # Check if document is small enough to keep as a single chunk
        if len(text) <= self.max_chunk_size:
            # Extract content features
            content_features = self._extract_content_features(text)
            enhanced_metadata = base_metadata.copy()
            for key, value in content_features.items():
                enhanced_metadata[key] = value
                
            return [Document(
                page_content=text,
                metadata=enhanced_metadata
            )]
            
        # If parser document is too long, split by sections
        # but try to keep code blocks and parser definitions intact
        lines = text.split('\n')
        sections = []
        current_section = []
        in_code_block = False
        
        for line in lines:
            # Toggle code block state
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                current_section.append(line)
                continue
                
            # If we're in a code block, don't split
            if in_code_block:
                current_section.append(line)
                continue
                
            # Check for section headers
            is_header = False
            for pattern, _ in self.section_patterns:
                if re.match(pattern, line):
                    is_header = True
                    # If we already have content, finalize the current section
                    if current_section:
                        sections.append('\n'.join(current_section))
                        current_section = []
                    break
                    
            current_section.append(line)
            
        # Add the last section if it exists
        if current_section:
            sections.append('\n'.join(current_section))
            
        # Further process sections if they're too large
        result_docs = []
        for i, section in enumerate(sections):
            if len(section) <= self.max_chunk_size:
                section_metadata = base_metadata.copy()
                section_metadata["chunk_index"] = i
                section_metadata["chunk_id"] = f"{base_metadata.get('id', 'doc')}_section_{i}"
                
                # Extract content features
                content_features = self._extract_content_features(section)
                for key, value in content_features.items():
                    section_metadata[key] = value
                    
                result_docs.append(Document(
                    page_content=section,
                    metadata=section_metadata
                ))
            else:
                # If a section is too large, use semantic chunking
                section_doc = Document(
                    page_content=section,
                    metadata=base_metadata.copy()
                )
                section_doc.metadata["section_index"] = i
                
                # Use semantic boundaries for further splitting
                sub_chunks = self._chunk_by_semantic_boundaries(section_doc)
                
                # Update metadata to reflect the section
                for j, chunk in enumerate(sub_chunks):
                    chunk.metadata["chunk_id"] = f"{base_metadata.get('id', 'doc')}_section_{i}_chunk_{j}"
                    
                result_docs.extend(sub_chunks)
                
        return result_docs
    
    def _chunk_use_case_document(self, document: Document) -> List[Document]:
        """Chunk use case document with awareness of use case structure.
        
        Args:
            document: Use case document to chunk
            
        Returns:
            List of document chunks
        """
        text = document.page_content
        base_metadata = document.metadata.copy()
        
        # Use cases often have sections for different vendors/products
        # Split mainly by section headers with enhanced metadata
        sections = []
        current_lines = []
        current_header = ""
        current_level = 0
        section_headers = []
        
        lines = text.split('\n')
        
        for line in lines:
            header_match = False
            header_level = 0
            header_text = ""
            
            # Check if this line is a header
            for pattern, level in self.section_patterns:
                match = re.match(pattern, line)
                if match:
                    header_match = True
                    header_level = level
                    if level == 1 or level == 2:  # Major sections
                        header_text = match.group(1).strip()
                    break
            
            if header_match and header_level <= 2:  # Major section header
                # Save the current section if it exists
                if current_lines:
                    section_text = '\n'.join(current_lines)
                    sections.append({
                        "text": section_text,
                        "header": current_header,
                        "level": current_level,
                        "path": list(section_headers)  # Copy the current path
                    })
                
                # Update the section headers path
                if header_level == 1:  # Top-level reset
                    section_headers = [header_text]
                else:
                    # If going to a higher level, pop headers
                    while len(section_headers) >= header_level:
                        section_headers.pop()
                    section_headers.append(header_text)
                
                # Start a new section
                current_lines = [line]
                current_header = header_text
                current_level = header_level
            else:
                current_lines.append(line)
        
        # Add the last section
        if current_lines:
            section_text = '\n'.join(current_lines)
            sections.append({
                "text": section_text,
                "header": current_header,
                "level": current_level,
                "path": list(section_headers)
            })
        
        # Create documents from sections with rich metadata
        result_docs = []
        for i, section in enumerate(sections):
            section_text = section["text"]
            
            # Skip empty sections
            if not section_text.strip():
                continue
                
            section_metadata = base_metadata.copy()
            section_metadata["chunk_index"] = i
            section_metadata["chunk_id"] = f"{base_metadata.get('id', 'doc')}_section_{i}"
            section_metadata["section_header"] = section["header"]
            section_metadata["section_level"] = section["level"]
            section_metadata["section_path"] = "/".join(section["path"])
            
            # Try to extract vendor and product information from headers
            if section["path"]:  # If we have path information
                for path_component in section["path"]:
                    # Check if this might be a vendor
                    if not section_metadata.get("vendor") and any(vendor.lower() in path_component.lower() 
                                                              for vendor in ["Microsoft", "Cisco", "AWS", "Google", "IBM"]):
                        section_metadata["vendor"] = path_component
                        
                    # Check if this might be an Exabeam product
                    for product in self.exabeam_terms["product"]:
                        if product.lower() in path_component.lower():
                            section_metadata["product"] = product
                            break
            
            # Extract content features for rich metadata
            content_features = self._extract_content_features(section_text)
            for key, value in content_features.items():
                section_metadata[key] = value
            
            # If section is too large, further split using semantic boundaries
            if len(section_text) > self.max_chunk_size:
                section_doc = Document(
                    page_content=section_text,
                    metadata=section_metadata
                )
                
                sub_chunks = self._chunk_by_semantic_boundaries(section_doc)
                result_docs.extend(sub_chunks)
            else:
                result_docs.append(Document(
                    page_content=section_text,
                    metadata=section_metadata
                ))
                
        return result_docs
    
    def _chunk_data_source_document(self, document: Document) -> List[Document]:
        """Chunk data source document with awareness of data source structure.
        
        Args:
            document: Data source document to chunk
            
        Returns:
            List of document chunks
        """
        text = document.page_content
        base_metadata = document.metadata.copy()
        
        # Check that this is indeed a data source document (safety check)
        is_data_source = False
        if "data_source" in base_metadata.get("doc_type", "").lower():
            is_data_source = True
        if "ds_" in base_metadata.get("file_name", "").lower():
            is_data_source = True
        if "vendor:" in text.lower() or "product:" in text.lower():
            is_data_source = True
            
        if not is_data_source:
            logger.warning("Document might not be a data source. Using semantic boundary chunking.")
            return self._chunk_by_semantic_boundaries(document)
            
        # Some data source documents are just table-based references
        # If the document is mostly tables, use a simpler chunking approach
        table_lines = len(re.findall(r'^\|.*\|$', text, re.MULTILINE))
        total_lines = len(text.split('\n'))
        
        if table_lines > 0 and table_lines / total_lines > 0.3:  # If >30% of lines are table lines
            logger.info("Data source document is table-heavy. Using table-aware chunking.")
            return self._chunk_table_heavy_document(document)
        
        # Handle special case for very small documents (first fallback)
        if len(text) <= self.max_chunk_size:
            # Extract content features
            content_features = self._extract_content_features(text)
            enhanced_metadata = base_metadata.copy()
            enhanced_metadata["content_type"] = "data_source"
            for key, value in content_features.items():
                enhanced_metadata[key] = value
                
            return [Document(
                page_content=text,
                metadata=enhanced_metadata
            )]
        
        # Try section-based chunking first
        chunk_results = self._chunk_data_source_by_sections(document)
        
        # If section-based chunking failed, fall back to fixed-size chunking
        if not chunk_results:
            logger.warning("Section-based chunking failed. Using fixed-size chunking.")
            return self._chunk_data_source_fixed_size(document)
            
        return chunk_results
        
    def _chunk_data_source_by_sections(self, document: Document) -> List[Document]:
        """Chunk data source document by sections (helper method).
        
        Args:
            document: Data source document
            
        Returns:
            List of document chunks
        """
        text = document.page_content
        base_metadata = document.metadata.copy()
        
        # Initial metadata extraction to enrich all chunks
        base_features = self._extract_content_features(text)
        
        # Data source documents often have sections for configuration, event types, etc.
        sections = []
        current_lines = []
        current_header = ""
        current_level = 0
        section_headers = []
        
        lines = text.split('\n')
        
        # Look for vendor/product pattern at the beginning
        vendor = ""
        product = ""
        
        if len(lines) > 3:
            vendor_match = re.match(r'^vendor:\s*(.+?)$', lines[0], re.IGNORECASE)
            if vendor_match:
                vendor = vendor_match.group(1).strip()
                
            product_match = re.match(r'^product:\s*(.+?)$', lines[2], re.IGNORECASE)
            if product_match:
                product = product_match.group(1).strip()
                
        if vendor:
            base_metadata["vendor"] = vendor
        if product:
            base_metadata["product"] = product
            
        # Special handling for markdown tables which are common in data source documents
        in_table = False
        table_buffer = []
        
        for line in lines:
            # Check for table markers
            if re.match(r'^\|.*\|$', line) and ('--' in line or ':--' in line or '--:' in line):
                in_table = True
                if table_buffer:
                    table_buffer.append(line)
                else:
                    # This is a new table, add the previous line which should be the header
                    if current_lines and re.match(r'^\|.*\|$', current_lines[-1]):
                        table_buffer.append(current_lines.pop())
                        table_buffer.append(line)
                continue
                
            if in_table:
                if re.match(r'^\|.*\|$', line):
                    table_buffer.append(line)
                    continue
                else:
                    # Table has ended
                    in_table = False
                    if table_buffer:
                        current_lines.extend(table_buffer)
                        table_buffer = []
            
            header_match = False
            header_level = 0
            header_text = ""
            
            # Check if this line is a header
            for pattern, level in self.section_patterns:
                match = re.match(pattern, line)
                if match:
                    header_match = True
                    header_level = level
                    header_text = match.group(1).strip()
                    break
            
            # Also check for underlined headers (===== or -----)
            if not header_match and len(current_lines) > 0:
                if re.match(r'^=+$', line.strip()):
                    header_match = True
                    header_level = 1
                    header_text = current_lines[-1].strip()
                    current_lines.pop()  # Remove the header line as we'll add it with the header text
                elif re.match(r'^-+$', line.strip()):
                    header_match = True
                    header_level = 2
                    header_text = current_lines[-1].strip()
                    current_lines.pop()  # Remove the header line as we'll add it with the header text
            
            if header_match:  # Any header level for data sources
                # Save the current section if it exists
                if current_lines:
                    section_text = '\n'.join(current_lines)
                    sections.append({
                        "text": section_text,
                        "header": current_header,
                        "level": current_level,
                        "path": list(section_headers)  # Copy the current path
                    })
                
                # Update the section headers path
                if header_level == 1:  # Top-level reset
                    section_headers = [header_text]
                elif header_level <= len(section_headers):
                    # If going to a higher level, pop headers
                    while len(section_headers) >= header_level:
                        if section_headers:  # Ensure list is not empty before popping
                            section_headers.pop()
                        else:
                            break
                    section_headers.append(header_text)
                else:
                    section_headers.append(header_text)
                
                # Start a new section
                current_lines = []
                if header_level == 1:
                    current_lines.append(f"# {header_text}")
                elif header_level == 2:
                    current_lines.append(f"## {header_text}")
                else:
                    current_lines.append(f"{'#' * header_level} {header_text}")
                    
                current_header = header_text
                current_level = header_level
            else:
                current_lines.append(line)
        
        # Add any remaining table lines
        if table_buffer:
            current_lines.extend(table_buffer)
        
        # Add the last section
        if current_lines:
            section_text = '\n'.join(current_lines)
            sections.append({
                "text": section_text,
                "header": current_header,
                "level": current_level,
                "path": list(section_headers) if section_headers else []  # Ensure we don't pass None
            })
        
        # If no clear sections were found, handle as a special case
        if len(sections) <= 1 and not sections[0]["header"]:
            logger.info("No clear sections found in data source document. Using alternate chunking.")
            return self._chunk_data_source_fixed_size(document)
        
        # Process the sections into chunks
        result_docs = []
        for i, section in enumerate(sections):
            section_text = section["text"]
            
            # Skip truly empty sections
            if not section_text.strip():
                continue
                
            section_metadata = base_metadata.copy()
            section_metadata["chunk_index"] = i
            section_metadata["chunk_id"] = f"{base_metadata.get('id', 'doc')}_section_{i}"
            section_metadata["section_header"] = section["header"]
            section_metadata["section_level"] = section["level"]
            section_metadata["content_type"] = "data_source"
            
            # Add base features to metadata
            for key, value in base_features.items():
                if key not in section_metadata:
                    section_metadata[key] = value
            
            # Safely join path with fallback to empty string
            if section["path"]:
                section_metadata["section_path"] = "/".join(section["path"])
            else:
                section_metadata["section_path"] = ""
            
            # Look for event types and parser information in headers and content
            if section["header"]:
                header_lower = section["header"].lower()
                if "event" in header_lower or "type" in header_lower:
                    section_metadata["content_type"] = "event_type"
                elif "parser" in header_lower or "parsing" in header_lower:
                    section_metadata["content_type"] = "parser"
                elif "configuration" in header_lower or "setup" in header_lower:
                    section_metadata["content_type"] = "configuration"
                elif "vendor" in header_lower or "product" in header_lower:
                    section_metadata["content_type"] = "metadata"
                elif "mitre" in header_lower or "att&ck" in header_lower:
                    section_metadata["content_type"] = "mitre"
            
            # Extract content features for rich metadata
            content_features = self._extract_content_features(section_text)
            for key, value in content_features.items():
                # Don't overwrite content_type if already determined from header
                if key != "content_type" or "content_type" not in section_metadata:
                    section_metadata[key] = value
            
            # If section is too large, further split using semantic boundaries
            if len(section_text) > self.max_chunk_size:
                section_doc = Document(
                    page_content=section_text,
                    metadata=section_metadata
                )
                
                sub_chunks = self._chunk_by_semantic_boundaries(section_doc)
                result_docs.extend(sub_chunks)
            else:
                result_docs.append(Document(
                    page_content=section_text,
                    metadata=section_metadata
                ))
        
        return result_docs
    
    def _chunk_table_heavy_document(self, document: Document) -> List[Document]:
        """Handle chunking for table-heavy data source documents.
        
        Args:
            document: Data source document with many tables
            
        Returns:
            List of document chunks
        """
        text = document.page_content
        base_metadata = document.metadata.copy()
        base_metadata["content_type"] = "data_source"
        base_metadata["table_heavy"] = True
        
        # Extract content features for the whole document
        content_features = self._extract_content_features(text)
        for key, value in content_features.items():
            base_metadata[key] = value
            
        # Extract tables and their surrounding context
        table_chunks = []
        current_chunk_lines = []
        current_chunk_tables = 0
        in_table = False
        
        for line in text.split('\n'):
            # Detect table start/end
            if re.match(r'^\|.*\|$', line) and ('--' in line or ':--' in line or '--:' in line):
                in_table = True
                current_chunk_tables += 1
                
            current_chunk_lines.append(line)
            
            # If we're in a table and hit a non-table line, table ended
            if in_table and not re.match(r'^\|.*\|$', line) and not line.strip() == '':
                in_table = False
                
            # Create a new chunk if we've accumulated enough content
            # Either based on the number of tables or total line count
            if (current_chunk_tables >= 2 or len(current_chunk_lines) > 50) and not in_table:
                table_chunks.append('\n'.join(current_chunk_lines))
                current_chunk_lines = []
                current_chunk_tables = 0
                
        # Add any remaining content
        if current_chunk_lines:
            table_chunks.append('\n'.join(current_chunk_lines))
            
        # Create document chunks
        result_docs = []
        for i, chunk_text in enumerate(table_chunks):
            if not chunk_text.strip():
                continue
                
            chunk_metadata = base_metadata.copy()
            chunk_metadata["chunk_index"] = i
            chunk_metadata["chunk_id"] = f"{base_metadata.get('id', 'doc')}_table_chunk_{i}"
            
            # Extract specific features for this chunk
            chunk_features = self._extract_content_features(chunk_text)
            for key, value in chunk_features.items():
                if key != "content_type":  # Preserve the data_source type
                    chunk_metadata[key] = value
                    
            result_docs.append(Document(
                page_content=chunk_text,
                metadata=chunk_metadata
            ))
            
        return result_docs
    
    def _chunk_data_source_fixed_size(self, document: Document) -> List[Document]:
        """Chunk data source document using fixed size chunks as a fallback.
        
        Args:
            document: Data source document
            
        Returns:
            List of document chunks
        """
        text = document.page_content
        base_metadata = document.metadata.copy()
        base_metadata["content_type"] = "data_source"
        base_metadata["chunking_method"] = "fixed_size"
        
        # Extract content features for the whole document
        content_features = self._extract_content_features(text)
        for key, value in content_features.items():
            if key != "content_type":  # Preserve data_source type
                base_metadata[key] = value
                
        # Use a larger chunk size for data sources to preserve context
        chunk_size = min(2000, max(1000, len(text) // 3))
        chunk_overlap = min(300, chunk_size // 3)
        
        # Simple recursive character text splitter
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        # Split the text
        chunks = splitter.split_text(text)
        
        # Create document chunks
        result_docs = []
        for i, chunk_text in enumerate(chunks):
            if not chunk_text.strip():
                continue
                
            chunk_metadata = base_metadata.copy()
            chunk_metadata["chunk_index"] = i
            chunk_metadata["chunk_id"] = f"{base_metadata.get('id', 'doc')}_chunk_{i}"
            
            result_docs.append(Document(
                page_content=chunk_text,
                metadata=chunk_metadata
            ))
            
        return result_docs