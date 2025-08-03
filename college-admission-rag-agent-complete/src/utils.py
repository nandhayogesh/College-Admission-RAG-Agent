"""
Utility functions for the college admission RAG system
"""

import re
import string
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())

    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?;:-]', '', text)

    return text

def is_admission_related(query: str) -> bool:
    """Check if query is related to college admission"""
    admission_keywords = [
        'admission', 'apply', 'application', 'requirement', 'deadline',
        'tuition', 'fee', 'scholarship', 'financial aid', 'gpa',
        'transcript', 'sat', 'act', 'essay', 'recommendation',
        'program', 'major', 'course', 'enrollment', 'registration'
    ]

    query_lower = query.lower()
    return any(keyword in query_lower for keyword in admission_keywords)

def format_response(response: str) -> str:
    """Format response for better readability"""
    if not response:
        return ""

    # Ensure proper sentence endings
    response = response.strip()
    if response and not response.endswith(('.', '!', '?')):
        response += '.'

    return response

def extract_key_phrases(text: str) -> List[str]:
    """Extract key phrases from text"""
    # Simple keyword extraction (in production, use more sophisticated NLP)
    words = text.lower().split()

    # Common admission-related phrases
    key_phrases = []
    admission_terms = [
        'application deadline', 'admission requirements', 'gpa requirement',
        'test scores', 'financial aid', 'scholarship opportunities',
        'transfer credits', 'course prerequisites', 'tuition fees'
    ]

    for phrase in admission_terms:
        if phrase in text.lower():
            key_phrases.append(phrase)

    return key_phrases

def validate_file_type(filename: str) -> bool:
    """Validate if file type is supported"""
    allowed_extensions = {'.pdf', '.doc', '.docx', '.txt'}
    file_ext = '.' + filename.lower().split('.')[-1] if '.' in filename else ''
    return file_ext in allowed_extensions

def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text

    # Try to cut at sentence boundary
    truncated = text[:max_length]
    last_period = truncated.rfind('.')

    if last_period > max_length * 0.8:  # If we can cut at a sentence boundary
        return truncated[:last_period + 1]
    else:
        return truncated + "..."

class QueryProcessor:
    """Process and analyze user queries"""

    @staticmethod
    def preprocess_query(query: str) -> str:
        """Preprocess user query"""
        if not query:
            return ""

        # Clean and normalize
        query = clean_text(query)

        # Expand common abbreviations
        abbreviations = {
            'gpa': 'grade point average',
            'sat': 'scholastic assessment test',
            'act': 'american college testing',
            'fafsa': 'free application for federal student aid'
        }

        query_lower = query.lower()
        for abbr, full_form in abbreviations.items():
            query_lower = query_lower.replace(abbr, full_form)

        return query_lower

    @staticmethod
    def extract_intent(query: str) -> str:
        """Extract user intent from query"""
        query_lower = query.lower()

        # Define intent patterns
        intent_patterns = {
            'requirements': ['requirement', 'need', 'must have', 'prerequisite'],
            'deadlines': ['deadline', 'due date', 'when', 'by when'],
            'costs': ['cost', 'tuition', 'fee', 'price', 'expensive'],
            'process': ['how to', 'process', 'steps', 'procedure'],
            'programs': ['program', 'major', 'course', 'degree'],
            'financial_aid': ['financial aid', 'scholarship', 'grant', 'loan']
        }

        for intent, keywords in intent_patterns.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent

        return 'general'
