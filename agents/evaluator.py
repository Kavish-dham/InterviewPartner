"""
Evaluator Agent
Scores answers using a structured rubric
"""

from typing import Dict, Optional
import re


class EvaluatorAgent:
    """Evaluates and scores interview answers"""
    
    def __init__(self):
        self.scores = []
    
    def evaluate(self, question: str, answer: str, question_type: str = "general") -> Dict[str, float]:
        """Evaluate an answer and return scores"""
        if not answer or len(answer.strip()) < 10:
            return self._default_low_scores()
        
        scores = {
            "clarity": self._score_clarity(answer),
            "communication": self._score_communication(answer),
            "star_structure": self._score_star_structure(answer, question_type),
            "role_relevance": self._score_role_relevance(question, answer),
            "technical_depth": self._score_technical_depth(answer, question_type),
        }
        
        # Calculate overall score
        scores["overall"] = sum(scores.values()) / len(scores)
        
        self.scores.append(scores)
        return scores
    
    def _score_clarity(self, answer: str) -> float:
        """Score clarity of the answer (1-10)"""
        score = 5.0  # Base score
        
        # Positive indicators
        if len(answer) > 100:
            score += 1.0
        if any(word in answer.lower() for word in ["specifically", "for example", "to illustrate"]):
            score += 0.5
        if answer.count(".") > 2:  # Well-structured sentences
            score += 0.5
        
        # Negative indicators
        if "um" in answer.lower() or "uh" in answer.lower():
            score -= 0.5
        if answer.count("like") > 3:
            score -= 0.5
        if len(answer) < 50:
            score -= 2.0
        
        return max(1.0, min(10.0, score))
    
    def _score_communication(self, answer: str) -> float:
        """Score communication effectiveness (1-10)"""
        score = 5.0
        
        # Positive indicators
        if len(answer.split()) > 50:  # Substantive answer
            score += 1.5
        if any(word in answer.lower() for word in ["because", "therefore", "as a result"]):
            score += 0.5  # Shows reasoning
        if answer.count(",") > 3:  # Well-structured
            score += 0.5
        
        # Negative indicators
        if len(answer.split()) < 20:
            score -= 2.0
        if answer.count("I don't know") > 0 or answer.count("I'm not sure") > 0:
            score -= 1.0
        
        return max(1.0, min(10.0, score))
    
    def _score_star_structure(self, answer: str, question_type: str) -> float:
        """Score STAR format usage (1-10)"""
        if question_type != "behavioral":
            return 7.0  # Not applicable, neutral score
        
        score = 3.0  # Base score
        
        answer_lower = answer.lower()
        
        # Check for STAR components
        situation_indicators = ["situation", "context", "when", "where", "background"]
        task_indicators = ["task", "goal", "objective", "responsibility", "challenge"]
        action_indicators = ["action", "did", "implemented", "created", "developed", "worked"]
        result_indicators = ["result", "outcome", "impact", "achieved", "improved", "saved"]
        
        if any(indicator in answer_lower for indicator in situation_indicators):
            score += 1.5
        if any(indicator in answer_lower for indicator in task_indicators):
            score += 1.5
        if any(indicator in answer_lower for indicator in action_indicators):
            score += 1.5
        if any(indicator in answer_lower for indicator in result_indicators):
            score += 1.5
        
        # Bonus for clear structure
        if answer.count(".") > 3:
            score += 0.5
        
        return max(1.0, min(10.0, score))
    
    def _score_role_relevance(self, question: str, answer: str) -> float:
        """Score relevance to the role (1-10)"""
        score = 5.0
        
        # Extract keywords from question
        question_lower = question.lower()
        answer_lower = answer.lower()
        
        # Check if answer addresses the question
        question_keywords = set(re.findall(r'\b\w{4,}\b', question_lower))
        answer_keywords = set(re.findall(r'\b\w{4,}\b', answer_lower))
        
        overlap = len(question_keywords.intersection(answer_keywords))
        if overlap > 0:
            score += min(2.0, overlap * 0.3)
        
        # Check for professional language
        professional_terms = ["project", "team", "experience", "developed", "implemented", "managed"]
        if any(term in answer_lower for term in professional_terms):
            score += 1.0
        
        return max(1.0, min(10.0, score))
    
    def _score_technical_depth(self, answer: str, question_type: str) -> float:
        """Score technical depth (1-10)"""
        if question_type != "technical":
            return 7.0  # Not applicable, neutral score
        
        score = 4.0
        
        answer_lower = answer.lower()
        
        # Technical indicators
        tech_indicators = [
            "algorithm", "architecture", "system", "database", "api", "framework",
            "optimization", "scalability", "performance", "debug", "test", "deploy",
            "code", "implementation", "design", "pattern", "protocol"
        ]
        
        found_indicators = sum(1 for indicator in tech_indicators if indicator in answer_lower)
        score += min(3.0, found_indicators * 0.5)
        
        # Depth indicators
        if len(answer.split()) > 100:
            score += 1.0
        if any(word in answer_lower for word in ["because", "reason", "why", "how"]):
            score += 1.0
        
        return max(1.0, min(10.0, score))
    
    def _default_low_scores(self) -> Dict[str, float]:
        """Return default low scores for insufficient answers"""
        return {
            "clarity": 3.0,
            "communication": 3.0,
            "star_structure": 3.0,
            "role_relevance": 3.0,
            "technical_depth": 3.0,
            "overall": 3.0,
        }
    
    def get_average_scores(self) -> Dict[str, float]:
        """Get average scores across all evaluations"""
        if not self.scores:
            return {}
        
        averages = {}
        for key in self.scores[0].keys():
            averages[key] = sum(s[key] for s in self.scores) / len(self.scores)
        
        return averages

