"""Chunk quality evaluation metrics for EXASPERATION vectorization enhancement."""

import logging
import re
import string
from typing import List, Dict, Any, Optional, Tuple, Union
import nltk
from langchain.schema import Document
import numpy as np

logger = logging.getLogger(__name__)

class ChunkQualityEvaluator:
    """Evaluates semantic chunk quality for vectorization enhancement."""
    
    def __init__(self):
        """Initialize the chunk quality evaluator."""
        # Initialize NLP tools
        self.nlp = self._initialize_nlp()
        
        logger.info("Initialized ChunkQualityEvaluator")
    
    def _initialize_nlp(self):
        """Initialize NLP tools for text analysis."""
        try:
            # Download required NLTK resources if not already available
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('stopwords', quiet=True)
            return nltk
        except Exception as e:
            logger.warning(f"Error initializing NLP tools: {str(e)}. "
                         "Falling back to basic text analysis.")
            return None
    
    def evaluate_chunk(self, chunk: Document) -> Dict[str, float]:
        """Evaluate overall quality of a document chunk.
        
        Args:
            chunk: Document to evaluate
            
        Returns:
            Dictionary of quality metrics with scores
        """
        text = chunk.page_content
        
        # Skip empty chunks
        if not text.strip():
            return {
                "coherence": 0.0,
                "information_density": 0.0,
                "entity_preservation": 0.0,
                "context_completeness": 0.0,
                "overall_quality": 0.0
            }
        
        # Calculate individual metrics
        coherence = self.evaluate_coherence(text)
        information_density = self.evaluate_information_density(text)
        entity_preservation = self.evaluate_entity_preservation(chunk)
        context_completeness = self.evaluate_context_completeness(text)
        
        # Calculate overall quality score (weighted average)
        overall_quality = (
            0.35 * coherence +
            0.30 * information_density +
            0.20 * entity_preservation +
            0.15 * context_completeness
        )
        
        return {
            "coherence": round(coherence, 2),
            "information_density": round(information_density, 2),
            "entity_preservation": round(entity_preservation, 2),
            "context_completeness": round(context_completeness, 2),
            "overall_quality": round(overall_quality, 2)
        }
    
    def evaluate_coherence(self, text: str) -> float:
        """Evaluate semantic coherence of a chunk.
        
        Args:
            text: Text to evaluate
            
        Returns:
            Coherence score (0-1)
        """
        if not text or not self.nlp:
            return 0.5  # Default medium coherence
        
        try:
            # Split into sentences
            sentences = self.nlp.sent_tokenize(text)
            if len(sentences) <= 1:
                return 0.7  # Single sentence is coherent by definition
            
            # For coherence, we measure:
            # 1. Topic consistency (term overlap between sentences)
            # 2. Logical flow (proper beginning/ending, transition words)
            # 3. Structural integrity (e.g., not cutting in the middle of a list)
            
            # Calculate term overlap between adjacent sentences
            sentence_similarities = []
            for i in range(len(sentences) - 1):
                s1_tokens = set(self.nlp.word_tokenize(sentences[i].lower()))
                s2_tokens = set(self.nlp.word_tokenize(sentences[i + 1].lower()))
                
                # Remove stopwords and punctuation
                stopwords = set(self.nlp.corpus.stopwords.words('english')) if hasattr(self.nlp.corpus, 'stopwords') else set()
                s1_tokens = {t for t in s1_tokens if t not in stopwords and t not in string.punctuation}
                s2_tokens = {t for t in s2_tokens if t not in stopwords and t not in string.punctuation}
                
                # Calculate Jaccard similarity
                if s1_tokens and s2_tokens:
                    similarity = len(s1_tokens.intersection(s2_tokens)) / len(s1_tokens.union(s2_tokens))
                    sentence_similarities.append(similarity)
            
            # Average similarity between adjacent sentences
            avg_similarity = sum(sentence_similarities) / len(sentence_similarities) if sentence_similarities else 0.5
            
            # Check for structural issues
            structural_score = 1.0
            
            # Check if text starts mid-sentence (e.g., no capital letter, starts with conjunction)
            if text and not text[0].isupper() and text.split()[0].lower() in ["and", "but", "or", "so", "because", "however"]:
                structural_score -= 0.2
            
            # Check if text ends mid-sentence (e.g., no period at end)
            if text and not text.rstrip()[-1] in ['.', '!', '?', ':', ';']:
                structural_score -= 0.2
            
            # Check for broken lists or code blocks
            if text.count('```') % 2 != 0:  # Unclosed code block
                structural_score -= 0.3
                
            list_start_pattern = r'^\s*[-*+]\s+'  # List item pattern
            if re.search(list_start_pattern, text, re.MULTILINE) and text.count('\n- ') <= 1:
                # Likely a broken list (just one item)
                structural_score -= 0.2
                
            # Combine metrics
            coherence_score = (0.7 * avg_similarity + 0.3 * structural_score)
            
            return max(0.1, min(1.0, coherence_score))  # Ensure between 0.1 and 1.0
            
        except Exception as e:
            logger.debug(f"Error calculating coherence: {str(e)}")
            return 0.5  # Default medium coherence
    
    def evaluate_information_density(self, text: str) -> float:
        """Evaluate information density of a chunk.
        
        Args:
            text: Text to evaluate
            
        Returns:
            Information density score (0-1)
        """
        if not text or not self.nlp:
            return 0.5  # Default medium density
        
        try:
            # Tokenize text
            tokens = self.nlp.word_tokenize(text)
            if not tokens:
                return 0.5
            
            # Calculate metrics
            sentences = self.nlp.sent_tokenize(text)
            sentence_count = len(sentences)
            token_count = len(tokens)
            
            if sentence_count == 0:
                return 0.5
                
            avg_sentence_length = token_count / sentence_count
            
            # Get stopwords
            stopwords = set(self.nlp.corpus.stopwords.words('english')) if hasattr(self.nlp.corpus, 'stopwords') else set()
            
            # Count non-stopwords (content words)
            content_words = [t.lower() for t in tokens if t.lower() not in stopwords and t not in string.punctuation]
            content_word_ratio = len(content_words) / max(1, len(tokens))
            
            # Count unique words (lexical diversity)
            unique_words = len(set(t.lower() for t in tokens if t not in string.punctuation))
            lexical_diversity = unique_words / max(1, len(tokens))
            
            # Count named entities
            try:
                pos_tags = self.nlp.pos_tag(tokens)
                named_entities = self.nlp.ne_chunk(pos_tags)
                entity_count = sum(1 for chunk in named_entities if hasattr(chunk, 'label'))
                entity_density = entity_count / max(1, sentence_count)
            except Exception:
                entity_density = 0.0
            
            # Count technical/specialized terms
            tech_terms_pattern = r'\b(configuration|authentication|parser|technique|credential|protocol|encryption|registry|database|query|interface|endpoint|algorithm|parameter|method|function|class|object|module|server|client|api|sdk|framework)\b'
            tech_term_matches = re.findall(tech_terms_pattern, text, re.IGNORECASE)
            tech_term_density = len(tech_term_matches) / max(1, token_count)
            
            # Detect structured content
            structured_content_patterns = {
                "code": r'```[\s\S]*?```',
                "table": r'\|[^\n]*\|[^\n]*\n(\|[:\-]+\|[:\-]+[^\n]*\n)+',
                "list": r'(^\s*[-*+]\s+.+?$(\n^\s*[-*+]\s+.+?$)+)',
                "json": r'\{[\s\S]*?\}',
                "xml": r'<[\s\S]*?>[\s\S]*?</[\s\S]*?>'
            }
            
            structured_content_score = 0.0
            for pattern in structured_content_patterns.values():
                matches = re.findall(pattern, text, re.MULTILINE)
                structured_content_score += 0.1 * min(1.0, len(matches))
            
            # Combine all factors
            density_score = (
                0.25 * min(1.0, content_word_ratio * 1.5) +
                0.20 * min(1.0, lexical_diversity * 3.0) +
                0.20 * min(1.0, entity_density * 2.0) +
                0.15 * min(1.0, tech_term_density * 5.0) +
                0.20 * min(1.0, structured_content_score)
            )
            
            return max(0.1, min(1.0, density_score))  # Ensure between 0.1 and 1.0
            
        except Exception as e:
            logger.debug(f"Error calculating information density: {str(e)}")
            return 0.5  # Default medium density
    
    def evaluate_entity_preservation(self, chunk: Document) -> float:
        """Evaluate how well entities are preserved in chunks.
        
        Args:
            chunk: Document chunk to evaluate
            
        Returns:
            Entity preservation score (0-1)
        """
        if not chunk.page_content.strip():
            return 0.0
            
        # Check for extracted entities in metadata
        metadata = chunk.metadata
        entity_categories = [
            "extracted_products", 
            "extracted_data_sources", 
            "extracted_parsers",
            "extracted_use_cases",
            "extracted_mitre",
            "extracted_event_types",
            "extracted_fields"
        ]
        
        # Count how many entity types have been captured
        entity_types_found = sum(1 for category in entity_categories if category in metadata and metadata[category])
        
        # Calculate base score based on how many types of entities were captured
        base_score = min(1.0, entity_types_found / max(1, len(entity_categories)))
        
        # Count total entities across all categories
        total_entities = sum(
            len(metadata[category]) for category in entity_categories 
            if category in metadata and metadata[category]
        )
        
        # Bonus for relationships
        relationship_bonus = 0.0
        if "relationships" in metadata and metadata["relationships"]:
            relationship_count = len(metadata["relationships"])
            relationship_bonus = min(0.3, relationship_count * 0.1)
            
        # Text length factor (longer text should have more entities)
        text_length = len(chunk.page_content)
        length_factor = min(1.0, text_length / 1000)  # Normalize with 1000 chars as reference
        
        # Expected entity count based on length
        expected_entities = length_factor * 5  # Expected roughly 5 entities per 1000 chars
        entity_ratio = min(2.0, total_entities / max(1, expected_entities))
        
        # Calculate final score
        entity_score = (
            0.6 * base_score +
            0.3 * min(1.0, entity_ratio) +
            0.1 * relationship_bonus
        )
        
        return max(0.1, min(1.0, entity_score))  # Ensure between 0.1 and 1.0
    
    def evaluate_context_completeness(self, text: str) -> float:
        """Evaluate how complete the context is within the chunk.
        
        Args:
            text: Text to evaluate
            
        Returns:
            Context completeness score (0-1)
        """
        if not text:
            return 0.0
            
        # Detect section boundaries
        section_patterns = [
            r'^\s*#\s+(.+?)$',      # Level 1 header
            r'^\s*##\s+(.+?)$',     # Level 2 header
            r'^\s*###\s+(.+?)$',    # Level 3 header
            r'^\s*####\s+(.+?)$'    # Level 4 header
        ]
        
        # Check if chunk contains complete sections
        headers = []
        lines = text.split('\n')
        for line in lines:
            for pattern in section_patterns:
                if re.match(pattern, line, re.MULTILINE):
                    headers.append(line)
                    break
        
        # Complete section score (having headers is good)
        section_score = min(1.0, len(headers) * 0.3) if headers else 0.3
        
        # Check for hanging headers (headers at the end with little content)
        hanging_header_penalty = 0.0
        if headers:
            last_header_pos = max(text.rfind(h) for h in headers)
            text_after_last_header = text[last_header_pos:]
            if len(text_after_last_header) < 100:  # Minimal content after header
                hanging_header_penalty = 0.2
        
        # Content integrity checks
        integrity_score = 1.0
        
        # Check for broken code blocks
        if text.count('```') % 2 != 0:
            integrity_score -= 0.3
        
        # Check for broken lists
        list_items = re.findall(r'^\s*[-*+]\s+.+?$', text, re.MULTILINE)
        if list_items and len(list_items) == 1:
            # Single list item might indicate a broken list
            integrity_score -= 0.2
        
        # Check for broken tables
        table_pattern = r'\|[^\n]*\|'
        table_rows = re.findall(table_pattern, text, re.MULTILINE)
        if 1 < len(table_rows) < 3:
            # Likely a broken table (header only or just one data row)
            integrity_score -= 0.3
            
        # Check for broken sentences
        if text and not text.rstrip()[-1] in ['.', '!', '?', ':', ';']:
            integrity_score -= 0.2
        
        # Calculate final score
        completeness_score = (
            0.5 * section_score +
            0.5 * integrity_score
        ) - hanging_header_penalty
        
        return max(0.1, min(1.0, completeness_score))  # Ensure between 0.1 and 1.0
    
    def evaluate_chunk_set(self, chunks: List[Document]) -> Dict[str, Any]:
        """Evaluate the quality of a set of chunks as a whole.
        
        Args:
            chunks: List of document chunks to evaluate
            
        Returns:
            Dictionary of quality metrics for the entire set
        """
        if not chunks:
            return {
                "average_quality": 0.0,
                "quality_distribution": {},
                "chunk_count": 0,
                "chunk_qualities": []
            }
        
        # Evaluate each chunk
        chunk_qualities = [self.evaluate_chunk(chunk) for chunk in chunks]
        
        # Calculate average metrics
        avg_quality = sum(q["overall_quality"] for q in chunk_qualities) / len(chunk_qualities)
        avg_coherence = sum(q["coherence"] for q in chunk_qualities) / len(chunk_qualities)
        avg_density = sum(q["information_density"] for q in chunk_qualities) / len(chunk_qualities)
        avg_entities = sum(q["entity_preservation"] for q in chunk_qualities) / len(chunk_qualities)
        avg_context = sum(q["context_completeness"] for q in chunk_qualities) / len(chunk_qualities)
        
        # Calculate quality distribution
        quality_ranges = {
            "excellent": 0,
            "good": 0,
            "average": 0,
            "poor": 0,
            "bad": 0
        }
        
        for q in chunk_qualities:
            if q["overall_quality"] >= 0.8:
                quality_ranges["excellent"] += 1
            elif q["overall_quality"] >= 0.6:
                quality_ranges["good"] += 1
            elif q["overall_quality"] >= 0.4:
                quality_ranges["average"] += 1
            elif q["overall_quality"] >= 0.2:
                quality_ranges["poor"] += 1
            else:
                quality_ranges["bad"] += 1
        
        # Convert to percentages
        for key in quality_ranges:
            quality_ranges[key] = round(quality_ranges[key] / len(chunk_qualities) * 100, 1)
        
        return {
            "average_quality": round(avg_quality, 2),
            "average_coherence": round(avg_coherence, 2),
            "average_information_density": round(avg_density, 2),
            "average_entity_preservation": round(avg_entities, 2),
            "average_context_completeness": round(avg_context, 2),
            "quality_distribution": quality_ranges,
            "chunk_count": len(chunks),
            "chunk_qualities": chunk_qualities
        }
    
    def compare_chunking_strategies(self, 
                                   original_doc: Document, 
                                   strategy1_chunks: List[Document], 
                                   strategy2_chunks: List[Document]) -> Dict[str, Any]:
        """Compare the quality of two different chunking strategies.
        
        Args:
            original_doc: Original document before chunking
            strategy1_chunks: Chunks from first chunking strategy
            strategy2_chunks: Chunks from second chunking strategy
            
        Returns:
            Dictionary comparing the quality metrics of both strategies
        """
        if not strategy1_chunks or not strategy2_chunks:
            return {
                "comparison": "Invalid - one or both strategies produced no chunks"
            }
        
        # Evaluate both strategies
        strategy1_evaluation = self.evaluate_chunk_set(strategy1_chunks)
        strategy2_evaluation = self.evaluate_chunk_set(strategy2_chunks)
        
        # Calculate relative metrics
        metrics = ["average_quality", "average_coherence", "average_information_density", 
                 "average_entity_preservation", "average_context_completeness"]
        
        comparison = {}
        for metric in metrics:
            if metric in strategy1_evaluation and metric in strategy2_evaluation:
                strategy1_value = strategy1_evaluation[metric]
                strategy2_value = strategy2_evaluation[metric]
                
                # Calculate difference
                difference = strategy2_value - strategy1_value
                percentage_diff = difference / max(0.01, strategy1_value) * 100
                
                comparison[metric] = {
                    "strategy1": strategy1_value,
                    "strategy2": strategy2_value,
                    "difference": round(difference, 2),
                    "percentage_difference": round(percentage_diff, 1),
                    "better_strategy": "strategy2" if difference > 0 else "strategy1" if difference < 0 else "equal"
                }
        
        # Overall comparison
        strategy1_quality = strategy1_evaluation["average_quality"]
        strategy2_quality = strategy2_evaluation["average_quality"]
        
        overall_winner = "strategy2" if strategy2_quality > strategy1_quality else "strategy1" if strategy1_quality > strategy2_quality else "equal"
        
        return {
            "strategy1_chunks": len(strategy1_chunks),
            "strategy2_chunks": len(strategy2_chunks),
            "metrics_comparison": comparison,
            "overall_better_strategy": overall_winner,
            "strategy1_evaluation": strategy1_evaluation,
            "strategy2_evaluation": strategy2_evaluation
        }