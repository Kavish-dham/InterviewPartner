# How to Run the Interview Practice System

## Quick Start Guide

### Option 1: Run Services Manually (Current Setup)

All services are already running in the background. You can access them at:

#### Service URLs:
- **API Gateway**: http://localhost:8000
- **Interview Service**: http://localhost:8001  
- **Voice Service**: http://localhost:8002
- **API Documentation**: http://localhost:8000/docs (Swagger UI)

#### To Restart Services:

```bash
cd "/Users/kavishdham/Desktop/Interview Partner"
source venv/bin/activate

# Terminal 1: Interview Service
python services/interview-service/main.py

# Terminal 2: Voice Service  
python services/voice-service/main.py

# Terminal 3: API Gateway
python services/api-gateway/main.py
```

### Option 2: Using Docker Compose

```bash
cd "/Users/kavishdham/Desktop/Interview Partner"
docker-compose up --build
```

## How to Use the System

### 1. Web Browser (Swagger UI - Easiest)

Open your browser and go to:
```
http://localhost:8000/docs
```

This provides an interactive API interface where you can:
- Create sessions
- Start interviews
- Submit answers
- Get feedback
- All with a visual interface!

### 2. Command Line (cURL)

#### Create a Session:
```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "resume": "Your resume text here",
    "job_description": "Job description text here",
    "interview_type": "Mixed"
  }'
```

#### Start Interview:
```bash
curl -X POST http://localhost:8000/api/sessions/{session_id}/start
```

#### Submit Answer:
```bash
curl -X POST "http://localhost:8000/api/sessions/{session_id}/submit-answer?collect_mode=true" \
  -H "Content-Type: application/json" \
  -d '{"answer": "Your answer here"}'
```

#### Get Next Question:
```bash
curl -X POST http://localhost:8000/api/sessions/{session_id}/next-question
```

#### End Interview & Get Report:
```bash
curl -X POST http://localhost:8000/api/sessions/{session_id}/evaluate-all
curl -X POST http://localhost:8000/api/sessions/{session_id}/end
```

### 3. Python Client

Run the example client:
```bash
cd "/Users/kavishdham/Desktop/Interview Partner"
source venv/bin/activate
python services/client-example.py
```

### 4. WebSocket for Real-Time Voice

Connect via WebSocket for voice interaction:

```python
import asyncio
import websockets
import json

async def voice_interview():
    session_id = "your-session-id"
    async with websockets.connect(f"ws://localhost:8000/ws/{session_id}") as ws:
        # Send audio data
        await ws.send(json.dumps({
            "type": "audio",
            "audio_data": base64_encoded_audio
        }))
        
        # Receive transcription
        response = await ws.recv()
        print(json.loads(response))

asyncio.run(voice_interview())
```

### 5. Create a Simple Web Interface

You can create an HTML file to interact with the API:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Interview Practice</title>
</head>
<body>
    <h1>Interview Practice System</h1>
    <div id="app">
        <button onclick="createSession()">Start Interview</button>
        <div id="question"></div>
        <input type="text" id="answer" placeholder="Your answer">
        <button onclick="submitAnswer()">Submit</button>
    </div>
    
    <script>
        let sessionId = null;
        
        async function createSession() {
            const response = await fetch('http://localhost:8000/api/sessions', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    resume: "Your resume",
                    job_description: "Job description",
                    interview_type: "Mixed"
                })
            });
            const data = await response.json();
            sessionId = data.session_id;
            startInterview();
        }
        
        async function startInterview() {
            const response = await fetch(`http://localhost:8000/api/sessions/${sessionId}/start`, {
                method: 'POST'
            });
            const data = await response.json();
            document.getElementById('question').textContent = data.question;
        }
        
        async function submitAnswer() {
            const answer = document.getElementById('answer').value;
            await fetch(`http://localhost:8000/api/sessions/${sessionId}/submit-answer?collect_mode=true`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({answer: answer})
            });
            getNextQuestion();
        }
        
        async function getNextQuestion() {
            const response = await fetch(`http://localhost:8000/api/sessions/${sessionId}/next-question`, {
                method: 'POST'
            });
            const data = await response.json();
            document.getElementById('question').textContent = data.question;
            document.getElementById('answer').value = '';
        }
    </script>
</body>
</html>
```

## Testing the System

### Health Check:
```bash
curl http://localhost:8000/health
```

### Check All Services:
```bash
curl http://localhost:8000/health
curl http://localhost:8001/health  
curl http://localhost:8002/health
```

## Troubleshooting

### Services Not Running?
```bash
# Check if ports are in use
lsof -i :8000
lsof -i :8001
lsof -i :8002

# Kill processes if needed
kill -9 <PID>
```

### Restart All Services:
```bash
# Stop all Python processes
pkill -f "python.*main.py"

# Restart
cd "/Users/kavishdham/Desktop/Interview Partner"
source venv/bin/activate
python services/interview-service/main.py &
python services/voice-service/main.py &
python services/api-gateway/main.py &
```

## Recommended: Use Swagger UI

The easiest way to interact with the system is through the Swagger UI:

1. Open browser
2. Go to: http://localhost:8000/docs
3. Try out all endpoints interactively
4. See request/response formats
5. Test the API without writing code

This is the best way to explore and test the system!

