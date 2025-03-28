"""Unit tests for the semantic document chunker integration."""

import unittest
from typing import List, Dict
from langchain.schema import Document
import logging

from src.data_processing.semantic_document_chunker import SemanticDocumentChunker
from src.data_processing.semantic_chunker import SemanticChunker
from src.data_processing.document_analyzer import DocumentAnalyzer

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestSemanticDocumentChunker(unittest.TestCase):
    """Test cases for the SemanticDocumentChunker."""
    
    def setUp(self):
        """Set up test environment."""
        self.chunker = SemanticDocumentChunker(chunk_size=1000, chunk_overlap=200)
        
        # Sample test documents
        self.parser_document = Document(
            page_content="""# Sample Parser Document
            
## Overview
This is a parser for Windows event logs that extracts authentication events.

## Parser Definition
```
Parser Windows_Security {
    match {
        source = "Windows"
        eventlog = "Security"
    }
    
    extract {
        event_type = "Authentication"
        user = field("Account Name")
        status = field("Status")
        source_ip = field("Source Network Address")
    }
}
```

## Event Types
This parser generates the following event types:
- Authentication
- Failed Login
- Account Lockout

## Fields
The following fields are extracted:
- user: The username of the account
- status: Success or failure
- source_ip: IP address of the login attempt

## Examples
Example log entry:
```
Event ID 4624: An account was successfully logged on.
Account Name: john.doe
Status: Success
Source Network Address: 192.168.1.100
```
            """,
            metadata={
                "id": "parser_123",
                "doc_type": "parser",
                "content_type": "parser",
                "title": "Windows Security Parser"
            }
        )
        
        self.use_case_document = Document(
            page_content="""# Account Compromise Detection Use Case
            
## Overview
This use case detects potential account compromise by monitoring for suspicious login patterns.

## Supported MITRE ATT&CK Techniques
- T1078: Valid Accounts
- T1110: Brute Force

## Detection Logic
The detection looks for:
1. Multiple failed login attempts followed by a success
2. Logins from unusual locations
3. Logins at unusual times

## Exabeam Advanced Analytics Integration
This use case leverages Exabeam Advanced Analytics for:
- User behavior modeling
- Peer group analysis
- Risk scoring

## Supported Data Sources
- Windows Active Directory
- Cisco ASA VPN
- Okta
- Azure AD

## Implementation
For Windows Active Directory, configure the following:
1. Enable auditing for logon events
2. Set up Exabeam collectors
3. Create rule triggers for suspicious patterns

For Cisco ASA VPN, ensure:
- Proper logging configuration
- Authentication event forwarding
            """,
            metadata={
                "id": "usecase_456",
                "doc_type": "use_case",
                "content_type": "use_case",
                "title": "Account Compromise Detection"
            }
        )
        
        self.data_source_document = Document(
            page_content="""# Cisco ASA Data Source Configuration
            
## Overview
This document describes how to configure Cisco ASA as a data source for Exabeam.

## Data Source Details
- Vendor: Cisco
- Product: ASA
- Version: 9.x+
- Event Types: Authentication, VPN, Firewall

## Configuration
### Syslog Configuration
Configure the Cisco ASA to send logs to Exabeam:
```
logging enable
logging host inside 10.1.1.100
logging trap informational
```

### Event Types
The following event types are generated:
- Authentication events (login success/failure)
- VPN connection events
- Firewall allow/deny events

### Parser Support
This data source is supported by the following parsers:
- Cisco_ASA_Auth
- Cisco_ASA_VPN
- Cisco_ASA_Firewall

## Troubleshooting
Common issues include:
1. Incorrect logging level
2. Network connectivity problems
3. Timestamp synchronization issues
            """,
            metadata={
                "id": "datasource_789",
                "doc_type": "data_source",
                "content_type": "data_source",
                "title": "Cisco ASA Data Source"
            }
        )
    
    def test_initialization(self):
        """Test chunker initialization."""
        self.assertIsInstance(self.chunker.semantic_chunker, SemanticChunker)
        self.assertIsInstance(self.chunker.document_analyzer, DocumentAnalyzer)
    
    def test_split_text(self):
        """Test split_text method."""
        text = "This is a test document. It has multiple sentences. We want to see how it gets chunked."
        metadata = {"id": "test_doc", "content_type": "test"}
        
        # Split text
        result = self.chunker.split_text(text, metadata)
        
        # Check results
        self.assertTrue(len(result) > 0)
        self.assertIsInstance(result[0], Document)
        self.assertIn("chunk_id", result[0].metadata)
        self.assertIn("id", result[0].metadata)
        self.assertEqual(result[0].metadata["id"], "test_doc")
    
    def test_split_documents_parser(self):
        """Test splitting parser documents."""
        # Split parser document
        result = self.chunker.split_documents([self.parser_document])
        
        # Check results
        self.assertTrue(len(result) > 0)
        self.assertIsInstance(result[0], Document)
        
        # Verify metadata
        self.assertIn("chunk_id", result[0].metadata)
        self.assertIn("doc_type", result[0].metadata)
        self.assertEqual(result[0].metadata["doc_type"], "parser")
        
        # Check for parser-specific metadata enrichment
        self.assertIn("extracted_parsers", result[0].metadata)
        self.assertIn("content_classifications", result[0].metadata)
        
        # Verify content type preserved
        self.assertEqual(result[0].metadata["content_type"], "parser")
    
    def test_split_documents_use_case(self):
        """Test splitting use case documents."""
        # Split use case document
        result = self.chunker.split_documents([self.use_case_document])
        
        # Check results
        self.assertTrue(len(result) > 0)
        self.assertIsInstance(result[0], Document)
        
        # Verify metadata
        self.assertIn("chunk_id", result[0].metadata)
        self.assertIn("doc_type", result[0].metadata)
        self.assertEqual(result[0].metadata["doc_type"], "use_case")
        
        # Check for use case-specific metadata enrichment
        for doc in result:
            if "extracted_mitre" in doc.metadata:
                # Found MITRE metadata in at least one chunk
                mitre_found = True
                break
        else:
            mitre_found = False
            
        self.assertTrue(mitre_found, "MITRE ATT&CK information not extracted")
        
        # Verify title preserved
        self.assertEqual(result[0].metadata["title"], "Account Compromise Detection")
    
    def test_split_documents_data_source(self):
        """Test splitting data source documents."""
        # Split data source document
        result = self.chunker.split_documents([self.data_source_document])
        
        # Check results
        self.assertTrue(len(result) > 0)
        self.assertIsInstance(result[0], Document)
        
        # Verify metadata
        self.assertIn("chunk_id", result[0].metadata)
        self.assertIn("doc_type", result[0].metadata)
        self.assertEqual(result[0].metadata["doc_type"], "data_source")
        
        # Check for data source-specific metadata enrichment
        vendor_found = False
        for doc in result:
            if "extracted_data_sources" in doc.metadata:
                ds_entities = doc.metadata["extracted_data_sources"]
                for entity in ds_entities:
                    if entity["name"] == "Cisco":
                        vendor_found = True
                        break
                if vendor_found:
                    break
                        
        self.assertTrue(vendor_found, "Vendor information not extracted")
    
    def test_metadata_compatibility(self):
        """Test metadata compatibility preservation."""
        # Create a document with specific metadata
        doc = Document(
            page_content="This is a test document with specific metadata.",
            metadata={
                "id": "test_123",
                "doc_type": "reference",
                "content_type": "documentation",
                "title": "Test Document",
                "vendor": "Example Vendor",
                "product": "Example Product",
                "mitre_tactics": ["Initial Access", "Execution"],
                "mitre_techniques": ["T1566", "T1059"],
                "custom_field": "Custom Value"
            }
        )
        
        # Split the document
        result = self.chunker.split_documents([doc])
        
        # Verify critical metadata fields are preserved
        self.assertTrue(len(result) > 0)
        result_doc = result[0]
        
        self.assertEqual(result_doc.metadata["id"], "test_123")
        self.assertEqual(result_doc.metadata["doc_type"], "reference")
        self.assertEqual(result_doc.metadata["content_type"], "documentation")
        self.assertEqual(result_doc.metadata["title"], "Test Document")
        self.assertEqual(result_doc.metadata["vendor"], "Example Vendor")
        self.assertEqual(result_doc.metadata["product"], "Example Product")
        self.assertEqual(result_doc.metadata["mitre_tactics"], ["Initial Access", "Execution"])
        self.assertEqual(result_doc.metadata["mitre_techniques"], ["T1566", "T1059"])
    
    def test_entity_extraction(self):
        """Test entity extraction."""
        # Create a document with different entity types
        doc = Document(
            page_content="""
            Exabeam Advanced Analytics helps detect threats like T1078 Valid Accounts.
            Cisco ASA firewalls generate authentication logs that can be parsed by
            the Cisco_ASA_Auth parser. This supports the Account Compromise Detection
            use case by monitoring authentication events.
            """,
            metadata={"id": "entity_test"}
        )
        
        # Split and analyze
        result = self.chunker.split_documents([doc])
        
        # Verify entity extraction
        self.assertTrue(len(result) > 0)
        result_doc = result[0]
        
        # Check for extracted entities
        entity_categories = [
            "extracted_products", 
            "extracted_data_sources", 
            "extracted_parsers",
            "extracted_mitre"
        ]
        
        entities_found = False
        for category in entity_categories:
            if category in result_doc.metadata and len(result_doc.metadata[category]) > 0:
                entities_found = True
                break
                
        self.assertTrue(entities_found, "No entities were extracted from the document")
    
    def test_empty_document_handling(self):
        """Test handling of empty documents."""
        # Create an empty document
        empty_doc = Document(
            page_content="",
            metadata={"id": "empty_doc"}
        )
        
        # Process the empty document
        result = self.chunker.split_documents([empty_doc])
        
        # Should return an empty list
        self.assertEqual(len(result), 0, "Empty document should result in empty chunks list")
    
    def test_multiple_documents(self):
        """Test processing multiple documents at once."""
        # Create a list of documents
        docs = [
            self.parser_document,
            self.use_case_document,
            self.data_source_document
        ]
        
        # Process all documents
        result = self.chunker.split_documents(docs)
        
        # Check results
        self.assertTrue(len(result) > 0)
        
        # Count documents by type
        doc_types = {}
        for doc in result:
            doc_type = doc.metadata.get("doc_type", "unknown")
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
            
        # Verify we have chunks for all document types
        self.assertIn("parser", doc_types)
        self.assertIn("use_case", doc_types)
        self.assertIn("data_source", doc_types)


if __name__ == "__main__":
    unittest.main()