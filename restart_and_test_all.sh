#!/bin/bash
echo "=== Restarting All Services and Testing ==="

# Kill all services
pkill -f "python.*api-gateway"
pkill -f "python.*interview-service"
pkill -f "python.*voice-service"
sleep 3

cd "/Users/kavishdham/Desktop/Interview Partner"
source venv/bin/activate

# Start services
echo "Starting services..."
python services/api-gateway/main.py > /tmp/gateway.log 2>&1 &
sleep 4

python services/interview-service/main.py > /tmp/interview.log 2>&1 &
sleep 2

python services/voice-service/main.py > /tmp/voice.log 2>&1 &
sleep 2

# Wait for health
for i in {1..10}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✓ Services ready"
        break
    fi
    sleep 1
done

# Test endpoints
echo ""
echo "Testing PDF endpoint..."
curl -s -X POST http://localhost:8000/api/parse-pdf \
    -H "Content-Type: application/json" \
    -d '{"file_data": "JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFszIDAgUl0KL0NvdW50IDEKPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1BhcmVudCAyIDAgUgovTWVkaWFCb3ggWzAgMCA2MTIgNzkyXQovUmVzb3VyY2VzIDw8Ci9Gb250IDw8Ci9GMSA8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEKL0Jhc2VGb250IC9IZWx2ZXRpY2EKPj4KPj4KPj4KZW5kb2JqCnhyZWYKMCA0CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAwOSAwMDAwMCBuIAowMDAwMDAwMDU4IDAwMDAwIG4gCjAwMDAwMDAxMTUgMDAwMDAgbiAKdHJhaWxlcgo8PAovU2l6ZSA0Ci9Sb290IDEgMCBSCj4+CnN0YXJ0eHJlZgoxNDUKJSVFT0Y=", "file_name": "test.pdf"}' | python3 -m json.tool

echo ""
echo "Testing transcription endpoint..."
curl -s -X POST http://localhost:8000/api/voice/transcribe \
    -H "Content-Type: application/json" \
    -d '{"audio_data": "UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAAB9AAACABAAZGF0YQAAAAA=", "audio_format": "wav"}' | python3 -m json.tool

echo ""
echo "=== Done ==="

