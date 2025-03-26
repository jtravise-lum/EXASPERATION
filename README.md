# EXASPERATION

**Exabeam Automated Search Assistant Preventing Exasperating Research And Time-wasting In Official Notes**

## Overview

EXASPERATION is a Retrieval Augmented Generation (RAG) system designed to make Exabeam's extensive documentation accessible and useful. By combining vector search technology with large language models, EXASPERATION allows users to ask natural language questions about Exabeam and receive accurate, contextual answers without needing to navigate through thousands of pages of documentation.

## The Problem

Exabeam's documentation, while comprehensive, can be challenging to navigate. With over 10,000 pages of content covering various data sources, parsers, correlation rules, and use cases, finding specific information can be time-consuming and frustrating. EXASPERATION transforms this "documentation wilderness" into a searchable knowledge base that responds to your queries directly.

## Features

- **Natural Language Queries**: Ask questions in plain English about Exabeam features, configurations, or troubleshooting
- **Contextual Understanding**: The system understands relationships between different parts of the documentation
- **Source Citations**: All responses include references to the original documentation
- **Low-latency Responses**: Get answers in seconds rather than hours of manual searching
- **Continuous Learning**: The system can be updated as new documentation is released

## Technical Architecture

EXASPERATION uses a modular architecture consisting of:

1. **Document Processing Pipeline**: Chunks Exabeam documentation and extracts metadata
2. **Vector Database**: Stores embeddings of document chunks for semantic search
3. **Retrieval Engine**: Finds the most relevant documentation segments for a given query
4. **LLM Integration**: Generates human-readable responses based on retrieved context
5. **Simple Web Interface**: Allows for easy interaction with the system

## Getting Started

### Prerequisites

- Python 3.8+
- 8GB+ RAM recommended
- 2GB disk space for vector database

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/exasperation.git
cd exasperation

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database (this will download and process documentation)
python initialize_db.py
```

### Usage

```bash
# Start the web interface
python app.py
```

Then open your browser to http://localhost:8000 to begin asking questions.

## Example Queries

- "What parsers are available for 1Password?"
- "How does the Audit Tampering use case work with Microsoft products?"
- "Explain the T1070.001 MITRE technique and how Exabeam detects it"
- "What correlation rules are available for detecting lateral movement?"
- "How do I set up the integration with Cisco ACS?"

## Roadmap

- [ ] Add support for PDF documentation
- [ ] Implement user feedback mechanism to improve retrieval quality
- [ ] Create CLI interface for integration with scripts
- [ ] Add visualization for relationships between components
- [ ] Support for real-time documentation updates

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Exabeam team for creating such *thorough* documentation
- The open-source community for amazing tools that make this possible
- Everyone who has ever muttered "I know it's in the docs somewhere..." while searching frantically

---

**EXASPERATION**: *Because life's too short to read the manual... entirely.*
