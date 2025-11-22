#!/bin/bash
# Detailed endpoint testing with full responses

echo "=========================================="
echo "DETAILED ENDPOINT TESTING"
echo "=========================================="
echo ""

# Test 1: Health Checks
echo "1. HEALTH CHECKS"
echo "-----------------"
echo "API Gateway:"
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""
echo "Interview Service:"
curl -s http://localhost:8001/health | python3 -m json.tool
echo ""
echo "Voice Service:"
curl -s http://localhost:8002/health | python3 -m json.tool
echo ""

# Test 2: Voice Service - List Voices
echo "2. VOICE SERVICE - LIST VOICES"
echo "-------------------------------"
curl -s http://localhost:8002/voices | python3 -m json.tool
echo ""

# Test 3: Voice Service - TTS
echo "3. VOICE SERVICE - TEXT TO SPEECH"
echo "----------------------------------"
TTS_RESPONSE=$(curl -s -X POST http://localhost:8002/synthesize \
    -H "Content-Type: application/json" \
    -d '{"text": "Hello, welcome to your interview practice session.", "speed": 1.0}')

echo "TTS Response (showing structure, audio data truncated):"
echo $TTS_RESPONSE | python3 -c "import sys, json; d=json.load(sys.stdin); d['audio_data']=d['audio_data'][:50]+'...' if len(d.get('audio_data',''))>50 else d.get('audio_data',''); print(json.dumps(d, indent=2))" 2>/dev/null || echo $TTS_RESPONSE
echo ""

# Test 4: Create Session
echo "4. CREATE INTERVIEW SESSION"
echo "---------------------------"
SESSION_RESPONSE=$(curl -s -X POST http://localhost:8000/api/sessions \
    -H "Content-Type: application/json" \
    -d '{
        "resume": "Software Engineer with 5 years experience in Python, AWS, Docker, and microservices. Led teams of 5+ engineers.",
        "job_description": "Senior Software Engineer requiring Python, cloud technologies, microservices architecture, and team leadership.",
        "interview_type": "Mixed"
    }')

echo $SESSION_RESPONSE | python3 -m json.tool
SESSION_ID=$(echo $SESSION_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['session_id'])" 2>/dev/null)
echo "Session ID: $SESSION_ID"
echo ""

# Test 5: Get Session Status
echo "5. GET SESSION STATUS"
echo "---------------------"
curl -s http://localhost:8000/api/sessions/$SESSION_ID | python3 -m json.tool
echo ""

# Test 6: Start Interview
echo "6. START INTERVIEW"
echo "------------------"
START_RESPONSE=$(curl -s -X POST http://localhost:8000/api/sessions/$SESSION_ID/start)
echo $START_RESPONSE | python3 -c "import sys, json; d=json.load(sys.stdin); d['audio']=d.get('audio','')[:50]+'...' if d.get('audio') and len(d.get('audio',''))>50 else d.get('audio',''); print(json.dumps(d, indent=2))" 2>/dev/null || echo $START_RESPONSE
echo ""

# Test 7: Submit Answer
echo "7. SUBMIT ANSWER (COLLECT MODE)"
echo "--------------------------------"
ANSWER_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/sessions/$SESSION_ID/submit-answer?collect_mode=true" \
    -H "Content-Type: application/json" \
    -d '{"answer": "I have 5 years of experience with Python, working on microservices architecture. I have led teams and delivered scalable cloud solutions using AWS services like EC2, S3, and Lambda."}')
echo $ANSWER_RESPONSE | python3 -m json.tool
echo ""

# Test 8: Get Next Question
echo "8. GET NEXT QUESTION"
echo "---------------------"
NEXT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/sessions/$SESSION_ID/next-question)
echo $NEXT_RESPONSE | python3 -c "import sys, json; d=json.load(sys.stdin); d['audio']=d.get('audio','')[:50]+'...' if d.get('audio') and len(d.get('audio',''))>50 else d.get('audio',''); print(json.dumps(d, indent=2))" 2>/dev/null || echo $NEXT_RESPONSE
echo ""

# Test 9: Submit Another Answer
echo "9. SUBMIT SECOND ANSWER"
echo "-----------------------"
ANSWER2_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/sessions/$SESSION_ID/submit-answer?collect_mode=true" \
    -H "Content-Type: application/json" \
    -d '{"answer": "In my previous role, I implemented a microservices architecture that improved system scalability by 300% and reduced deployment time by 50%."}')
echo $ANSWER2_RESPONSE | python3 -m json.tool
echo ""

# Test 10: Evaluate All
echo "10. EVALUATE ALL ANSWERS"
echo "-----------------------"
EVAL_RESPONSE=$(curl -s -X POST http://localhost:8000/api/sessions/$SESSION_ID/evaluate-all)
echo $EVAL_RESPONSE | python3 -m json.tool | head -50
echo ""

# Test 11: End Interview - Final Report
echo "11. END INTERVIEW - FINAL REPORT"
echo "---------------------------------"
REPORT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/sessions/$SESSION_ID/end)
echo $REPORT_RESPONSE | python3 -c "import sys, json; d=json.load(sys.stdin); d['audio_summary']=d.get('audio_summary','')[:50]+'...' if d.get('audio_summary') and len(d.get('audio_summary',''))>50 else d.get('audio_summary',''); print(json.dumps(d, indent=2))" 2>/dev/null || echo $REPORT_RESPONSE
echo ""

# Test 12: Voice Transcription (structure test)
echo "12. VOICE TRANSCRIPTION ENDPOINT (Structure Test)"
echo "--------------------------------------------------"
echo "Testing endpoint structure (will fail with invalid audio, but endpoint is accessible):"
curl -s -X POST http://localhost:8002/transcribe-base64 \
    -H "Content-Type: application/json" \
    -d '{"audio_data": "dGVzdA==", "audio_format": "wav"}' | python3 -m json.tool 2>/dev/null || echo "Endpoint accessible (requires valid audio for full test)"
echo ""

echo "=========================================="
echo "ALL TESTS COMPLETED"
echo "=========================================="

