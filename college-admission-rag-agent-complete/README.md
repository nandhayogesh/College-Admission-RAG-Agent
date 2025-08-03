# College Admission RAG Agent

A College Admission Agent powered by RAG (Retrieval-Augmented Generation) using IBM watsonx.ai and IBM Granite models.

## Features
- Natural language query processing for admission-related questions
- RAG-based information retrieval from college documents
- Integration with IBM watsonx.ai and IBM Granite models
- Web interface for easy interaction
- Document management for admission policies and FAQs

## Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`
4. Run the application: `python app.py`

## Architecture
- **Backend**: Flask API with RAG implementation
- **AI Models**: IBM Granite via watsonx.ai
- **Vector Database**: Chroma/FAISS for document embeddings
- **Frontend**: HTML/CSS/JavaScript interface

## Documentation
See `docs/` folder for detailed setup and usage instructions.
