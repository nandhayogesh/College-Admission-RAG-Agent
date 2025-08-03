import unittest
from unittest.mock import Mock, patch
from src.rag_engine import RAGEngine

class TestRAGEngine(unittest.TestCase):
    def setUp(self):
        self.mock_watsonx = Mock()
        self.mock_doc_manager = Mock()
        self.rag_engine = RAGEngine(self.mock_watsonx, self.mock_doc_manager)

    def test_process_query(self):
        # Test basic query processing
        query = "What are admission requirements?"
        result = self.rag_engine.process_query(query)

        self.assertIn('answer', result)
        self.assertIn('sources', result)
        self.assertIn('confidence', result)

if __name__ == '__main__':
    unittest.main()
