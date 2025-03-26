# EXASPERATION Project Orientation for Code Agents

## Project Overview

EXASPERATION (Exabeam Automated Search Assistant Preventing Exasperating Research And Time-wasting In Official Notes) is a Retrieval Augmented Generation (RAG) system designed to make Exabeam's extensive documentation accessible through natural language queries.

The system processes the Exabeam Content-Library-CIM2 repository (https://github.com/ExabeamLabs/Content-Library-CIM2) which contains comprehensive security documentation spanning data sources, parsers, correlation rules, and use cases. The goal is to allow users to ask questions in natural language and receive accurate, contextual answers with citations to the original documentation.

## Current Implementation Status

The project has three major components, with varying levels of completion:

1. **Document Ingestion** (85% complete)
   - Document loading with specialized metadata extraction ✅
   - Content-specific preprocessing by document type ✅
   - Advanced chunking strategies based on document structure ✅
   - Dual-model embedding system design ✅
   - Vector database interface design ✅
   - ChromaDB Docker setup and configuration ✅
   - Document ingestion pipeline ⏳ (next priority)

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

We've implemented the ChromaDB integration with:

1. **Docker Compose setup** for ChromaDB
   - Persistent volume mounting for data storage
   - Containerized deployment with health checks

2. **Dual-mode support** in VectorDatabase class
   - Server mode: Connects to ChromaDB server instance
   - Local mode: Uses direct file-based persistence

3. **Custom embedding function** that works with our multi-modal approach
   - Routes documents to appropriate embedding model based on content type
   - Handles metadata-aware embedding creation

4. **Rich metadata filtering** for targeted search

## Immediate Next Steps

### Your priority tasks are:

1. **Complete document ingestion pipeline**
   - Implement the ExabeamIngestionPipeline class
   - Create efficient batching for large document collections
   - Build initialization and testing scripts
   - Set up progress tracking and reporting

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
- `docker-compose.yml`: Docker configuration for ChromaDB

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
   - `src/data_processing/vector_store.py`: Vector database implementation with server/client modes
   - `docker-compose.yml`: ChromaDB Docker configuration

3. Check configuration:
   - `src/config.py`: System configuration with ChromaDB settings
   - `.env.example`: Template for environment variables

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

4. **Docker integration**:
   - Ensure all components work well with containerization
   - Default to using the Docker ChromaDB server
   - Support local mode as a fallback option

## Testing Your Implementation

1. The repository contains the Exabeam Content-Library-CIM2 in `data/content-library-cim2/`
2. Start the ChromaDB server with Docker Compose before running tests
3. For query processing, start with testing on use case documents which have clear relationships

## Resources and Dependencies

- Python 3.8+ required
- Docker and Docker Compose for ChromaDB
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
6. Works seamlessly with the Docker ChromaDB setup

Remember, the priority is creating a working document ingestion pipeline with the Docker ChromaDB integration, followed by query processing functionality. Focus on these areas before moving to LLM integration.