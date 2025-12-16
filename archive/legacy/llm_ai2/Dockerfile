# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for TensorFlow
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Set the entrypoint to run the hybrid model
ENTRYPOINT ["python", "scripts/run_final_hybrid.py"]

# Default command (can be overridden)
CMD []
