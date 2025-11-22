"""
Interview Session Manager
Coordinates all agents to conduct interview sessions
"""

from typing import Optional, Dict, List, Any
from agents import (
    InterviewerAgent,
    FollowupAgent,
    EvaluatorAgent,
    FeedbackAgent,
    ReportAgent,
)


class InterviewSession:
    """Manages the interview session and coordinates agents"""
    
    def __init__(self):
        self.resume = ""
        self.job_description = ""
        self.interview_type = "Mixed"
        
        # Initialize agents
        self.interviewer = InterviewerAgent()
        self.followup = FollowupAgent()
        self.evaluator = EvaluatorAgent()
        self.feedback = FeedbackAgent()
        self.report = ReportAgent()
        
        # Session state
        self.question_count = 0
        self.current_question = ""
        self.current_answer = ""
        self.all_scores = []
        self.all_feedback = []
        self.session_active = False
        self.current_question_type = "general"
        self.collected_answers = []  # For iterative collection mode
    
    def initialize(self, resume: str = "", job_description: str = "", 
                  interview_type: str = "Mixed"):
        """Initialize the session with user inputs"""
        self.resume = resume
        self.job_description = job_description
        self.interview_type = interview_type
        
        # Update agent contexts
        self.interviewer.update_context(resume, job_description, interview_type)
        
        self.session_active = True
        self.question_count = 0
    
    def start_interview(self) -> str:
        """Start the interview and return the first question"""
        if not self.resume or not self.job_description:
            return "Please share your resume (paste text) and the job description for the role you are targeting. Also tell me the interview style you want: Behavioral, Technical, or Mixed."
        
        self.session_active = True
        question = self.interviewer.generate_opening_question()
        self.current_question = question
        self.question_count += 1
        self._determine_question_type(question)
        return question
    
    def process_answer(self, answer: str) -> Dict[str, Any]:
        """Process user's answer and return evaluation/feedback"""
        if not self.session_active:
            return {"error": "Session not active. Please start an interview first."}
        
        self.current_answer = answer
        
        # Determine if follow-up is needed
        followup_question = None
        if self.followup.should_ask_followup(answer, self.current_question_type):
            followup_question = self.followup.generate_followup(
                self.current_question, answer, self.current_question_type
            )
        
        # Evaluate the answer
        scores = self.evaluator.evaluate(
            self.current_question, answer, self.current_question_type
        )
        self.all_scores.append(scores)
        
        # Generate feedback
        feedback = self.feedback.generate_feedback(
            self.current_question, answer, scores, self.current_question_type
        )
        self.all_feedback.append(feedback)
        
        # Format response
        response = {
            "question": self.current_question,
            "answer": answer,
            "assessment": self._format_assessment(scores),
            "feedback": self._format_feedback(feedback),
        }
        
        # Add follow-up if needed
        if followup_question:
            response["followup_question"] = followup_question
        
        return response
    
    def get_next_question(self) -> Optional[str]:
        """Get the next interview question"""
        if not self.session_active:
            return None
        
        question = self.interviewer.generate_question(
            self.current_answer, self.question_count
        )
        self.current_question = question
        self.question_count += 1
        self.current_answer = ""
        self._determine_question_type(question)
        return question
    
    def end_interview(self) -> Dict[str, Any]:
        """End the interview and generate final report"""
        if not self.session_active:
            return {"error": "No active session to end."}
        
        self.session_active = False
        
        # Generate final report
        report = self.report.generate_report(
            self.all_scores, self.all_feedback, self.interview_type
        )
        
        return {
            "final_report": self._format_final_report(report),
            "session_summary": {
                "total_questions": self.question_count,
                "total_answers": len(self.all_scores),
            }
        }
    
    def _determine_question_type(self, question: str):
        """Determine the type of question (behavioral, technical, general)"""
        question_lower = question.lower()
        
        behavioral_keywords = [
            "tell me about a time", "describe a situation", "give me an example",
            "when did you", "situation", "conflict", "challenge", "pressure"
        ]
        
        technical_keywords = [
            "technical", "how would you", "explain", "algorithm", "system",
            "design", "implement", "debug", "optimize", "architecture"
        ]
        
        if any(keyword in question_lower for keyword in behavioral_keywords):
            self.current_question_type = "behavioral"
        elif any(keyword in question_lower for keyword in technical_keywords):
            self.current_question_type = "technical"
        else:
            self.current_question_type = "general"
    
    def _format_assessment(self, scores: Dict[str, float]) -> str:
        """Format assessment scores"""
        return f"""**ASSESSMENT**

Clarity: {scores.get('clarity', 0):.1f}/10
Communication: {scores.get('communication', 0):.1f}/10
STAR / Structure: {scores.get('star_structure', 0):.1f}/10
Role relevance: {scores.get('role_relevance', 0):.1f}/10
Technical depth (if applicable): {scores.get('technical_depth', 0):.1f}/10
Overall Score: {scores.get('overall', 0):.1f}/10"""
    
    def _format_feedback(self, feedback: Dict[str, Any]) -> str:
        """Format feedback"""
        strengths = "\n".join(f"• {s}" for s in feedback.get("strengths", []))
        improvements = "\n".join(f"• {i}" for i in feedback.get("improvements", []))
        sample = feedback.get("sample_answer", "")
        
        return f"""**FEEDBACK**

Strengths:
{strengths}

Areas to Improve:
{improvements}

Sample Improved Answer:
{sample}"""
    
    def _format_final_report(self, report: Dict[str, Any]) -> str:
        """Format final report"""
        avg_score = report.get("average_score", 0.0)
        strengths = "\n".join(f"• {s}" for s in report.get("key_strengths", []))
        improvements = "\n".join(f"• {i}" for i in report.get("key_improvements", []))
        topics = "\n".join(f"• {t}" for t in report.get("recommended_topics", []))
        next_focus = report.get("next_focus", "")
        
        # Add detailed scores if available
        detailed_scores = report.get("detailed_scores", {})
        score_details = ""
        if detailed_scores:
            score_details = "\n\n**Detailed Average Scores:**\n"
            for key, value in detailed_scores.items():
                if key != "overall":
                    score_details += f"{key.replace('_', ' ').title()}: {value:.1f}/10\n"
        
        return f"""**FINAL REPORT**

Average Score: {avg_score:.1f}/10{score_details}

Key Strengths:
{strengths}

Key Improvement Areas:
{improvements}

Recommended practice topics:
{topics}

Next session focus:
{next_focus}"""

