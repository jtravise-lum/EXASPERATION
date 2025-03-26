# EXASPERATION Implementation Documentation

## Overview

EXASPERATION (Exabeam Automated Search Assistant Preventing Exasperating Research And Time-wasting In Official Notes) is a Retrieval Augmented Generation (RAG) system designed to make Exabeam's extensive documentation accessible through natural language queries. This document details the technical implementation of the system, focusing on the core components and architectural decisions.

## Core Components

### Document Ingestion

We've implemented a specialized document processing system for the Exabeam Content-Library-CIM2 repository:

1. **ExabeamDocumentLoader**: Loads content from the repository with category-based organization
   - Identifies different document types (overview, data sources, use cases, parsers, rules/models)
   - Extracts rich metadata including vendor, product, use case, and MITRE ATT&CK information
   - Handles the diverse structure of Exabeam documentation

2. **ExabeamPreprocessor**: Cleans and normalizes content for improved retrieval
   - Applies document type-specific cleaning strategies
   - Formats tables and structured content for better semantic understanding
   - Retains important context while removing noise

3. **ExabeamChunker**: Implements advanced chunking strategies based on document type
   - Uses markdown headers for structured documentation
   - Splits use case documents by vendor sections
   - Splits data source documents by use case references
   - Preserves parser documentation as single chunks where possible
   - Extracts event type information from rules and models

### Vector Database and Embeddings

We use a dual-model approach with Voyage AI for embeddings, with parallel processing for improved performance:

1. **MultiModalEmbeddingProvider**: Selects the appropriate embedding model based on content
   - `voyage-3-large`: For natural language documentation, use cases, explanations
   - `voyage-code-3`: For structured data formats, parsers, and implementation details
   - Intelligently routes documents to the best model based on content and metadata
   - Handles fallback and error recovery
   - Implements multi-threaded parallel processing with configurable worker count
   - Uses thread pools to process multiple document batches concurrently
   - Optimizes embedding operations for maximum throughput

2. **CustomEmbeddingFunction**: Integrates multi-modal embeddings with Chroma DB
   - Maintains document metadata during embedding
   - Ensures proper model selection during both indexing and search
   - Preserves content-aware embedding model selection

3. **VectorDatabase**: Manages the Chroma vector database
   - Docker-based deployment with persistent storage
   - Flexible configuration for server or local mode
   - Handles document addition and retrieval
   - Supports filtered searches and relevance scoring
   - Manages collection lifecycle with reset capability
   - Provides connection strategies for both Docker and local environments
   - Implements version compatibility for ChromaDB APIs (0.4.x through 0.6.0)
   - Uses robust error handling and retry mechanisms for server operations
   - Includes fallback strategies for API differences between versions

4. **ExabeamIngestionPipeline**: Orchestrates the end-to-end ingestion process
   - Manages document loading, chunking, embedding, and storage
   - Implements efficient batch processing with configurable sizes
   - Provides detailed progress tracking and statistics
   - Handles error recovery and reporting

## Implementation Status

The current implementation focuses on document ingestion:

- ✅ Specialized document loader with metadata extraction
- ✅ Content-specific document cleaning and preprocessing
- ✅ Advanced chunking strategies based on document type
- ✅ Dual-model Voyage AI embedding integration
- ✅ Vector database with multi-modal embedding support

Next phases to implement:

- Complete the document ingestion pipeline
- Add query processing and expansion
- Implement LLM integration with Anthropic Claude
- Create API and interface components

## Technical Decisions

### Embedding Models

We chose Voyage AI for embeddings with a dual-model approach:

- **voyage-3-large**: Better for natural language documentation
  - Captures semantic relationships between security concepts
  - Optimizes retrieval of use cases and explanatory content
  - Cost: $0.00018/1K tokens

- **voyage-code-3**: Better for structured data formats and parsers
  - Captures technical patterns in configuration examples
  - Optimizes retrieval of implementation details
  - Cost: $0.00018/1K tokens

The system intelligently routes documents to the optimal model based on content type and metadata, improving retrieval accuracy across diverse content.

### Chunking Strategy

We implemented a hybrid chunking approach that considers document structure:

1. Use case documents: Split by vendor sections
2. Data source documents: Preserve vendor/product headers and split by use case
3. Parser documents: Keep as single chunks where possible
4. Rules/models documents: Extract event type information

This approach preserves important context while creating appropriately sized chunks for retrieval.

## Next Steps

1. Complete the ingestion pipeline implementation
2. Create the query processing module with query expansion
3. Implement the retriever with re-ranking
4. Add LLM integration with prompt templates
5. Create the API and interface components