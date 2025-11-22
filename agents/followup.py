"""
Followup Agent
Generates probing follow-up questions based on user responses
"""

from typing import Optional, List


class FollowupAgent:
    """Generates contextual follow-up questions"""
    
    def __init__(self):
        self.followup_count = 0
    
    def should_ask_followup(self, answer: str, question_type: str = "general") -> bool:
        """Determine if a follow-up question is needed"""
        if not answer or len(answer.strip()) < 50:
            return True  # Answer is too short
        
        # Check if answer seems incomplete
        incomplete_indicators = [
            "I'm not sure",
            "I don't know",
            "I can't remember",
            "I guess",
            "maybe",
        ]
        
        answer_lower = answer.lower()
        if any(indicator in answer_lower for indicator in incomplete_indicators):
            return True
        
        # Check if answer lacks structure (for STAR questions)
        if question_type == "behavioral":
            star_indicators = ["situation", "task", "action", "result"]
            if not any(indicator in answer_lower for indicator in star_indicators):
                return True
        
        return False
    
    def generate_followup(self, question: str, answer: str, question_type: str = "general") -> Optional[str]:
        """Generate a contextual follow-up question"""
        if not self.should_ask_followup(answer, question_type):
            return None
        
        self.followup_count += 1
        
        answer_lower = answer.lower()
        
        # Behavioral follow-ups
        if question_type == "behavioral":
            if "situation" not in answer_lower and "context" not in answer_lower:
                return "Can you provide more context about the situation you were in?"
            if "task" not in answer_lower and "goal" not in answer_lower:
                return "What was your specific role or responsibility in that situation?"
            if "action" not in answer_lower and "did" not in answer_lower:
                return "What specific actions did you take to address this?"
            if "result" not in answer_lower and "outcome" not in answer_lower:
                return "What was the outcome or result of your actions?"
        
        # Technical follow-ups
        if question_type == "technical":
            if "how" not in answer_lower and "approach" not in answer_lower:
                return "Can you walk me through your approach step by step?"
            if "challenge" not in answer_lower and "difficulty" not in answer_lower:
                return "What were the main challenges you encountered?"
            if "learn" not in answer_lower and "takeaway" not in answer_lower:
                return "What did you learn from this experience?"
        
        # General follow-ups
        general_followups = [
            "Can you provide more detail about that?",
            "What specific example can you share?",
            "How did that impact the project or team?",
            "Can you elaborate on that point?",
            "What was the most challenging aspect?",
        ]
        
        # Context-specific follow-ups
        if len(answer.strip()) < 50:
            return "Can you expand on that answer? I'd like to hear more details."
        
        if "I don't know" in answer_lower or "I'm not sure" in answer_lower:
            return "That's okay. Can you think of a related experience or how you might approach this?"
        
        # Default follow-up
        return "Can you tell me more about that?"

