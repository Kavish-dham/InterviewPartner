'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import { Container, Box, Typography, Button, Card, CardContent, Stepper, Step, StepLabel, RadioGroup, FormControlLabel, Radio, FormControl, FormLabel } from '@mui/material';
import { Psychology, Code, Shuffle } from '@mui/icons-material';
import { api } from '@/lib/api';

const steps = ['Upload Information', 'Select Role', 'Interview'];
const interviewTypes = [
  { value: 'Behavioral', label: 'Behavioral', icon: <Psychology />, desc: 'Focus on STAR format questions about past experiences' },
  { value: 'Technical', label: 'Technical', icon: <Code />, desc: 'Role-specific technical questions and problem-solving' },
  { value: 'Mixed', label: 'Mixed', icon: <Shuffle />, desc: 'Combination of behavioral and technical questions' },
];

export default function SelectRolePage() {
  const router = useRouter();
  const [selectedType, setSelectedType] = useState('Mixed');
  const [isLoading, setIsLoading] = useState(false);
  const [resume, setResume] = useState('');
  const [jobDescription, setJobDescription] = useState('');

  useEffect(() => {
    // Get data from sessionStorage
    const storedResume = sessionStorage.getItem('resume');
    const storedJobDesc = sessionStorage.getItem('jobDescription');
    
    if (!storedResume || !storedJobDesc) {
      router.push('/upload');
      return;
    }
    
    setResume(storedResume);
    setJobDescription(storedJobDesc);
  }, [router]);

  const handleStartInterview = async () => {
    setIsLoading(true);
    try {
      const session = await api.createSession({
        resume,
        job_description: jobDescription,
        interview_type: selectedType as 'Behavioral' | 'Technical' | 'Mixed',
      });

      sessionStorage.setItem('sessionId', session.session_id);
      router.push('/interview');
    } catch (error) {
      console.error('Error creating session:', error);
      alert('Failed to create interview session. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50' }}>
      <Header />
      
      <Container maxWidth="md" sx={{ py: 6 }}>
        <Stepper activeStep={1} sx={{ mb: 6 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        <Card elevation={2} sx={{ borderRadius: 3 }}>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
              Select Interview Type
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
              Choose the type of interview you want to practice
            </Typography>

            <FormControl component="fieldset" fullWidth>
              <FormLabel component="legend" sx={{ mb: 2, fontWeight: 600 }}>
                Interview Style
              </FormLabel>
              <RadioGroup
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
              >
                {interviewTypes.map((type) => (
                  <Card
                    key={type.value}
                    sx={{
                      mb: 2,
                      border: selectedType === type.value ? '2px solid' : '1px solid',
                      borderColor: selectedType === type.value ? 'primary.main' : 'grey.300',
                      borderRadius: 2,
                      cursor: 'pointer',
                      transition: 'all 0.2s',
                      '&:hover': {
                        borderColor: 'primary.main',
                      },
                    }}
                    onClick={() => setSelectedType(type.value)}
                  >
                    <CardContent>
                      <FormControlLabel
                        value={type.value}
                        control={<Radio />}
                        label={
                          <Box>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                              <Box sx={{ color: 'primary.main' }}>{type.icon}</Box>
                              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                                {type.label}
                              </Typography>
                            </Box>
                            <Typography variant="body2" color="text.secondary">
                              {type.desc}
                            </Typography>
                          </Box>
                        }
                        sx={{ m: 0, width: '100%' }}
                      />
                    </CardContent>
                  </Card>
                ))}
              </RadioGroup>
            </FormControl>

            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end', mt: 4 }}>
              <Button
                variant="outlined"
                onClick={() => router.back()}
                sx={{ textTransform: 'none' }}
                disabled={isLoading}
              >
                Back
              </Button>
              <Button
                variant="contained"
                onClick={handleStartInterview}
                disabled={isLoading}
                sx={{ textTransform: 'none', px: 4 }}
              >
                {isLoading ? 'Starting...' : 'Start Interview'}
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
}

