'use client';

import { useState, useRef, useEffect } from 'react';
import { Box, Typography, Button, Card, CardContent, CircularProgress, Alert, IconButton } from '@mui/material';
import { Mic, Stop, VolumeUp, Pause, PlayArrow } from '@mui/icons-material';
import QuestionCard from './QuestionCard';
import { Question } from '@/lib/api';

interface VoiceInterviewProps {
  sessionId: string;
  currentQuestion: Question | null;
  onAnswerSubmit: (answer: string) => Promise<void>;
  onNextQuestion: () => Promise<void>;
  isLoading: boolean;
}

export default function VoiceInterview({
  sessionId,
  currentQuestion,
  onAnswerSubmit,
  onNextQuestion,
  isLoading,
}: VoiceInterviewProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcribedText, setTranscribedText] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioError, setAudioError] = useState<string | null>(null);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const questionAudioRef = useRef<HTMLAudioElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  // Auto-play question when it changes
  useEffect(() => {
    if (currentQuestion?.audio) {
      playQuestionAudio(currentQuestion.audio);
    }
  }, [currentQuestion]);

  const playQuestionAudio = (base64Audio: string) => {
    try {
      // Stop any existing audio
      if (questionAudioRef.current) {
        questionAudioRef.current.pause();
        questionAudioRef.current = null;
      }

      const audio = new Audio(`data:audio/wav;base64,${base64Audio}`);
      questionAudioRef.current = audio;
      setIsPlaying(true);
      setAudioError(null);

      audio.onended = () => {
        setIsPlaying(false);
        // Auto-start recording after question finishes
        setTimeout(() => {
          startRecording();
        }, 500);
      };

      audio.onerror = () => {
        setIsPlaying(false);
        setAudioError('Failed to play audio');
      };

      audio.play().catch((err) => {
        console.error('Audio play failed:', err);
        setIsPlaying(false);
        setAudioError('Please allow audio playback permissions');
      });
    } catch (err) {
      console.error('Error playing audio:', err);
      setIsPlaying(false);
      setAudioError('Error playing question audio');
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        // MediaRecorder typically produces webm on Chrome/Firefox
      // MediaRecorder produces webm, but we need to convert to WAV for SpeechRecognition
      const mimeType = mediaRecorder.mimeType || 'audio/webm';
      const audioBlob = new Blob(audioChunksRef.current, { type: mimeType });
      
      // Convert WebM to WAV using Web Audio API
      await convertAndSubmitAnswer(audioBlob);
        stream.getTracks().forEach(track => track.stop());
        streamRef.current = null;
      };

      mediaRecorder.start();
      setIsRecording(true);
      setAudioError(null);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      setAudioError('Microphone access denied. Please enable microphone permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsProcessing(true);
    }
  };

  const convertAndSubmitAnswer = async (audioBlob: Blob) => {
    try {
      // Convert WebM/audio blob to WAV using Web Audio API
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const arrayBuffer = await audioBlob.arrayBuffer();
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
      
      // Convert to WAV
      const wavBlob = audioBufferToWav(audioBuffer);
      await processAndSubmitAnswer(wavBlob, 'audio/wav');
    } catch (error: any) {
      console.error('Audio conversion error:', error);
      // Fallback: try sending as-is
      await processAndSubmitAnswer(audioBlob, 'audio/webm');
    }
  };

  const audioBufferToWav = (buffer: AudioBuffer): Blob => {
    const length = buffer.length;
    const numberOfChannels = buffer.numberOfChannels;
    const sampleRate = buffer.sampleRate;
    const bytesPerSample = 2;
    const blockAlign = numberOfChannels * bytesPerSample;
    const byteRate = sampleRate * blockAlign;
    const dataSize = length * blockAlign;
    const bufferSize = 44 + dataSize;
    const arrayBuffer = new ArrayBuffer(bufferSize);
    const view = new DataView(arrayBuffer);

    // WAV header
    const writeString = (offset: number, string: string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };

    writeString(0, 'RIFF');
    view.setUint32(4, bufferSize - 8, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, numberOfChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, byteRate, true);
    view.setUint16(32, blockAlign, true);
    view.setUint16(34, 16, true);
    writeString(36, 'data');
    view.setUint32(40, dataSize, true);

    // Convert float samples to 16-bit PCM
    let offset = 44;
    for (let i = 0; i < length; i++) {
      for (let channel = 0; channel < numberOfChannels; channel++) {
        const sample = Math.max(-1, Math.min(1, buffer.getChannelData(channel)[i]));
        view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
        offset += 2;
      }
    }

    return new Blob([arrayBuffer], { type: 'audio/wav' });
  };

  const processAndSubmitAnswer = async (audioBlob: Blob, mimeType: string = 'audio/wav') => {
    try {
      // Convert blob to base64
      const reader = new FileReader();
      reader.onloadend = async () => {
        const result = reader.result as string;
        // Remove data URL prefix (data:audio/webm;base64,)
        const base64Audio = result.includes(',') ? result.split(',')[1] : result;
        
        // Determine format from mime type
        const audioFormat = mimeType.includes('webm') ? 'webm' : 
                           mimeType.includes('wav') ? 'wav' : 
                           mimeType.includes('mp3') ? 'mp3' : 'webm';
        
        try {
          // Call transcription API
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/voice/transcribe`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              audio_data: base64Audio,
              audio_format: audioFormat
            }),
          });

          if (response.ok) {
            const data = await response.json();
            const transcribed = data.text || '';
            setTranscribedText(transcribed);
            
            // Auto-submit the answer
            if (transcribed.trim()) {
              await onAnswerSubmit(transcribed);
              setTranscribedText('');
              
              // Get next question
              await onNextQuestion();
            } else {
              setAudioError('Could not transcribe audio. Please try again.');
              setIsProcessing(false);
            }
          } else {
            try {
              const errorData = await response.json();
              // Handle FastAPI validation error format
              const errorMessage = Array.isArray(errorData.detail) 
                ? errorData.detail.map((e: any) => e.msg || e.message || String(e)).join(', ')
                : errorData.detail || errorData.message || 'Transcription failed';
              setAudioError(errorMessage);
            } catch {
              setAudioError('Transcription failed. Please try again.');
            }
            setIsProcessing(false);
          }
        } catch (error: any) {
          console.error('Transcription error:', error);
          setAudioError(error.message || 'Error transcribing audio. Please try again.');
          setIsProcessing(false);
        }
      };
      reader.onerror = () => {
        setAudioError('Error reading audio file');
        setIsProcessing(false);
      };
      reader.readAsDataURL(audioBlob);
    } catch (error: any) {
      console.error('Error processing audio:', error);
      setIsProcessing(false);
      setAudioError(error.message || 'Error processing audio');
    }
  };

  const handleManualStart = () => {
    if (!isPlaying && !isRecording && !isProcessing) {
      startRecording();
    }
  };

  return (
    <Box>
      {audioError && (
        <Alert severity="warning" sx={{ mb: 2 }} onClose={() => setAudioError(null)}>
          {audioError}
        </Alert>
      )}

      {currentQuestion && (
        <QuestionCard
          question={currentQuestion.question}
          questionNumber={currentQuestion.question_number}
          questionType={currentQuestion.question_type}
        />
      )}

      <Card elevation={2} sx={{ borderRadius: 3, mb: 3 }}>
        <CardContent sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
            Voice Interview Mode
          </Typography>

          {/* Question Audio Status */}
          {isPlaying && (
            <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 2 }}>
              <VolumeUp color="primary" />
              <Typography variant="body1" color="primary">
                Playing question...
              </Typography>
            </Box>
          )}

          {/* Recording Status */}
          {isRecording && (
            <Box sx={{ mb: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 2, mb: 2 }}>
                <Box
                  sx={{
                    width: 16,
                    height: 16,
                    borderRadius: '50%',
                    bgcolor: 'error.main',
                    animation: 'pulse 1.5s ease-in-out infinite',
                    '@keyframes pulse': {
                      '0%, 100%': { opacity: 1 },
                      '50%': { opacity: 0.5 },
                    },
                  }}
                />
                <Typography variant="h6" color="error">
                  Recording your answer...
                </Typography>
              </Box>
              <Button
                variant="contained"
                color="error"
                startIcon={<Stop />}
                onClick={stopRecording}
                sx={{ textTransform: 'none', px: 4 }}
              >
                Stop Recording
              </Button>
            </Box>
          )}

          {/* Processing Status */}
          {isProcessing && (
            <Box sx={{ mb: 3 }}>
              <CircularProgress sx={{ mb: 2 }} />
              <Typography variant="body1" color="text.secondary">
                Processing your answer...
              </Typography>
            </Box>
          )}

          {/* Transcribed Text */}
          {transcribedText && (
            <Box sx={{ mb: 3, p: 2, bgcolor: 'grey.100', borderRadius: 2 }}>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                Transcribed:
              </Typography>
              <Typography variant="body1">
                {transcribedText}
              </Typography>
            </Box>
          )}

          {/* Manual Start Button (if not auto-started) */}
          {!isPlaying && !isRecording && !isProcessing && !isLoading && (
            <Button
              variant="contained"
              size="large"
              startIcon={<Mic />}
              onClick={handleManualStart}
              disabled={isLoading}
              sx={{
                textTransform: 'none',
                px: 4,
                py: 1.5,
                fontSize: '1.1rem',
                minWidth: 200,
              }}
            >
              Start Recording Answer
            </Button>
          )}

          {/* Instructions */}
          {!isPlaying && !isRecording && !isProcessing && (
            <Typography variant="body2" color="text.secondary" sx={{ mt: 3 }}>
              {currentQuestion?.audio
                ? 'The question will play automatically. Then you can record your answer.'
                : 'Click the button above to start recording your answer.'}
            </Typography>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}

