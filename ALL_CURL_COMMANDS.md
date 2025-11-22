# Complete cURL Command Reference

## ✅ All Endpoints Tested and Working

### 1. Health Checks

```bash
# API Gateway
curl http://localhost:8000/health

# Interview Service
curl http://localhost:8001/health

# Voice Service
curl http://localhost:8002/health
```

### 2. Voice Service Endpoints

#### List Available Voices
```bash
curl http://localhost:8002/voices
```

#### Text-to-Speech (TTS)
```bash
curl -X POST http://localhost:8002/synthesize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, welcome to your interview practice session.",
    "speed": 1.0,
    "pitch": 1.0
  }'
```

#### Speech-to-Text (STT) - File Upload
```bash
curl -X POST http://localhost:8002/transcribe \
  -F "file=@your_audio.wav" \
  -F "language=en"
```

#### Speech-to-Text (STT) - Base64
```bash
curl -X POST http://localhost:8002/transcribe-base64 \
  -H "Content-Type: application/json" \
  -d '{
    "audio_data": "base64_encoded_audio_here",
    "audio_format": "wav",
    "language": "en"
  }'
```

### 3. Interview Service - Complete Flow

#### Step 1: Create Session
```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "resume": "Software Engineer with 5 years of experience in Python, AWS, and microservices architecture. Led multiple teams and delivered scalable solutions.",
    "job_description": "Senior Software Engineer role requiring Python, cloud technologies, microservices, and leadership experience.",
    "interview_type": "Mixed"
  }'
```

**Response:**
```json
{
  "session_id": "uuid-here",
  "status": "created",
  "question_count": 0,
  "answer_count": 0
}
```

#### Step 2: Get Session Status
```bash
SESSION_ID="your-session-id-here"
curl http://localhost:8000/api/sessions/$SESSION_ID
```

#### Step 3: Start Interview
```bash
curl -X POST http://localhost:8000/api/sessions/$SESSION_ID/start
```

**Response includes:**
- Question text
- Question number
- Question type
- **Audio (base64)** - TTS audio of the question

#### Step 4: Submit Answer (Collect Mode - Iterative)
```bash
curl -X POST "http://localhost:8000/api/sessions/$SESSION_ID/submit-answer?collect_mode=true" \
  -H "Content-Type: application/json" \
  -d '{
    "answer": "I have 5 years of experience with Python, working on microservices architecture. I have led teams and delivered scalable cloud solutions using AWS services."
  }'
```

#### Step 5: Get Next Question
```bash
curl -X POST http://localhost:8000/api/sessions/$SESSION_ID/next-question
```

**Response includes:**
- Next question text
- **Audio (base64)** - TTS audio of the question

#### Step 6: Submit More Answers (Repeat Steps 4-5)
```bash
# Submit answer
curl -X POST "http://localhost:8000/api/sessions/$SESSION_ID/submit-answer?collect_mode=true" \
  -H "Content-Type: application/json" \
  -d '{"answer": "Your answer here"}'

# Get next question
curl -X POST http://localhost:8000/api/sessions/$SESSION_ID/next-question
```

#### Step 7: Evaluate All Collected Answers
```bash
curl -X POST http://localhost:8000/api/sessions/$SESSION_ID/evaluate-all
```

**Response:**
```json
{
  "session_id": "...",
  "evaluations": [
    {
      "question": "...",
      "answer": "...",
      "scores": {
        "clarity": 7.5,
        "communication": 8.0,
        "star_structure": 7.0,
        "role_relevance": 8.0,
        "technical_depth": 7.5,
        "overall": 7.6
      },
      "feedback": {
        "strengths": [...],
        "improvements": [...],
        "sample_answer": "..."
      }
    }
  ],
  "total_evaluated": 2
}
```

#### Step 8: End Interview & Get Final Report
```bash
curl -X POST http://localhost:8000/api/sessions/$SESSION_ID/end
```

**Response:**
```json
{
  "session_id": "...",
  "average_score": 7.2,
  "detailed_scores": {
    "clarity": 7.0,
    "communication": 7.5,
    "star_structure": 7.0,
    "role_relevance": 8.0,
    "technical_depth": 7.5,
    "overall": 7.2
  },
  "key_strengths": [...],
  "key_improvements": [...],
  "recommended_topics": [...],
  "next_focus": "...",
  "total_questions": 5,
  "total_answers": 5,
  "audio_summary": "base64_audio_here"
}
```

### 4. API Gateway - Voice Integration

#### Transcribe Audio via Gateway
```bash
curl -X POST http://localhost:8000/api/voice/transcribe \
  -H "Content-Type: application/json" \
  -d '{
    "audio_data": "base64_encoded_audio"
  }'
```

### 5. Complete Interview Example (One Script)

```bash
#!/bin/bash

# Create session
SESSION_RESPONSE=$(curl -s -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "resume": "Software Engineer with 5 years experience",
    "job_description": "Senior Software Engineer role",
    "interview_type": "Mixed"
  }')

SESSION_ID=$(echo $SESSION_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['session_id'])")

echo "Session ID: $SESSION_ID"

# Start interview
echo "Starting interview..."
curl -s -X POST http://localhost:8000/api/sessions/$SESSION_ID/start | python3 -m json.tool

# Submit answer 1
echo "Submitting answer 1..."
curl -s -X POST "http://localhost:8000/api/sessions/$SESSION_ID/submit-answer?collect_mode=true" \
  -H "Content-Type: application/json" \
  -d '{"answer": "I have extensive experience with Python and microservices."}'

# Get question 2
echo "Getting question 2..."
curl -s -X POST http://localhost:8000/api/sessions/$SESSION_ID/next-question | python3 -m json.tool

# Submit answer 2
echo "Submitting answer 2..."
curl -s -X POST "http://localhost:8000/api/sessions/$SESSION_ID/submit-answer?collect_mode=true" \
  -H "Content-Type: application/json" \
  -d '{"answer": "In my previous role, I led a team that improved system performance."}'

# Evaluate all
echo "Evaluating all answers..."
curl -s -X POST http://localhost:8000/api/sessions/$SESSION_ID/evaluate-all | python3 -m json.tool

# Get final report
echo "Getting final report..."
curl -s -X POST http://localhost:8000/api/sessions/$SESSION_ID/end | python3 -m json.tool
```

## Test Results Summary

✅ **All Services**: Healthy and Operational
✅ **Voice TTS**: Working (generates audio)
✅ **Voice STT**: Working (requires valid audio)
✅ **Session Management**: Working
✅ **Interview Flow**: Complete
✅ **Answer Collection**: Working (iterative mode)
✅ **Evaluation System**: Working
✅ **Final Reports**: Working with audio summary

## Quick Test Commands

```bash
# Quick health check
curl http://localhost:8000/health && echo ""

# Quick session test
SESSION=$(curl -s -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"resume":"Test","job_description":"Test","interview_type":"Mixed"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['session_id'])")

curl -X POST http://localhost:8000/api/sessions/$SESSION/start
```

## WebSocket Connection (Voice)

For real-time voice interaction, connect to:
```
ws://localhost:8000/ws/{session_id}
```

Send messages:
```json
{
  "type": "audio",
  "audio_data": "base64_encoded_audio"
}
```

Or commands:
```json
{
  "type": "command",
  "command": "next_question"
}
```

