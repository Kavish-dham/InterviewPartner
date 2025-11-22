'use client';

import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import { Container, Box, Typography, Button, Grid, Card, CardContent } from '@mui/material';
import { Mic, Assessment, Speed, Feedback } from '@mui/icons-material';

export default function Home() {
  const router = useRouter();

  const features = [
    {
      icon: <Mic fontSize="large" />,
      title: 'Voice-Based Interviews',
      description: 'Practice with real-time voice interaction using advanced speech recognition',
    },
    {
      icon: <Assessment fontSize="large" />,
      title: 'Real-Time Evaluation',
      description: 'Get instant feedback on your answers with detailed scoring and analysis',
    },
    {
      icon: <Speed fontSize="large" />,
      title: 'Personalized Questions',
      description: 'Questions tailored to your resume and target job description',
    },
    {
      icon: <Feedback fontSize="large" />,
      title: 'Comprehensive Feedback',
      description: 'Receive strengths, improvements, and sample answers after each response',
    },
  ];

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50' }}>
      <Header />
      
      <Container maxWidth="lg" sx={{ py: 8 }}>
        {/* Hero Section */}
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          <Typography
            variant="h1"
            sx={{
              fontSize: { xs: '2.5rem', md: '4rem' },
              fontWeight: 700,
              mb: 2,
              background: 'linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Interview Practice Partner
          </Typography>
          <Typography
            variant="h5"
            color="text.secondary"
            sx={{ mb: 4, maxWidth: '600px', mx: 'auto' }}
          >
            Master your interview skills with AI-powered practice sessions.
            Get personalized feedback and improve with every session.
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={() => router.push('/upload')}
            sx={{
              px: 4,
              py: 1.5,
              fontSize: '1.1rem',
              textTransform: 'none',
              borderRadius: 3,
            }}
          >
            Start Interview Practice
          </Button>
        </Box>

        {/* Features Grid */}
        <Grid container spacing={4} sx={{ mb: 8 }}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card
                elevation={0}
                sx={{
                  height: '100%',
                  p: 3,
                  borderRadius: 3,
                  border: '1px solid',
                  borderColor: 'grey.200',
                  transition: 'all 0.3s',
                  '&:hover': {
                    elevation: 4,
                    transform: 'translateY(-4px)',
                  },
                }}
              >
                <CardContent sx={{ textAlign: 'center' }}>
                  <Box sx={{ color: 'primary.main', mb: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {/* How It Works */}
        <Box sx={{ bgcolor: 'white', p: 6, borderRadius: 3, boxShadow: 1 }}>
          <Typography variant="h4" sx={{ fontWeight: 600, mb: 4, textAlign: 'center' }}>
            How It Works
          </Typography>
          <Grid container spacing={4}>
            {[
              { step: '1', title: 'Upload Resume & Job Description', desc: 'Provide your resume and target job description' },
              { step: '2', title: 'Select Interview Type', desc: 'Choose Behavioral, Technical, or Mixed interview style' },
              { step: '3', title: 'Practice Interview', desc: 'Answer questions via text or voice, get real-time feedback' },
              { step: '4', title: 'Review Report', desc: 'Get comprehensive evaluation and improvement recommendations' },
            ].map((item) => (
              <Grid item xs={12} md={3} key={item.step}>
                <Box sx={{ textAlign: 'center' }}>
                  <Box
                    sx={{
                      width: 48,
                      height: 48,
                      borderRadius: '50%',
                      bgcolor: 'primary.main',
                      color: 'white',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mx: 'auto',
                      mb: 2,
                      fontWeight: 600,
                    }}
                  >
                    {item.step}
                  </Box>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                    {item.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {item.desc}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Box>
      </Container>
    </Box>
  );
}

