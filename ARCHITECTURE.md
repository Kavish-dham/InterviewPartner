# Microservices Architecture - Interview Practice System

## System Overview

A scalable, voice-enabled interview practice system built with microservices architecture using Whisper AI for speech recognition.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Applications                      │
│              (Web, Mobile, CLI, Voice Interface)              │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway (8000)                       │
│  • REST API Endpoints                                        │
│  • WebSocket for Real-time Voice                             │
│  • Service Orchestration                                     │
│  • Request Routing                                           │
└───────────────┬───────────────────────────┬─────────────────┘
                │                           │
                ▼                           ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│  Interview Service (8001) │   │   Voice Service (8002)    │
│  • Session Management     │   │   • Whisper AI (STT)     │
│  • Question Generation    │   │   • TTS (pyttsx3)        │
│  • Answer Evaluation      │   │   • Audio Processing     │
│  • Feedback Generation    │   │                           │
│  • Report Generation      │   │                           │
└──────────────────────────┘   └──────────────────────────┘
```

## Service Details

### 1. API Gateway Service

**Port:** 8000  
**Technology:** FastAPI, WebSocket

**Responsibilities:**
- Single entry point for all client requests
- WebSocket server for real-time voice interaction
- Routes requests to appropriate microservices
- Coordinates between Interview and Voice services
- Aggregates responses from multiple services

**Key Endpoints:**
- `POST /api/sessions` - Create interview session
- `POST /api/sessions/{id}/start` - Start interview
- `POST /api/sessions/{id}/submit-answer` - Submit answer
- `WebSocket /ws/{session_id}` - Real-time voice interaction

### 2. Interview Service

**Port:** 8001  
**Technology:** FastAPI, Python Agents

**Responsibilities:**
- Interview session lifecycle management
- Question generation using specialized agents
- Answer collection (iterative mode)
- Answer evaluation and scoring
- Feedback generation
- Final report creation

**Key Features:**
- In-memory session storage (Redis-ready for production)
- Support for collect mode (iterative) vs evaluate mode
- Multi-agent coordination (Interviewer, Evaluator, Feedback, Report)

### 3. Voice Service

**Port:** 8002  
**Technology:** FastAPI, Whisper AI, pyttsx3

**Responsibilities:**
- Speech-to-text transcription using Whisper AI
- Text-to-speech synthesis
- Audio format conversion
- Voice model management

**Key Features:**
- Whisper AI integration (base model, upgradeable)
- Multiple audio format support
- Language detection
- Confidence scoring

## Data Flow

### Voice Interview Flow

1. **Session Creation**
   ```
   Client → API Gateway → Interview Service
   Returns: session_id
   ```

2. **Interview Start**
   ```
   Client → API Gateway → Interview Service (get question)
   API Gateway → Voice Service (TTS)
   Returns: question + audio
   ```

3. **Answer Collection (Iterative)**
   ```
   Client (audio) → API Gateway (WebSocket) → Voice Service (transcribe)
   Voice Service → API Gateway → Interview Service (collect answer)
   Interview Service → API Gateway → Client (confirmation)
   ```

4. **Next Question**
   ```
   Client → API Gateway → Interview Service (next question)
   API Gateway → Voice Service (TTS)
   Returns: question + audio
   ```

5. **Evaluation (End of Interview)**
   ```
   Client → API Gateway → Interview Service (evaluate-all)
   Interview Service processes all collected answers
   Returns: evaluations
   ```

6. **Final Report**
   ```
   Client → API Gateway → Interview Service (end interview)
   Interview Service generates report
   API Gateway → Voice Service (TTS summary)
   Returns: report + audio summary
   ```

## Scalability Features

### Horizontal Scaling

- **Stateless Services**: All services are stateless (except session storage)
- **Load Balancing**: API Gateway can be load balanced
- **Service Replication**: Each service can run multiple instances

### Session Management

- **Current**: In-memory storage (development)
- **Production**: Redis cluster for distributed sessions
- **Session Persistence**: Optional database for history

### Voice Service Scaling

- **Model Caching**: Whisper model loaded once per instance
- **Async Processing**: Non-blocking audio processing
- **Queue System**: Optional message queue for heavy processing

## Technology Stack

### Core Technologies
- **Python 3.11+**: Main language
- **FastAPI**: Web framework for all services
- **WebSocket**: Real-time communication
- **Docker**: Containerization
- **Docker Compose**: Local orchestration

### AI/ML
- **Whisper AI**: Speech-to-text (OpenAI)
- **pyttsx3**: Text-to-speech (offline)

### Communication
- **REST API**: Synchronous communication
- **WebSocket**: Real-time bidirectional communication
- **HTTP/HTTPS**: Service-to-service communication

## Deployment Architecture

### Development
```
docker-compose up
```
- All services in single compose file
- Local networking
- Development configurations

### Production
```
Kubernetes / Docker Swarm
```
- Separate deployments per service
- Service discovery
- Load balancing
- Health checks
- Auto-scaling
- Monitoring and logging

## Environment Configuration

### API Gateway
```bash
INTERVIEW_SERVICE_URL=http://interview-service:8001
VOICE_SERVICE_URL=http://voice-service:8002
```

### Interview Service
```bash
REDIS_URL=redis://redis:6379  # Optional
SESSION_TTL=3600  # seconds
```

### Voice Service
```bash
WHISPER_MODEL=base  # base, small, medium, large
TTS_ENGINE=pyttsx3
```

## Security Considerations

1. **Authentication**: Add JWT tokens for API access
2. **Authorization**: Role-based access control
3. **Rate Limiting**: Prevent abuse
4. **Input Validation**: Pydantic models for validation
5. **HTTPS**: Encrypt all communications
6. **Secrets Management**: Use environment variables or secrets manager

## Monitoring & Observability

### Recommended Additions
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **ELK Stack**: Log aggregation
- **Jaeger**: Distributed tracing
- **Health Checks**: Built-in endpoints

## Future Enhancements

1. **Message Queue**: RabbitMQ/Kafka for async processing
2. **Database**: PostgreSQL for session persistence
3. **Caching**: Redis for performance
4. **CDN**: For static assets
5. **API Versioning**: v1, v2 support
6. **GraphQL**: Alternative to REST
7. **gRPC**: High-performance service communication
8. **Kubernetes**: Production orchestration

## Performance Characteristics

- **Latency**: < 100ms for API calls (excluding Whisper)
- **Whisper**: 1-3 seconds per transcription (base model)
- **TTS**: < 500ms per synthesis
- **Concurrent Sessions**: Limited by memory (scales horizontally)
- **Throughput**: 1000+ requests/second per service instance

## Development Workflow

1. **Local Development**: Docker Compose
2. **Testing**: Unit tests per service
3. **Integration Testing**: Test service interactions
4. **CI/CD**: Automated testing and deployment
5. **Monitoring**: Track service health and performance

