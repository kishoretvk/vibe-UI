# Vibe-UI: AI-Powered Data Analysis Platform

Vibe-UI is transforming from a simple data visualization tool into a sophisticated AI-powered data analysis platform with storytelling capabilities, advanced charting, and scheduled reporting features.

## Architecture Overview

The application follows a microservices architecture with a React/TypeScript frontend and multiple Python backend services orchestrated through Docker.

### Frontend
- **Framework**: React 19.x with TypeScript
- **Styling**: Tailwind CSS with shadcn/ui components
- **Charting**: Chart.js as primary library with selective D3.js integration
- **State Management**: React Context API

### Backend Services
1. **AI Analysis Service** - Handles AI-powered data analysis and storytelling
2. **Data Processing Service** - Manages data cleaning, transformation, and processing
3. **Reporting Service** - Generates and manages reports
4. **Notification Service** - Handles notifications and alerts
5. **LLM Integration Service** - Manages integration with various LLM providers
6. **Cache Service** - Provides caching capabilities
7. **Scheduling Service** - Manages scheduled tasks and reports
8. **User Management Service** - Handles user authentication and authorization
9. **Data Generator Service** - Generates sample data for demos

### Data Integration
- **Relational Databases**: MySQL, PostgreSQL, SQL Server, Oracle
- **NoSQL Databases**: MongoDB, Redis, Cassandra
- **File Formats**: CSV, Excel, JSON, Parquet, Avro
- **APIs**: REST, GraphQL, SOAP, OData
- **Cloud Services**: AWS S3, Google Cloud Storage, Azure Blob Storage, Snowflake, BigQuery
- **Streaming**: Apache Kafka, Apache Pulsar, Amazon Kinesis, Azure Event Hubs

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+
- Python 3.11+

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vibe-ui
   ```

2. **Start the services**
   ```bash
   docker-compose up
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - API Gateway: http://localhost:80

### Development Setup

1. **Frontend Development**
   ```bash
   cd src
   npm install
   npm start
   ```

2. **Backend Development**
   Each service can be developed independently:
   ```bash
   cd backend/ai-analysis-service
   pip install -r requirements.txt
   python app.py
   ```

## Project Structure

```
vibe-ui/
├── backend/
│   ├── ai-analysis-service/
│   ├── data-processing-service/
│   ├── reporting-service/
│   ├── notification-service/
│   ├── llm-integration-service/
│   ├── cache-service/
│   ├── scheduling-service/
│   ├── user-management-service/
│   ├── data-generator-service/
│   └── shared/
├── src/
│   ├── components/
│   │   ├── ui/
│   │   ├── data/
│   │   ├── views/
│   │   └── utility/
│   ├── contexts/
│   ├── hooks/
│   ├── services/
│   ├── types/
│   ├── utils/
│   └── assets/
├── docker-compose.yml
└── README.md
```

## Sample Datasets

The application includes sample datasets for demonstration:
1. **Finance Dataset**: Revenue and expense data with anomalies
2. **E-commerce Dataset**: Sales and customer data
3. **Healthcare Dataset**: Patient and treatment data
4. **Marketing Dataset**: Campaign and engagement data

## Features

### AI-Powered Analysis
- Natural language querying of data
- Automated storytelling and insights generation
- Anomaly detection and explanation
- Trend analysis and forecasting
- Data correlation analysis

### Advanced Visualization
- Multiple chart types (bar, line, pie, scatter, etc.)
- Interactive dashboards with drill-down capabilities
- Custom visualization templates
- Export options (PDF, PNG, CSV)
- Real-time data visualization

### Reporting System
- Drag-and-drop report builder
- Customizable report templates
- Scheduled report generation
- Multi-channel delivery (email, Slack, etc.)
- Parameterized reports

### Data Integration
- Connect to multiple data sources
- Data quality assessment tools
- Automated data cleaning and validation
- Data transformation pipelines
- Real-time data streaming

## Testing

The project includes comprehensive testing strategies:
- Unit tests for all components and services
- Integration tests for service communication
- Load testing for performance validation
- Security testing for vulnerability assessment

## Deployment

The application can be deployed using:
- Docker Compose for development and small-scale production
- Kubernetes for large-scale production deployments
- Cloud platforms (AWS, GCP, Azure) with container orchestration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please open an issue on the repository.