'use client';

import { useState, useRef } from 'react';
import { Box, Button, Typography, Alert, CircularProgress } from '@mui/material';
import { CloudUpload, Description } from '@mui/icons-material';

interface PDFUploadProps {
  label: string;
  onFileUploaded: (text: string) => void;
  value?: string;
  error?: boolean;
}

export default function PDFUpload({ label, onFileUploaded, value, error }: PDFUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (file.type !== 'application/pdf') {
      setUploadError('Please upload a PDF file');
      return;
    }

    if (file.size > 10 * 1024 * 1024) { // 10MB limit
      setUploadError('File size must be less than 10MB');
      return;
    }

    setUploading(true);
    setUploadError(null);

    try {
      // Convert file to base64
      const reader = new FileReader();
      reader.onloadend = async () => {
        const base64 = (reader.result as string).split(',')[1];
        
        try {
          // Call backend to parse PDF
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/parse-pdf`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              file_name: file.name,
              file_data: base64 
            }),
          });

          if (response.ok) {
            const data = await response.json();
            onFileUploaded(data.text || '');
          } else {
            try {
              const errorData = await response.json();
              // Handle FastAPI validation error format
              const errorMessage = Array.isArray(errorData.detail) 
                ? errorData.detail.map((e: any) => e.msg || e.message || String(e)).join(', ')
                : errorData.detail || errorData.message || 'Failed to parse PDF';
              setUploadError(errorMessage);
            } catch {
              setUploadError('Failed to parse PDF');
            }
          }
        } catch (error) {
          console.error('PDF parsing error:', error);
          setUploadError('Error parsing PDF. Please try again or paste text directly.');
        } finally {
          setUploading(false);
        }
      };
      reader.readAsDataURL(file);
    } catch (error) {
      console.error('File read error:', error);
      setUploadError('Error reading file');
      setUploading(false);
    }
  };

  return (
    <Box>
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf"
        onChange={handleFileSelect}
        style={{ display: 'none' }}
      />
      
      <Button
        variant="outlined"
        startIcon={uploading ? <CircularProgress size={20} /> : <CloudUpload />}
        onClick={() => fileInputRef.current?.click()}
        disabled={uploading}
        sx={{ textTransform: 'none', mb: 2 }}
      >
        {uploading ? 'Uploading...' : `Upload ${label} PDF`}
      </Button>

      {uploadError && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setUploadError(null)}>
          {uploadError}
        </Alert>
      )}

      {value && !uploading && (
        <Alert severity="success" sx={{ mb: 2 }}>
          PDF uploaded and parsed successfully ({value.length} characters extracted)
        </Alert>
      )}
    </Box>
  );
}

