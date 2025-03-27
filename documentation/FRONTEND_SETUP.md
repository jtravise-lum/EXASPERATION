# EXASPERATION Frontend Setup Guide

This document provides instructions for setting up the EXASPERATION frontend development environment and deploying the application.

## Development Environment Setup

### Prerequisites

- Python 3.10+ installed
- Git for version control
- Docker and Docker Compose (for ChromaDB backend interaction)
- Node.js 16+ for frontend tools (optional)

### Initial Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/exasperation.git
   cd exasperation
   ```

2. Create a dedicated virtual environment:
   ```bash
   python -m venv frontend_venv
   source frontend_venv/bin/activate  # On Windows: frontend_venv\Scripts\activate
   ```

3. Install frontend dependencies:
   ```bash
   pip install -r frontend.requirements.txt
   ```

4. Create a configuration file:
   ```bash
   cp .env.frontend.example .env.frontend
   ```

5. Edit the `.env.frontend` file to set required configurations:
   ```
   # Frontend Configuration
   STREAMLIT_SERVER_PORT=8501
   STREAMLIT_SERVER_HEADLESS=true
   STREAMLIT_THEME_PRIMARY_COLOR=#0066CC
   STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

   # API Configuration
   EXASPERATION_API_URL=http://localhost:8000
   EXASPERATION_API_KEY=your_dev_api_key
   EXASPERATION_API_TIMEOUT=30

   # Feature Flags
   ENABLE_ANALYTICS=false
   ENABLE_AUTHENTICATION=false
   ENABLE_ADVANCED_FILTERS=true
   ENABLE_SUGGESTIONS=true
   ```

## Project Structure

Create the following directory structure for the frontend application:

```
frontend/
├── app.py                  # Main Streamlit application entry point
├── config.py               # Configuration management
├── assets/                 # Static assets
│   ├── css/                # Custom CSS
│   ├── images/             # Images and icons
│   └── js/                 # JavaScript files (if needed)
├── components/             # UI components
│   ├── __init__.py
│   ├── search_interface.py # Search input component
│   ├── results_display.py  # Results rendering component
│   ├── filters_panel.py    # Search filters component
│   ├── help_system.py      # Help and documentation component
│   ├── user_preferences.py # User settings component
│   └── notifications.py    # Notification system component
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── api_client.py       # Backend API client
│   ├── analytics.py        # Usage analytics
│   ├── auth.py             # Authentication helpers
│   └── formatting.py       # Text and result formatting
└── tests/                  # Test files
    ├── __init__.py
    ├── test_api_client.py
    ├── test_components.py
    └── test_utils.py
```

## Running the Application Locally

1. Ensure the backend API is running (or a mock is available)

2. Start the Streamlit application:
   ```bash
   cd frontend
   streamlit run app.py
   ```

3. Access the application at http://localhost:8501

## Testing

1. Run unit tests:
   ```bash
   cd frontend
   pytest
   ```

2. Run with test coverage:
   ```bash
   pytest --cov=. --cov-report=term-missing
   ```

## Docker Setup

1. Create a Dockerfile for the frontend:
   ```dockerfile
   FROM python:3.10-slim

   WORKDIR /app

   COPY frontend.requirements.txt .
   RUN pip install --no-cache-dir -r frontend.requirements.txt

   COPY frontend/ .
   COPY .env.frontend .env.frontend

   EXPOSE 8501

   CMD ["streamlit", "run", "app.py"]
   ```

2. Build and run the Docker container:
   ```bash
   docker build -t exasperation-frontend .
   docker run -p 8501:8501 exasperation-frontend
   ```

## Production Deployment

### Environment Configuration

For production deployment, update the `.env.frontend` file with production settings:
```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Production API endpoint
EXASPERATION_API_URL=https://api.exasperation.example.com/v1
EXASPERATION_API_KEY=${SECURE_API_KEY}
EXASPERATION_API_TIMEOUT=30

# Enable production features
ENABLE_ANALYTICS=true
ENABLE_AUTHENTICATION=true
ENABLE_ADVANCED_FILTERS=true
ENABLE_SUGGESTIONS=true
```

### Deployment Options

#### Option 1: Docker Compose

1. Add the frontend service to your `docker-compose.yml`:
   ```yaml
   version: '3'
   services:
     frontend:
       build:
         context: .
         dockerfile: Dockerfile.frontend
       ports:
         - "8501:8501"
       environment:
         - STREAMLIT_SERVER_PORT=8501
         - EXASPERATION_API_URL=http://api:8000
       depends_on:
         - api
       restart: always
       volumes:
         - ./frontend:/app
     
     # Other services (API, ChromaDB, etc.)
   ```

2. Deploy with Docker Compose:
   ```bash
   docker-compose up -d
   ```

#### Option 2: Streamlit Cloud

1. Push your repository to GitHub

2. Connect your repository to Streamlit Cloud

3. Configure the deployment settings:
   - Main file path: `frontend/app.py`
   - Python version: 3.10
   - Requirements: `frontend.requirements.txt`
   - Secrets: Add your production environment variables

#### Option 3: Kubernetes

1. Create a Kubernetes deployment file:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: exasperation-frontend
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: exasperation-frontend
     template:
       metadata:
         labels:
           app: exasperation-frontend
       spec:
         containers:
         - name: frontend
           image: exasperation-frontend:latest
           ports:
           - containerPort: 8501
           env:
           - name: STREAMLIT_SERVER_PORT
             value: "8501"
           - name: EXASPERATION_API_URL
             valueFrom:
               configMapKeyRef:
                 name: exasperation-config
                 key: api-url
   ```

2. Create a service for the frontend:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: exasperation-frontend
   spec:
     selector:
       app: exasperation-frontend
     ports:
     - port: 80
       targetPort: 8501
     type: LoadBalancer
   ```

## Troubleshooting

### Common Issues

1. **API Connection Issues**
   - Check if the API endpoint is correctly configured in `.env.frontend`
   - Verify the API is running and accessible
   - Check API key permissions

2. **Streamlit Display Problems**
   - Clear browser cache
   - Try using incognito/private browsing mode
   - Check browser console for errors

3. **Dependency Issues**
   - Ensure you're using the correct Python version
   - Verify all packages are installed with `pip list`
   - Try recreating the virtual environment

### Logging

Enable detailed logging by setting:
```
STREAMLIT_LOG_LEVEL=debug
```

View logs:
- In development: Console output
- In Docker: `docker logs exasperation-frontend`
- In Kubernetes: `kubectl logs deployment/exasperation-frontend`

## Performance Optimization

1. Enable Streamlit caching for expensive operations:
   ```python
   @st.cache_data
   def fetch_data_from_api():
       # API calls here
       return data
   ```

2. Use session state efficiently to avoid recomputation:
   ```python
   if "results" not in st.session_state:
       st.session_state.results = []
   ```

3. Optimize image assets:
   - Use WebP format for images
   - Implement lazy loading for images
   - Minimize CSS and JavaScript

## Security Considerations

1. Never hardcode API keys in source code
2. Validate all user inputs before sending to API
3. Implement proper content security policy
4. Use HTTPS for all API communications
5. Implement session timeouts for authenticated users
6. Sanitize any HTML content before rendering