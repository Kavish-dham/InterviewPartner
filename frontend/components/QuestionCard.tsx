'use client';

import { Card, CardContent, Typography, Box, Chip } from '@mui/material';
import { QuestionAnswer } from '@mui/icons-material';

interface QuestionCardProps {
  question: string;
  questionNumber: number;
  questionType?: string;
}

export default function QuestionCard({ question, questionNumber, questionType }: QuestionCardProps) {
  const getTypeColor = (type?: string) => {
    switch (type?.toLowerCase()) {
      case 'behavioral':
        return 'primary';
      case 'technical':
        return 'secondary';
      default:
        return 'default';
    }
  };

  return (
    <Card elevation={2} sx={{ mb: 3, borderRadius: 3 }}>
      <CardContent sx={{ p: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <QuestionAnswer color="primary" />
          <Typography variant="overline" color="text.secondary" sx={{ fontWeight: 600 }}>
            Question {questionNumber}
          </Typography>
          {questionType && (
            <Chip
              label={questionType}
              size="small"
              color={getTypeColor(questionType)}
              sx={{ textTransform: 'capitalize' }}
            />
          )}
        </Box>
        <Typography variant="h6" sx={{ fontWeight: 500, lineHeight: 1.6 }}>
          {question}
        </Typography>
      </CardContent>
    </Card>
  );
}

