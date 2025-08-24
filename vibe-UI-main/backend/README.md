# Backend Services

This directory contains the microservices architecture for the Vibe-UI backend.

## Services

1. **ai-analysis-service** - Handles AI-powered data analysis and storytelling
2. **data-processing-service** - Manages data cleaning, transformation, and processing
3. **reporting-service** - Generates and manages reports
4. **notification-service** - Handles notifications and alerts
5. **llm-integration-service** - Manages integration with various LLM providers
6. **cache-service** - Provides caching capabilities
7. **scheduling-service** - Manages scheduled tasks and reports
8. **user-management-service** - Handles user authentication and authorization
9. **data-generator-service** - Generates sample data for demos (current app.py functionality)
10. **shared** - Shared libraries and utilities used across services

## Getting Started

Each service is containerized and can be run independently or together using Docker Compose.

```bash
# Start all services
docker-compose up

# Start specific service
docker-compose up ai-analysis-service
```