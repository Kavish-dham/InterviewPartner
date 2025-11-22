'use client';

import { useState, useRef, useEffect } from 'react';
import { IconButton, Tooltip, CircularProgress } from '@mui/material';
import { Mic, Stop, PlayArrow } from '@mui/icons-material';

interface VoiceRecorderProps {
  onTranscribe: (text: string) => void;
  onRecordingComplete?: (audioBlob: Blob) => void;
}

export default function VoiceRecorder({ onTranscribe, onRecordingComplete }: VoiceRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        if (onRecordingComplete) {
          onRecordingComplete(audioBlob);
        }
        await processAudio(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Microphone access denied. Please enable microphone permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsProcessing(true);
    }
  };

  const processAudio = async (audioBlob: Blob) => {
    try {
      // Convert blob to base64
      const reader = new FileReader();
      reader.onloadend = async () => {
        const base64Audio = (reader.result as string).split(',')[1];
        
        // Call transcription API
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/voice/transcribe`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ audio_data: base64Audio }),
        });

        if (response.ok) {
          const data = await response.json();
          onTranscribe(data.text || '');
        } else {
          console.error('Transcription failed');
        }
        setIsProcessing(false);
      };
      reader.readAsDataURL(audioBlob);
    } catch (error) {
      console.error('Error processing audio:', error);
      setIsProcessing(false);
    }
  };

  return (
    <Tooltip title={isRecording ? 'Stop recording' : 'Start voice recording'}>
      <IconButton
        onClick={isRecording ? stopRecording : startRecording}
        disabled={isProcessing}
        sx={{
          width: 64,
          height: 64,
          bgcolor: isRecording ? 'error.main' : 'primary.main',
          color: 'white',
          '&:hover': {
            bgcolor: isRecording ? 'error.dark' : 'primary.dark',
          },
        }}
        aria-label={isRecording ? 'Stop recording' : 'Start recording'}
      >
        {isProcessing ? (
          <CircularProgress size={24} color="inherit" />
        ) : isRecording ? (
          <Stop fontSize="large" />
        ) : (
          <Mic fontSize="large" />
        )}
      </IconButton>
    </Tooltip>
  );
}

