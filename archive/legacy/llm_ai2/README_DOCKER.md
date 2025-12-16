# Docker Containerization Guide

## 🐳 Running the Hybrid Stock Market Prediction System in Docker

This guide shows you how to containerize and run the AI stock market hybrid prediction system using Docker.

## 📋 Prerequisites

- Docker Desktop installed and running
- At least 4GB RAM available for TensorFlow
- Internet connection for downloading base images

## 🚀 Quick Start

### 1. Build the Docker Image

```bash
# Windows (PowerShell/CMD)
docker build -t stock-market-hybrid-ai .

# Linux/Mac
docker build -t stock-market-hybrid-ai .
```

### 2. Run with Demo Data

```bash
docker run --rm stock-market-hybrid-ai
```

### 3. Run with Custom Inputs

```bash
# Custom macro data and text
docker run --rm stock-market-hybrid-ai \
  --macro-json '{"inflation_rate":3.1,"interest_rate":5.25,"unemployment_rate":4.1,"GDP_growth":2.0,"sp500_index":4500}' \
  --text "Tech earnings strong, healthcare investment up"

# Custom text only (uses demo macro data)
docker run --rm stock-market-hybrid-ai \
  --text "Oil prices surge, tech stocks decline"
```

## 🛠️ Advanced Usage

### Interactive Mode

```bash
# Get help
docker run -it stock-market-hybrid-ai --help

# Interactive shell
docker run -it --entrypoint /bin/bash stock-market-hybrid-ai
```

### Using Docker Compose

```bash
# Build and run with docker-compose
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

### Volume Mounts

```bash
# Mount models directory for persistence
docker run --rm -v $(pwd)/models:/app/models stock-market-hybrid-ai

# Mount logs directory
docker run --rm -v $(pwd)/logs:/app/logs stock-market-hybrid-ai
```

## 📁 Project Structure in Container

```
/app/
├── hybrid/                 # Hybrid model logic
├── tier3/                  # Core MLP and LLM modules
├── models/                 # Trained MLP models (mounted)
├── scripts/                # CLI scripts
├── logs/                   # Output logs (mounted)
└── requirements.txt        # Python dependencies
```

## 🔧 Customization

### Environment Variables

```bash
# Set Python unbuffered mode
docker run --rm -e PYTHONUNBUFFERED=1 stock-market-hybrid-ai

# Set custom API keys (if needed)
docker run --rm -e TOGETHER_API_KEY=your_key stock-market-hybrid-ai
```

### Resource Limits

```bash
# Limit memory usage
docker run --rm --memory=4g stock-market-hybrid-ai

# Limit CPU usage
docker run --rm --cpus=2.0 stock-market-hybrid-ai
```

## 📊 Example Outputs

### Demo Run
```json
{
  "direction": "DOWN",
  "sectors": ["Technology", "Healthcare"],
  "companies": ["AAPL", "MSFT", "NVDA", "JNJ", "PFE", "UNH"],
  "explanation": "Positive market indicators suggest favorable sentiment.",
  "sector_explanation": "Technology: tech sector performance with market sentiment influence; top companies: AAPL, MSFT, NVDA. Healthcare: stable healthcare demand with defensive characteristics; top companies: JNJ, PFE, UNH."
}
```

### Custom Input Run
```bash
docker run --rm stock-market-hybrid-ai \
  --macro-json '{"inflation_rate":2.5,"interest_rate":4.0,"unemployment_rate":3.8,"GDP_growth":2.1,"sp500_index":4500}' \
  --text "Federal Reserve signals rate cuts, inflation cools"
```

## 🚨 Troubleshooting

### Common Issues

1. **Out of Memory**: Increase Docker memory limit to 4GB+
2. **Model Loading Errors**: Ensure models directory is properly mounted
3. **API Connection Issues**: Check internet connectivity and API keys
4. **Permission Errors**: Run with appropriate user permissions

### Debug Mode

```bash
# Run with verbose output
docker run --rm -e PYTHONUNBUFFERED=1 stock-market-hybrid-ai --text "test"

# Check container logs
docker logs <container_id>
```

### Cleanup

```bash
# Remove all containers
docker container prune

# Remove all images
docker image prune -a

# Remove all volumes
docker volume prune
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Test Docker Image

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: docker build -t stock-market-hybrid-ai .
      - name: Test Docker image
        run: docker run --rm stock-market-hybrid-ai --help
```

## 📈 Production Deployment

### Multi-stage Build (Optional)

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
ENTRYPOINT ["python", "scripts/run_final_hybrid.py"]
```

### Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import tensorflow as tf; print('OK')" || exit 1
```

## 🎯 Next Steps

1. **Deploy to Cloud**: AWS ECS, Google Cloud Run, Azure Container Instances
2. **Orchestration**: Kubernetes, Docker Swarm
3. **Monitoring**: Prometheus, Grafana, ELK Stack
4. **Security**: Image scanning, secret management, network policies

---

**Happy Containerizing! 🐳📈**
