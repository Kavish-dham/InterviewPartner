# Quick Start - Microservices Architecture

## Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)
- 4GB+ RAM (Whisper model needs memory)

## Quick Start with Docker

```bash
# Navigate to project directory
cd "/Users/kavishdham/Desktop/Interview Partner"

# Start all services
docker-compose up --build

# Services will be available at:
# - API Gateway: http://localhost:8000
# - Interview Service: http://localhost:8001
# - Voice Service: http://localhost:8002
```

## Test the System

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Create a Session
```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "resume": "Software Engineer with 5 years experience",
    "job_description": "Senior Software Engineer role",
    "interview_type": "Mixed"
  }'
```

### 3. Start Interview
```bash
curl -X POST http://localhost:8000/api/sessions/{session_id}/start
```

### 4. Submit Answer
```bash
curl -X POST "http://localhost:8000/api/sessions/{session_id}/submit-answer?collect_mode=true" \
  -H "Content-Type: application/json" \
  -d '{"answer": "Your answer here"}'
```

## Python Client Example

```bash
# Run REST API example
python services/client-example.py

# Run WebSocket voice example
python services/client-example.py voice
```

## WebSocket Voice Interaction

Connect to WebSocket for real-time voice:

```python
import websockets
import json

async with websockets.connect("ws://localhost:8000/ws/{session_id}") as ws:
    # Send audio
    await ws.send(json.dumps({
        "type": "audio",
        "audio_data": base64_encoded_audio
    }))
    
    # Receive transcription
    response = await ws.recv()
    print(json.loads(response))
```

## Service URLs

- **API Gateway**: http://localhost:8000
- **Interview Service**: http://localhost:8001  
- **Voice Service**: http://localhost:8002
- **API Docs**: http://localhost:8000/docs (Swagger UI)

## Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Troubleshooting

### Whisper Model Download
First run will download Whisper model (~150MB). This may take time.

### Port Conflicts
If ports are in use, modify `docker-compose.yml` port mappings.

### Memory Issues
Whisper needs RAM. If issues occur:
- Use smaller model: Set `WHISPER_MODEL=base` in voice service
- Increase Docker memory limit

### Service Not Starting
Check logs:
```bash
docker-compose logs interview-service
docker-compose logs voice-service
docker-compose logs api-gateway
```

