# EXABOMINATION Data Ingestion Process

## Overview

This document describes the data ingestion process for the EXABOMINATION system, which involves loading, preprocessing, chunking, embedding, and storing documents to enable efficient retrieval and answering of natural language queries. The system is designed to handle a variety of document types and maintain an up-to-date knowledge base.

## Document Sources

The EXABOMINATION system ingests data from the following sources:

*   **Exabeam Content Library:** The primary source of information is the Exabeam Content Library, specifically the data available in the `Content-Library-CIM2` repository. This repository contains a variety of documents related to the Exabeam Common Information Model (CIM), including:
    *   **Use Cases:** Descriptions of various security use cases and how they are implemented within Exabeam.
    *   **Parsers:** Documentation on parsers for various data sources, explaining how they transform raw logs into the CIM.
    *   **Data Sources:** Information about supported data sources and their integration with Exabeam.
    *   **Rules:** Details on the rules used for detection and alerting.
    *   **Overviews:** General documentation about the CIM and related topics.
* **Other sources:** In the future, other sources could be added.

## Document Loading

The document loading process involves:

1.  **Retrieval:** Downloading or accessing documents from the specified sources. This process is done through the use of custom `exabeam_loader.py` and `exabeam_ingestion.py` files.
2.  **Parsing:** Extracting the content and metadata from the raw document files. The system is designed to handle multiple formats, such as:
    *   **Markdown (.md):** For documentation files.
    * **JSON (.json):** For structured data.
    * **YAML (.yaml):** For structured data.
    * **Plain text (.txt):** For simple text files.

## Document Preprocessing

Once documents are loaded, they undergo preprocessing to prepare them for chunking and embedding. This includes:

1.  **Cleaning:** Removing irrelevant characters, whitespace, and formatting artifacts.
2.  **Normalization:** Converting text to a consistent format (e.g., lowercase).
3.  **Metadata Extraction:** Identifying and extracting relevant metadata from the document content or header, including:
    *   **Document Type:** (Use Case, Parser, Rule, etc.)
    *   **Vendor:** (Microsoft, Cisco, etc.)
    *   **Product:** (Active Directory, ASA, etc.)
    *   **Last Updated:** (Date of last modification)
4. **Other transformations:** Other transformations can be performed as needed.

## Document Chunking

To enable effective information retrieval, documents are split into smaller, meaningful units called "chunks." The system uses different chunking strategies:

*   **Semantic Chunking:** Using natural language processing to identify logical sections and split the document accordingly, as defined in the `semantic_chunker.py` and `semantic_document_chunker.py` files.
*   **Fixed-Size Chunking:** Splitting the document into chunks of a predefined size.
* **Sliding window:** Creating overlapping chunks to capture context between sections.
* **Exabeam chunking**: A custom chunking method for the Exabeam documentation that takes into account the specific structure of the Exabeam documentation.

The optimal chunking strategy is chosen based on the document type and content.

## Embedding Generation

Each chunk is transformed into a numerical vector representation called an "embedding." These embeddings capture the semantic meaning of the text, allowing the system to understand the relationships between different chunks. The system uses a dual-model approach:

*   **Voyage AI Embeddings:**
    *   **voyage-3-large:** Used for natural language content, providing general-purpose semantic embeddings.
    *   **voyage-code-3:** Used for structured data and code-related content (e.g., parsers), providing embeddings that are sensitive to code structure and semantics.
*   **Content-Aware Model Routing:** The system determines the most appropriate embedding model based on the content of the chunk.
* **Caching:** The embeddings are cached to avoid recomputing them for the same document.

## Vector Database Storage

The generated embeddings, along with the corresponding document chunks and metadata, are stored in a vector database:

*   **Chroma DB:** A high-performance vector database is used for efficient storage and retrieval.
*   **Persistence:** The database is configured for persistent storage, ensuring data is not lost between restarts.
*   **Metadata Filtering:** The schema includes metadata fields to enable filtering search results by document type, vendor, product, and other relevant attributes.
* **Automatic Backups:** Automatic backups are configured.

## Data Update Strategy

To ensure the knowledge base remains accurate and up-to-date, the following data update strategy is implemented:

1.  **Periodic Refresh:** The system periodically checks the Exabeam Content Library for updates.
2.  **New Content:** When new documents are added to the source, they are automatically ingested, processed, embedded, and added to the vector database.
3.  **Modified Content:** When documents are modified, the corresponding embeddings are recomputed, and the vector database is updated.
4. **Full re-ingestion**: If needed, a full re-ingestion of the data can be done.
5.  **Versioning:** The system maintains a document versioning system to track changes and enable rollback if necessary.
6. **Error Handling:** The system is designed to handle errors and failures during the ingestion process.

This process allows the EXABOMINATION system to keep its knowledge base up-to-date and ensure that users receive relevant and accurate information.