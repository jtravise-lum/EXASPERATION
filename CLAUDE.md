# EXASPERATION Development Guidelines

## Build & Run Commands
- ALWAYS USE THE CORRECT VENV: `source chromadb_venv/bin/activate`
- Install dependencies: `pip install -r chromadb.requirements.txt`
- Initialize database: `python initialize_db.py`
- Start application: `python app.py`
- Run tests: `pytest`
- Run single test: `pytest tests/path_to_test.py::test_function_name -v`
- Lint code: `pylint **/*.py`
- Format code: `black .`
- Run ChromaDB checks: `source chromadb_venv/bin/activate && python check_chromadb.py`
- Test query engine: `source chromadb_venv/bin/activate && python test_query.py "Your query here"`

## Code Style Guidelines
- **Python version**: Python 3.8+ (preferably 3.10+)
- **Formatting**: Black with default settings
- **Imports**: Group standard library, third-party, and local imports with single blank line between groups
- **Docstrings**: Google style docstrings for all public functions and classes
- **Naming**: snake_case for variables/functions, PascalCase for classes, UPPER_CASE for constants
- **Error handling**: Use specific exceptions, always include error messages
- **Type hints**: Required for all function parameters and return values
- **Testing**: Write unit tests for all new functionality
- **Container practices**: Support Docker deployment with proper environment variables

## Security & Performance
- Store API keys securely using environment variables
- Implement proper rate limiting for API calls
- Apply caching strategies for improved performance
- Follow least privilege principle for all components