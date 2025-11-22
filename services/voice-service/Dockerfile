FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY services/voice-service/requirements.txt .
COPY requirements.txt ../

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r services/voice-service/requirements.txt

# Copy application code
COPY services/shared/ ../services/shared/
COPY services/voice-service/ .

# Expose port
EXPOSE 8002

# Run service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]

