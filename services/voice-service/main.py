"""
Voice Service
Handles speech-to-text and text-to-speech
Uses SpeechRecognition as primary STT (can be extended with Whisper later)
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import speech_recognition as sr
import pyttsx3
import io
import base64
import tempfile
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from services.shared.models import (
    VoiceTranscriptionRequest,
    VoiceTranscriptionResponse,
    VoiceSynthesisRequest,
    VoiceSynthesisResponse,
)

app = FastAPI(title="Voice Service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recognizer and TTS engine
recognizer = None
tts_engine = None


def get_recognizer():
    """Initialize speech recognizer"""
    global recognizer
    if recognizer is None:
        recognizer = sr.Recognizer()
    return recognizer


def get_tts_engine():
    """Initialize TTS engine"""
    global tts_engine
    if tts_engine is None:
        try:
            tts_engine = pyttsx3.init()
            # Configure voice properties
            voices = tts_engine.getProperty('voices')
            if voices:
                tts_engine.setProperty('voice', voices[0].id)
            tts_engine.setProperty('rate', 150)  # Speed
            tts_engine.setProperty('volume', 0.9)  # Volume
        except Exception as e:
            print(f"Warning: TTS initialization failed: {e}")
            tts_engine = None
    return tts_engine


@app.post("/transcribe", response_model=VoiceTranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...), language: str = None):
    """
    Transcribe audio to text using SpeechRecognition
    Accepts audio file upload (WAV format recommended)
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Load recognizer
            r = get_recognizer()
            
            # Load audio file
            with sr.AudioFile(tmp_file_path) as source:
                audio = r.record(source)
            
            # Try Google Speech Recognition first (free, requires internet)
            try:
                text = r.recognize_google(audio, language=language if language else "en-US")
                confidence = 0.8  # Google doesn't provide confidence, use default
            except sr.UnknownValueError:
                # Fallback to sphinx (offline, but less accurate)
                try:
                    text = r.recognize_sphinx(audio)
                    confidence = 0.6
                except:
                    text = ""
                    confidence = 0.0
            
            language_detected = language if language else "en-US"
            
            return VoiceTranscriptionResponse(
                text=text,
                confidence=confidence,
                language=language_detected
            )
        finally:
            # Clean up temp file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")


@app.post("/transcribe-base64", response_model=VoiceTranscriptionResponse)
async def transcribe_audio_base64(request: VoiceTranscriptionRequest):
    """
    Transcribe audio from base64 encoded data
    Supports webm, wav, and other formats
    """
    try:
        # Decode base64 audio
        try:
            audio_bytes = base64.b64decode(request.audio_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid base64 data: {str(e)}")
        
        # Determine file extension based on format
        file_ext = request.audio_format if request.audio_format in ['wav', 'webm', 'mp3', 'ogg'] else 'wav'
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name
        
        try:
            r = get_recognizer()
            
            # Try to load audio file
            try:
                with sr.AudioFile(tmp_file_path) as source:
                    # Adjust for ambient noise
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.record(source)
            except Exception as e:
                # If AudioFile fails, try converting with pydub if available
                raise HTTPException(status_code=400, detail=f"Audio file could not be read: {str(e)}. Please ensure the audio is in a supported format (WAV, WebM).")
            
            # Try Google Speech Recognition first
            try:
                text = r.recognize_google(audio, language=request.language if request.language else "en-US")
                confidence = 0.8
            except sr.UnknownValueError:
                # Could not understand audio
                text = ""
                confidence = 0.0
                raise HTTPException(status_code=400, detail="Speech Recognition could not understand audio. Please speak more clearly.")
            except sr.RequestError as e:
                # API error
                raise HTTPException(status_code=500, detail=f"Could not request results from Google Speech Recognition service: {str(e)}")
            
            language_detected = request.language if request.language else "en-US"
            
            return VoiceTranscriptionResponse(
                text=text,
                confidence=confidence,
                language=language_detected
            )
        finally:
            # Clean up temp file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")


@app.post("/synthesize", response_model=VoiceSynthesisResponse)
async def synthesize_speech(request: VoiceSynthesisRequest):
    """
    Convert text to speech
    Returns audio as base64 encoded WAV
    """
    try:
        engine = get_tts_engine()
        
        if engine is None:
            raise HTTPException(status_code=503, detail="TTS engine not available")
        
        # Set voice properties
        if request.voice_id:
            voices = engine.getProperty('voices')
            if voices and request.voice_id in [v.id for v in voices]:
                engine.setProperty('voice', request.voice_id)
        
        engine.setProperty('rate', int(150 * request.speed))
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file_path = tmp_file.name
        
        try:
            # Generate speech
            engine.save_to_file(request.text, tmp_file_path)
            engine.runAndWait()
            
            # Read audio file
            with open(tmp_file_path, 'rb') as f:
                audio_data = f.read()
            
            # Estimate duration (rough calculation)
            duration = len(audio_data) / 16000  # Assuming 16kHz sample rate
            
            # Encode to base64
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            return VoiceSynthesisResponse(
                audio_data=audio_base64.encode('utf-8'),  # Return as bytes for model
                audio_format="wav",
                duration=duration
            )
        finally:
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech synthesis error: {str(e)}")


@app.get("/voices")
async def list_voices():
    """List available TTS voices"""
    try:
        engine = get_tts_engine()
        
        if engine is None:
            return {"voices": []}
        
        voices = engine.getProperty('voices')
        
        return {
            "voices": [
                {
                    "id": voice.id,
                    "name": voice.name,
                    "languages": getattr(voice, 'languages', [])
                }
                for voice in voices
            ] if voices else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing voices: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "voice-service",
        "recognizer_loaded": recognizer is not None,
        "tts_loaded": tts_engine is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
