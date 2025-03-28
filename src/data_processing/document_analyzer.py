"""Advanced document analysis for Exabeam documentation."""

import logging
import re
from typing import List, Dict, Any, Optional, Tuple, Union
from collections import defaultdict
import nltk
from langchain.schema import Document

logger = logging.getLogger(__name__)

class DocumentAnalyzer:
    """Performs advanced analysis of documents to extract entities and relationships."""
    
    def __init__(self):
        """Initialize the document analyzer."""
        # Initialize NLP tools
        self.nlp = self._initialize_nlp()
        
        # Define patterns for security and Exabeam entities
        self._init_entity_patterns()
        
        logger.info("Initialized DocumentAnalyzer")
    
    def _initialize_nlp(self):
        """Initialize NLP tools for entity extraction."""
        try:
            # Download required NLTK resources if not already available
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('maxent_ne_chunker', quiet=True)
            nltk.download('words', quiet=True)
            return nltk
        except Exception as e:
            logger.warning(f"Error initializing NLP tools: {str(e)}. "
                         "Falling back to regex-based analysis.")
            return None
    
    def _init_entity_patterns(self):
        """Initialize patterns for identifying security and Exabeam entities."""
        # Exabeam product patterns
        self.product_patterns = [
            r'\b(Advanced Analytics|Data Lake|Case Management|Cloud Security|Threat Hunter|Entity Analytics)\b'
        ]
        
        # Data source patterns
        self.data_source_patterns = [
            r'\b(Windows|Linux|Unix|MacOS|Cisco|Palo Alto|Fortinet|CheckPoint|Juniper|AWS|Azure|GCP)\b',
            r'\b([\w\-]+) (logs|events|data source)\b',
            r'\b(firewall|router|switch|IDS|IPS|WAF|EDR|endpoint|authentication|directory|database)\b'
        ]
        
        # Parser patterns
        self.parser_patterns = [
            r'\bparser(s)?\b',
            r'\bpars(e|ing)\b',
            r'\bextract(s|ing|ion)?\b',
            r'\bformat(s|ting)?\b'
        ]
        
        # Use case patterns
        self.use_case_patterns = [
            r'\buse case(s)?\b',
            r'\bscenario(s)?\b',
            r'\bdetect(s|ing|ion)?\b',
            r'\balert(s|ing)?\b',
            r'\bmonitoring\b',
            r'\brule trigger(s|ing)?\b'
        ]
        
        # MITRE ATT&CK patterns
        self.mitre_patterns = [
            r'\b(T\d{4}(?:\.\d{1,3})?)\b',  # Technique IDs
            r'\b(Initial Access|Execution|Persistence|Privilege Escalation|Defense Evasion|Credential Access|Discovery|Lateral Movement|Collection|Command and Control|Exfiltration|Impact)\b'  # Tactics
        ]
        
        # Event type patterns
        self.event_type_patterns = [
            r'\bevent type(s)?\b',
            r'\bevent(s)?\b',
            r'\blog(s)?\b',
            r'\balert(s)?\b',
            r'\b(authentication|network|process|file|registry|database|email|dlp|iam)\b'
        ]
        
        # Field patterns
        self.field_patterns = [
            r'\bfield(s)?\b',
            r'\battribute(s)?\b',
            r'\bproperty|properties\b',
            r'\bparameter(s)?\b',
            r'\bvariable(s)?\b'
        ]
    
    def extract_entities(self, text: str) -> Dict[str, List[Dict[str, str]]]:
        """Extract named entities from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of entity types with lists of extracted entities
        """
        entities = {
            "products": [],
            "data_sources": [],
            "parsers": [],
            "use_cases": [],
            "mitre": [],
            "event_types": [],
            "fields": []
        }
        
        # Extract NLTK entities if available
        if self.nlp:
            try:
                tokens = self.nlp.word_tokenize(text)
                pos_tags = self.nlp.pos_tag(tokens)
                nltk_entities = self.nlp.ne_chunk(pos_tags)
                
                for chunk in nltk_entities:
                    if hasattr(chunk, 'label'):
                        entity_text = ' '.join(c[0] for c in chunk)
                        if chunk.label() == 'ORGANIZATION':
                            # Check if it's an Exabeam product
                            for pattern in self.product_patterns:
                                if re.search(pattern, entity_text, re.IGNORECASE):
                                    entities["products"].append({
                                        "name": entity_text,
                                        "type": "Exabeam product"
                                    })
                                    break
                        elif chunk.label() == 'GPE' or chunk.label() == 'ORGANIZATION':
                            # Check if it's a data source vendor
                            for pattern in self.data_source_patterns:
                                if re.search(pattern, entity_text, re.IGNORECASE):
                                    entities["data_sources"].append({
                                        "name": entity_text,
                                        "type": "vendor"
                                    })
                                    break
            except Exception as e:
                logger.debug(f"Error in NLTK entity extraction: {str(e)}")
        
        # Extract entities using regex patterns
        # Products
        for pattern in self.product_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities["products"].append({
                    "name": match.group(0),
                    "type": "Exabeam product"
                })
        
        # Data sources
        for pattern in self.data_source_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities["data_sources"].append({
                    "name": match.group(0),
                    "type": "data source"
                })
        
        # Parsers
        parser_context = []
        for pattern in self.parser_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                # Get surrounding context for parser references
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                # Look for parser names in context
                parser_name_match = re.search(r'\b([A-Za-z0-9_\-]+) parser\b', context, re.IGNORECASE)
                if parser_name_match:
                    entities["parsers"].append({
                        "name": parser_name_match.group(1),
                        "type": "parser"
                    })
                else:
                    parser_context.append(context)
        
        # Use cases
        for pattern in self.use_case_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                # Get surrounding context for use case references
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                # Look for use case names in context
                use_case_match = re.search(r'\b([A-Za-z0-9_\- ]+) use case\b', context, re.IGNORECASE)
                if use_case_match:
                    entities["use_cases"].append({
                        "name": use_case_match.group(1),
                        "type": "use case"
                    })
        
        # MITRE ATT&CK
        for pattern in self.mitre_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                # Check if it's a technique ID or tactic
                if re.match(r'T\d{4}', match.group(0)):
                    entity_type = "technique"
                else:
                    entity_type = "tactic"
                    
                entities["mitre"].append({
                    "name": match.group(0),
                    "type": entity_type
                })
        
        # Event types
        for pattern in self.event_type_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                # Only add actual event types, not just mentions of the word "event"
                if not re.match(r'\bevent(s)?\b', match.group(0), re.IGNORECASE) or "type" in match.group(0).lower():
                    entities["event_types"].append({
                        "name": match.group(0),
                        "type": "event type"
                    })
        
        # Fields
        for pattern in self.field_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                # Get surrounding context for field references
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 30)
                context = text[start:end]
                
                # Look for field names in context
                field_match = re.search(r'\b([A-Za-z0-9_\-]+)\s+field\b', context, re.IGNORECASE)
                if field_match:
                    entities["fields"].append({
                        "name": field_match.group(1),
                        "type": "field"
                    })
        
        # Deduplicate entities
        for entity_type in entities:
            unique_entities = []
            seen = set()
            for entity in entities[entity_type]:
                if entity["name"].lower() not in seen:
                    unique_entities.append(entity)
                    seen.add(entity["name"].lower())
            entities[entity_type] = unique_entities
        
        return entities
    
    def extract_relationships(self, text: str, entities: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, Any]]:
        """Extract relationships between entities in text.
        
        Args:
            text: Text to analyze
            entities: Dictionary of extracted entities
            
        Returns:
            List of relationships between entities
        """
        relationships = []
        
        # Find relationships between data sources and parsers
        for data_source in entities["data_sources"]:
            ds_name = data_source["name"]
            ds_pattern = re.escape(ds_name)
            
            # Look for text connecting data sources and parsers
            parser_connections = re.finditer(
                r'\b' + ds_pattern + r'\b[^.]*?parser',
                text,
                re.IGNORECASE
            )
            
            for match in parser_connections:
                # Find the closest parser entity
                for parser in entities["parsers"]:
                    if parser["name"].lower() in match.group(0).lower():
                        relationships.append({
                            "source": data_source,
                            "target": parser,
                            "type": "has_parser"
                        })
                        break
        
        # Find relationships between data sources and use cases
        for data_source in entities["data_sources"]:
            ds_name = data_source["name"]
            ds_pattern = re.escape(ds_name)
            
            # Look for text connecting data sources and use cases
            use_case_connections = re.finditer(
                r'\b' + ds_pattern + r'\b[^.]*?use case',
                text,
                re.IGNORECASE
            )
            
            for match in use_case_connections:
                # Find the closest use case entity
                for use_case in entities["use_cases"]:
                    if use_case["name"].lower() in match.group(0).lower():
                        relationships.append({
                            "source": data_source,
                            "target": use_case,
                            "type": "supports_use_case"
                        })
                        break
        
        # Find relationships between use cases and MITRE techniques
        for use_case in entities["use_cases"]:
            uc_name = use_case["name"]
            uc_pattern = re.escape(uc_name)
            
            # Look for text connecting use cases and MITRE techniques
            mitre_connections = re.finditer(
                r'\b' + uc_pattern + r'\b[^.]*?T\d{4}',
                text,
                re.IGNORECASE
            )
            
            for match in mitre_connections:
                # Find the closest MITRE technique
                for mitre in entities["mitre"]:
                    if mitre["type"] == "technique" and mitre["name"].lower() in match.group(0).lower():
                        relationships.append({
                            "source": use_case,
                            "target": mitre,
                            "type": "detects_technique"
                        })
                        break
        
        # Find relationships between parsers and event types
        for parser in entities["parsers"]:
            parser_name = parser["name"]
            parser_pattern = re.escape(parser_name)
            
            # Look for text connecting parsers and event types
            event_type_connections = re.finditer(
                r'\b' + parser_pattern + r'\b[^.]*?event',
                text,
                re.IGNORECASE
            )
            
            for match in event_type_connections:
                # Find the closest event type entity
                for event_type in entities["event_types"]:
                    if event_type["name"].lower() in match.group(0).lower():
                        relationships.append({
                            "source": parser,
                            "target": event_type,
                            "type": "generates_event_type"
                        })
                        break
        
        return relationships
    
    def classify_content(self, text: str) -> Dict[str, float]:
        """Classify document content into different categories with confidence scores.
        
        Args:
            text: Text to classify
            
        Returns:
            Dictionary of content categories with confidence scores
        """
        classifications = {
            "overview": 0.0,
            "technical": 0.0,
            "configuration": 0.0,
            "parser": 0.0,
            "use_case": 0.0,
            "reference": 0.0
        }
        
        # Count indicators for each classification
        overview_indicators = [
            r'\boverview\b',
            r'\bintroduction\b',
            r'\bsummary\b',
            r'\bdescription\b',
            r'\babout\b'
        ]
        
        technical_indicators = [
            r'\btechnical\b',
            r'\bimplementation\b',
            r'\barchitecture\b',
            r'\bdesign\b',
            r'\bspecification\b'
        ]
        
        configuration_indicators = [
            r'\bconfiguration\b',
            r'\bsetup\b',
            r'\binstall\b',
            r'\bdeploy\b',
            r'\bsettings\b'
        ]
        
        parser_indicators = [
            r'\bparser\b',
            r'\bparsing\b',
            r'\bnormalization\b',
            r'\bextract\b',
            r'\btransform\b'
        ]
        
        use_case_indicators = [
            r'\buse case\b',
            r'\bscenario\b',
            r'\bdetection\b',
            r'\balert\b',
            r'\bthreat\b'
        ]
        
        reference_indicators = [
            r'\breference\b',
            r'\bappendix\b',
            r'\bglossary\b',
            r'\bdocumentation\b',
            r'\bmanual\b'
        ]
        
        # Count matches for each category
        total_indicators = 0
        
        for pattern in overview_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            classifications["overview"] += len(matches)
            total_indicators += len(matches)
        
        for pattern in technical_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            classifications["technical"] += len(matches)
            total_indicators += len(matches)
        
        for pattern in configuration_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            classifications["configuration"] += len(matches)
            total_indicators += len(matches)
        
        for pattern in parser_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            classifications["parser"] += len(matches)
            total_indicators += len(matches)
        
        for pattern in use_case_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            classifications["use_case"] += len(matches)
            total_indicators += len(matches)
        
        for pattern in reference_indicators:
            matches = re.findall(pattern, text, re.IGNORECASE)
            classifications["reference"] += len(matches)
            total_indicators += len(matches)
        
        # Convert counts to confidence scores
        if total_indicators > 0:
            for category in classifications:
                classifications[category] = round(classifications[category] / total_indicators, 2)
        
        # Ensure at least one category has a minimum score
        if all(score < 0.2 for score in classifications.values()):
            # Set default classification based on content
            if re.search(r'\bparser\b', text, re.IGNORECASE):
                classifications["parser"] = 0.6
            elif re.search(r'\buse case\b', text, re.IGNORECASE):
                classifications["use_case"] = 0.6
            elif re.search(r'\bconfiguration\b', text, re.IGNORECASE):
                classifications["configuration"] = 0.6
            elif re.search(r'\boverview\b', text, re.IGNORECASE):
                classifications["overview"] = 0.6
            else:
                # Default to technical if nothing else matches
                classifications["technical"] = 0.4
        
        return classifications
    
    def enrich_document(self, document: Document) -> Document:
        """Enrich a document with extracted entities, relationships, and classifications.
        
        Args:
            document: Document to enrich
            
        Returns:
            Enriched document with enhanced metadata
        """
        if not document.page_content.strip():
            return document  # Skip empty documents
        
        text = document.page_content
        metadata = document.metadata.copy()
        
        # Extract entities
        entities = self.extract_entities(text)
        for entity_type, entity_list in entities.items():
            if entity_list:  # Only add non-empty entity lists
                metadata[f"extracted_{entity_type}"] = entity_list
        
        # Extract relationships
        relationships = self.extract_relationships(text, entities)
        if relationships:  # Only add if non-empty
            metadata["relationships"] = relationships
        
        # Classify content
        classifications = self.classify_content(text)
        metadata["content_classifications"] = classifications
        
        # Set primary content type based on highest classification score
        if classifications:
            primary_type = max(classifications.items(), key=lambda x: x[1])
            if primary_type[1] >= 0.3:  # Only set if score is significant
                metadata["primary_content_type"] = primary_type[0]
        
        return Document(
            page_content=document.page_content,
            metadata=metadata
        )
    
    def analyze_documents(self, documents: List[Document]) -> List[Document]:
        """Analyze and enrich a list of documents.
        
        Args:
            documents: List of documents to analyze
            
        Returns:
            List of enriched documents with enhanced metadata
        """
        enriched_documents = []
        
        for document in documents:
            enriched_doc = self.enrich_document(document)
            enriched_documents.append(enriched_doc)
        
        # Post-process to cross-reference related documents
        return self._cross_reference_documents(enriched_documents)
    
    def _cross_reference_documents(self, documents: List[Document]) -> List[Document]:
        """Add cross-references between related documents.
        
        Args:
            documents: List of enriched documents
            
        Returns:
            List of documents with cross-reference metadata
        """
        # Build entity-to-document index
        entity_index = defaultdict(list)
        
        for i, doc in enumerate(documents):
            # Index by data sources
            if "extracted_data_sources" in doc.metadata:
                for entity in doc.metadata["extracted_data_sources"]:
                    key = ("data_source", entity["name"].lower())
                    entity_index[key].append(i)
            
            # Index by parsers
            if "extracted_parsers" in doc.metadata:
                for entity in doc.metadata["extracted_parsers"]:
                    key = ("parser", entity["name"].lower())
                    entity_index[key].append(i)
            
            # Index by use cases
            if "extracted_use_cases" in doc.metadata:
                for entity in doc.metadata["extracted_use_cases"]:
                    key = ("use_case", entity["name"].lower())
                    entity_index[key].append(i)
            
            # Index by MITRE techniques
            if "extracted_mitre" in doc.metadata:
                for entity in doc.metadata["extracted_mitre"]:
                    if entity["type"] == "technique":
                        key = ("mitre_technique", entity["name"].lower())
                        entity_index[key].append(i)
        
        # Add cross-references to documents
        for i, doc in enumerate(documents):
            related_docs = set()
            
            # Find related documents based on shared entities
            for entity_type in ["extracted_data_sources", "extracted_parsers", 
                              "extracted_use_cases", "extracted_mitre"]:
                if entity_type in doc.metadata:
                    for entity in doc.metadata[entity_type]:
                        # Determine the key type based on entity_type
                        if entity_type == "extracted_data_sources":
                            key_type = "data_source"
                        elif entity_type == "extracted_parsers":
                            key_type = "parser"
                        elif entity_type == "extracted_use_cases":
                            key_type = "use_case"
                        elif entity_type == "extracted_mitre" and entity["type"] == "technique":
                            key_type = "mitre_technique"
                        else:
                            continue
                        
                        key = (key_type, entity["name"].lower())
                        for related_idx in entity_index[key]:
                            if related_idx != i:  # Don't add self-reference
                                related_docs.add(related_idx)
            
            # Add related document references
            if related_docs:
                doc.metadata["related_documents"] = [
                    {
                        "id": documents[rel_idx].metadata.get("chunk_id", f"doc_{rel_idx}"),
                        "similarity": "entity",  # Relationship is based on shared entities
                        "primary_content_type": documents[rel_idx].metadata.get("primary_content_type", "unknown")
                    }
                    for rel_idx in related_docs
                ]
        
        return documents