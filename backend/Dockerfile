FROM --platform=linux/arm64 pytorch/pytorch:latest

WORKDIR /backend

# Install system dependencies
RUN apt-get update && \
    apt-get -y install libpq-dev gcc git ninja-build && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# 
# Dockerfile

# Copy model files from the backend/lib/ml/model directory into the container
# Dockerfile located inside backend/

# Copy model files from backend/lib/ml/model/ into the container
COPY lib/ml/model/activities_model.pkl /app/.lib/ml/model/activities_model.pkl
COPY lib/ml/model/clothing_model.pkl /app/.lib/ml/model/clothing_model.pkl
COPY lib/ml/model/tool_model.pkl /app/.lib/ml/model/tool_model.pkl
COPY lib/ml/synthetic_activities_data.csv /app/.lib/ml/synthetic_activities_data.csv

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt --timeout=1000

# Copy the entire backend directory
COPY . .

EXPOSE 8000

# Use absolute path for PYTHONPATH in CMD
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]