'use client';

import Header from '@/components/Header';
import { Container, Box, Typography, Card, CardContent, Grid } from '@mui/material';
import { Assessment, TrendingUp, History } from '@mui/icons-material';

export default function DashboardPage() {
  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'grey.50' }}>
      <Header />
      
      <Container maxWidth="lg" sx={{ py: 6 }}>
        <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
          Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
          Track your interview practice progress and performance
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card elevation={2} sx={{ borderRadius: 3, height: '100%' }}>
              <CardContent sx={{ p: 4, textAlign: 'center' }}>
                <Assessment sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
                  0
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Total Sessions
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card elevation={2} sx={{ borderRadius: 3, height: '100%' }}>
              <CardContent sx={{ p: 4, textAlign: 'center' }}>
                <TrendingUp sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
                <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
                  --
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Average Score
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card elevation={2} sx={{ borderRadius: 3, height: '100%' }}>
              <CardContent sx={{ p: 4, textAlign: 'center' }}>
                <History sx={{ fontSize: 48, color: 'secondary.main', mb: 2 }} />
                <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
                  0
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Questions Answered
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Card elevation={2} sx={{ borderRadius: 3, mt: 4 }}>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
              Recent Sessions
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 4 }}>
              No sessions yet. Start your first interview practice session!
            </Typography>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
}

