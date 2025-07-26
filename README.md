# Phone Comparer - AI-Powered Phone Comparison Assistant

A sophisticated multi-agent phone comparison system built with LangGraph, featuring intelligent out-of-domain detection, context-aware conversations, and comprehensive monitoring.

## Features

- **Multi-Agent Architecture**: Specialized agents for OOD detection and response generation
- **Context-Aware Conversations**: Maintains conversation history for natural follow-up questions
- **Intelligent OOD Detection**: Agent-based detection with conversation context
- **RAG Pipeline**: Vector-based retrieval with phone specifications
- **Real-time Monitoring**: Prometheus metrics and Grafana dashboards
- **Production-Ready**: Kubernetes deployment with proper logging and error handling

## Architecture

### Multi-Agent System (LangGraph)

The system uses a sophisticated multi-agent architecture built with LangGraph:

```
User Query → OOD Detection Agent → Response Generation Agent → Response
```

#### Agents:

1. **OOD Detection Agent** (`ood_detection_agent.py`)
   - Detects out-of-domain queries using LLM
   - Uses conversation context for intelligent detection
   - Prevents off-topic responses

2. **Response Generation Agent** (`response_agent.py`)
   - Generates phone-related responses using RAG
   - Maintains conversation context
   - Handles session management

3. **Graph Orchestrator** (`build_agent_graph.py`)
   - Manages agent communication
   - Handles state flow between agents
   - Ensures proper error handling

### RAG Pipeline

- **Data Ingestion**: Processes markdown files with phone specifications
- **Vector Store**: AstraDB for efficient document retrieval
- **Embedding Model**: BAAI/bge-base-en-v1.5 for semantic search
- **Retrieval**: Top-k document retrieval with history-aware context

### Context-Aware Conversations

- **Session Management**: LangChain's built-in chat history
- **Follow-up Support**: Natural conversation flow
- **Context Preservation**: Maintains comparison context across messages

## Monitoring & Observability

### Custom Metrics (Prometheus)

The system tracks comprehensive metrics:

- **`http_requests_total`**: Total HTTP requests
- **`model_response_total`**: Total model responses
- **`model_response_latency_seconds`**: Response time histograms
- **`out_of_domain_queries_total`**: OOD query tracking
- **`http_request_duration_seconds`**: Request duration tracking

### Monitoring Stack

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Custom Dashboards**: Real-time system monitoring

## 🛠Technology Stack

### Core Technologies
- **LangGraph**: Multi-agent orchestration
- **LangChain**: RAG pipeline and history management
- **Groq**: Fast LLM inference (llama-3.1-8b-instant)
- **AstraDB**: Vector database for document storage
- **Flask**: Web application framework

### Monitoring & Deployment
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Kubernetes**: Container orchestration
- **Docker**: Containerization

### Data & Storage
- **Markdown Files**: Phone specifications and features
- **Vector Embeddings**: Semantic search capabilities
- **Session Storage**: Conversation history management

## Project Structure

```
phone comparer/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── comparer/                # Core business logic
│   ├── __init__.py
│   ├── config.py            # Configuration management
│   ├── data_ingestion.py    # Data loading pipeline
│   ├── data_converter.py    # Data processing
│   ├── rag_chain.py         # RAG system
│   ├── ood_detection_agent.py   # OOD detection agent
│   ├── response_agent.py    # Response generation agent
│   ├── build_agent_graph.py # Graph orchestration
│   └── multi_agent_phone_system.py # System wrapper
├── utils/                   # Shared utilities
│   ├── logger.py           # Logging configuration
│   └── custom_exception.py # Custom exceptions
├── data/                   # Phone specifications
│   ├── apple/              # iPhone data
│   └── samsung/            # Samsung data
├── static/                 # CSS assets
├── templates/              # HTML templates
├── logs/                   # Application logs
└── deployment/             # Kubernetes manifests
    ├── flask-deployment.yaml
    ├── prometheus/
    └── grafana/
```

## Quick Start

### Prerequisites

- Python 3.8+
- Docker and Kubernetes (for deployment)
- AstraDB account
- Groq API key
- HuggingFace account

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd phone-comparer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Web UI: http://localhost:5001
   - Metrics: http://localhost:5001/metrics

### Production Deployment

1. **Build Docker image**
   ```bash
   docker build -t phone-comparer:latest .
   ```

2. **Deploy to Kubernetes**
   ```bash
   kubectl apply -f deployment/
   ```

3. **Access services**
   - Application: LoadBalancer IP
   - Grafana: http://cluster-ip:3000
   - Prometheus: http://cluster-ip:9090

## Usage Examples

### Basic Phone Comparison
```
User: "Compare iPhone 15 and Samsung S25"
Bot: [Detailed comparison with specs, features, and differences]
```

### Follow-up Questions
```
User: "What about the camera?"
Bot: [Context-aware camera comparison between iPhone 15 and Samsung S25]
```

### Feature-Specific Queries
```
User: "Which has better battery life?"
Bot: [Battery comparison with specific details]
```

## Configuration

### Environment Variables

```bash
# AstraDB Configuration
ASTRA_DB_API_ENDPOINT=your-astra-endpoint
ASTRA_DB_APPLICATION_TOKEN=your-token
ASTRA_DB_KEYSPACE=your-keyspace

# Groq API Configuration
GROQ_API_KEY=your-groq-key

# HuggingFace Configuration
HUGGINGFACEHUB_API_TOKEN=your-huggingface-key
HF_TOKEN=your-huggingface-key

# Model Configuration
MODEL_NAME=llama-3.1-8b-instant
EMBEDDING_MODEL=BAAI/bge-base-en-v1.5
```

### Monitoring Configuration

- **Prometheus**: Scrapes metrics every 15 seconds
- **Grafana**: Pre-configured dashboards for system monitoring
- **Custom Metrics**: Application-specific metrics for phone comparison analytics

## Key Features

### Multi-Agent Intelligence
- **Specialized Agents**: Each agent has a specific role
- **Intelligent Routing**: Automatic decision making
- **Context Preservation**: Maintains conversation state
- **Error Recovery**: Graceful handling of failures

### Advanced RAG Pipeline
- **Semantic Search**: Vector-based document retrieval
- **History Integration**: Conversation-aware responses
- **Dynamic Context**: Real-time context building

### Production Monitoring
- **Real-time Metrics**: Live system monitoring
- **Custom Dashboards**: Phone comparison analytics
- **Performance Tracking**: Response time optimization
