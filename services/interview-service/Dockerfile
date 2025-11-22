FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY services/interview-service/requirements.txt .
COPY requirements.txt ../

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r services/interview-service/requirements.txt

# Copy application code
COPY agents/ ../agents/
COPY utils/ ../utils/
COPY session.py ../
COPY services/shared/ ../services/shared/
COPY services/interview-service/ .

# Expose port
EXPOSE 8001

# Run service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

