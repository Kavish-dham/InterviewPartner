'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import VoiceInterview from '@/components/VoiceInterview';
import { Container, Box, Typography, Button, CircularProgress, Alert, Tabs, Tab } from '@mui/material';
import { api, Question } from '@/lib/api';

export default function InterviewPage() {
  const router = useRouter();
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [mode, setMode] = useState<'voice' | 'text'>('voice');

  useEffect(() => {
    const storedSessionId = sessionStorage.getItem('sessionId');
    if (!storedSessionId) {
      router.push('/select-role');
      return;
    }

    setSessionId(storedSessionId);
    startInterview(storedSessionId);
  }, [router]);

  const startInterview = async (sid: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const question = await api.startInterview(sid);
      setCurrentQuestion(question);
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail 
        ? (Array.isArray(err.response.data.detail) 
            ? err.response.data.detail.map((e: any) => e.msg || String(e)).join(', ')
            : err.response.data.detail)
        : err.message || 'Failed to start interview';
      setError(errorMsg);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnswerSubmit = async (answer: string) => {
    if (!answer.trim() || !sessionId) return;

    setIsLoading(true);
    setError(null);
    try {
      await api.submitAnswer(sessionId, answer, true);
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail 
        ? (Array.isArray(err.response.data.detail) 
            ? err.response.data.detail.map((e: any) => e.msg || String(e)).join(', ')
            : err.response.data.detail)
        : err.message || 'Failed to submit answer';
      setError(errorMsg);
      setIsLoading(false);
      throw err;
    }
  };

  const handleNextQuestion = async () => {
    if (!sessionId) return;

    setIsLoading(true);
    setError(null);
    try {
      const nextQuestion = await api.getNextQuestion(sessionId);
      setCurrentQuestion(nextQuestion);
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail 
        ? (Array.isArray(err.response.data.detail) 
            ? err.response.data.detail.map((e: any) => e.msg || String(e)).join(', ')
            : err.response.data.detail)
        : err.message || 'Failed to get next question';
      setError(errorMsg);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEndInterview = async () => {
    if (!sessionId) return;
    
    setIsLoading(true);
    try {
      // Evaluate all answers first
      await api.evaluateAll(sessionId);
      router.push('/report');
    } catch (err: any) {
      // Error message is already extracted by axios interceptor
      setError(err.message || 'Failed to end interview');
      setIsLoading(false);
    }
  };

  if (isLoading && !currentQuestion) {
    return (
      <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress size={60} />
          <Typography variant="h6" sx={{ mt: 2 }}>
            Starting interview...
          </Typography>
        </Box>
      </Box>
    );
  }

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50' }}>
      <Header />
      
      <Container maxWidth="lg" sx={{ py: 4 }}>
        {error && (
          <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h4" sx={{ fontWeight: 600 }}>
            Interview Session
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="outlined"
              onClick={() => router.push('/feedback')}
              disabled={isLoading}
              sx={{ textTransform: 'none' }}
            >
              View Feedback
            </Button>
            <Button
              variant="outlined"
              onClick={handleEndInterview}
              disabled={isLoading}
              sx={{ textTransform: 'none' }}
            >
              End Interview
            </Button>
          </Box>
        </Box>

        {currentQuestion && mode === 'voice' && (
          <VoiceInterview
            sessionId={sessionId!}
            currentQuestion={currentQuestion}
            onAnswerSubmit={handleAnswerSubmit}
            onNextQuestion={handleNextQuestion}
            isLoading={isLoading}
          />
        )}

        {isLoading && !currentQuestion && (
          <Box sx={{ textAlign: 'center', mt: 4 }}>
            <CircularProgress size={60} />
            <Typography variant="h6" sx={{ mt: 2 }}>
              {currentQuestion ? 'Processing...' : 'Starting interview...'}
            </Typography>
          </Box>
        )}
      </Container>
    </Box>
  );
}

