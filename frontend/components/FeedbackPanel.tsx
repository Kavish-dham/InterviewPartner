'use client';

import { Card, CardContent, Typography, Box, List, ListItem, ListItemIcon, ListItemText, Divider } from '@mui/material';
import { CheckCircle, Warning, Lightbulb } from '@mui/icons-material';

interface FeedbackPanelProps {
  strengths: string[];
  improvements: string[];
  sampleAnswer?: string;
}

export default function FeedbackPanel({ strengths, improvements, sampleAnswer }: FeedbackPanelProps) {
  return (
    <Card elevation={2} sx={{ mt: 3, borderRadius: 3 }}>
      <CardContent sx={{ p: 4 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
          Feedback
        </Typography>

        {strengths.length > 0 && (
          <Box sx={{ mb: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
              <CheckCircle color="success" />
              <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                Strengths
              </Typography>
            </Box>
            <List dense>
              {strengths.map((strength, index) => (
                <ListItem key={index} sx={{ pl: 0 }}>
                  <ListItemIcon sx={{ minWidth: 32 }}>
                    <CheckCircle color="success" fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary={strength} />
                </ListItem>
              ))}
            </List>
          </Box>
        )}

        {improvements.length > 0 && (
          <>
            <Divider sx={{ my: 3 }} />
            <Box sx={{ mb: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <Warning color="warning" />
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                  Areas to Improve
                </Typography>
              </Box>
              <List dense>
                {improvements.map((improvement, index) => (
                  <ListItem key={index} sx={{ pl: 0 }}>
                    <ListItemIcon sx={{ minWidth: 32 }}>
                      <Warning color="warning" fontSize="small" />
                    </ListItemIcon>
                    <ListItemText primary={improvement} />
                  </ListItem>
                ))}
              </List>
            </Box>
          </>
        )}

        {sampleAnswer && (
          <>
            <Divider sx={{ my: 3 }} />
            <Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <Lightbulb color="primary" />
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                  Sample Improved Answer
                </Typography>
              </Box>
              <Box
                sx={{
                  bgcolor: 'grey.50',
                  p: 2,
                  borderRadius: 2,
                  border: '1px solid',
                  borderColor: 'grey.200',
                }}
              >
                <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', lineHeight: 1.8 }}>
                  {sampleAnswer}
                </Typography>
              </Box>
            </Box>
          </>
        )}
      </CardContent>
    </Card>
  );
}

