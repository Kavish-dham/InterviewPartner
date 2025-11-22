'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import ScoreDisplay from '@/components/ScoreDisplay';
import FeedbackPanel from '@/components/FeedbackPanel';
import { Container, Box, Typography, Button, Card, CardContent, CircularProgress } from '@mui/material';
import { ArrowForward, ArrowBack } from '@mui/icons-material';
import { api, Evaluation } from '@/lib/api';

export default function FeedbackPage() {
  const router = useRouter();
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [evaluations, setEvaluations] = useState<Evaluation[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const storedSessionId = sessionStorage.getItem('sessionId');
    if (!storedSessionId) {
      router.push('/interview');
      return;
    }

    setSessionId(storedSessionId);
    loadEvaluations(storedSessionId);
  }, [router]);

  const loadEvaluations = async (sid: string) => {
    try {
      const result = await api.evaluateAll(sid);
      // Transform evaluations to match expected format
      const transformed = result.evaluations.map((evaluation: any) => ({
        question: evaluation.question,
        answer: evaluation.answer,
        scores: evaluation.scores || {},
        feedback: typeof evaluation.feedback === 'string' 
          ? parseFeedbackString(evaluation.feedback)
          : evaluation.feedback || { strengths: [], improvements: [], sample_answer: '' },
      }));
      setEvaluations(transformed);
    } catch (error) {
      console.error('Error loading evaluations:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const parseFeedbackString = (feedbackStr: string) => {
    const strengths: string[] = [];
    const improvements: string[] = [];
    let sampleAnswer = '';

    if (!feedbackStr) {
      return { strengths, improvements, sample_answer: sampleAnswer };
    }

    const lines = feedbackStr.split('\n');
    let currentSection = '';
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      
      if (!line) continue;

      // Detect section headers
      if (line.toLowerCase().includes('strength') && !line.toLowerCase().includes('improve')) {
        currentSection = 'strengths';
        continue;
      } else if (line.toLowerCase().includes('improve') || line.toLowerCase().includes('area')) {
        currentSection = 'improvements';
        continue;
      } else if (line.toLowerCase().includes('sample') || line.toLowerCase().includes('example')) {
        currentSection = 'sample';
        continue;
      }

      // Parse bullet points
      if (line.startsWith('•') || line.startsWith('-') || line.startsWith('*')) {
        const text = line.substring(1).trim();
        if (text) {
          if (currentSection === 'strengths') {
            strengths.push(text);
          } else if (currentSection === 'improvements') {
            improvements.push(text);
          }
        }
      } else if (currentSection === 'sample' && line) {
        // Collect sample answer text
        if (line.toLowerCase().includes('sample') || line.toLowerCase().includes('example')) {
          continue; // Skip header line
        }
        sampleAnswer += line + '\n';
      } else if (currentSection === 'strengths' && line && !line.toLowerCase().includes('strength')) {
        // Try to extract strengths even without bullets
        if (line.length > 10) {
          strengths.push(line);
        }
      } else if (currentSection === 'improvements' && line && !line.toLowerCase().includes('improve')) {
        // Try to extract improvements even without bullets
        if (line.length > 10) {
          improvements.push(line);
        }
      }
    }

    return {
      strengths: strengths.length > 0 ? strengths : ['Good attempt at answering the question'],
      improvements: improvements.length > 0 ? improvements : ['Provide more specific examples and details'],
      sample_answer: sampleAnswer.trim() || 'Consider structuring your answer using the STAR method (Situation, Task, Action, Result) with specific examples from your experience.',
    };
  };

  const handleNext = () => {
    if (currentIndex < evaluations.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      router.push('/report');
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  if (isLoading) {
    return (
      <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (evaluations.length === 0) {
    return (
      <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50' }}>
        <Header />
        <Container maxWidth="lg" sx={{ py: 6, textAlign: 'center' }}>
          <Typography variant="h5" sx={{ mb: 2 }}>
            No evaluations available
          </Typography>
          <Button variant="contained" onClick={() => router.push('/interview')}>
            Go to Interview
          </Button>
        </Container>
      </Box>
    );
  }

  const currentEval = evaluations[currentIndex];

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50' }}>
      <Header />
      
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography variant="h4" sx={{ fontWeight: 600 }}>
            Answer Feedback
          </Typography>
          <Typography variant="body1" color="text.secondary">
            {currentIndex + 1} of {evaluations.length}
          </Typography>
        </Box>

        <Card elevation={2} sx={{ borderRadius: 3, mb: 3 }}>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
              Question
            </Typography>
            <Typography variant="body1" sx={{ mb: 3, color: 'text.secondary' }}>
              {currentEval.question}
            </Typography>

            <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
              Your Answer
            </Typography>
            <Typography variant="body1" sx={{ mb: 4, color: 'text.secondary' }}>
              {currentEval.answer}
            </Typography>

            {currentEval.scores && Object.keys(currentEval.scores).length > 0 && (
              <ScoreDisplay scores={currentEval.scores} />
            )}
          </CardContent>
        </Card>

        {currentEval.feedback && (
          <FeedbackPanel
            strengths={currentEval.feedback.strengths || []}
            improvements={currentEval.feedback.improvements || []}
            sampleAnswer={currentEval.feedback.sample_answer}
          />
        )}

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button
            variant="outlined"
            startIcon={<ArrowBack />}
            onClick={handlePrevious}
            disabled={currentIndex === 0}
            sx={{ textTransform: 'none' }}
          >
            Previous
          </Button>
          <Button
            variant="contained"
            endIcon={currentIndex === evaluations.length - 1 ? undefined : <ArrowForward />}
            onClick={handleNext}
            sx={{ textTransform: 'none', px: 4 }}
          >
            {currentIndex === evaluations.length - 1 ? 'View Final Report' : 'Next'}
          </Button>
        </Box>
      </Container>
    </Box>
  );
}

