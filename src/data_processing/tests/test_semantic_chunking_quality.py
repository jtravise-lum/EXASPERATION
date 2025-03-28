#!/usr/bin/env python3
"""Test script for evaluating semantic chunking quality with real Exabeam documentation."""

import os
import sys
import logging
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from langchain.schema import Document

# Add the root directory to sys.path to make imports work - use relative paths
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent.parent
sys.path.append(str(root_dir))
from src.data_processing.chunker import DocumentChunker
from src.data_processing.semantic_document_chunker import SemanticDocumentChunker
from src.data_processing.chunk_quality_evaluator import ChunkQualityEvaluator

# Configure logging
logging.basicConfig(level=logging.INFO, 
                  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define specific example documents for each category using relative paths
# These will be resolved relative to the root directory
SAMPLE_DOCUMENTS = {
    "parser": [
        "data/Content-Library-CIM2/DS/APC/apc/Ps/pC_apcastrendpointloginsuccesswebuser.md",
        "data/Content-Library-CIM2/DS/Accellion/kiteworks/Ps/pC_accellionkwkvappactivitysuccessrequestedafile.md"
    ],
    "data_source": [
        "data/Content-Library-CIM2/DS/APC/apc/ds_apc_apc.md",
        "data/Content-Library-CIM2/DS/Abnormal_Security/abnormal_security/ds_abnormal_security_abnormal_security.md"
    ],
    "use_case": [
        "data/Content-Library-CIM2/DS/APC/apc/RM/r_m_apc_apc_Abnormal_Authentication_&_Access.md",
        "data/Content-Library-CIM2/DS/Abnormal_Security/abnormal_security/RM/r_m_abnormal_security_abnormal_security_Compromised_Credentials.md"
    ]
}

class ChunkingBenchmark:
    """Benchmark tool for comparing chunking strategies."""
    
    def __init__(self, content_dir: str):
        """Initialize the benchmark.
        
        Args:
            content_dir: Directory containing Exabeam documentation
        """
        self.content_dir = Path(content_dir)
        self.standard_chunker = DocumentChunker(chunk_size=1000, chunk_overlap=200)
        self.semantic_chunker = SemanticDocumentChunker(chunk_size=1000, chunk_overlap=200)
        self.evaluator = ChunkQualityEvaluator()
        
        logger.info(f"Initialized ChunkingBenchmark with content directory: {content_dir}")
    
    def load_document(self, file_path: str) -> Optional[Document]:
        """Load a document from file.
        
        Args:
            file_path: Path to document file
            
        Returns:
            Loaded document or None if loading fails
        """
        path = Path(file_path)
        if not path.exists():
            logger.warning(f"File not found: {file_path}")
            return None
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract basic metadata from path
            parts = path.parts
            doc_id = path.stem
            
            # Try to determine document type from path
            doc_type = "unknown"
            if "DS" in parts:
                doc_type = "data_source"
            elif "UC" in parts:
                doc_type = "use_case"
            elif "Ps" in parts:
                doc_type = "parser"
            elif "RM" in parts:
                doc_type = "use_case"  # Reference Model documents are use cases
                
            # Check filename patterns
            filename = path.name.lower()
            if filename.startswith("ds_"):
                doc_type = "data_source"
            elif filename.startswith("uc_"):
                doc_type = "use_case"
            elif filename.startswith("r_m_"):
                doc_type = "use_case"
            elif "parser" in filename or filename.startswith("pc_"):
                doc_type = "parser"
                
            # Create document with metadata
            doc = Document(
                page_content=content,
                metadata={
                    "id": doc_id,
                    "doc_type": doc_type,
                    "source_path": str(path),
                    "file_name": path.name
                }
            )
            
            return doc
            
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {str(e)}")
            return None
    
    def benchmark_document(self, doc_path: str) -> Dict[str, Any]:
        """Benchmark different chunking strategies on a single document.
        
        Args:
            doc_path: Path to document file
            
        Returns:
            Benchmark results
        """
        # Load document
        doc = self.load_document(doc_path)
        if not doc:
            return {"error": f"Failed to load document: {doc_path}"}
            
        # Apply both chunking strategies
        start_time_standard = time.time()
        standard_chunks = self.standard_chunker.split_documents([doc])
        standard_time = time.time() - start_time_standard
        
        start_time_semantic = time.time()
        semantic_chunks = self.semantic_chunker.split_documents([doc])
        semantic_time = time.time() - start_time_semantic
        
        # Evaluate quality
        comparison = self.evaluator.compare_chunking_strategies(
            doc, standard_chunks, semantic_chunks
        )
        
        # Add performance metrics
        performance = {
            "standard_chunking_time": standard_time,
            "semantic_chunking_time": semantic_time,
            "time_difference_percentage": ((semantic_time - standard_time) / standard_time) * 100,
            "standard_chunks_count": len(standard_chunks),
            "semantic_chunks_count": len(semantic_chunks)
        }
        
        # Add document metadata
        metadata = {
            "file_path": doc_path,
            "doc_id": doc.metadata.get("id", "unknown"),
            "doc_type": doc.metadata.get("doc_type", "unknown"),
            "content_length": len(doc.page_content)
        }
        
        result = {
            "metadata": metadata,
            "performance": performance,
            "quality_comparison": comparison
        }
        
        return result
    
    def run_category_benchmark(self, category: str) -> Dict[str, Any]:
        """Run benchmark on a specific document category using sample documents.
        
        Args:
            category: Document category to test ('parser', 'data_source', 'use_case')
            
        Returns:
            Benchmark results
        """
        if category not in SAMPLE_DOCUMENTS:
            return {"error": f"Unknown category: {category}"}
            
        doc_paths = SAMPLE_DOCUMENTS[category]
        if not doc_paths:
            return {"error": f"No sample documents defined for category: {category}"}
            
        logger.info(f"Running benchmark on {len(doc_paths)} {category} documents")
        
        # Run benchmark on each document
        doc_results = {}
        for path in doc_paths:
            logger.info(f"Benchmarking document: {path}")
            try:
                result = self.benchmark_document(path)
                doc_id = Path(path).stem
                doc_results[doc_id] = result
            except Exception as e:
                logger.error(f"Error benchmarking {path}: {str(e)}")
        
        # Aggregate results
        overall_metrics = self._aggregate_results(doc_results)
        
        return {
            "document_results": doc_results,
            "overall_metrics": overall_metrics
        }
    
    def _aggregate_results(self, doc_results: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate benchmark results across documents.
        
        Args:
            doc_results: Individual document benchmark results
            
        Returns:
            Aggregated metrics
        """
        if not doc_results:
            return {}
            
        # Performance metrics
        standard_times = []
        semantic_times = []
        standard_counts = []
        semantic_counts = []
        
        # Quality metrics
        quality_improvements = []
        coherence_improvements = []
        density_improvements = []
        entity_improvements = []
        context_improvements = []
        
        # Process each document result
        for doc_id, result in doc_results.items():
            if "performance" in result:
                perf = result["performance"]
                standard_times.append(perf.get("standard_chunking_time", 0))
                semantic_times.append(perf.get("semantic_chunking_time", 0))
                standard_counts.append(perf.get("standard_chunks_count", 0))
                semantic_counts.append(perf.get("semantic_chunks_count", 0))
            
            if "quality_comparison" in result and "metrics_comparison" in result["quality_comparison"]:
                metrics = result["quality_comparison"]["metrics_comparison"]
                
                # Extract quality improvements (semantic - standard)
                if "average_quality" in metrics:
                    diff = metrics["average_quality"].get("difference", 0)
                    quality_improvements.append(diff)
                    
                if "average_coherence" in metrics:
                    diff = metrics["average_coherence"].get("difference", 0)
                    coherence_improvements.append(diff)
                    
                if "average_information_density" in metrics:
                    diff = metrics["average_information_density"].get("difference", 0)
                    density_improvements.append(diff)
                    
                if "average_entity_preservation" in metrics:
                    diff = metrics["average_entity_preservation"].get("difference", 0)
                    entity_improvements.append(diff)
                    
                if "average_context_completeness" in metrics:
                    diff = metrics["average_context_completeness"].get("difference", 0)
                    context_improvements.append(diff)
        
        # Calculate aggregate metrics
        return {
            "document_count": len(doc_results),
            "performance": {
                "avg_standard_time": sum(standard_times) / len(standard_times) if standard_times else 0,
                "avg_semantic_time": sum(semantic_times) / len(semantic_times) if semantic_times else 0,
                "avg_time_increase_percentage": ((sum(semantic_times) - sum(standard_times)) / sum(standard_times)) * 100 if sum(standard_times) > 0 else 0,
                "avg_standard_chunks": sum(standard_counts) / len(standard_counts) if standard_counts else 0,
                "avg_semantic_chunks": sum(semantic_counts) / len(semantic_counts) if semantic_counts else 0,
                "chunk_count_difference_percentage": ((sum(semantic_counts) - sum(standard_counts)) / sum(standard_counts)) * 100 if sum(standard_counts) > 0 else 0
            },
            "quality": {
                "avg_quality_improvement": sum(quality_improvements) / len(quality_improvements) if quality_improvements else 0,
                "avg_coherence_improvement": sum(coherence_improvements) / len(coherence_improvements) if coherence_improvements else 0,
                "avg_density_improvement": sum(density_improvements) / len(density_improvements) if density_improvements else 0,
                "avg_entity_improvement": sum(entity_improvements) / len(entity_improvements) if entity_improvements else 0,
                "avg_context_improvement": sum(context_improvements) / len(context_improvements) if context_improvements else 0,
                "quality_improvement_percentage": (sum(quality_improvements) / len(quality_improvements)) * 100 if quality_improvements else 0
            }
        }
    
    def visualize_results(self, results: Dict[str, Any], output_dir: str = "./results"):
        """Generate visualizations of benchmark results.
        
        Args:
            results: Benchmark results
            output_dir: Directory to save visualizations
        """
        os.makedirs(output_dir, exist_ok=True)
        
        if "overall_metrics" not in results:
            logger.error("No overall metrics found in results")
            return
            
        metrics = results["overall_metrics"]
        
        # Quality improvement chart
        if "quality" in metrics:
            quality = metrics["quality"]
            categories = [
                "Overall Quality", 
                "Coherence", 
                "Information Density",
                "Entity Preservation",
                "Context Completeness"
            ]
            
            values = [
                quality.get("avg_quality_improvement", 0) * 100,
                quality.get("avg_coherence_improvement", 0) * 100,
                quality.get("avg_density_improvement", 0) * 100,
                quality.get("avg_entity_improvement", 0) * 100,
                quality.get("avg_context_improvement", 0) * 100
            ]
            
            plt.figure(figsize=(10, 6))
            colors = ['green' if x > 0 else 'red' for x in values]
            plt.bar(categories, values, color=colors)
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            plt.title("Quality Improvements: Semantic vs Standard Chunking (%)")
            plt.ylabel("Improvement (%)")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(f"{output_dir}/quality_improvements.png")
            
        # Performance comparison
        if "performance" in metrics:
            perf = metrics["performance"]
            
            # Time comparison
            plt.figure(figsize=(8, 5))
            times = [
                perf.get("avg_standard_time", 0),
                perf.get("avg_semantic_time", 0)
            ]
            plt.bar(["Standard Chunking", "Semantic Chunking"], times)
            plt.title("Average Processing Time Comparison")
            plt.ylabel("Time (seconds)")
            plt.tight_layout()
            plt.savefig(f"{output_dir}/processing_time.png")
            
            # Chunk count comparison
            plt.figure(figsize=(8, 5))
            counts = [
                perf.get("avg_standard_chunks", 0),
                perf.get("avg_semantic_chunks", 0)
            ]
            plt.bar(["Standard Chunking", "Semantic Chunking"], counts)
            plt.title("Average Chunk Count Comparison")
            plt.ylabel("Number of Chunks")
            plt.tight_layout()
            plt.savefig(f"{output_dir}/chunk_counts.png")
        
        # Document-specific comparisons
        if "document_results" in results:
            doc_results = results["document_results"]
            
            # Quality improvement by document
            doc_ids = []
            improvements = []
            
            for doc_id, result in doc_results.items():
                if "quality_comparison" in result and "metrics_comparison" in result["quality_comparison"]:
                    metrics_comp = result["quality_comparison"]["metrics_comparison"]
                    if "average_quality" in metrics_comp:
                        diff = metrics_comp["average_quality"].get("difference", 0) * 100
                        doc_ids.append(doc_id)
                        improvements.append(diff)
            
            if doc_ids:
                plt.figure(figsize=(10, 6))
                colors = ['green' if x > 0 else 'red' for x in improvements]
                plt.bar(doc_ids, improvements, color=colors)
                plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
                plt.title("Quality Improvement by Document (%)")
                plt.ylabel("Improvement (%)")
                plt.tight_layout()
                plt.savefig(f"{output_dir}/quality_by_document.png")
        
        logger.info(f"Visualizations saved to {output_dir}")


def main():
    """Run the benchmark with specific sample documents."""
    # Use relative paths based on project root
    root_dir = Path(__file__).resolve().parent.parent.parent
    content_dir = root_dir / "data" / "Content-Library-CIM2"
    
    # Check for alternate casing in directory name
    if not content_dir.exists():
        content_dir = root_dir / "data" / "content-library-cim2"
    
    if not content_dir.exists():
        logger.error(f"Content directory not found: {content_dir}")
        return
    
    # Output directory for results
    output_dir = root_dir / "results"
    os.makedirs(output_dir, exist_ok=True)
    
    benchmark = ChunkingBenchmark(content_dir)
    
    # Run benchmarks for each document type
    categories = ["parser", "data_source", "use_case"]
    
    for category in categories:
        logger.info(f"Running benchmark for {category} documents")
        results = benchmark.run_category_benchmark(category)
        
        # Save results
        category_dir = os.path.join(output_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        
        # Generate visualizations
        benchmark.visualize_results(results, category_dir)
        
        # Write summary
        if "overall_metrics" in results:
            with open(os.path.join(category_dir, "summary.txt"), "w") as f:
                metrics = results["overall_metrics"]
                f.write(f"# {category.upper()} Document Chunking Benchmark\n\n")
                
                f.write("## Performance Metrics\n")
                perf = metrics.get("performance", {})
                f.write(f"- Standard chunking time: {perf.get('avg_standard_time', 0):.3f} seconds\n")
                f.write(f"- Semantic chunking time: {perf.get('avg_semantic_time', 0):.3f} seconds\n")
                f.write(f"- Time increase: {perf.get('avg_time_increase_percentage', 0):.1f}%\n")
                f.write(f"- Standard chunks count: {perf.get('avg_standard_chunks', 0):.1f}\n")
                f.write(f"- Semantic chunks count: {perf.get('avg_semantic_chunks', 0):.1f}\n")
                f.write(f"- Chunk count difference: {perf.get('chunk_count_difference_percentage', 0):.1f}%\n\n")
                
                f.write("## Quality Metrics\n")
                quality = metrics.get("quality", {})
                f.write(f"- Overall quality improvement: {quality.get('avg_quality_improvement', 0) * 100:.1f}%\n")
                f.write(f"- Coherence improvement: {quality.get('avg_coherence_improvement', 0) * 100:.1f}%\n")
                f.write(f"- Information density improvement: {quality.get('avg_density_improvement', 0) * 100:.1f}%\n")
                f.write(f"- Entity preservation improvement: {quality.get('avg_entity_improvement', 0) * 100:.1f}%\n")
                f.write(f"- Context completeness improvement: {quality.get('avg_context_improvement', 0) * 100:.1f}%\n")
    
    logger.info(f"Benchmark results saved to {output_dir}")
    logger.info("NOTE: This script generates test files in the results directory. Remember to clean them up when done.")


if __name__ == "__main__":
    main()