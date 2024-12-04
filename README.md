# AI Knowledge Base

A Flask-based application for building and querying a semantic knowledge base from PDF and text documents. The application uses state-of-the-art language models to process documents, create embeddings, and provide intelligent semantic search capabilities.

## Features

- **Document Processing**
  - Support for PDF and text file formats
  - Automatic text extraction and chunking
  - Document metadata tracking
  - Secure file handling

- **Semantic Search**
  - Advanced embedding generation using Sentence Transformers
  - Semantic similarity search with configurable threshold
  - Context-aware responses
  - Source tracking for search results

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd aiknowledgebase
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the server:
```bash
python app.py
```

2. The server will start on `http://localhost:5000` with the following endpoints:

### Endpoints

- **POST /upload**
  - Upload PDF or text files
  - Request: Multipart form data with files under "files[]"
  - Response: JSON with upload status and processed files

- **GET /files**
  - List all uploaded files and their metadata
  - Response: JSON with file information

- **POST /query**
  - Search through processed documents
  - Request: JSON with "query" field
  - Response: JSON with relevant context and sources

## Configuration

Key configuration parameters in `app.py`:
- `SIMILARITY_THRESHOLD`: Controls the relevance threshold for search results (default: 0.3)
- `MAX_CONTEXT_LENGTH`: Maximum context length for responses (default: 4000 characters)
- `UPLOAD_FOLDER`: Directory for storing uploaded files

## Security Notes

- Files are securely processed using `secure_filename`
- Environment variables are used for sensitive data
- CORS is enabled for cross-origin requests
- File type validation is implemented

## Dependencies

Key dependencies include:
- Flask: Web framework
- Sentence Transformers: For document embeddings
- PyPDF2: PDF processing
- OpenAI: For advanced query processing
- LangChain: Text processing utilities

For a complete list of dependencies, see `requirements.txt`.

## Building with Bazel

This project uses Bazel as its build system. Here are the key commands:

### Prerequisites

1. Install Bazel:
```bash
brew install bazelisk
```

### Building and Running

1. Build the project:
```bash
bazel build //:run
```

2. Run the application:
```bash
bazel run //:run
```

### Project Structure

The project uses a modular structure with Bazel BUILD files:
- `//:run` - Main application binary
- `//app:app_lib` - Core application library
- `//app/config:config_lib` - Configuration module
- `//app/routes:routes_lib` - API routes
- `//app/services:services_lib` - Core services

### Dependencies

Dependencies are managed through:
- `WORKSPACE` - Bazel workspace configuration
- `third_party/requirements_lock.txt` - Python package dependencies

## Error Handling

The application includes comprehensive error handling for:
- File upload issues
- Processing errors
- Invalid file types
- API failures

All errors are logged for debugging purposes.

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

[Your chosen license]
