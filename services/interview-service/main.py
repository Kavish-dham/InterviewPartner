"""
Interview Service
Core interview logic with REST API
Handles session management, question generation, and evaluation
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Optional
import uuid
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from session import InterviewSession
from services.shared.models import (
    SessionCreate,
    SessionStatus,
    InterviewRequest,
    QuestionResponse,
    AnswerSubmission,
    EvaluationRequest,
    EvaluationResponse,
    InterviewResponse,
    FinalReportRequest,
    FinalReportResponse,
)

app = FastAPI(title="Interview Service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage (use Redis in production)
sessions: Dict[str, InterviewSession] = {}


@app.post("/sessions", response_model=InterviewResponse)
async def create_session(session_data: SessionCreate):
    """Create a new interview session"""
    session_id = str(uuid.uuid4())
    
    session = InterviewSession()
    session.initialize(
        resume=session_data.resume,
        job_description=session_data.job_description,
        interview_type=session_data.interview_type.value
    )
    
    sessions[session_id] = session
    
    return InterviewResponse(
        session_id=session_id,
        status=SessionStatus.CREATED,
        question_count=0,
        answer_count=0,
        current_question=None
    )


@app.get("/sessions/{session_id}", response_model=InterviewResponse)
async def get_session_status(session_id: str):
    """Get session status"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    return InterviewResponse(
        session_id=session_id,
        status=SessionStatus.ACTIVE if session.session_active else SessionStatus.COMPLETED,
        question_count=session.question_count,
        answer_count=len(session.all_scores),
        current_question=session.current_question if session.session_active else None
    )


@app.post("/sessions/{session_id}/start", response_model=QuestionResponse)
async def start_interview(session_id: str):
    """Start the interview and get first question"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    question = session.start_interview()
    
    return QuestionResponse(
        session_id=session_id,
        question=question,
        question_number=session.question_count,
        question_type=session.current_question_type,
        followup_needed=False
    )


@app.post("/sessions/{session_id}/next-question", response_model=QuestionResponse)
async def get_next_question(session_id: str):
    """Get the next interview question"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    if not session.session_active:
        raise HTTPException(status_code=400, detail="Session is not active")
    
    question = session.get_next_question()
    
    if not question:
        raise HTTPException(status_code=400, detail="No more questions available")
    
    return QuestionResponse(
        session_id=session_id,
        question=question,
        question_number=session.question_count,
        question_type=session.current_question_type,
        followup_needed=False
    )


@app.post("/sessions/{session_id}/submit-answer", response_model=EvaluationResponse)
async def submit_answer(session_id: str, answer_data: AnswerSubmission, collect_mode: bool = True):
    """Submit an answer (collect mode: just store, evaluate mode: evaluate immediately)"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    if not session.session_active:
        raise HTTPException(status_code=400, detail="Session is not active")
    
    if collect_mode:
        # Just collect the answer, don't evaluate yet
        # Store in a temporary structure
        if not hasattr(session, 'collected_answers'):
            session.collected_answers = []
        
        session.collected_answers.append({
            'question': answer_data.question,
            'answer': answer_data.answer,
            'question_type': answer_data.question_type or session.current_question_type
        })
        
        return EvaluationResponse(
            session_id=session_id,
            question=answer_data.question,
            answer=answer_data.answer,
            scores={},
            feedback={},
            followup_question=None
        )
    else:
        # Evaluate immediately (legacy mode)
        result = session.process_answer(answer_data.answer)
        
        return EvaluationResponse(
            session_id=session_id,
            question=result.get('question', answer_data.question),
            answer=result.get('answer', answer_data.answer),
            scores=result.get('scores', {}),
            feedback=result.get('feedback', {}),
            followup_question=result.get('followup_question')
        )


@app.post("/sessions/{session_id}/evaluate-all", response_model=Dict)
async def evaluate_all_answers(session_id: str):
    """Evaluate all collected answers and generate feedback"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    if not hasattr(session, 'collected_answers') or not session.collected_answers:
        raise HTTPException(status_code=400, detail="No answers collected to evaluate")
    
    # Process all collected answers
    evaluations = []
    for qa_pair in session.collected_answers:
        result = session.process_answer(qa_pair['answer'])
        evaluations.append({
            'question': qa_pair['question'],
            'answer': qa_pair['answer'],
            'scores': result.get('scores', {}),
            'feedback': result.get('feedback', {})
        })
    
    return {
        'session_id': session_id,
        'evaluations': evaluations,
        'total_evaluated': len(evaluations)
    }


@app.post("/sessions/{session_id}/end", response_model=FinalReportResponse)
async def end_interview(session_id: str):
    """End interview and generate final report"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    # Evaluate any remaining collected answers
    if hasattr(session, 'collected_answers') and session.collected_answers:
        for qa_pair in session.collected_answers:
            session.process_answer(qa_pair['answer'])
    
    result = session.end_interview()
    
    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])
    
    report_text = result.get('final_report', '')
    summary = result.get('session_summary', {})
    
    # Parse report to extract structured data
    # For now, return basic structure
    avg_scores = session.evaluator.get_average_scores() if session.all_scores else {}
    
    return FinalReportResponse(
        session_id=session_id,
        average_score=avg_scores.get('overall', 0.0),
        detailed_scores=avg_scores,
        key_strengths=[],  # Would parse from report_text
        key_improvements=[],  # Would parse from report_text
        recommended_topics=[],  # Would parse from report_text
        next_focus="",  # Would parse from report_text
        total_questions=summary.get('total_questions', 0),
        total_answers=summary.get('total_answers', 0)
    )


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    del sessions[session_id]
    return {"message": "Session deleted"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "interview-service",
        "active_sessions": len(sessions)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

