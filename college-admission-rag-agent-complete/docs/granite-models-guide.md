# IBM Granite Models Integration Guide

## Overview
IBM Granite is a family of foundation models specifically designed for enterprise applications. This guide covers how to use Granite models with IBM Cloud Lite for the College Admission RAG Agent.

## Available Granite Models

### Granite 3.2 Series (Recommended for Lite)

#### granite-3-2b-instruct
- **Parameters**: 2 billion
- **Best for**: Lite accounts, efficient token usage
- **Capabilities**: 
  - Question answering
  - Text summarization
  - Content generation
  - Instruction following
- **Token efficiency**: High (optimal for free tier)

#### granite-3-8b-instruct  
- **Parameters**: 8 billion
- **Best for**: Higher quality responses
- **Capabilities**:
  - Complex reasoning
  - Detailed explanations
  - Multi-turn conversations
  - Advanced instruction following
- **Token efficiency**: Moderate (use carefully with free tier)

### Granite Vision Models

#### granite-vision-3-2-2b
- **Use case**: Image analysis and description
- **Integration**: For processing admission-related images/documents
- **Lite compatibility**: Limited usage recommended

## Model Configuration

### Environment Variables
```bash
# Primary model for text generation
MODEL_ID=ibm/granite-3-2b-instruct

# Alternative models for different use cases
FALLBACK_MODEL_ID=ibm/granite-3-8b-instruct
VISION_MODEL_ID=ibm/granite-vision-3-2-2b
```

### Python Integration
```python
from ibm_watsonx_ai.foundation_models import Model

# Initialize Granite model
model = Model(
    model_id="ibm/granite-3-2b-instruct",
    credentials=credentials,
    project_id=project_id,
    params={
        "decoding_method": "greedy",
        "max_new_tokens": 500,
        "temperature": 0.1,
        "repetition_penalty": 1.0
    }
)
```

## Prompt Engineering for Granite

### Best Practices

#### Structure Your Prompts
```python
prompt_template = '''You are a College Admission Assistant powered by IBM Granite.

Context: {context}
Question: {question}

Instructions:
1. Use only the provided context information
2. Be helpful and professional
3. If information is not available, say so clearly
4. Provide specific details when available

Answer:'''
```

#### Token Optimization
- **Be specific**: Clear, focused prompts get better results
- **Use templates**: Consistent structure improves efficiency
- **Limit context**: Include only relevant information
- **Set max tokens**: Control response length

### College Admission Specific Prompts

#### Admission Requirements
```python
requirements_prompt = '''Based on the admission information provided, what are the requirements for {program}?

Context: {context}

Please list:
1. Academic requirements (GPA, test scores)
2. Required documents
3. Application deadlines
4. Any special requirements

Answer:'''
```

#### Financial Information
```python
financial_prompt = '''Using the provided financial information, what are the costs for attending this college?

Context: {context}

Please provide:
1. Tuition and fees
2. Room and board costs
3. Additional expenses
4. Financial aid options

Answer:'''
```

## Performance Optimization

### Token Management
```python
def optimize_prompt(query, context, max_context_tokens=1000):
    # Truncate context if too long
    if len(context.split()) > max_context_tokens:
        words = context.split()[:max_context_tokens]
        context = ' '.join(words) + '...'

    return construct_prompt(query, context)
```

### Response Caching
```python
import hashlib
import json

class ResponseCache:
    def __init__(self):
        self.cache = {}

    def get_cache_key(self, query, context):
        content = f"{query}:{context}"
        return hashlib.md5(content.encode()).hexdigest()

    def get_response(self, query, context):
        key = self.get_cache_key(query, context)
        return self.cache.get(key)

    def set_response(self, query, context, response):
        key = self.get_cache_key(query, context)
        self.cache[key] = response
```

## Error Handling

### Quota Management
```python
def handle_quota_exceeded():
    return {
        'response': '''I've reached my processing limit for now. Here are some general admission tips:

        1. Check application deadlines early
        2. Prepare required documents in advance
        3. Contact the admissions office directly for specific questions
        4. Visit the college website for the most current information

        Please try again later or contact admissions directly.''',
        'sources': [],
        'confidence': 0.0
    }
```

### Fallback Responses
```python
def get_fallback_response(query):
    if 'deadline' in query.lower():
        return "Please check the college website or contact admissions for current deadlines."
    elif 'cost' in query.lower() or 'tuition' in query.lower():
        return "For current tuition and fee information, please visit the college's financial aid office."
    else:
        return "I don't have specific information about that. Please contact the admissions office."
```

## Monitoring and Analytics

### Usage Tracking
```python
import time
from datetime import datetime

class UsageTracker:
    def __init__(self):
        self.usage_log = []

    def log_request(self, query, tokens_used, response_time):
        self.usage_log.append({
            'timestamp': datetime.now().isoformat(),
            'query': query[:100],  # First 100 chars for privacy
            'tokens_used': tokens_used,
            'response_time': response_time
        })

    def get_daily_usage(self):
        today = datetime.now().date()
        today_usage = [
            log for log in self.usage_log 
            if datetime.fromisoformat(log['timestamp']).date() == today
        ]
        return sum(log['tokens_used'] for log in today_usage)
```

### Performance Metrics
```python
def calculate_metrics():
    return {
        'average_response_time': sum(log['response_time'] for log in usage_log) / len(usage_log),
        'total_tokens_used': sum(log['tokens_used'] for log in usage_log),
        'queries_per_day': len([log for log in usage_log if is_today(log['timestamp'])]),
        'most_common_topics': analyze_query_topics(usage_log)
    }
```

## Advanced Features

### Multi-Model Strategy
```python
class GraniteModelManager:
    def __init__(self):
        self.primary_model = "ibm/granite-3-2b-instruct"
        self.advanced_model = "ibm/granite-3-8b-instruct"
        self.token_budget = 1000  # Monthly limit for lite account

    def select_model(self, query_complexity):
        if self.token_budget > 200 and query_complexity > 0.7:
            return self.advanced_model
        return self.primary_model
```

### Context-Aware Responses
```python
def enhance_context(query, documents):
    # Prioritize relevant sections
    scored_chunks = []
    for doc in documents:
        for chunk in doc['chunks']:
            relevance = calculate_relevance(query, chunk['text'])
            scored_chunks.append((chunk, relevance))

    # Sort by relevance and take top chunks
    top_chunks = sorted(scored_chunks, key=lambda x: x[1], reverse=True)[:5]
    return ' '.join([chunk[0]['text'] for chunk in top_chunks])
```

## Best Practices Summary

### For IBM Cloud Lite Users
1. **Start with granite-3-2b-instruct** for development
2. **Monitor token usage** closely
3. **Implement caching** for common queries
4. **Use efficient prompts** to minimize tokens
5. **Set up usage alerts** in IBM Cloud console

### For Production Deployment
1. **Test thoroughly** with lite account first
2. **Implement graceful degradation** for quota limits
3. **Monitor performance** and optimize continuously
4. **Plan for scaling** when ready to upgrade
5. **Maintain fallback responses** for service interruptions

---

**Remember**: IBM Granite models are designed for enterprise use but work excellently within IBM Cloud Lite constraints for development and small-scale deployments.
