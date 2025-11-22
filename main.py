"""
Main entry point for the Interview Practice System
Multi-agent system for conducting interview simulations
"""

import sys
from session import InterviewSession
from utils.parser import parse_pdf, parse_text


def print_separator():
    """Print a visual separator"""
    print("\n" + "="*70 + "\n")


def print_header(text: str):
    """Print a formatted header"""
    print_separator()
    print(f"  {text}")
    print_separator()


def main():
    """Main application loop"""
    print_header("Interview Practice System - Multi-Agent Interview Simulator")
    
    session = InterviewSession()
    
    # Initial setup
    print("Welcome! I'm your interview practice partner.")
    print("\nTo get started, I'll need:")
    print("1. Your resume (text or PDF path)")
    print("2. Job description (text or PDF path)")
    print("3. Interview type: Behavioral, Technical, or Mixed")
    print("\nYou can also type 'help' at any time for commands.")
    
    # Collect initial information
    resume = ""
    job_description = ""
    interview_type = "Mixed"
    
    print_separator()
    
    # Get resume
    resume_input = input("Resume (paste text or provide PDF path): ").strip()
    if resume_input.lower().endswith('.pdf'):
        resume = parse_pdf(resume_input)
        if not resume:
            print("Warning: Could not parse PDF. Please paste text directly.")
            resume = input("Resume (paste text): ").strip()
    else:
        resume = resume_input
    
    # Get job description
    job_desc_input = input("\nJob Description (paste text or provide PDF path): ").strip()
    if job_desc_input.lower().endswith('.pdf'):
        job_description = parse_pdf(job_desc_input)
        if not job_description:
            print("Warning: Could not parse PDF. Please paste text directly.")
            job_description = input("Job Description (paste text): ").strip()
    else:
        job_description = job_desc_input
    
    # Get interview type
    interview_type_input = input("\nInterview Type (Behavioral/Technical/Mixed) [default: Mixed]: ").strip()
    if interview_type_input:
        interview_type = interview_type_input.capitalize()
        if interview_type not in ["Behavioral", "Technical", "Mixed"]:
            interview_type = "Mixed"
            print("Invalid type. Using 'Mixed'.")
    
    # Initialize session
    session.initialize(resume, job_description, interview_type)
    
    # Start interview
    print_separator()
    print_header("Interview Started")
    
    current_question = session.start_interview()
    print(f"\n[Interviewer]: {current_question}\n")
    
    # Main interview loop
    while True:
        user_input = input("Your answer (or 'next' for next question, 'end' to finish): ").strip()
        
        if user_input.lower() == 'end' or user_input.lower() == 'end interview':
            break
        elif user_input.lower() == 'next':
            next_q = session.get_next_question()
            if next_q:
                print(f"\n[Interviewer]: {next_q}\n")
            else:
                print("\nNo more questions. Type 'end' to finish the interview.")
            continue
        elif user_input.lower() == 'help':
            print("\nCommands:")
            print("  'next' - Skip to next question")
            print("  'end' or 'end interview' - Finish interview and get report")
            print("  'help' - Show this help message")
            print()
            continue
        elif not user_input:
            print("Please provide an answer or use a command.")
            continue
        
        # Process answer
        print_separator()
        result = session.process_answer(user_input)
        
        # Display assessment
        if "assessment" in result:
            print(result["assessment"])
            print()
        
        # Display feedback
        if "feedback" in result:
            print(result["feedback"])
            print()
        
        # Handle follow-up question
        if "followup_question" in result:
            print(f"[Follow-up]: {result['followup_question']}\n")
            followup_answer = input("Your follow-up answer: ").strip()
            if followup_answer:
                # Process follow-up answer
                followup_result = session.process_answer(followup_answer)
                if "assessment" in followup_result:
                    print_separator()
                    print(followup_result["assessment"])
                    print()
                if "feedback" in followup_result:
                    print(followup_result["feedback"])
                    print()
        
        # Ask next question
        print_separator()
        next_question = session.get_next_question()
        if next_question:
            print(f"[Interviewer]: {next_question}\n")
        else:
            print("No more questions prepared. Type 'end' to finish.")
    
    # Generate final report
    print_separator()
    print_header("Interview Complete - Final Report")
    
    final_result = session.end_interview()
    if "final_report" in final_result:
        print(final_result["final_report"])
        print()
    
    if "session_summary" in final_result:
        summary = final_result["session_summary"]
        print(f"Session Summary: {summary['total_questions']} questions, {summary['total_answers']} answers evaluated")
    
    print_separator()
    print("Thank you for practicing with us! Good luck with your interviews!")
    print_separator()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterview session interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        sys.exit(1)

