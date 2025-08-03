# IBM Cloud Lite Setup Guide for College Admission RAG Agent

## Overview
This guide walks you through setting up IBM Cloud Lite services specifically for the College Admission RAG Agent. All services used are available in IBM Cloud's free tier.

## Step 1: Create IBM Cloud Lite Account

### Sign Up Process
1. Visit [IBM Cloud Registration](https://cloud.ibm.com/registration)
2. Fill in your details:
   - Email address
   - First and Last name
   - Country/Region
3. Verify your email address
4. Complete account setup

### Account Benefits (Lite Tier)
- **No credit card required** for Lite services
- **Never expires** - Lite services don't have time limits
- **Free tier** - Access to 40+ services with Lite plans
- **Resource limits** - Reasonable usage limits for development

## Step 2: Access watsonx.ai

### Enable watsonx.ai Service
1. Log into [IBM Cloud Console](https://cloud.ibm.com)
2. Go to "Catalog" → "AI" → "watsonx.ai"
3. Select the **Lite plan** (free tier)
4. Click "Create" to provision the service

### watsonx.ai Lite Features
- Access to IBM Granite foundation models
- **Free tier limits:**
  - 1,000 tokens per month for text generation
  - Basic model access including Granite-2B models
  - Prompt Lab access
  - Model deployment capabilities

## Step 3: Create watsonx.ai Project

### Project Setup
1. Navigate to [watsonx.ai Platform](https://dataplatform.cloud.ibm.com/wx/home)
2. Click "Create Project"
3. Choose "Empty Project"
4. Enter project details:
   - Name: "College Admission RAG"
   - Description: "RAG system for college admission queries"
5. Click "Create"

### Project Configuration
1. Go to "Services" → "Associate Service"
2. Select your watsonx.ai instance
3. Note your **Project ID** from the project settings

## Step 4: Generate API Credentials

### Create API Key
1. In IBM Cloud Console, go to "Manage" → "Access (IAM)"
2. Click "API Keys" → "Create"
3. Enter description: "College Admission RAG API Key"
4. Click "Create"
5. **Copy and save the API key** (you can't retrieve it later)

### Service Credentials
Your application needs these credentials:
- **IBM_CLOUD_API_KEY**: The API key you just created
- **WATSONX_PROJECT_ID**: From your watsonx.ai project
- **WATSONX_URL**: Regional endpoint (usually us-south.ml.cloud.ibm.com)

## Step 5: Configure Application

### Environment Setup
1. Copy `.env.example` to `.env`
2. Fill in your credentials:
```bash
IBM_CLOUD_API_KEY=your_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
MODEL_ID=ibm/granite-3-2b-instruct
```

### Test Connection
Run the health check to verify setup:
```bash
python -c "from src.watsonx_client import WatsonxClient; client = WatsonxClient(); print('✅ Connection successful!' if client.is_connected() else '❌ Connection failed')"
```

## Available IBM Granite Models (Lite Compatible)

### Granite 3.2 Models (Recommended for Lite)
- **granite-3-2b-instruct**: 2B parameter model, efficient for lite usage
- **granite-3-8b-instruct**: 8B parameter model, more capable but uses more tokens

### Model Selection Tips
- Use **2B models** for Lite accounts to maximize token usage
- **8B models** provide better responses but consume tokens faster
- Monitor usage in IBM Cloud billing dashboard

## Monitoring Usage (Important for Lite Accounts)

### Token Tracking
1. Go to IBM Cloud Console → "Billing and Usage"
2. Monitor watsonx.ai service usage
3. Set up spending alerts (optional)

### Usage Optimization
- **Shorter prompts**: Reduce token consumption
- **Caching responses**: Store common answers locally
- **Batch processing**: Group similar queries
- **Fallback responses**: Use local responses when quota exceeded

## Upgrading from Lite

### When to Upgrade
- Exceeding monthly token limits
- Need for more advanced models
- Higher concurrency requirements
- Production deployment needs

### Upgrade Options
- **Pay-as-you-go**: Pay only for what you use above free tier
- **Subscription plans**: Fixed monthly rates for predictable usage
- **Enterprise plans**: Custom pricing for large deployments

## Troubleshooting

### Common Issues

#### Authentication Errors
- **Symptom**: 401 Unauthorized errors
- **Solution**: Verify API key is correct and has watsonx.ai access
- **Check**: Ensure API key hasn't expired

#### Quota Exceeded
- **Symptom**: 429 Too Many Requests errors
- **Solution**: Wait for quota reset or upgrade plan
- **Check**: Monitor usage in IBM Cloud console

#### Model Not Found
- **Symptom**: Model ID not found errors
- **Solution**: Verify model ID spelling and availability in your region
- **Check**: Use `ibm/granite-3-2b-instruct` for Lite accounts

#### Connection Timeouts
- **Symptom**: Request timeout errors
- **Solution**: Check network connectivity and IBM Cloud status
- **Check**: Try different regional endpoints

## Best Practices for Lite Accounts

### Resource Management
1. **Monitor usage** regularly through IBM Cloud console
2. **Implement caching** to reduce API calls
3. **Use efficient prompts** to minimize token usage
4. **Set usage alerts** to avoid unexpected charges

### Development Strategy
1. **Start with Lite** for development and testing
2. **Optimize locally** before deploying
3. **Test with sample data** to estimate usage
4. **Plan for scaling** when ready for production

### Security
1. **Protect API keys** - never commit to version control
2. **Use environment variables** for all credentials
3. **Implement rate limiting** to prevent abuse
4. **Monitor access logs** for unusual activity

## Support Resources

### Documentation
- [IBM Cloud Lite Documentation](https://cloud.ibm.com/docs/account?topic=account-accounts)
- [watsonx.ai Documentation](https://dataplatform.cloud.ibm.com/docs/content/wsj/getting-started/welcome-main.html)
- [IBM Granite Models Guide](https://www.ibm.com/granite)

### Community Support
- [IBM Developer Community](https://developer.ibm.com/communities/)
- [Stack Overflow - IBM watsonx](https://stackoverflow.com/questions/tagged/ibm-watsonx)
- [GitHub Issues](https://github.com/IBM/watsonx-ai-samples/issues)

### Getting Help
1. Check documentation first
2. Search community forums
3. Contact IBM Cloud support (available for Lite accounts)
4. File GitHub issues for code-specific problems

---

**Remember**: IBM Cloud Lite services are perfect for development, learning, and small-scale deployments. The College Admission RAG Agent is designed to work efficiently within Lite tier limits while providing full functionality.
