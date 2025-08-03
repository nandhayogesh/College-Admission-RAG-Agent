# Deployment Guide

## Docker Deployment

### Build Docker Image
```bash
docker build -t college-admission-rag .
```

### Run Container
```bash
docker run -p 5000:5000 --env-file .env college-admission-rag
```

## IBM Cloud Deployment

### Using Code Engine
1. Build and push image to IBM Container Registry
2. Deploy to Code Engine with environment variables
3. Configure custom domain if needed

### Environment Variables for Production
- Set `FLASK_ENV=production`
- Configure logging level
- Set secure secret key

## Scaling Considerations
- Use Redis for session storage
- Implement proper caching
- Consider using managed vector database
- Set up load balancing for high traffic
