# Frontend Setup Guide

## Quick Start

```bash
cd frontend
npm install
npm run dev
```

## If npm install fails

```bash
# Clear npm cache
npm cache clean --force

# Or use yarn instead
yarn install
yarn dev
```

## Environment Setup

1. Create `.env.local` file:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

2. Make sure backend services are running:
```bash
# In project root
source venv/bin/activate
python services/api-gateway/main.py &
python services/interview-service/main.py &
python services/voice-service/main.py &
```

## Run Frontend

```bash
cd frontend
npm run dev
```

Open http://localhost:3000

## Project Structure

- `app/` - Next.js pages (App Router)
- `components/` - Reusable React components
- `lib/` - API client and utilities

## Pages Flow

1. `/` - Landing page
2. `/upload` - Upload resume & job description
3. `/select-role` - Choose interview type
4. `/interview` - Main interview screen
5. `/feedback` - View feedback after answers
6. `/report` - Final comprehensive report
7. `/dashboard` - Analytics (placeholder)

## Features

✅ All pages connected to backend
✅ Voice recording integration
✅ Real-time question display
✅ Answer submission
✅ Feedback display
✅ Final report with scores
✅ Responsive design
✅ Material-UI components
✅ TailwindCSS styling

