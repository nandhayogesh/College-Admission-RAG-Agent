"""
RAG (Retrieval-Augmented Generation) Engine for College Admission queries
"""

import logging
from typing import Dict, List, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

logger = logging.getLogger(__name__)

class RAGEngine:
    """RAG engine combining retrieval and generation"""

    def __init__(self, watsonx_client, document_manager):
        self.watsonx_client = watsonx_client
        self.document_manager = document_manager
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self._initialize_vector_store()

    def _initialize_vector_store(self):
        """Initialize FAISS vector store"""
        try:
            # Load existing embeddings or create new index
            documents = self.document_manager.get_all_documents()

            if documents:
                embeddings = []
                self.document_texts = []

                for doc in documents:
                    for chunk in doc['chunks']:
                        embedding = self.embedding_model.encode(chunk['text'])
                        embeddings.append(embedding)
                        self.document_texts.append({
                            'text': chunk['text'],
                            'source': doc['filename'],
                            'chunk_id': chunk['id']
                        })

                if embeddings:
                    embeddings_array = np.array(embeddings).astype('float32')
                    self.index = faiss.IndexFlatIP(embeddings_array.shape[1])
                    self.index.add(embeddings_array)
                    logger.info(f"Initialized vector store with {len(embeddings)} embeddings")
                else:
                    self.index = None
                    self.document_texts = []
            else:
                self.index = None
                self.document_texts = []
                logger.info("No documents found, initialized empty vector store")

        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            self.index = None
            self.document_texts = []

    def process_query(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Process user query using RAG"""
        try:
            # Retrieve relevant context
            context_info = self._retrieve_context(query, top_k)

            # Generate response using context
            if context_info['contexts']:
                context_text = "\n\n".join(context_info['contexts'])
                response = self.watsonx_client.generate_response(query, context_text)
                confidence = context_info['avg_score']
            else:
                # No relevant context found
                response = self._handle_no_context(query)
                confidence = 0.0

            return {
                'answer': response,
                'sources': context_info['sources'],
                'confidence': confidence,
                'query': query
            }

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                'answer': "I apologize, but I encountered an error processing your question. Please try again.",
                'sources': [],
                'confidence': 0.0,
                'query': query
            }

    def _retrieve_context(self, query: str, top_k: int) -> Dict[str, Any]:
        """Retrieve relevant context using vector similarity"""
        if not self.index or not self.document_texts:
            return {'contexts': [], 'sources': [], 'avg_score': 0.0}

        try:
            # Encode query
            query_embedding = self.embedding_model.encode([query]).astype('float32')

            # Search for similar chunks
            scores, indices = self.index.search(query_embedding, min(top_k, len(self.document_texts)))

            contexts = []
            sources = []
            valid_scores = []

            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.document_texts) and score > 0.3:  # Threshold for relevance
                    doc_info = self.document_texts[idx]
                    contexts.append(doc_info['text'])
                    sources.append({
                        'source': doc_info['source'],
                        'chunk_id': doc_info['chunk_id'],
                        'score': float(score)
                    })
                    valid_scores.append(score)

            avg_score = np.mean(valid_scores) if valid_scores else 0.0

            return {
                'contexts': contexts,
                'sources': sources,
                'avg_score': float(avg_score)
            }

        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return {'contexts': [], 'sources': [], 'avg_score': 0.0}

    def _handle_no_context(self, query: str) -> str:
        """Handle queries when no relevant context is found"""
        general_response = """I don't have specific information about that topic in my knowledge base. 
        However, I'd recommend contacting the admissions office directly for the most accurate and up-to-date information. 

        For general admission inquiries, you can typically find information about:
        - Application deadlines and requirements
        - Tuition and financial aid
        - Academic programs and prerequisites  
        - Campus life and facilities
        - Transfer credit policies

        Is there anything else about college admissions I can help you with?"""

        return general_response

    def add_document_to_index(self, document_chunks: List[Dict]):
        """Add new document chunks to the vector index"""
        try:
            if not document_chunks:
                return

            new_embeddings = []
            new_texts = []

            for chunk in document_chunks:
                embedding = self.embedding_model.encode(chunk['text'])
                new_embeddings.append(embedding)
                new_texts.append({
                    'text': chunk['text'],
                    'source': chunk['source'],
                    'chunk_id': chunk['id']
                })

            if new_embeddings:
                new_embeddings_array = np.array(new_embeddings).astype('float32')

                if self.index is None:
                    # Create new index
                    self.index = faiss.IndexFlatIP(new_embeddings_array.shape[1])
                    self.document_texts = []

                self.index.add(new_embeddings_array)
                self.document_texts.extend(new_texts)

                logger.info(f"Added {len(new_embeddings)} new embeddings to index")

        except Exception as e:
            logger.error(f"Error adding document to index: {e}")
