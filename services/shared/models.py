"""
Shared data models for microservices communication
"""

from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from enum import Enum


class InterviewType(str, Enum):
    BEHAVIORAL = "Behavioral"
    TECHNICAL = "Technical"
    MIXED = "Mixed"


class SessionStatus(str, Enum):
    CREATED = "created"
    ACTIVE = "active"
    COLLECTING = "collecting"
    EVALUATING = "evaluating"
    COMPLETED = "completed"
    ERROR = "error"


# Interview Service Models
class SessionCreate(BaseModel):
    resume: str
    job_description: str
    interview_type: InterviewType = InterviewType.MIXED


class InterviewRequest(BaseModel):
    session_id: str


class QuestionResponse(BaseModel):
    session_id: str
    question: str
    question_number: int
    question_type: str
    followup_needed: bool = False


class AnswerSubmission(BaseModel):
    session_id: str
    question: str
    answer: str
    question_type: Optional[str] = None


class EvaluationRequest(BaseModel):
    session_id: str
    collect_mode: bool = True  # If True, just collect. If False, evaluate immediately


class EvaluationResponse(BaseModel):
    session_id: str
    question: str
    answer: str
    scores: Dict[str, float]
    feedback: Dict[str, Any]
    followup_question: Optional[str] = None


class InterviewResponse(BaseModel):
    session_id: str
    status: SessionStatus
    question_count: int
    answer_count: int
    current_question: Optional[str] = None


# Voice Service Models
class VoiceTranscriptionRequest(BaseModel):
    audio_data: str  # Base64 encoded audio string
    audio_format: str = "wav"  # wav, mp3, etc.
    language: Optional[str] = None  # Auto-detect if None


class VoiceTranscriptionResponse(BaseModel):
    text: str
    confidence: float
    language: Optional[str] = None


class VoiceSynthesisRequest(BaseModel):
    text: str
    voice_id: Optional[str] = None
    speed: float = 1.0
    pitch: float = 1.0


class VoiceSynthesisResponse(BaseModel):
    audio_data: bytes  # Base64 encoded audio
    audio_format: str = "wav"
    duration: float  # seconds


# PDF Parsing Models
class PDFParseRequest(BaseModel):
    file_data: str  # Base64 encoded PDF
    file_name: str = "document.pdf"


class PDFParseResponse(BaseModel):
    text: str
    file_name: str


# Final Report Models
class FinalReportRequest(BaseModel):
    session_id: str


class FinalReportResponse(BaseModel):
    session_id: str
    average_score: float
    detailed_scores: Dict[str, float]
    key_strengths: List[str]
    key_improvements: List[str]
    recommended_topics: List[str]
    next_focus: str
    total_questions: int
    total_answers: int

