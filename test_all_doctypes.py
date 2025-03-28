#!/usr/bin/env python3
"""Test script to verify semantic chunking works with all document types across all data directories."""

import os
import sys
import logging
import json
from pathlib import Path
from typing import Dict, Any, List
from collections import defaultdict

# Add the root directory to sys.path to make imports work
sys.path.append(str(Path(__file__).resolve().parent))
from src.data_processing.semantic_document_chunker import SemanticDocumentChunker
from langchain.schema import Document

# Configure logging
logging.basicConfig(level=logging.INFO, 
                  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def determine_doc_type(file_path: str) -> str:
    """Determine the document type based on file path and content.
    
    Args:
        file_path: The path to the document
        
    Returns:
        The document type as a string (data_source, parser, use_case, unknown)
    """
    file_path_lower = file_path.lower()
    filename = os.path.basename(file_path_lower)
    
    # Check for data source documents
    if "ds_" in filename or "/ds/" in file_path_lower:
        return "data_source"
    
    # Check for parser documents
    if "pc_" in filename or "/ps/" in file_path_lower or "parser" in filename:
        return "parser"
    
    # Check for use case documents
    if "uc_" in filename or "use_case" in filename or "/rm/" in file_path_lower or "r_m_" in filename:
        return "use_case"
        
    # Try to infer from the first few lines of content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_lines = "".join(f.readline() for _ in range(10)).lower()
            
            if "parser" in first_lines or "normalize" in first_lines:
                return "parser"
            if "use case" in first_lines or "detection" in first_lines:
                return "use_case"
            if "data source" in first_lines or "vendor" in first_lines:
                return "data_source"
    except Exception:
        pass
        
    # Default to unknown if we couldn't determine
    return "unknown"

def find_document_files(base_dir: str, limit: int = 10) -> Dict[str, List[str]]:
    """Find document files in the given directory by type.
    
    Args:
        base_dir: The directory to search in
        limit: Maximum number of files per type to return
        
    Returns:
        Dictionary mapping document types to lists of file paths
    """
    files_by_type = defaultdict(list)
    base_path = Path(base_dir)
    
    # Walk through the directory
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                # Determine document type
                doc_type = determine_doc_type(file_path)
                
                # Only add if we haven't reached the limit for this type
                if len(files_by_type[doc_type]) < limit:
                    files_by_type[doc_type].append(file_path)
                    
                # If we have enough of each type, exit early
                if all(len(files) >= limit for doc_type, files in files_by_type.items() 
                       if doc_type != "unknown"):
                    return files_by_type
    
    return files_by_type

def test_semantic_chunking(file_path: str, doc_type: str) -> Dict[str, Any]:
    """Test semantic chunking on a single file.
    
    Args:
        file_path: Path to the document file
        doc_type: The document type
        
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
    """Test semantic chunking on all document types across all directories."""
    data_dirs = [
        "/home/johnt/EXASPERATION/data/CIMLibrary",
        "/home/johnt/EXASPERATION/data/Content-Library-CIM1",
        "/home/johnt/EXASPERATION/data/content-library-cim2",
        "/home/johnt/EXASPERATION/data/Content-Library-CIM2"
    ]
    
    results = {}
    
    for data_dir in data_dirs:
        if not os.path.exists(data_dir):
            logger.warning(f"Directory not found: {data_dir}")
            continue
            
        logger.info(f"Finding document files in {data_dir}")
        doc_files_by_type = find_document_files(data_dir)
        
        # Create results structure for this directory
        dir_name = os.path.basename(data_dir)
        results[dir_name] = {
            "total_files_tested": 0,
            "total_success_count": 0,
            "by_doc_type": {}
        }
        
        # Test each document type
        for doc_type, file_paths in doc_files_by_type.items():
            logger.info(f"Testing {len(file_paths)} {doc_type} documents from {data_dir}")
            
            type_results = []
            for file_path in file_paths:
                logger.info(f"Testing file: {os.path.basename(file_path)} ({doc_type})")
                result = test_semantic_chunking(file_path, doc_type)
                type_results.append(result)
            
            # Store results for this document type
            success_count = sum(1 for r in type_results if r.get("success", False))
            results[dir_name]["by_doc_type"][doc_type] = {
                "files_tested": len(type_results),
                "success_count": success_count,
                "success_rate": (success_count / len(type_results)) * 100 if type_results else 0,
                "details": type_results
            }
            
            # Update directory totals
            results[dir_name]["total_files_tested"] += len(type_results)
            results[dir_name]["total_success_count"] += success_count
    
    # Calculate overall success rate for the directory
    for dir_name in results:
        if results[dir_name]["total_files_tested"] > 0:
            results[dir_name]["total_success_rate"] = (
                results[dir_name]["total_success_count"] / results[dir_name]["total_files_tested"]
            ) * 100
        else:
            results[dir_name]["total_success_rate"] = 0
    
    # Print summary
    print("\nSummary of Semantic Chunking Test Results:")
    print("==========================================")
    
    for data_dir, dir_result in results.items():
        print(f"\n{data_dir}:")
        print(f"  Total files tested: {dir_result['total_files_tested']}")
        print(f"  Overall success rate: {dir_result.get('total_success_rate', 0):.1f}%")
        
        print("\n  Results by document type:")
        for doc_type, type_result in dir_result["by_doc_type"].items():
            print(f"    {doc_type}:")
            print(f"      Files tested: {type_result['files_tested']}")
            print(f"      Success rate: {type_result['success_rate']:.1f}%")
            
            # List any failures
            failures = [d for d in type_result["details"] if not d.get("success", False)]
            if failures:
                print(f"      Failed files ({len(failures)}):")
                for failure in failures[:3]:  # Show just the first few to avoid cluttering output
                    print(f"        - {os.path.basename(failure['file_path'])}: {failure.get('error', 'Unknown error')}")
                if len(failures) > 3:
                    print(f"        - ... and {len(failures)-3} more")
    
    # Write detailed results to a JSON file
    with open("/home/johnt/EXASPERATION/chunking_test_results.json", "w") as f:
        # Convert Path objects to strings to make it JSON serializable
        serializable_results = json.dumps(results, indent=2, default=str)
        f.write(serializable_results)
        
    print("\nDetailed results saved to: /home/johnt/EXASPERATION/chunking_test_results.json")

if __name__ == "__main__":
    main()