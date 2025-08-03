"""
Document Manager for handling college admission documents
"""

import os
import json
import uuid
import logging
from typing import Dict, List, Any
from werkzeug.utils import secure_filename
import PyPDF2
from docx import Document
import pandas as pd

logger = logging.getLogger(__name__)

class DocumentManager:
    """Manages document storage and processing"""

    def __init__(self, storage_path: str = "data/documents"):
        self.storage_path = storage_path
        self.metadata_file = os.path.join(storage_path, "metadata.json")
        self._ensure_storage_path()
        self._load_metadata()

    def _ensure_storage_path(self):
        """Ensure storage directories exist"""
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(os.path.join(self.storage_path, "uploads"), exist_ok=True)

    def _load_metadata(self):
        """Load document metadata"""
        try:
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
            else:
                self.metadata = {"documents": []}
                self._save_metadata()
        except Exception as e:
            logger.error(f"Error loading metadata: {e}")
            self.metadata = {"documents": []}

    def _save_metadata(self):
        """Save document metadata"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")

    def add_document(self, file) -> Dict[str, Any]:
        """Add a new document"""
        try:
            # Generate unique ID
            doc_id = str(uuid.uuid4())
            filename = secure_filename(file.filename)
            file_path = os.path.join(self.storage_path, "uploads", f"{doc_id}_{filename}")

            # Save file
            file.save(file_path)

            # Extract text and create chunks
            text_content = self._extract_text(file_path, filename)
            chunks = self._create_chunks(text_content, doc_id, filename)

            # Store metadata
            doc_metadata = {
                "id": doc_id,
                "filename": filename,
                "file_path": file_path,
                "upload_date": pd.Timestamp.now().isoformat(),
                "chunks": len(chunks),
                "file_size": os.path.getsize(file_path)
            }

            self.metadata["documents"].append(doc_metadata)
            self._save_metadata()

            logger.info(f"Added document {filename} with {len(chunks)} chunks")

            return {
                "id": doc_id,
                "chunks": len(chunks),
                "filename": filename
            }

        except Exception as e:
            logger.error(f"Error adding document: {e}")
            raise

    def _extract_text(self, file_path: str, filename: str) -> str:
        """Extract text from various file formats"""
        try:
            file_ext = filename.lower().split('.')[-1]

            if file_ext == 'pdf':
                return self._extract_pdf_text(file_path)
            elif file_ext in ['doc', 'docx']:
                return self._extract_docx_text(file_path)
            elif file_ext == 'txt':
                return self._extract_txt_text(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")

        except Exception as e:
            logger.error(f"Error extracting text from {filename}: {e}")
            raise

    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text

    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX"""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def _extract_txt_text(self, file_path: str) -> str:
        """Extract text from TXT"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _create_chunks(self, text: str, doc_id: str, filename: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict]:
        """Create text chunks for RAG"""
        chunks = []
        words = text.split()

        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = ' '.join(chunk_words)

            if len(chunk_text.strip()) > 50:  # Skip very small chunks
                chunks.append({
                    "id": f"{doc_id}_chunk_{len(chunks)}",
                    "text": chunk_text.strip(),
                    "source": filename,
                    "doc_id": doc_id,
                    "chunk_index": len(chunks)
                })

        return chunks

    def get_all_documents(self) -> List[Dict]:
        """Get all document metadata with chunks"""
        documents_with_chunks = []

        for doc_meta in self.metadata["documents"]:
            # For this example, we'll regenerate chunks from stored files
            # In production, you might want to cache chunks
            try:
                text_content = self._extract_text(doc_meta["file_path"], doc_meta["filename"])
                chunks = self._create_chunks(text_content, doc_meta["id"], doc_meta["filename"])

                doc_with_chunks = doc_meta.copy()
                doc_with_chunks["chunks"] = chunks
                documents_with_chunks.append(doc_with_chunks)

            except Exception as e:
                logger.error(f"Error loading document {doc_meta['filename']}: {e}")
                continue

        return documents_with_chunks

    def get_document_count(self) -> int:
        """Get total number of documents"""
        return len(self.metadata["documents"])

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document"""
        try:
            # Find document
            doc_to_remove = None
            for doc in self.metadata["documents"]:
                if doc["id"] == doc_id:
                    doc_to_remove = doc
                    break

            if not doc_to_remove:
                return False

            # Remove file
            if os.path.exists(doc_to_remove["file_path"]):
                os.remove(doc_to_remove["file_path"])

            # Remove from metadata
            self.metadata["documents"].remove(doc_to_remove)
            self._save_metadata()

            logger.info(f"Deleted document {doc_to_remove['filename']}")
            return True

        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {e}")
            return False
