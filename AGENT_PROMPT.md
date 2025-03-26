# EXASPERATION Project Orientation for Code Agents

## Project Overview

EXASPERATION (Exabeam Automated Search Assistant Preventing Exasperating Research And Time-wasting In Official Notes) is a Retrieval Augmented Generation (RAG) system designed to make Exabeam's extensive documentation accessible through natural language queries.

The system processes the Exabeam Content-Library-CIM2 repository (https://github.com/ExabeamLabs/Content-Library-CIM2) which contains comprehensive security documentation spanning data sources, parsers, correlation rules, and use cases. The goal is to allow users to ask questions in natural language and receive accurate, contextual answers with citations to the original documentation.

## Current Implementation Status

The project has three major components, with varying levels of completion:

1. **Document Ingestion** (80% complete)
   - Document loading with specialized metadata extraction ✅
   - Content-specific preprocessing by document type ✅
   - Advanced chunking strategies based on document structure ✅
   - Dual-model embedding system design ✅
   - Vector database interface design ✅
   - Actual ChromaDB integration ⏳ (next priority)

2. **Query Processing and Search** (0% complete)
   - Query preprocessing and expansion ⏳
   - Hybrid search implementation ⏳
   - Results re-ranking ⏳
   - Context assembly ⏳

3. **LLM Response Generation** (0% complete)
   - Claude API integration ⏳
   - Prompt engineering system ⏳
   - Response generation with citations ⏳
   - Error handling and fallbacks ⏳

## Technical Architecture Decisions

### Document Processing

We've implemented specialized processing for Exabeam content that:

1. **Maintains document relationships**: Preserves connections between vendors, products, use cases, and technical details
2. **Extracts rich metadata**: Captures vendor names, product types, use cases, MITRE ATT&CK references
3. **Uses document-specific chunking**: Different strategies based on content type:
   - Use case documents: Split by vendor sections
   - Data source documents: Preserve headers and split by use case reference
   - Parser documents: Keep as single chunks when possible
   - Rules/models documents: Extract event type information

### Embedding Strategy

We're using a dual-model approach with Voyage AI:

1. **voyage-3-large** ($0.00018/1K tokens)
   - For natural language documentation, use cases, and general descriptions
   - Better captures semantic relationships between security concepts

2. **voyage-code-3** ($0.00018/1K tokens)
   - For structured data formats, parsers, and implementation details
   - Better captures technical patterns in configuration examples

3. **Content-aware routing**
   - System detects document type and routes to appropriate model
   - Uses metadata and content analysis for selection
   - Includes fallback mechanisms if a model fails

### Vector Database

We've designed (but not yet implemented) a vector database integration with:

1. **ChromaDB** as the vector store
2. **Custom embedding function** that works with our multi-modal approach
3. **Rich metadata filtering** for targeted search

## Immediate Next Steps

### Your priority tasks are:

1. **Complete ChromaDB integration**
   - Implement the actual integration with ChromaDB
   - Set up persistence and connection management
   - Create the document ingestion pipeline
   - Build initialization and testing scripts

2. **Implement query processing**
   - Create query preprocessing module
   - Implement query expansion for security terminology
   - Set up hybrid search capabilities
   - Build metadata filtering system

## Repository Structure

- `src/data_processing/`: Document loader, preprocessor, chunker, embedding
- `src/retrieval/`: Query processing, search, and reranking (partially implemented)
- `src/llm_integration/`: LLM interface (placeholder only)
- `documentation/`: Project plans and specifications

## Key Files to Review

1. Start with the implementation documents:
   - `IMPLEMENTATION.md`: Full technical design overview
   - `IMPLEMENTATION_CHECKLIST.md`: Current progress status
   - `NEXT_STEPS.md`: Detailed roadmap by phase

2. Review code implementation:
   - `src/data_processing/exabeam_loader.py`: Document loading and metadata extraction
   - `src/data_processing/exabeam_preprocessor.py`: Content cleaning strategies
   - `src/data_processing/exabeam_chunker.py`: Document chunking logic
   - `src/data_processing/embeddings.py`: Dual-model embedding implementation
   - `src/data_processing/vector_store.py`: Vector database interface design

3. Check configuration:
   - `src/config.py`: System configuration and environment setup

## Development Guidelines

1. **Code style**:
   - Follow Google Python Style Guide
   - Use type hints consistently
   - Document all functions and classes with Google-style docstrings
   - Include error handling for API calls

2. **Architecture principles**:
   - Maintain separation of concerns between system components
   - Design for testability and component isolation
   - Cache expensive operations where reasonable
   - Include logging at appropriate levels
   - Handle failures gracefully with fallbacks

3. **Security considerations**:
   - Store API keys securely using environment variables
   - Implement rate limiting for external APIs
   - Validate user inputs before processing
   - Sanitize content before displaying to users

## Testing Your Implementation

1. The repository contains the Exabeam Content-Library-CIM2 in `data/content-library-cim2/`
2. After implementing ChromaDB, you can test on a small subset of the documentation
3. For query processing, start with testing on use case documents which have clear relationships

## Resources and Dependencies

- Python 3.8+ required
- See `requirements.txt` for all Python dependencies
- You'll need Voyage AI API keys for embedding (stored in .env file)
- You'll need Claude API keys for response generation (stored in .env file)

## Success Criteria

Your implementation will be successful if it:

1. Can process content from Exabeam Content-Library-CIM2 into ChromaDB vector store
2. Properly associates embeddings with document chunks and metadata
3. Supports metadata-filtered vector search
4. Processes natural language queries with appropriate expansion
5. Returns relevant document chunks with proper context

Remember, the priority is creating a working document ingestion pipeline with ChromaDB integration, followed by query processing functionality. Focus on these areas before moving to LLM integration.