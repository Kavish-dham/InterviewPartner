"""
Report Agent
Generates final evaluation and development plan
"""

from typing import Dict, List, Optional


class ReportAgent:
    """Generates final interview session report"""
    
    def __init__(self):
        pass
    
    def generate_report(self, all_scores: List[Dict[str, float]], 
                       all_feedback: List[Dict[str, any]],
                       interview_type: str = "Mixed") -> Dict[str, any]:
        """Generate comprehensive final report"""
        if not all_scores:
            return {
                "average_score": 0.0,
                "key_strengths": ["No answers evaluated yet"],
                "key_improvements": ["Complete the interview to receive feedback"],
                "recommended_topics": [],
                "next_focus": "Complete interview questions",
            }
        
        # Calculate averages
        avg_scores = self._calculate_averages(all_scores)
        
        # Identify key strengths and improvements
        strengths = self._identify_key_strengths(all_scores, all_feedback)
        improvements = self._identify_key_improvements(all_scores, all_feedback)
        
        # Recommend practice topics
        topics = self._recommend_topics(all_scores, interview_type)
        
        # Next session focus
        next_focus = self._suggest_next_focus(improvements, interview_type)
        
        return {
            "average_score": avg_scores.get("overall", 0.0),
            "detailed_scores": avg_scores,
            "key_strengths": strengths,
            "key_improvements": improvements,
            "recommended_topics": topics,
            "next_focus": next_focus,
        }
    
    def _calculate_averages(self, all_scores: List[Dict[str, float]]) -> Dict[str, float]:
        """Calculate average scores across all answers"""
        if not all_scores:
            return {}
        
        averages = {}
        for key in all_scores[0].keys():
            averages[key] = sum(s[key] for s in all_scores) / len(all_scores)
        
        return averages
    
    def _identify_key_strengths(self, all_scores: List[Dict[str, float]], 
                                all_feedback: List[Dict[str, any]]) -> List[str]:
        """Identify key strengths across the interview"""
        strengths = []
        
        if not all_scores:
            return strengths
        
        # Analyze average scores
        avg_scores = self._calculate_averages(all_scores)
        
        if avg_scores.get("clarity", 0) >= 7.0:
            strengths.append("Strong clarity and articulation")
        if avg_scores.get("communication", 0) >= 7.0:
            strengths.append("Effective communication skills")
        if avg_scores.get("star_structure", 0) >= 7.0:
            strengths.append("Good use of structured response formats (STAR)")
        if avg_scores.get("technical_depth", 0) >= 7.0:
            strengths.append("Solid technical knowledge and depth")
        if avg_scores.get("role_relevance", 0) >= 7.0:
            strengths.append("Answers were relevant to the role")
        
        # Extract common strengths from feedback
        common_strengths = {}
        for feedback in all_feedback:
            for strength in feedback.get("strengths", []):
                common_strengths[strength] = common_strengths.get(strength, 0) + 1
        
        # Add most common strengths
        if common_strengths:
            top_strength = max(common_strengths.items(), key=lambda x: x[1])
            if top_strength[1] > 1:
                strengths.append(top_strength[0])
        
        if not strengths:
            strengths.append("Demonstrated effort in answering questions")
        
        return strengths[:5]  # Top 5 strengths
    
    def _identify_key_improvements(self, all_scores: List[Dict[str, float]], 
                                  all_feedback: List[Dict[str, any]]) -> List[str]:
        """Identify key improvement areas"""
        improvements = []
        
        if not all_scores:
            return improvements
        
        # Analyze average scores
        avg_scores = self._calculate_averages(all_scores)
        
        if avg_scores.get("clarity", 0) < 6.0:
            improvements.append("Improve clarity and specificity in responses")
        if avg_scores.get("communication", 0) < 6.0:
            improvements.append("Enhance communication with more detail and context")
        if avg_scores.get("star_structure", 0) < 6.0:
            improvements.append("Practice using STAR format for behavioral questions")
        if avg_scores.get("technical_depth", 0) < 6.0:
            improvements.append("Develop deeper technical explanations and reasoning")
        if avg_scores.get("role_relevance", 0) < 6.0:
            improvements.append("Better connect answers to role requirements")
        
        # Extract common improvements from feedback
        common_improvements = {}
        for feedback in all_feedback:
            for improvement in feedback.get("improvements", []):
                common_improvements[improvement] = common_improvements.get(improvement, 0) + 1
        
        # Add most common improvements
        if common_improvements:
            top_improvement = max(common_improvements.items(), key=lambda x: x[1])
            if top_improvement[1] > 1:
                improvements.append(top_improvement[0])
        
        if not improvements:
            improvements.append("Continue practicing to refine your responses")
        
        return improvements[:5]  # Top 5 improvements
    
    def _recommend_topics(self, all_scores: List[Dict[str, float]], 
                         interview_type: str) -> List[str]:
        """Recommend practice topics based on performance"""
        topics = []
        
        if not all_scores:
            return topics
        
        avg_scores = self._calculate_averages(all_scores)
        
        if avg_scores.get("star_structure", 0) < 7.0:
            topics.append("STAR method for behavioral questions")
        
        if avg_scores.get("technical_depth", 0) < 7.0:
            topics.append("Technical problem-solving and system design")
        
        if avg_scores.get("clarity", 0) < 7.0:
            topics.append("Clear and concise communication")
        
        if avg_scores.get("role_relevance", 0) < 7.0:
            topics.append("Tailoring answers to specific roles")
        
        if interview_type in ["Behavioral", "Mixed"]:
            topics.extend([
                "Conflict resolution scenarios",
                "Leadership and teamwork examples",
                "Handling failure and learning from mistakes",
            ])
        
        if interview_type in ["Technical", "Mixed"]:
            topics.extend([
                "System architecture and design",
                "Debugging and problem-solving",
                "Technology-specific deep dives",
            ])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_topics = []
        for topic in topics:
            if topic not in seen:
                seen.add(topic)
                unique_topics.append(topic)
        
        return unique_topics[:8]  # Top 8 topics
    
    def _suggest_next_focus(self, improvements: List[str], interview_type: str) -> str:
        """Suggest focus for next practice session"""
        if not improvements:
            return "Continue practicing with more interview questions"
        
        # Focus on the most critical improvement
        if any("STAR" in imp or "structure" in imp.lower() for imp in improvements):
            return "Focus on mastering the STAR format for behavioral questions"
        
        if any("technical" in imp.lower() for imp in improvements):
            return "Deepen technical knowledge and problem-solving skills"
        
        if any("clarity" in imp.lower() or "communication" in imp.lower() for imp in improvements):
            return "Work on clear and structured communication"
        
        return improvements[0] if improvements else "Continue general interview practice"

