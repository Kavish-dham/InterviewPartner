"""
API Gateway
Main entry point with WebSocket support for real-time voice interaction
Coordinates Interview Service and Voice Service
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import json
import base64
import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from services.shared.models import (
    SessionCreate, 
    InterviewType, 
    PDFParseRequest, 
    PDFParseResponse,
    VoiceTranscriptionRequest
)

app = FastAPI(title="Interview Practice API Gateway", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs (use environment variables in production)
INTERVIEW_SERVICE_URL = os.getenv("INTERVIEW_SERVICE_URL", "http://localhost:8001")
VOICE_SERVICE_URL = os.getenv("VOICE_SERVICE_URL", "http://localhost:8002")

# HTTP client for service communication
http_client = httpx.AsyncClient(timeout=30.0)


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
    
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
    
    async def send_message(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)


manager = ConnectionManager()


@app.post("/api/sessions")
async def create_session(session_data: SessionCreate):
    """Create a new interview session"""
    try:
        response = await http_client.post(
            f"{INTERVIEW_SERVICE_URL}/sessions",
            json={
                "resume": session_data.resume,
                "job_description": session_data.job_description,
                "interview_type": session_data.interview_type.value
            }
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session status"""
    try:
        response = await http_client.get(f"{INTERVIEW_SERVICE_URL}/sessions/{session_id}")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session: {str(e)}")


@app.post("/api/sessions/{session_id}/start")
async def start_interview(session_id: str):
    """Start interview and get first question"""
    try:
        response = await http_client.post(f"{INTERVIEW_SERVICE_URL}/sessions/{session_id}/start")
        response.raise_for_status()
        question_data = response.json()
        
        # Get TTS audio for the question
        tts_response = await http_client.post(
            f"{VOICE_SERVICE_URL}/synthesize",
            json={"text": question_data["question"]}
        )
        tts_data = tts_response.json() if tts_response.status_code == 200 else None
        
        return {
            **question_data,
            "audio": tts_data.get("audio_data") if tts_data else None
        }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to start interview: {str(e)}")


@app.post("/api/sessions/{session_id}/submit-answer")
async def submit_answer(session_id: str, answer_data: dict):
    """Submit an answer"""
    try:
        answer = answer_data.get("answer", "")
        collect_mode = answer_data.get("collect_mode", True)
        
        # Get current question from session
        session_response = await http_client.get(f"{INTERVIEW_SERVICE_URL}/sessions/{session_id}")
        session = session_response.json()
        current_question = session.get("current_question", "")
        
        response = await http_client.post(
            f"{INTERVIEW_SERVICE_URL}/sessions/{session_id}/submit-answer",
            params={"collect_mode": collect_mode},
            json={
                "session_id": session_id,
                "question": current_question,
                "answer": answer
            }
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit answer: {str(e)}")


@app.post("/api/sessions/{session_id}/next-question")
async def get_next_question(session_id: str):
    """Get next question with TTS audio"""
    try:
        response = await http_client.post(f"{INTERVIEW_SERVICE_URL}/sessions/{session_id}/next-question")
        response.raise_for_status()
        question_data = response.json()
        
        # Get TTS audio
        tts_response = await http_client.post(
            f"{VOICE_SERVICE_URL}/synthesize",
            json={"text": question_data["question"]}
        )
        tts_data = tts_response.json() if tts_response.status_code == 200 else None
        
        return {
            **question_data,
            "audio": tts_data.get("audio_data") if tts_data else None
        }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to get next question: {str(e)}")


@app.post("/api/sessions/{session_id}/evaluate-all")
async def evaluate_all(session_id: str):
    """Evaluate all collected answers"""
    try:
        response = await http_client.post(f"{INTERVIEW_SERVICE_URL}/sessions/{session_id}/evaluate-all")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to evaluate: {str(e)}")


@app.post("/api/sessions/{session_id}/end")
async def end_interview(session_id: str):
    """End interview and get final report"""
    try:
        response = await http_client.post(f"{INTERVIEW_SERVICE_URL}/sessions/{session_id}/end")
        response.raise_for_status()
        report = response.json()
        
        # Generate TTS for feedback summary
        feedback_text = f"Your average score was {report.get('average_score', 0):.1f} out of 10."
        tts_response = await http_client.post(
            f"{VOICE_SERVICE_URL}/synthesize",
            json={"text": feedback_text}
        )
        tts_data = tts_response.json() if tts_response.status_code == 200 else None
        
        return {
            **report,
            "audio_summary": tts_data.get("audio_data") if tts_data else None
        }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to end interview: {str(e)}")


@app.post("/api/voice/transcribe")
async def transcribe_audio(request: VoiceTranscriptionRequest):
    """Transcribe audio using Voice Service"""
    try:
        response = await http_client.post(
            f"{VOICE_SERVICE_URL}/transcribe-base64",
            json={
                "audio_data": request.audio_data,
                "audio_format": request.audio_format,
                "language": request.language
            }
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        error_detail = "Transcription failed"
        try:
            if hasattr(e, 'response') and e.response:
                error_response = e.response.json()
                error_detail = error_response.get('detail', str(e))
        except:
            error_detail = str(e)
        raise HTTPException(status_code=500, detail=error_detail)


@app.post("/api/parse-pdf", response_model=PDFParseResponse)
async def parse_pdf_endpoint(request: PDFParseRequest):
    """Parse PDF file and extract text"""
    try:
        import base64
        import tempfile
        import os
        
        # Import parser from project root
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
        from utils.parser import parse_pdf as parse_pdf_file
        
        if not request.file_data:
            raise HTTPException(status_code=400, detail="No file data provided")
        
        # Decode base64
        try:
            pdf_bytes = base64.b64decode(request.file_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid base64 data: {str(e)}")
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_file_path = tmp_file.name
        
        try:
            # Parse PDF
            text = parse_pdf_file(tmp_file_path)
            if not text:
                raise HTTPException(status_code=400, detail="Could not extract text from PDF")
            
            return PDFParseResponse(text=text, file_name=request.file_name)
        finally:
            # Clean up temp file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF parsing failed: {str(e)}")


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time voice interaction
    Handles bidirectional audio streaming
    """
    await manager.connect(websocket, session_id)
    
    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "session_id": session_id,
            "message": "Connected to interview session"
        })
        
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message_type = data.get("type")
            
            if message_type == "audio":
                # Handle audio transcription
                audio_base64 = data.get("audio_data")
                if audio_base64:
                    # Transcribe
                    transcribe_response = await http_client.post(
                        f"{VOICE_SERVICE_URL}/transcribe-base64",
                        json={
                            "audio_data": audio_base64,
                            "audio_format": "wav"
                        }
                    )
                    
                    if transcribe_response.status_code == 200:
                        transcription = transcribe_response.json()
                        text = transcription.get("text", "")
                        
                        # Send transcription back
                        await websocket.send_json({
                            "type": "transcription",
                            "text": text,
                            "confidence": transcription.get("confidence", 0.0)
                        })
                        
                        # Auto-submit if it's an answer
                        if text.strip():
                            answer_response = await http_client.post(
                                f"{INTERVIEW_SERVICE_URL}/sessions/{session_id}/submit-answer",
                                params={"collect_mode": True},
                                json={
                                    "session_id": session_id,
                                    "question": "",  # Will be filled by service
                                    "answer": text
                                }
                            )
                            
                            if answer_response.status_code == 200:
                                await websocket.send_json({
                                    "type": "answer_submitted",
                                    "message": "Answer received"
                                })
            
            elif message_type == "command":
                command = data.get("command")
                
                if command == "next_question":
                    # Get next question
                    question_response = await http_client.post(
                        f"{INTERVIEW_SERVICE_URL}/sessions/{session_id}/next-question"
                    )
                    
                    if question_response.status_code == 200:
                        question_data = question_response.json()
                        
                        # Get TTS
                        tts_response = await http_client.post(
                            f"{VOICE_SERVICE_URL}/synthesize",
                            json={"text": question_data["question"]}
                        )
                        
                        if tts_response.status_code == 200:
                            tts_data = tts_response.json()
                            await websocket.send_json({
                                "type": "question",
                                "question": question_data["question"],
                                "audio": tts_data.get("audio_data")
                            })
                
                elif command == "end_interview":
                    # Evaluate and get report
                    eval_response = await http_client.post(
                        f"{INTERVIEW_SERVICE_URL}/sessions/{session_id}/evaluate-all"
                    )
                    
                    end_response = await http_client.post(
                        f"{INTERVIEW_SERVICE_URL}/sessions/{session_id}/end"
                    )
                    
                    if end_response.status_code == 200:
                        report = end_response.json()
                        await websocket.send_json({
                            "type": "report",
                            "report": report
                        })
    
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
        manager.disconnect(session_id)


@app.get("/health")
async def health_check():
    """Health check for all services"""
    services_status = {}
    
    # Check Interview Service
    try:
        response = await http_client.get(f"{INTERVIEW_SERVICE_URL}/health", timeout=5.0)
        services_status["interview_service"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        services_status["interview_service"] = "unreachable"
    
    # Check Voice Service
    try:
        response = await http_client.get(f"{VOICE_SERVICE_URL}/health", timeout=5.0)
        services_status["voice_service"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        services_status["voice_service"] = "unreachable"
    
    return {
        "status": "healthy" if all(s == "healthy" for s in services_status.values()) else "degraded",
        "services": services_status
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

