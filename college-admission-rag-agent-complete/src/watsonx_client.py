"""
IBM watsonx.ai client for interacting with Granite models
"""

import os
import logging
from typing import Dict, Any, List
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.credentials import Credentials

logger = logging.getLogger(__name__)

class WatsonxClient:
    """Client for IBM watsonx.ai services"""

    def __init__(self):
        self.api_key = os.getenv('IBM_CLOUD_API_KEY')
        self.project_id = os.getenv('WATSONX_PROJECT_ID')
        self.url = os.getenv('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')
        self.model_id = os.getenv('MODEL_ID', 'ibm/granite-3-2b-instruct')

        if not self.api_key or not self.project_id:
            raise ValueError("IBM_CLOUD_API_KEY and WATSONX_PROJECT_ID must be set")

        self._initialize_model()

    def _initialize_model(self):
        """Initialize the Granite model"""
        try:
            credentials = Credentials(
                url=self.url,
                api_key=self.api_key
            )

            self.model = Model(
                model_id=self.model_id,
                credentials=credentials,
                project_id=self.project_id,
                params={
                    "decoding_method": "greedy",
                    "max_new_tokens": 500,
                    "temperature": 0.1,
                    "repetition_penalty": 1.0
                }
            )

            logger.info(f"Initialized model {self.model_id}")

        except Exception as e:
            logger.error(f"Failed to initialize watsonx model: {e}")
            raise

    def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate response using Granite model"""
        try:
            # Construct the prompt with context
            full_prompt = self._construct_prompt(prompt, context)

            # Generate response
            response = self.model.generate_text(prompt=full_prompt)

            return response.strip()

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble processing your request right now."

    def _construct_prompt(self, query: str, context: str) -> str:
        """Construct prompt for college admission queries"""
        prompt_template = """You are a College Admission Assistant powered by IBM Granite. You help prospective students with admission-related questions using official college information.

Context Information:
{context}

Student Question: {query}

Instructions:
1. Answer based on the provided context information
2. Be helpful, accurate, and professional
3. If information is not available in context, state that clearly
4. Provide specific details like deadlines, requirements, and procedures when available
5. Always be encouraging and supportive

Answer:"""

        return prompt_template.format(context=context, query=query)

    def is_connected(self) -> bool:
        """Check if connection to watsonx.ai is working"""
        try:
            # Simple test generation
            test_response = self.model.generate_text(prompt="Hello")
            return len(test_response) > 0
        except:
            return False
