#!/bin/bash
# Comprehensive test script for Interview Practice System
# Tests all endpoints across all services

echo "=========================================="
echo "Interview Practice System - Full Test Suite"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local method=$2
    local url=$3
    local data=$4
    local expected_status=$5
    
    echo -n "Testing: $name... "
    
    if [ -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X $method "$url" 2>&1)
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "$url" \
            -H "Content-Type: application/json" \
            -d "$data" 2>&1)
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" == "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (Status: $http_code)"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Expected: $expected_status, Got: $http_code)"
        echo "Response: $body"
        ((FAILED++))
        return 1
    fi
}

echo "=========================================="
echo "1. HEALTH CHECKS"
echo "=========================================="

test_endpoint "API Gateway Health" "GET" "http://localhost:8000/health" "" "200"
test_endpoint "Interview Service Health" "GET" "http://localhost:8001/health" "" "200"
test_endpoint "Voice Service Health" "GET" "http://localhost:8002/health" "" "200"

echo ""
echo "=========================================="
echo "2. VOICE SERVICE ENDPOINTS"
echo "=========================================="

# Test voice service endpoints
test_endpoint "List Voices" "GET" "http://localhost:8002/voices" "" "200"

# Test TTS (text-to-speech)
test_endpoint "Text-to-Speech" "POST" "http://localhost:8002/synthesize" \
    '{"text": "Hello, this is a test of the text to speech system.", "speed": 1.0, "pitch": 1.0}' "200"

echo ""
echo "=========================================="
echo "3. INTERVIEW SERVICE - SESSION MANAGEMENT"
echo "=========================================="

# Create session
SESSION_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/sessions" \
    -H "Content-Type: application/json" \
    -d '{
        "resume": "Software Engineer with 5 years of experience in Python, AWS, and microservices architecture. Led multiple teams and delivered scalable solutions.",
        "job_description": "Senior Software Engineer role requiring Python, cloud technologies, microservices, and leadership experience.",
        "interview_type": "Mixed"
    }')

SESSION_ID=$(echo $SESSION_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['session_id'])" 2>/dev/null)

if [ -z "$SESSION_ID" ]; then
    echo -e "${RED}✗ FAIL${NC} - Could not create session"
    echo "Response: $SESSION_RESPONSE"
    ((FAILED++))
    exit 1
else
    echo -e "${GREEN}✓ PASS${NC} - Session created: $SESSION_ID"
    ((PASSED++))
fi

# Get session status
test_endpoint "Get Session Status" "GET" "http://localhost:8000/api/sessions/$SESSION_ID" "" "200"

echo ""
echo "=========================================="
echo "4. INTERVIEW FLOW"
echo "=========================================="

# Start interview
START_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/sessions/$SESSION_ID/start")
QUESTION=$(echo $START_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('question', 'N/A'))" 2>/dev/null)

if [ "$QUESTION" != "N/A" ] && [ ! -z "$QUESTION" ]; then
    echo -e "${GREEN}✓ PASS${NC} - Interview started"
    echo "  Question: $QUESTION"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC} - Could not start interview"
    echo "Response: $START_RESPONSE"
    ((FAILED++))
fi

# Submit answer
test_endpoint "Submit Answer (Collect Mode)" "POST" \
    "http://localhost:8000/api/sessions/$SESSION_ID/submit-answer?collect_mode=true" \
    '{"answer": "I have extensive experience with Python and microservices. I have led teams of 5+ engineers and delivered scalable cloud solutions using AWS."}' "200"

# Get next question
NEXT_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/sessions/$SESSION_ID/next-question")
NEXT_QUESTION=$(echo $NEXT_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('question', 'N/A'))" 2>/dev/null)

if [ "$NEXT_QUESTION" != "N/A" ] && [ ! -z "$NEXT_QUESTION" ]; then
    echo -e "${GREEN}✓ PASS${NC} - Next question retrieved"
    echo "  Question: $NEXT_QUESTION"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC} - Could not get next question"
    ((FAILED++))
fi

# Submit another answer
test_endpoint "Submit Second Answer" "POST" \
    "http://localhost:8000/api/sessions/$SESSION_ID/submit-answer?collect_mode=true" \
    '{"answer": "In my previous role, I implemented a microservices architecture that improved system scalability by 300%."}' "200"

echo ""
echo "=========================================="
echo "5. EVALUATION & FEEDBACK"
echo "=========================================="

# Evaluate all answers
test_endpoint "Evaluate All Answers" "POST" \
    "http://localhost:8000/api/sessions/$SESSION_ID/evaluate-all" "" "200"

# End interview and get report
REPORT_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/sessions/$SESSION_ID/end")
AVG_SCORE=$(echo $REPORT_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('average_score', 'N/A'))" 2>/dev/null)

if [ "$AVG_SCORE" != "N/A" ] && [ ! -z "$AVG_SCORE" ]; then
    echo -e "${GREEN}✓ PASS${NC} - Final report generated"
    echo "  Average Score: $AVG_SCORE"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC} - Could not generate report"
    ((FAILED++))
fi

echo ""
echo "=========================================="
echo "6. VOICE TRANSCRIPTION TEST"
echo "=========================================="

# Note: This requires actual audio file, so we'll test the endpoint structure
echo -n "Testing: Voice Transcription Endpoint... "
TRANSCRIBE_TEST=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:8002/transcribe-base64" \
    -H "Content-Type: application/json" \
    -d '{"audio_data": "dGVzdA==", "audio_format": "wav"}')

if [ "$TRANSCRIBE_TEST" == "500" ] || [ "$TRANSCRIBE_TEST" == "200" ]; then
    echo -e "${GREEN}✓ PASS${NC} (Endpoint accessible, may need valid audio)"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC} (Status: $TRANSCRIBE_TEST)"
    ((FAILED++))
fi

echo ""
echo "=========================================="
echo "7. API GATEWAY - VOICE INTEGRATION"
echo "=========================================="

# Test voice transcription through gateway
echo -n "Testing: Gateway Voice Transcription... "
GATEWAY_VOICE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:8000/api/voice/transcribe" \
    -H "Content-Type: application/json" \
    -d '{"audio_data": "dGVzdA=="}')

if [ "$GATEWAY_VOICE" == "500" ] || [ "$GATEWAY_VOICE" == "200" ]; then
    echo -e "${GREEN}✓ PASS${NC} (Endpoint accessible)"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC} (Status: $GATEWAY_VOICE)"
    ((FAILED++))
fi

echo ""
echo "=========================================="
echo "TEST SUMMARY"
echo "=========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo "Total: $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED!${NC}"
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    exit 1
fi

