"""
Feedback Agent
Provides improvement suggestions, strengths, weaknesses, and example responses
"""

from typing import Dict, List, Optional


class FeedbackAgent:
    """Provides detailed feedback on interview answers"""
    
    def __init__(self):
        pass
    
    def generate_feedback(self, question: str, answer: str, scores: Dict[str, float], 
                         question_type: str = "general") -> Dict[str, any]:
        """Generate comprehensive feedback"""
        strengths = self._identify_strengths(answer, scores, question_type)
        improvements = self._identify_improvements(answer, scores, question_type)
        sample_answer = self._generate_sample_answer(question, question_type)
        
        return {
            "strengths": strengths,
            "improvements": improvements,
            "sample_answer": sample_answer,
        }
    
    def _identify_strengths(self, answer: str, scores: Dict[str, float], 
                           question_type: str) -> List[str]:
        """Identify strengths in the answer"""
        strengths = []
        
        if scores.get("clarity", 0) >= 7.0:
            strengths.append("Clear and well-articulated response")
        if scores.get("communication", 0) >= 7.0:
            strengths.append("Effective communication with good detail")
        if scores.get("star_structure", 0) >= 7.0 and question_type == "behavioral":
            strengths.append("Good use of STAR format structure")
        if scores.get("technical_depth", 0) >= 7.0 and question_type == "technical":
            strengths.append("Demonstrated solid technical knowledge")
        if scores.get("role_relevance", 0) >= 7.0:
            strengths.append("Answer was relevant to the role")
        
        if len(answer.split()) > 100:
            strengths.append("Comprehensive and detailed response")
        
        if not strengths:
            strengths.append("Attempted to address the question")
        
        return strengths
    
    def _identify_improvements(self, answer: str, scores: Dict[str, float], 
                              question_type: str) -> List[str]:
        """Identify areas for improvement"""
        improvements = []
        
        if scores.get("clarity", 0) < 6.0:
            improvements.append("Work on clarity - be more specific and concise")
        if scores.get("communication", 0) < 6.0:
            improvements.append("Enhance communication - provide more context and detail")
        if scores.get("star_structure", 0) < 6.0 and question_type == "behavioral":
            improvements.append("Use STAR format: clearly describe Situation, Task, Action, and Result")
        if scores.get("technical_depth", 0) < 6.0 and question_type == "technical":
            improvements.append("Provide more technical depth - explain your approach and reasoning")
        if scores.get("role_relevance", 0) < 6.0:
            improvements.append("Better connect your answer to the role requirements")
        
        if len(answer.split()) < 50:
            improvements.append("Provide more detail and examples")
        
        answer_lower = answer.lower()
        if "um" in answer_lower or "uh" in answer_lower:
            improvements.append("Reduce filler words - practice speaking more confidently")
        
        if question_type == "behavioral":
            star_components = ["situation", "task", "action", "result"]
            missing = [comp for comp in star_components if comp not in answer_lower]
            if missing:
                improvements.append(f"Ensure you cover all STAR components, especially: {', '.join(missing)}")
        
        if not improvements:
            improvements.append("Continue building on your strengths")
        
        return improvements
    
    def _generate_sample_answer(self, question: str, question_type: str) -> str:
        """Generate a sample improved answer"""
        if question_type == "behavioral":
            return self._sample_behavioral_answer(question)
        elif question_type == "technical":
            return self._sample_technical_answer(question)
        else:
            return self._sample_general_answer(question)
    
    def _sample_behavioral_answer(self, question: str) -> str:
        """Sample behavioral answer using STAR format"""
        return """Here's an example of a well-structured answer using STAR format:

**Situation:** In my previous role as a Software Engineer, we were facing a critical production issue that was affecting 30% of our users.

**Task:** My responsibility was to identify the root cause and implement a fix within 4 hours to minimize user impact.

**Action:** I immediately started by analyzing error logs and tracing the issue to a recent database migration. I collaborated with the database team to roll back the problematic change, then worked with the development team to create a safer migration script with proper testing.

**Result:** We resolved the issue within 3 hours, reducing user impact by 90%. The incident led to implementing better testing procedures for database changes, preventing similar issues in the future. This experience taught me the importance of thorough testing and quick problem-solving under pressure."""
    
    def _sample_technical_answer(self, question: str) -> str:
        """Sample technical answer"""
        return """Here's an example of a strong technical answer:

I would approach this by first understanding the requirements and constraints. Then I'd break down the problem into smaller components. 

For implementation, I'd start with a proof of concept to validate the approach, then iterate based on feedback. I'd ensure proper error handling, logging, and testing at each stage.

I'd also consider scalability from the start - thinking about how the solution would perform under load and what optimizations might be needed. Code review and documentation would be important to maintain quality and help future developers understand the system."""
    
    def _sample_general_answer(self, question: str) -> str:
        """Sample general answer"""
        return """Here's an example of a well-structured answer:

I would approach this by first gathering all relevant information and understanding the context. Then I'd outline my approach, considering different options and their trade-offs.

I'd provide specific examples from my experience where applicable, and explain my reasoning clearly. I'd also consider the impact on stakeholders and how to measure success.

Finally, I'd summarize the key points and be open to feedback or follow-up questions."""

