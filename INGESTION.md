# EXASPERATION Ingestion Tool

This document explains how to use the ingestion tools to process and index documents with the EXASPERATION system.

## Overview

The EXASPERATION system includes a powerful document ingestion pipeline with enhanced semantic chunking that produces higher quality chunks for retrieval. The system can process documents from various sources and store them in a vector database for fast semantic search.

## Using the Ingestion Wrapper Script

We've provided a convenient wrapper script to simplify running the ingestion pipeline:

```bash
./run_ingestion.sh
```

This script handles activating the proper virtual environment, setting up the necessary environment variables, and running the ingestion with the right parameters.

### Command-line Options

The wrapper script supports the following options:

| Option | Description |
|--------|-------------|
| `-d, --dir DIR` | Content directory to ingest (default: `data/Content-Library-CIM2`) |
| `-b, --batch SIZE` | Batch size for processing (default: 20) |
| `-m, --max NUM` | Maximum number of documents to process (for testing) |
| `-r, --reset` | Reset the database before ingestion |
| `-o, --output DIR` | Output database directory (default: `data/local_chromadb`) |
| `-s, --standard` | Use standard chunking instead of enhanced semantic chunking |
| `-h, --help` | Show help message |

### Examples

Process the default directory with semantic chunking:
```bash
./run_ingestion.sh
```

Process a different content directory:
```bash
./run_ingestion.sh -d data/CIMLibrary
```

Process a limited number of documents (for testing):
```bash
./run_ingestion.sh -d data/CIMLibrary/ActivityTypes -m 10
```

Reset the database before ingestion:
```bash
./run_ingestion.sh -r
```

Use standard chunking instead of semantic chunking:
```bash
./run_ingestion.sh -s
```

Specify a custom output directory:
```bash
./run_ingestion.sh -o /custom/path/chromadb
```

## Semantic vs. Standard Chunking

The ingestion pipeline offers two chunking strategies:

1. **Enhanced Semantic Chunking** (default): Our improved chunking system that:
   - Produces higher quality, more coherent chunks
   - Preserves entities and context better
   - Reduces chunk count significantly
   - Provides more intelligent document splitting

2. **Standard Chunking**: The original chunking system that:
   - Uses simpler, fixed-size chunking
   - Processes documents faster
   - Is less context-aware
   - Produces more chunks

You can toggle between these strategies using the `-s` flag on the wrapper script.

## Monitoring Ingestion

The ingestion process provides detailed logging to help you monitor its progress. Key things to watch for:

- Document loading progress
- Chunking statistics
- Embedding information
- Database storage confirmation

## Troubleshooting

If you encounter issues with ingestion:

1. **Missing Files**: Ensure the content directory exists and contains documents
2. **Environment Issues**: Check that virtual environments are properly set up
3. **Database Errors**: Try using the `-r` flag to reset the database
4. **Performance Problems**: Reduce batch size with `-b` or limit documents with `-m`
5. **Memory Errors**: Process fewer documents or use standard chunking with `-s`