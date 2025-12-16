# Use official Playwright image with Chromium preinstalled
FROM mcr.microsoft.com/playwright/python:v1.54.0-jammy

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUTF8=1

WORKDIR /app

# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app

# Simple CLI pipeline image
ENV RISK_LEVEL=medium
ENV RUN_PIPELINE_BEFORE_UPLOAD=true
ENV TOGETHER_MODEL="mistralai/Mistral-7B-Instruct-v0.1"

CMD sh -lc "python run_all_analysis.py"
