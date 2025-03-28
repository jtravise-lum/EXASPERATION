#!/usr/bin/env python3
"""Test script to verify semantic chunking works with sample documents of all types."""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Add the root directory to sys.path to make imports work
sys.path.append(str(Path(__file__).resolve().parent))
from src.data_processing.semantic_document_chunker import SemanticDocumentChunker
from langchain.schema import Document

# Configure logging
logging.basicConfig(level=logging.INFO, 
                  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Predefined test samples to ensure we test each document type
TEST_SAMPLES = [
    # Format: (file_path, doc_type)
    # Data source samples
    ("/home/johnt/EXASPERATION/data/CIMLibrary/ActivityTypes/ds_object-read.md", "data_source"),
    ("/home/johnt/EXASPERATION/data/Content-Library-CIM1/DataSources/Darktrace/Darktrace/ds_darktrace_darktrace.md", "data_source"),
    ("/home/johnt/EXASPERATION/data/Content-Library-CIM2/DS/APC/apc/ds_apc_apc.md", "data_source"),
    
    # Parser samples
    ("/home/johnt/EXASPERATION/data/Content-Library-CIM1/DataSources/Honeywell/Honeywell_Pro-Watch/Ps/pC_prowatchbadgeaccess1.md", "parser"), 
    ("/home/johnt/EXASPERATION/data/Content-Library-CIM2/DS/APC/apc/Ps/pC_apcastrendpointloginsuccesswebuser.md", "parser"),
    ("/home/johnt/EXASPERATION/data/Content-Library-CIM2/DS/Accellion/kiteworks/Ps/pC_accellionkwkvappactivitysuccessrequestedafile.md", "parser"),
    
    # Use case samples
    ("/home/johnt/EXASPERATION/data/Content-Library-CIM2/DS/APC/apc/RM/r_m_apc_apc_Abnormal_Authentication_&_Access.md", "use_case"),
    ("/home/johnt/EXASPERATION/data/Content-Library-CIM2/DS/Abnormal_Security/abnormal_security/RM/r_m_abnormal_security_abnormal_security_Compromised_Credentials.md", "use_case"),
    ("/home/johnt/EXASPERATION/data/Content-Library-CIM1/UseCases/uc_data_access.md", "use_case")
]

def test_semantic_chunking(file_path: str, doc_type: str) -> Dict[str, Any]:
    """Test semantic chunking on a single file.
    
    Args:
        file_path: Path to the document file
        doc_type: The document type
        
    Returns:
        Dictionary with test results
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "file_path": file_path,
                "doc_type": doc_type,
                "success": False,
                "error": "File not found"
            }
            
        # Read the document
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create document with metadata
        doc_id = Path(file_path).stem
        doc = Document(
            page_content=content,
            metadata={
                "id": doc_id,
                "doc_type": doc_type,
                "source_path": file_path,
                "file_name": Path(file_path).name
            }
        )
        
        # Create chunker and process document
        chunker = SemanticDocumentChunker(chunk_size=1000, chunk_overlap=200)
        chunks = chunker.split_documents([doc])
        
        return {
            "file_path": file_path,
            "doc_type": doc_type,
            "success": len(chunks) > 0,
            "chunk_count": len(chunks),
            "file_size": len(content)
        }
    except Exception as e:
        logger.error(f"Error processing {file_path}: {str(e)}")
        return {
            "file_path": file_path,
            "doc_type": doc_type,
            "success": False,
            "error": str(e)
        }

def main():
    """Test semantic chunking on sample documents of each type."""
    results_by_type = {
        "data_source": [],
        "parser": [],
        "use_case": []
    }
    
    # Process each test sample
    for file_path, doc_type in TEST_SAMPLES:
        logger.info(f"Testing file: {os.path.basename(file_path)} ({doc_type})")
        result = test_semantic_chunking(file_path, doc_type)
        results_by_type[doc_type].append(result)
    
    # Calculate success rates by document type
    summary = {}
    overall_success = True
    
    for doc_type, results in results_by_type.items():
        success_count = sum(1 for r in results if r.get("success", False))
        success_rate = (success_count / len(results)) * 100 if results else 0
        
        summary[doc_type] = {
            "files_tested": len(results),
            "success_count": success_count,
            "success_rate": success_rate
        }
        
        if success_count < len(results):
            overall_success = False
    
    # Print summary
    print("\nSummary of Sample Document Tests:")
    print("================================")
    
    for doc_type, stats in summary.items():
        print(f"\n{doc_type.upper()}:")
        print(f"  Files tested: {stats['files_tested']}")
        print(f"  Success rate: {stats['success_rate']:.1f}%")
        
        # Show details for each test
        for i, result in enumerate(results_by_type[doc_type]):
            filename = os.path.basename(result["file_path"])
            status = "✅ SUCCESS" if result.get("success", False) else "❌ FAILED"
            chunks = result.get("chunk_count", 0)
            error = result.get("error", "")
            
            print(f"  {i+1}. {filename}: {status} ({chunks} chunks)")
            if error:
                print(f"     Error: {error}")
    
    print("\nOverall Test Result:", "✅ PASSED" if overall_success else "❌ FAILED")

if __name__ == "__main__":
    main()