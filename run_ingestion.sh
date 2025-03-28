#!/bin/bash
# EXASPERATION Ingestion Wrapper Script
# This script simplifies running the ingestion pipeline with various options

# Set default values
CONTENT_DIR="data/Content-Library-CIM2"
BATCH_SIZE=20
MAX_DOCS=""
RESET=false
DISABLE_SEMANTIC=false
OUTPUT_DIR="data/local_chromadb"

# Display help message
show_help() {
    echo "EXASPERATION Ingestion Tool"
    echo "=========================="
    echo "This script runs the enhanced semantic chunking ingestion pipeline"
    echo
    echo "Usage: ./run_ingestion.sh [options]"
    echo
    echo "Options:"
    echo "  -d, --dir DIR       Content directory to ingest (default: $CONTENT_DIR)"
    echo "  -b, --batch SIZE    Batch size for processing (default: $BATCH_SIZE)"
    echo "  -m, --max NUM       Maximum number of documents to process (for testing)"
    echo "  -r, --reset         Reset the database before ingestion"
    echo "  -o, --output DIR    Output database directory (default: $OUTPUT_DIR)"
    echo "  -s, --standard      Use standard chunking instead of enhanced semantic chunking"
    echo "  -h, --help          Show this help message"
    echo
    echo "Examples:"
    echo "  ./run_ingestion.sh                                # Run with defaults"
    echo "  ./run_ingestion.sh -d data/CIMLibrary             # Ingest CIMLibrary"
    echo "  ./run_ingestion.sh -d data/CIMLibrary -m 10       # Ingest 10 docs from CIMLibrary"
    echo "  ./run_ingestion.sh -r                             # Reset DB and ingest"
    echo "  ./run_ingestion.sh -s                             # Use standard chunking"
    echo
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -d|--dir)
            CONTENT_DIR="$2"
            shift 2
            ;;
        -b|--batch)
            BATCH_SIZE="$2"
            shift 2
            ;;
        -m|--max)
            MAX_DOCS="$2"
            shift 2
            ;;
        -r|--reset)
            RESET=true
            shift
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -s|--standard)
            DISABLE_SEMANTIC=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check if content directory exists
if [ ! -d "$CONTENT_DIR" ]; then
    echo "Error: Content directory '$CONTENT_DIR' does not exist."
    exit 1
fi

# Activate the virtual environment
if [ -d "api_venv" ]; then
    source api_venv/bin/activate
elif [ -d "frontend_venv" ]; then
    source frontend_venv/bin/activate
else
    echo "Warning: No virtual environment found. Using system Python."
fi

# Prepare command arguments
CMD_ARGS="--content-dir $CONTENT_DIR --batch-size $BATCH_SIZE"

if [ ! -z "$MAX_DOCS" ]; then
    CMD_ARGS="$CMD_ARGS --max-docs $MAX_DOCS"
fi

if [ "$RESET" = true ]; then
    CMD_ARGS="$CMD_ARGS --reset"
fi

if [ "$DISABLE_SEMANTIC" = true ]; then
    # Set environment variable to disable semantic chunking
    export EXASPERATION_USE_SEMANTIC_CHUNKING=false
    echo "Using standard chunking (semantic chunking disabled)"
else
    export EXASPERATION_USE_SEMANTIC_CHUNKING=true
    echo "Using enhanced semantic chunking"
fi

# Create output directory for database if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Run the ingestion script with all arguments
echo "Starting ingestion from: $CONTENT_DIR"
echo "Database location: $OUTPUT_DIR"
echo "Parameters: $CMD_ARGS"

# Add script to disable semantic chunking if requested
if [ "$DISABLE_SEMANTIC" = true ]; then
    # Create a temporary patch script that modifies exabeam_chunker.py
    TMP_SCRIPT=$(mktemp)
    cat > $TMP_SCRIPT << 'EOF'
import sys

with open(sys.argv[1], 'r') as f:
    content = f.read()

# Replace default parameter to disable semantic chunking
content = content.replace('use_semantic_chunking: bool = True', 'use_semantic_chunking: bool = False')

with open(sys.argv[1], 'w') as f:
    f.write(content)
EOF

    # Apply the patch
    python $TMP_SCRIPT src/data_processing/exabeam_chunker.py
    rm $TMP_SCRIPT
fi

# Set custom database path environment variable
export EXASPERATION_DB_PATH="$OUTPUT_DIR"

# Execute the ingestion script
python scripts/db/local_ingest.py $CMD_ARGS

# Log completion
echo "Ingestion completed. Documents stored in: $OUTPUT_DIR"

# Return to original working directory
cd - > /dev/null

# Deactivate virtual environment if it was activated
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi