'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Mic, Assessment, Dashboard } from '@mui/icons-material';

export default function Header() {
  const pathname = usePathname();

  const navItems = [
    { label: 'Home', path: '/' },
    { label: 'Dashboard', path: '/dashboard' },
  ];

  return (
    <AppBar position="static" elevation={0} sx={{ bgcolor: 'white', color: 'text.primary', borderBottom: '1px solid #e5e7eb' }}>
      <Toolbar sx={{ justifyContent: 'space-between', px: { xs: 2, md: 4 } }}>
        <Link href="/" className="flex items-center gap-2 no-underline">
          <Mic className="text-primary-600" />
          <Typography variant="h6" component="div" sx={{ fontWeight: 600, color: 'text.primary' }}>
            Interview Practice
          </Typography>
        </Link>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          {navItems.map((item) => (
            <Link key={item.path} href={item.path}>
              <Button
                color={pathname === item.path ? 'primary' : 'inherit'}
                sx={{
                  textTransform: 'none',
                  fontWeight: pathname === item.path ? 600 : 400,
                }}
              >
                {item.label}
              </Button>
            </Link>
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  );
}

