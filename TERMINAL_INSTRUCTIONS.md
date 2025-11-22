# Terminal Instructions

## Two Separate Terminals Required

### Terminal 1: Backend Services
```bash
cd "/Users/kavishdham/Desktop/Interview Partner"
./start_backend.sh
```

This will start:
- API Gateway on http://localhost:8000
- Interview Service on http://localhost:8001
- Voice Service on http://localhost:8002

**Or manually:**
```bash
cd "/Users/kavishdham/Desktop/Interview Partner"
source venv/bin/activate
python services/api-gateway/main.py &
python services/interview-service/main.py &
python services/voice-service/main.py &
```

### Terminal 2: Frontend
```bash
cd "/Users/kavishdham/Desktop/Interview Partner/frontend"
./start_frontend.sh
```

This will start:
- Next.js dev server on http://localhost:3000

**Or manually:**
```bash
cd "/Users/kavishdham/Desktop/Interview Partner/frontend"
npm run dev
```

## Quick Start Commands

### Terminal 1 (Backend):
```bash
cd "/Users/kavishdham/Desktop/Interview Partner"
source venv/bin/activate
./start_backend.sh
```

### Terminal 2 (Frontend):
```bash
cd "/Users/kavishdham/Desktop/Interview Partner/frontend"
./start_frontend.sh
```

## Verify Services

### Check Backend:
```bash
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health
```

### Check Frontend:
Open browser: http://localhost:3000

## Stop Services

### Backend:
Press `Ctrl+C` in Terminal 1, or:
```bash
pkill -f "python.*api-gateway"
pkill -f "python.*interview-service"
pkill -f "python.*voice-service"
```

### Frontend:
Press `Ctrl+C` in Terminal 2, or:
```bash
pkill -f "next dev"
```

## All Services Running

✅ Backend: http://localhost:8000 (API Gateway)
✅ Frontend: http://localhost:3000 (Next.js)

Open http://localhost:3000 in your browser to use the application!

