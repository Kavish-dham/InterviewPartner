# Whisper API Setup (Optional)

## Current Setup
The system currently uses **SpeechRecognition** library with **Google Web Speech API** which:
- ✅ **No API key required** (free)
- ✅ Works out of the box
- ✅ Good accuracy for English
- ⚠️ Requires internet connection
- ⚠️ May have rate limits

## If You Want to Use OpenAI Whisper

### Option 1: OpenAI Whisper API (Cloud)
**Requires API Key**: Yes

1. Get API key from: https://platform.openai.com/api-keys
2. Add to environment:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

3. Update `services/voice-service/main.py` to use OpenAI API instead of SpeechRecognition

### Option 2: Local Whisper (No API Key Needed)
**Requires API Key**: No, but needs model download

1. Install whisper:
```bash
pip install openai-whisper
```

2. Download model (first time):
```python
import whisper
model = whisper.load_model("base")  # Downloads ~150MB
```

3. Update voice service to use local whisper

## Recommendation
**Keep current setup** (SpeechRecognition) unless you need:
- Better accuracy for non-English
- Offline transcription
- Higher rate limits

The current setup works well for interview practice!

