#!/usr/bin/env python3
"""Test script to verify semantic chunking works with all data directory sources."""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, List

# Add the root directory to sys.path to make imports work
sys.path.append(str(Path(__file__).resolve().parent))
from src.data_processing.semantic_document_chunker import SemanticDocumentChunker
from langchain.schema import Document

# Configure logging
logging.basicConfig(level=logging.INFO, 
                  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def find_data_source_files(base_dir: str) -> List[str]:
    """Find data source document files in the given directory.
    
    Args:
        base_dir: The directory to search in
        
    Returns:
        List of file paths to data source documents
    """
    data_source_files = []
    base_path = Path(base_dir)
    
    # Walk through the directory
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                # Check if it's likely a data source document
                if 'ds_' in file.lower() or '/DS/' in file_path:
                    data_source_files.append(file_path)
    
    return data_source_files

def test_semantic_chunking(file_path: str) -> Dict[str, Any]:
    """Test semantic chunking on a single file.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        Dictionary with test results
    """
    try:
        # Read the document
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create document with metadata
        doc_id = Path(file_path).stem
        doc = Document(
            page_content=content,
            metadata={
                "id": doc_id,
                "doc_type": "data_source",
                "source_path": file_path,
                "file_name": Path(file_path).name
            }
        )
        
        # Create chunker and process document
        chunker = SemanticDocumentChunker(chunk_size=1000, chunk_overlap=200)
        chunks = chunker.split_documents([doc])
        
        return {
            "file_path": file_path,
            "success": len(chunks) > 0,
            "chunk_count": len(chunks),
            "file_size": len(content)
        }
    except Exception as e:
        logger.error(f"Error processing {file_path}: {str(e)}")
        return {
            "file_path": file_path,
            "success": False,
            "error": str(e)
        }

def main():
    """Test semantic chunking on data source documents from all directories."""
    data_dirs = [
        "/home/johnt/EXASPERATION/data/CIMLibrary",
        "/home/johnt/EXASPERATION/data/Content-Library-CIM1",
        "/home/johnt/EXASPERATION/data/content-library-cim2",
        "/home/johnt/EXASPERATION/data/Content-Library-CIM2"
    ]
    
    results = {}
    
    # Test up to 5 data source files from each directory
    for data_dir in data_dirs:
        if not os.path.exists(data_dir):
            logger.warning(f"Directory not found: {data_dir}")
            continue
            
        logger.info(f"Testing files from {data_dir}")
        data_source_files = find_data_source_files(data_dir)
        
        # Limit to 5 files per directory to keep the test manageable
        test_files = data_source_files[:5]
        
        dir_results = []
        for file_path in test_files:
            logger.info(f"Testing file: {file_path}")
            result = test_semantic_chunking(file_path)
            dir_results.append(result)
            
        # Store results for this directory
        results[data_dir] = {
            "files_tested": len(dir_results),
            "success_count": sum(1 for r in dir_results if r.get("success", False)),
            "details": dir_results
        }
    
    # Print summary
    print("\nSummary of Results:")
    print("==================")
    
    overall_success = True
    for data_dir, dir_result in results.items():
        success_rate = (dir_result["success_count"] / dir_result["files_tested"]) * 100 if dir_result["files_tested"] > 0 else 0
        print(f"\n{os.path.basename(data_dir)}:")
        print(f"  Files tested: {dir_result['files_tested']}")
        print(f"  Success rate: {success_rate:.1f}%")
        
        if dir_result["success_count"] < dir_result["files_tested"]:
            overall_success = False
            print("  Failed files:")
            for detail in dir_result["details"]:
                if not detail.get("success", False):
                    print(f"    - {os.path.basename(detail['file_path'])}: {detail.get('error', 'Unknown error')}")
    
    print("\nOverall Test Result:", "PASSED" if overall_success else "FAILED")

if __name__ == "__main__":
    main()