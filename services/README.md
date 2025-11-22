# Microservices Architecture - Interview Practice System

## Architecture Overview

This system is built as a scalable microservices architecture with three main services:

### Services

1. **API Gateway** (Port 8000)
   - Main entry point for all requests
   - WebSocket support for real-time voice interaction
   - Routes requests to appropriate services
   - Coordinates Interview and Voice services

2. **Interview Service** (Port 8001)
   - Core interview logic and session management
   - Question generation using agents
   - Answer evaluation and feedback
   - Session state management

3. **Voice Service** (Port 8002)
   - Speech-to-text using Whisper AI
   - Text-to-speech using pyttsx3
   - Audio processing and transcription

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Setup

1. **Start Interview Service:**
```bash
cd services/interview-service
pip install -r requirements.txt
python main.py
```

2. **Start Voice Service:**
```bash
cd services/voice-service
pip install -r requirements.txt
python main.py
```

3. **Start API Gateway:**
```bash
cd services/api-gateway
pip install -r requirements.txt
python main.py
```

## API Endpoints

### API Gateway (http://localhost:8000)

- `POST /api/sessions` - Create interview session
- `GET /api/sessions/{session_id}` - Get session status
- `POST /api/sessions/{session_id}/start` - Start interview
- `POST /api/sessions/{session_id}/submit-answer` - Submit answer
- `POST /api/sessions/{session_id}/next-question` - Get next question
- `POST /api/sessions/{session_id}/evaluate-all` - Evaluate all answers
- `POST /api/sessions/{session_id}/end` - End interview and get report
- `POST /api/voice/transcribe` - Transcribe audio
- `WebSocket /ws/{session_id}` - Real-time voice interaction
- `GET /health` - Health check

### Interview Service (http://localhost:8001)

- `POST /sessions` - Create session
- `GET /sessions/{session_id}` - Get session
- `POST /sessions/{session_id}/start` - Start interview
- `POST /sessions/{session_id}/submit-answer` - Submit answer
- `POST /sessions/{session_id}/evaluate-all` - Evaluate all
- `POST /sessions/{session_id}/end` - End interview
- `GET /health` - Health check

### Voice Service (http://localhost:8002)

- `POST /transcribe` - Transcribe audio file
- `POST /transcribe-base64` - Transcribe base64 audio
- `POST /synthesize` - Text-to-speech
- `GET /voices` - List available voices
- `GET /health` - Health check

## Usage Examples

### REST API Example

```python
import httpx

async with httpx.AsyncClient() as client:
    # Create session
    session = await client.post(
        "http://localhost:8000/api/sessions",
        json={
            "resume": "Your resume text",
            "job_description": "Job description text",
            "interview_type": "Mixed"
        }
    )
    session_id = session.json()["session_id"]
    
    # Start interview
    question = await client.post(f"http://localhost:8000/api/sessions/{session_id}/start")
    print(question.json()["question"])
    
    # Submit answer
    await client.post(
        f"http://localhost:8000/api/sessions/{session_id}/submit-answer",
        params={"collect_mode": True},
        json={"answer": "Your answer"}
    )
```

### WebSocket Example

```python
import asyncio
import websockets
import json

async def voice_interview():
    async with websockets.connect("ws://localhost:8000/ws/{session_id}") as ws:
        # Send audio data
        await ws.send(json.dumps({
            "type": "audio",
            "audio_data": base64_encoded_audio
        }))
        
        # Receive transcription
        response = await ws.recv()
        data = json.loads(response)
        print(f"Transcribed: {data['text']}")
```

## Voice Interaction Flow

1. **Setup**: User provides resume and job description (via REST API)
2. **Start**: Interview begins, first question is asked (with TTS audio)
3. **Iterative Collection**: 
   - User speaks answer (audio sent via WebSocket)
   - Audio transcribed using Whisper AI
   - Answer collected (not evaluated yet)
   - Next question asked
4. **Evaluation**: After interview ends, all answers evaluated
5. **Feedback**: Comprehensive feedback delivered via voice

## Scaling Considerations

- **Session Storage**: Currently in-memory. Use Redis for production
- **Voice Service**: Whisper model loads once per instance. Consider model caching
- **Load Balancing**: Use nginx or similar for API Gateway
- **Database**: Add PostgreSQL/MongoDB for session persistence
- **Message Queue**: Use RabbitMQ/Kafka for async processing
- **Caching**: Redis for frequently accessed data

## Environment Variables

```bash
# API Gateway
INTERVIEW_SERVICE_URL=http://interview-service:8001
VOICE_SERVICE_URL=http://voice-service:8002

# Interview Service
REDIS_URL=redis://localhost:6379  # Optional

# Voice Service
WHISPER_MODEL=base  # base, small, medium, large
```

## Development

```bash
# Run client example
python services/client-example.py

# Run with voice WebSocket
python services/client-example.py voice
```

## Production Deployment

1. Use environment variables for configuration
2. Add Redis for session management
3. Use proper secrets management
4. Add monitoring (Prometheus, Grafana)
5. Set up logging aggregation
6. Use Kubernetes for orchestration
7. Add API rate limiting
8. Implement authentication/authorization

