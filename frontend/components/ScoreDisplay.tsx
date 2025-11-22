'use client';

import { Box, Typography, LinearProgress } from '@mui/material';
import { TrendingUp } from '@mui/icons-material';

interface ScoreDisplayProps {
  scores: {
    clarity: number;
    communication: number;
    star_structure: number;
    role_relevance: number;
    technical_depth: number;
    overall: number;
  };
  compact?: boolean;
}

export default function ScoreDisplay({ scores, compact = false }: ScoreDisplayProps) {
  const scoreItems = [
    { label: 'Clarity', value: scores.clarity },
    { label: 'Communication', value: scores.communication },
    { label: 'STAR Structure', value: scores.star_structure },
    { label: 'Role Relevance', value: scores.role_relevance },
    { label: 'Technical Depth', value: scores.technical_depth },
  ];

  const getColor = (score: number) => {
    if (score >= 8) return 'success';
    if (score >= 6) return 'primary';
    if (score >= 4) return 'warning';
    return 'error';
  };

  if (compact) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <TrendingUp color="primary" />
        <Typography variant="h5" sx={{ fontWeight: 600 }}>
          {scores.overall.toFixed(1)}/10
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ mt: 2 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
        <TrendingUp color="primary" fontSize="large" />
        <Typography variant="h5" sx={{ fontWeight: 600 }}>
          Overall Score: {scores.overall.toFixed(1)}/10
        </Typography>
      </Box>
      
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        {scoreItems.map((item) => (
          <Box key={item.label}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
              <Typography variant="body2" color="text.secondary">
                {item.label}
              </Typography>
              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                {item.value.toFixed(1)}/10
              </Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={item.value * 10}
              color={getColor(item.value) as any}
              sx={{ height: 8, borderRadius: 1 }}
            />
          </Box>
        ))}
      </Box>
    </Box>
  );
}

