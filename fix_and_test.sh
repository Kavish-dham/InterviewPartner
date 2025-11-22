#!/bin/bash
# Fix and test all endpoints

echo "=== Fixing and Testing Interview Practice System ==="
echo ""

# Kill existing services
echo "1. Stopping existing services..."
pkill -f "python.*api-gateway/main.py"
pkill -f "python.*interview-service/main.py"
pkill -f "python.*voice-service/main.py"
sleep 2

# Start services
echo "2. Starting services..."
cd "/Users/kavishdham/Desktop/Interview Partner"
source venv/bin/activate

# Start in background
python services/api-gateway/main.py > /tmp/api-gateway.log 2>&1 &
GATEWAY_PID=$!
sleep 3

python services/interview-service/main.py > /tmp/interview-service.log 2>&1 &
INTERVIEW_PID=$!
sleep 2

python services/voice-service/main.py > /tmp/voice-service.log 2>&1 &
VOICE_PID=$!
sleep 2

echo "Services started (PIDs: Gateway=$GATEWAY_PID, Interview=$INTERVIEW_PID, Voice=$VOICE_PID)"
echo ""

# Wait for services to be ready
echo "3. Waiting for services to be ready..."
for i in {1..10}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✓ Services are ready!"
        break
    fi
    sleep 1
done

# Test endpoints
echo ""
echo "4. Testing endpoints..."

# Test PDF endpoint
echo -n "Testing PDF parsing... "
PDF_TEST=$(curl -s -X POST http://localhost:8000/api/parse-pdf \
    -H "Content-Type: application/json" \
    -d '{"file_data": "JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFszIDAgUl0KL0NvdW50IDEKPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1BhcmVudCAyIDAgUgovTWVkaWFCb3ggWzAgMCA2MTIgNzkyXQovUmVzb3VyY2VzIDw8Ci9Gb250IDw8Ci9GMSA8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EKPj4KPj4KPj4KZW5kb2JqCnhyZWYKMCA0CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAwOSAwMDAwMCBuIAowMDAwMDAwMDU4IDAwMDAwIG4gCjAwMDAwMDAxMTUgMDAwMDAgbiAKdHJhaWxlcgo8PAovU2l6ZSA0Ci9Sb290IDEgMCBSCj4+CnN0YXJ0eHJlZgoxNDUKJSVFT0Y=", "file_name": "test.pdf"}')

if echo "$PDF_TEST" | grep -q "text"; then
    echo "✓ PASS"
else
    echo "✗ FAIL"
    echo "Response: $PDF_TEST"
fi

# Test transcription endpoint
echo -n "Testing voice transcription... "
# Create minimal WAV file (silence)
WAV_B64="UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAAB9AAACABAAZGF0YQAAAAA="
TRANS_TEST=$(curl -s -X POST http://localhost:8000/api/voice/transcribe \
    -H "Content-Type: application/json" \
    -d "{\"audio_data\": \"$WAV_B64\", \"audio_format\": \"wav\"}")

if echo "$TRANS_TEST" | grep -q "text\|confidence"; then
    echo "✓ PASS"
else
    echo "✗ FAIL"
    echo "Response: $TRANS_TEST"
fi

echo ""
echo "=== Test Complete ==="
echo "Services are running. Check logs:"
echo "  Gateway: tail -f /tmp/api-gateway.log"
echo "  Interview: tail -f /tmp/interview-service.log"
echo "  Voice: tail -f /tmp/voice-service.log"

