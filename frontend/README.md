# Interview Practice Partner - Frontend

Modern, responsive frontend for the Interview Practice System built with Next.js, React, TypeScript, TailwindCSS, and Material-UI.

## Features

- 🎨 Modern, Apple-style UI design
- 📱 Fully responsive (mobile, tablet, desktop)
- 🎤 Voice recording and transcription
- 📊 Real-time scoring and feedback
- 📈 Comprehensive final reports
- ♿ Accessible and keyboard-friendly

## Tech Stack

- **Next.js 14** (App Router)
- **React 18**
- **TypeScript**
- **TailwindCSS**
- **Material-UI (MUI)**
- **Axios** for API calls

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend services running (see main README)

### Installation

```bash
cd frontend
npm install
```

### Environment Setup

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── page.tsx           # Landing page
│   ├── upload/            # Resume & job description upload
│   ├── select-role/       # Interview type selection
│   ├── interview/         # Main interview screen
│   ├── feedback/          # Answer feedback display
│   ├── report/            # Final report summary
│   └── dashboard/         # Analytics dashboard
├── components/            # Reusable UI components
│   ├── Header.tsx
│   ├── QuestionCard.tsx
│   ├── VoiceRecorder.tsx
│   ├── ScoreDisplay.tsx
│   └── FeedbackPanel.tsx
├── lib/                  # Utilities
│   ├── api.ts            # API client
│   └── theme.ts          # MUI theme
└── public/              # Static assets
```

## Pages

### `/` - Landing Page
- Feature showcase
- How it works section
- CTA to start interview

### `/upload` - Upload Information
- Resume text input
- Job description input
- Form validation

### `/select-role` - Interview Type Selection
- Behavioral/Technical/Mixed options
- Creates session with backend
- Navigates to interview

### `/interview` - Interview Screen
- Question display with audio
- Text answer input
- Voice recording button
- Submit answer functionality
- Next question flow

### `/feedback` - Answer Feedback
- Score display
- Strengths and improvements
- Sample answers
- Navigation between answers

### `/report` - Final Report
- Overall score
- Detailed breakdown
- Key strengths/improvements
- Recommended topics
- Next focus areas

### `/dashboard` - Analytics (Placeholder)
- Session statistics
- Performance metrics
- Recent sessions

## API Integration

All API calls are handled through `lib/api.ts`:

```typescript
import { api } from '@/lib/api';

// Create session
const session = await api.createSession({
  resume: '...',
  job_description: '...',
  interview_type: 'Mixed'
});

// Start interview
const question = await api.startInterview(sessionId);

// Submit answer
await api.submitAnswer(sessionId, answer, true);

// Get next question
const nextQuestion = await api.getNextQuestion(sessionId);

// Evaluate all
const evaluations = await api.evaluateAll(sessionId);

// End interview
const report = await api.endInterview(sessionId);
```

## Voice Recording

The `VoiceRecorder` component:
- Uses browser MediaRecorder API
- Records audio from microphone
- Converts to base64
- Sends to backend for transcription
- Updates answer input with transcribed text

## Styling

- **TailwindCSS** for utility-first styling
- **Material-UI** for complex components
- Apple-style spacing and typography
- Responsive breakpoints: xs, sm, md, lg

## Build for Production

```bash
npm run build
npm start
```

## Backend Connection

The frontend connects to:
- **API Gateway**: `http://localhost:8000` (default)
- All endpoints prefixed with `/api/`
- WebSocket for real-time voice: `ws://localhost:8000/ws/{session_id}`

## Features in Detail

### Voice Integration
- Microphone access request
- Real-time recording
- Audio transcription via backend
- TTS audio playback for questions

### State Management
- Session storage for resume/job description
- Session ID persistence
- Question/answer state management

### Error Handling
- API error catching
- User-friendly error messages
- Loading states
- Form validation

## Development

```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint
npm run lint
```

## Notes

- All API calls are async/await
- Session data stored in sessionStorage
- Audio playback handled automatically
- Responsive design tested on mobile/tablet/desktop
- Accessible with proper ARIA labels

