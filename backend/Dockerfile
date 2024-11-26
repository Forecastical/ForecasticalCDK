FROM --platform=linux/arm64 pytorch/pytorch:latest

WORKDIR /backend

# Install system dependencies
RUN apt-get update && \
    apt-get -y install libpq-dev gcc git ninja-build && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt --timeout=1000

# Copy the entire backend directory
COPY . .

EXPOSE 8000

# Use absolute path for PYTHONPATH in CMD
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]