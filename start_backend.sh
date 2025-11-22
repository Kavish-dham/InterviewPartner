#!/bin/bash
# Backend Services Startup Script
# Run this in Terminal 1

cd "/Users/kavishdham/Desktop/Interview Partner"
source venv/bin/activate

echo "=========================================="
echo "Starting Backend Services"
echo "=========================================="
echo ""
echo "Starting API Gateway (port 8000)..."
python services/api-gateway/main.py &
GATEWAY_PID=$!
sleep 3

echo "Starting Interview Service (port 8001)..."
python services/interview-service/main.py &
INTERVIEW_PID=$!
sleep 2

echo "Starting Voice Service (port 8002)..."
python services/voice-service/main.py &
VOICE_PID=$!
sleep 2

echo ""
echo "=========================================="
echo "Backend Services Started"
echo "=========================================="
echo "API Gateway PID: $GATEWAY_PID (http://localhost:8000)"
echo "Interview Service PID: $INTERVIEW_PID (http://localhost:8001)"
echo "Voice Service PID: $VOICE_PID (http://localhost:8002)"
echo ""
echo "Health Check:"
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""
echo "Press Ctrl+C to stop all services"
echo "=========================================="

# Wait for interrupt
trap "kill $GATEWAY_PID $INTERVIEW_PID $VOICE_PID 2>/dev/null; exit" INT TERM
wait

