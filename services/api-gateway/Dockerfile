FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY services/api-gateway/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services/shared/ ../services/shared/
COPY services/api-gateway/ .

# Expose port
EXPOSE 8000

# Run service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

