"""
Interviewer Agent
Conducts the interview and manages conversation flow
"""

import random
from typing import Optional, Dict, List


class InterviewerAgent:
    """Conducts interviews and manages conversation flow"""
    
    def __init__(self, resume: str = "", job_description: str = "", interview_type: str = "Mixed"):
        self.resume = resume
        self.job_description = job_description
        self.interview_type = interview_type
        self.questions_asked = []
        self.current_topic = None
        
    def generate_opening_question(self) -> str:
        """Generate the first question based on role and resume"""
        if not self.resume or not self.job_description:
            return "Please share your resume (paste text) and the job description for the role you are targeting. Also tell me the interview style you want: Behavioral, Technical, or Mixed."
        
        # Extract key information for personalization
        opening_questions = []
        
        if self.interview_type in ["Behavioral", "Mixed"]:
            opening_questions.extend([
                "Tell me about yourself and why you're interested in this role.",
                "Walk me through your background and what draws you to this position.",
                "Can you start by introducing yourself and explaining your interest in this role?",
            ])
        
        if self.interview_type in ["Technical", "Mixed"]:
            opening_questions.extend([
                "Let's start with your technical background. Can you tell me about your experience with the technologies mentioned in this role?",
                "I'd like to understand your technical expertise. How does your background align with the requirements for this position?",
            ])
        
        if opening_questions:
            question = random.choice(opening_questions)
            self.questions_asked.append(question)
            return question
        
        return "Tell me about yourself and why you're interested in this role."
    
    def generate_question(self, previous_answer: Optional[str] = None, question_count: int = 0) -> str:
        """Generate the next interview question"""
        if question_count == 0:
            return self.generate_opening_question()
        
        # Generate contextual questions based on interview type
        questions = []
        
        if self.interview_type in ["Behavioral", "Mixed"]:
            behavioral_questions = self._generate_behavioral_questions()
            questions.extend(behavioral_questions)
        
        if self.interview_type in ["Technical", "Mixed"]:
            technical_questions = self._generate_technical_questions()
            questions.extend(technical_questions)
        
        # Filter out already asked questions
        available_questions = [q for q in questions if q not in self.questions_asked]
        
        if not available_questions:
            # If all questions asked, generate follow-up variations
            available_questions = questions
        
        if available_questions:
            question = random.choice(available_questions)
            self.questions_asked.append(question)
            return question
        
        return "Can you tell me more about a challenging project you've worked on?"
    
    def _generate_behavioral_questions(self) -> List[str]:
        """Generate behavioral interview questions"""
        questions = [
            "Tell me about a time when you had to work under pressure. How did you handle it?",
            "Describe a situation where you had to deal with a difficult team member or conflict.",
            "Can you give me an example of a time you took initiative on a project?",
            "Tell me about a time you had to learn something new quickly for a project.",
            "Describe a situation where you had to make a difficult decision with limited information.",
            "Can you share an example of when you had to adapt to a significant change at work?",
            "Tell me about a time you failed at something. What did you learn from it?",
            "Describe a project where you had to collaborate with multiple stakeholders.",
            "Can you give me an example of when you had to persuade someone to see things your way?",
            "Tell me about a time you had to prioritize multiple competing deadlines.",
        ]
        return questions
    
    def _generate_technical_questions(self) -> List[str]:
        """Generate technical interview questions based on job description"""
        # Extract technical keywords from job description (simplified)
        tech_keywords = self._extract_tech_keywords()
        
        questions = [
            "Can you walk me through how you would approach [a technical problem relevant to this role]?",
            "Tell me about a technical challenge you've faced and how you solved it.",
            "How do you stay current with technology trends in your field?",
            "Can you describe a complex technical project you've worked on?",
            "What's your experience with [relevant technology]?",
            "How would you debug a production issue that's affecting multiple users?",
            "Can you explain [a technical concept relevant to the role]?",
            "Tell me about a time you had to optimize performance in a system you built.",
        ]
        
        # Personalize questions with extracted keywords
        if tech_keywords:
            personalized = [
                f"Can you describe your experience with {tech_keywords[0]}?",
                f"How have you used {tech_keywords[0]} in your previous projects?",
                f"Tell me about a project where you leveraged {tech_keywords[0]}.",
            ]
            questions.extend(personalized)
        
        return questions
    
    def _extract_tech_keywords(self) -> List[str]:
        """Extract technical keywords from job description"""
        common_tech = [
            "Python", "JavaScript", "Java", "React", "AWS", "Docker", "Kubernetes",
            "SQL", "MongoDB", "PostgreSQL", "Git", "CI/CD", "Agile", "Scrum",
            "Machine Learning", "Data Science", "API", "REST", "GraphQL",
            "Microservices", "Cloud", "DevOps", "Testing", "Security"
        ]
        
        found_keywords = []
        job_desc_lower = self.job_description.lower()
        
        for tech in common_tech:
            if tech.lower() in job_desc_lower:
                found_keywords.append(tech)
        
        return found_keywords[:5]  # Return top 5
    
    def update_context(self, resume: str, job_description: str, interview_type: str):
        """Update agent context with new information"""
        self.resume = resume
        self.job_description = job_description
        self.interview_type = interview_type

