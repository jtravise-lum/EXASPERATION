FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY frontend.requirements.txt .
COPY chromadb.requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r frontend.requirements.txt -r chromadb.requirements.txt

# Copy the entire repository to ensure proper module imports
COPY . /app/

# Expose port for API
EXPOSE 8888

# Set environment variables
ENV PYTHONPATH=/app
ENV DEBUG_MODE=True

# Run the application
CMD ["uvicorn", "frontend.api.app:app", "--host", "0.0.0.0", "--port", "8888"]