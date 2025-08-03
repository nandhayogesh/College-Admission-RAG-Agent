#!/usr/bin/env python3
"""
College Admission RAG Agent - Main Application
Powered by IBM watsonx.ai and IBM Granite models
"""

import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging

from src.rag_engine import RAGEngine
from src.document_manager import DocumentManager
from src.watsonx_client import WatsonxClient

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'college-admission-rag-secret')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
try:
    watsonx_client = WatsonxClient()
    document_manager = DocumentManager()
    rag_engine = RAGEngine(watsonx_client, document_manager)
    logger.info("Application components initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize components: {e}")
    raise

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    """Handle user queries"""
    try:
        data = request.get_json()
        user_query = data.get('query', '').strip()

        if not user_query:
            return jsonify({'error': 'Query cannot be empty'}), 400

        # Process query through RAG engine
        response = rag_engine.process_query(user_query)

        return jsonify({
            'response': response['answer'],
            'sources': response.get('sources', []),
            'confidence': response.get('confidence', 0.0)
        })

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/upload', methods=['POST'])
def upload_document():
    """Upload and process new documents"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Process document
        result = document_manager.add_document(file)

        return jsonify({
            'message': 'Document uploaded successfully',
            'document_id': result['id'],
            'chunks_created': result['chunks']
        })

    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        return jsonify({'error': 'Failed to upload document'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'watsonx_connected': watsonx_client.is_connected(),
        'documents_loaded': document_manager.get_document_count()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
