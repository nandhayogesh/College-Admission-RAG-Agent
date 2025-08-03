# College Admission RAG Agent Documentation

## Overview
This documentation provides detailed information about setting up, configuring, and using the College Admission RAG Agent.

## Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Usage](#usage)
4. [API Reference](#api-reference)
5. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.8 or higher
- IBM Cloud account with watsonx.ai access
- At least 4GB RAM recommended

### Setup Steps
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure your credentials

## Configuration

### Environment Variables
- `IBM_CLOUD_API_KEY`: Your IBM Cloud API key
- `WATSONX_PROJECT_ID`: Your watsonx.ai project ID
- `MODEL_ID`: Granite model to use (default: ibm/granite-3-2b-instruct)

### Document Setup
1. Place admission documents in `data/documents/` folder
2. Supported formats: PDF, DOC, DOCX, TXT
3. Documents will be automatically processed on startup

## Usage

### Starting the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Uploading Documents
1. Click "Upload Document" in the sidebar
2. Select PDF, DOC, DOCX, or TXT files
3. Documents are automatically processed and indexed

### Asking Questions
Type your admission-related questions in the chat interface. Examples:
- "What are the admission requirements?"
- "When is the application deadline?"
- "How much is tuition?"

## API Reference

### POST /api/query
Submit a query to the RAG system.

**Request:**
```json
{
  "query": "What are the admission requirements?"
}
```

**Response:**
```json
{
  "response": "The admission requirements include...",
  "sources": [
    {
      "source": "admission_info.pdf",
      "score": 0.85
    }
  ],
  "confidence": 0.82
}
```

### POST /api/upload
Upload a new document.

**Request:** Multipart form data with file

**Response:**
```json
{
  "message": "Document uploaded successfully",
  "document_id": "uuid",
  "chunks_created": 15
}
```

### GET /api/health
Check system health status.

**Response:**
```json
{
  "status": "healthy",
  "watsonx_connected": true,
  "documents_loaded": 5
}
```

## Troubleshooting

### Common Issues

1. **watsonx.ai Connection Failed**
   - Verify your IBM Cloud API key
   - Check project ID is correct
   - Ensure sufficient API credits

2. **Document Upload Failed**
   - Check file format (PDF, DOC, DOCX, TXT only)
   - Ensure file size is under 10MB
   - Verify write permissions in data/ directory

3. **Poor Response Quality**
   - Upload more relevant documents
   - Check if documents contain the information being queried
   - Consider adjusting chunk size in document_manager.py

### Logs
Application logs are displayed in the console. For production, configure proper logging to files.

### Performance Tips
- Use smaller, focused documents for better retrieval
- Regularly update documents to keep information current
- Monitor API usage to avoid rate limits
