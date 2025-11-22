'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import PDFUpload from '@/components/PDFUpload';
import { Container, Box, Typography, TextField, Button, Card, CardContent, Stepper, Step, StepLabel, Divider } from '@mui/material';
import { Description, Work } from '@mui/icons-material';

const steps = ['Upload Information', 'Select Role', 'Interview'];

export default function UploadPage() {
  const router = useRouter();
  const [resume, setResume] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [errors, setErrors] = useState({ resume: false, jobDescription: false });

  const handleNext = () => {
    const newErrors = {
      resume: !resume.trim(),
      jobDescription: !jobDescription.trim(),
    };
    setErrors(newErrors);

    if (!newErrors.resume && !newErrors.jobDescription) {
      // Store in sessionStorage for next page
      sessionStorage.setItem('resume', resume);
      sessionStorage.setItem('jobDescription', jobDescription);
      router.push('/select-role');
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50' }}>
      <Header />
      
      <Container maxWidth="md" sx={{ py: 6 }}>
        <Stepper activeStep={0} sx={{ mb: 6 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        <Card elevation={2} sx={{ borderRadius: 3 }}>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
              Upload Your Information
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
              Provide your resume and the job description for the role you're targeting
            </Typography>

            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              <Box>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Description color="primary" />
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                      Resume
                    </Typography>
                  </Box>
                  <PDFUpload
                    label="Resume"
                    onFileUploaded={(text) => setResume(text)}
                    value={resume}
                    error={errors.resume}
                  />
                </Box>
                <Divider sx={{ mb: 2 }} />
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  Or paste your resume text below:
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={8}
                  placeholder="Paste your resume text here..."
                  value={resume}
                  onChange={(e) => setResume(e.target.value)}
                  error={errors.resume}
                  helperText={errors.resume ? 'Resume is required' : 'Paste your resume content or upload a PDF'}
                  sx={{ bgcolor: 'white' }}
                />
              </Box>

              <Box>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Work color="primary" />
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                      Job Description
                    </Typography>
                  </Box>
                  <PDFUpload
                    label="Job Description"
                    onFileUploaded={(text) => setJobDescription(text)}
                    value={jobDescription}
                    error={errors.jobDescription}
                  />
                </Box>
                <Divider sx={{ mb: 2 }} />
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  Or paste the job description below:
                </Typography>
                <TextField
                  fullWidth
                  multiline
                  rows={8}
                  placeholder="Paste the job description here..."
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  error={errors.jobDescription}
                  helperText={errors.jobDescription ? 'Job description is required' : 'Paste the job description or upload a PDF'}
                  sx={{ bgcolor: 'white' }}
                />
              </Box>

              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end', mt: 2 }}>
                <Button
                  variant="outlined"
                  onClick={() => router.back()}
                  sx={{ textTransform: 'none' }}
                >
                  Back
                </Button>
                <Button
                  variant="contained"
                  onClick={handleNext}
                  sx={{ textTransform: 'none', px: 4 }}
                >
                  Continue
                </Button>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
}

