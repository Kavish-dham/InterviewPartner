'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import ScoreDisplay from '@/components/ScoreDisplay';
import { Container, Box, Typography, Button, Card, CardContent, List, ListItem, ListItemText, Divider, Chip } from '@mui/material';
import { TrendingUp, CheckCircle, Warning, School, Home } from '@mui/icons-material';
import { api, FinalReport } from '@/lib/api';

export default function ReportPage() {
  const router = useRouter();
  const [report, setReport] = useState<FinalReport | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const sessionId = sessionStorage.getItem('sessionId');
    if (!sessionId) {
      router.push('/interview');
      return;
    }

    loadReport(sessionId);
  }, [router]);

  const loadReport = async (sessionId: string) => {
    try {
      const finalReport = await api.endInterview(sessionId);
      setReport(finalReport);
      
      // Play audio summary if available
      if (finalReport.audio_summary) {
        try {
          const audio = new Audio(`data:audio/wav;base64,${finalReport.audio_summary}`);
          audio.play().catch(err => console.error('Audio play failed:', err));
        } catch (err) {
          console.error('Error playing audio:', err);
        }
      }
    } catch (error) {
      console.error('Error loading report:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Typography variant="h6">Loading final report...</Typography>
      </Box>
    );
  }

  if (!report) {
    return (
      <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50' }}>
        <Header />
        <Container maxWidth="lg" sx={{ py: 6, textAlign: 'center' }}>
          <Typography variant="h5" sx={{ mb: 2 }}>
            Report not available
          </Typography>
          <Button variant="contained" onClick={() => router.push('/')}>
            Start New Interview
          </Button>
        </Container>
      </Box>
    );
  }

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50' }}>
      <Header />
      
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <TrendingUp sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
          <Typography variant="h3" sx={{ fontWeight: 700, mb: 1 }}>
            Interview Complete
          </Typography>
          <Typography variant="h5" color="text.secondary">
            Your Final Evaluation Report
          </Typography>
        </Box>

        {/* Overall Score Card */}
        <Card elevation={3} sx={{ borderRadius: 3, mb: 4, bgcolor: 'primary.50' }}>
          <CardContent sx={{ p: 4, textAlign: 'center' }}>
            <Typography variant="h2" sx={{ fontWeight: 700, color: 'primary.main', mb: 1 }}>
              {report.average_score.toFixed(1)}/10
            </Typography>
            <Typography variant="h6" color="text.secondary">
              Average Score
            </Typography>
            <Box sx={{ mt: 3 }}>
              <ScoreDisplay scores={report.detailed_scores} />
            </Box>
          </CardContent>
        </Card>

        <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3, mb: 4 }}>
          {/* Key Strengths */}
          <Card elevation={2} sx={{ borderRadius: 3 }}>
            <CardContent sx={{ p: 4 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <CheckCircle color="success" />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Key Strengths
                </Typography>
              </Box>
              {report.key_strengths && report.key_strengths.length > 0 ? (
                <List>
                  {report.key_strengths.map((strength, index) => (
                    <ListItem key={index} sx={{ pl: 0 }}>
                      <ListItemText
                        primary={strength}
                        primaryTypographyProps={{ variant: 'body1' }}
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  Continue practicing to build your strengths
                </Typography>
              )}
            </CardContent>
          </Card>

          {/* Areas to Improve */}
          <Card elevation={2} sx={{ borderRadius: 3 }}>
            <CardContent sx={{ p: 4 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <Warning color="warning" />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Areas to Improve
                </Typography>
              </Box>
              {report.key_improvements && report.key_improvements.length > 0 ? (
                <List>
                  {report.key_improvements.map((improvement, index) => (
                    <ListItem key={index} sx={{ pl: 0 }}>
                      <ListItemText
                        primary={improvement}
                        primaryTypographyProps={{ variant: 'body1' }}
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  Great job! Keep building on your strengths
                </Typography>
              )}
            </CardContent>
          </Card>
        </Box>

        {/* Recommended Topics */}
        {report.recommended_topics && report.recommended_topics.length > 0 && (
          <Card elevation={2} sx={{ borderRadius: 3, mb: 4 }}>
            <CardContent sx={{ p: 4 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <School color="primary" />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Recommended Practice Topics
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {report.recommended_topics.map((topic, index) => (
                  <Chip
                    key={index}
                    label={topic}
                    color="primary"
                    variant="outlined"
                    sx={{ mb: 1 }}
                  />
                ))}
              </Box>
            </CardContent>
          </Card>
        )}

        {/* Next Focus */}
        {report.next_focus && (
          <Card elevation={2} sx={{ borderRadius: 3, mb: 4, bgcolor: 'grey.100' }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                Next Session Focus
              </Typography>
              <Typography variant="body1" color="text.secondary">
                {report.next_focus}
              </Typography>
            </CardContent>
          </Card>
        )}

        {/* Session Summary */}
        <Card elevation={1} sx={{ borderRadius: 3, mb: 4 }}>
          <CardContent sx={{ p: 3 }}>
            <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center' }}>
              Session Summary: {report.total_questions} questions • {report.total_answers} answers evaluated
            </Typography>
          </CardContent>
        </Card>

        {/* Action Buttons */}
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
          <Button
            variant="outlined"
            startIcon={<Home />}
            onClick={() => router.push('/')}
            sx={{ textTransform: 'none', px: 4 }}
          >
            Home
          </Button>
          <Button
            variant="contained"
            onClick={() => {
              sessionStorage.clear();
              router.push('/upload');
            }}
            sx={{ textTransform: 'none', px: 4 }}
          >
            Start New Interview
          </Button>
        </Box>
      </Container>
    </Box>
  );
}

