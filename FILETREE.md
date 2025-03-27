# EXASPERATION Project Structure

This document provides an overview of the EXASPERATION project file structure to help developers understand the organization of the codebase.

## Root Directory

```
/
├── README.md                 # Project overview and documentation
├── CHANGES_LOG.md            # Record of changes and updates
├── IMPLEMENTATION.md         # Implementation details
├── IMPLEMENTATION_CHECKLIST.md # Implementation progress
├── NEXT_STEPS.md             # Planned enhancements
├── FILETREE.md               # This file - project structure documentation
├── CLAUDE.md                 # Development guidelines
├── AGENT_PROMPT.md           # AI assistant instructions
├── docker-compose.yml        # Docker configuration
├── .env.example              # Environment variables template
├── start_all.sh              # Symlink to scripts/run/start_all.sh
├── stop_all.sh               # Symlink to scripts/run/stop_all.sh
```

## Scripts Directory

```
/scripts
├── README.md                 # Scripts directory documentation
├── run/                      # Scripts for running the application
│   ├── start_all.sh          # Start all services
│   ├── stop_all.sh           # Stop all services
│   ├── run_frontend.sh       # Run frontend only
│   ├── run_api.sh            # Run API only
│   └── ...
├── setup/                    # Installation and setup scripts
│   ├── setup.sh              # Main setup script
│   ├── setup_frontend.sh     # Setup frontend environment
│   ├── setup_embedding.sh    # Setup embedding environment
│   └── ...
├── db/                       # Database management scripts
│   ├── check_chromadb.py     # Check ChromaDB connection
│   ├── reset_db.sh           # Reset database
│   └── ...
├── tests/                    # Testing scripts
│   ├── test_api.sh           # Test API
│   ├── test_query.py         # Test query engine
│   └── ...
└── utilities/                # Utility scripts
```

## Source Code

```
/src
├── __init__.py
├── config.py                # Configuration settings
├── initialize_db.py         # Database initialization
├── data_processing/         # Data processing components
│   ├── __init__.py
│   ├── chunker.py           # Document chunking logic
│   ├── document_loader.py   # Document loading utilities
│   ├── embeddings.py        # Embedding utilities
│   ├── exabeam_chunker.py   # Exabeam specific chunking
│   ├── exabeam_ingestion.py # Exabeam ingestion pipeline
│   ├── exabeam_loader.py    # Exabeam specific loading
│   ├── exabeam_preprocessor.py # Exabeam preprocessing
│   ├── exabeam_processor.py # Exabeam processing logic
│   └── vector_store.py      # Vector database interface
├── retrieval/               # Retrieval components
│   ├── __init__.py
│   ├── query_processor.py   # Query processing
│   ├── reranker.py          # Result reranking
│   └── retriever.py         # Document retrieval
└── llm_integration/         # LLM integration components
    ├── __init__.py
    ├── base.py              # Base LLM interface
    ├── llm_factory.py       # LLM factory pattern
    ├── prompt_templates.py  # Prompt templates
    ├── providers.py         # LLM providers
    └── query_engine.py      # Query handling
```

## Frontend

```
/frontend
├── README.md                # Frontend documentation
├── app.py                   # Main Streamlit application
├── config.py                # Frontend configuration
├── healthcheck.py           # Health check endpoint
├── api/                     # API components
│   ├── README.md            # API documentation
│   ├── __init__.py
│   ├── app.py               # FastAPI application
│   ├── auth.py              # Authentication
│   ├── main.py              # API entry point
│   ├── models.py            # Data models
│   ├── routes.py            # API routes
│   ├── service.py           # Service layer
│   └── test_client.py       # API test client
├── assets/                  # Static assets
│   ├── css/                 # CSS styles
│   ├── images/              # Images
│   └── js/                  # JavaScript
├── components/              # UI components
│   ├── __init__.py
│   ├── filters_panel.py     # Search filters
│   ├── help_system.py       # Help system
│   ├── notifications.py     # Notification system
│   ├── results_display.py   # Results display
│   ├── search_interface.py  # Search interface
│   └── user_preferences.py  # User preferences
└── utils/                   # Utility functions
    ├── __init__.py
    ├── analytics.py         # Analytics
    └── api_client.py        # API client
```

## Data and Documentation

```
/data
├── Content-Library-CIM2/    # Exabeam content library (data source)
├── chromadb/                # ChromaDB vector database
├── chromadb.backup/         # Database backups
└── chromadb_logs/           # Database logs

/documentation
├── DEPLOYMENT.md            # Deployment instructions
├── DOCKER_GUIDE.md          # Docker configuration guide
├── FRONTEND_API_CONTRACT.md # API contract documentation
├── FRONTEND_CADDY.md        # Caddy configuration
├── FRONTEND_COMPONENTS.md   # Frontend components documentation
├── FRONTEND_MOCKUPS.md      # UI mockups
├── FRONTEND_PLAN.md         # Frontend implementation plan
├── FRONTEND_SETUP.md        # Frontend setup guide
└── IMPLEMENTATION_PLAN.md   # Overall implementation plan
```

## Virtual Environments

```
/chromadb_venv               # Virtual environment for embeddings/ChromaDB
/frontend_venv               # Virtual environment for frontend
/api_venv                    # Virtual environment for API
```

## Docker and Deployment

```
/api
├── Dockerfile               # API Dockerfile

/frontend
├── Dockerfile               # Frontend Dockerfile

/caddy-docker
├── docker-compose.yml       # Caddy Docker Compose
├── caddy/                   # Caddy configuration
│   ├── config/              # Caddy config
│   ├── data/                # Caddy data
│   └── certs/               # SSL certificates
└── logs/                    # Caddy logs
```

## Logs and Infrastructure

```
/logs
└── caddy/                   # Caddy logs
```