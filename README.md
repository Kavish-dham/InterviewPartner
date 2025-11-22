# Interview Practice System - Multi-Agent Interview Simulator

A sophisticated multi-agent system that conducts realistic job interview simulations tailored to your resume and target role. The system uses specialized AI agents to provide comprehensive interview practice with real-time feedback and evaluation.

## Features

- **Multi-Agent Architecture**: Five specialized agents work together to provide a complete interview experience
- **Personalized Questions**: Questions are tailored based on your resume and job description
- **Multiple Interview Types**: Supports Behavioral, Technical, and Mixed interview styles
- **Real-Time Evaluation**: Get scored feedback after each answer
- **Comprehensive Feedback**: Receive strengths, improvement areas, and sample answers
- **Final Report**: Get a complete evaluation with development recommendations
- **PDF Support**: Can parse resume and job description from PDF files

## System Architecture

### Agents

1. **[interviewer]** - Conducts the interview and manages conversation flow
2. **[followup]** - Generates probing follow-up questions based on responses
3. **[evaluator]** - Scores answers using a structured rubric (1-10 scale)
4. **[feedback]** - Provides improvement suggestions, strengths, and example responses
5. **[report]** - Generates final evaluation and development plan

### Interview Flow

1. User provides resume and job description
2. Interviewer asks personalized questions
3. User responds
4. Followup agent may ask deeper questions if needed
5. Evaluator scores the response
6. Feedback agent provides detailed feedback
7. Process continues until user ends interview
8. Report agent generates final evaluation

## Installation

1. Clone or download this repository
2. Create and activate a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Option 1: Using the run script (macOS/Linux)

```bash
./run.sh
```

### Option 2: Manual activation

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py
```

### Option 3: One-line command (macOS/Linux)

```bash
source venv/bin/activate && python main.py
```

### Input Format

The system will prompt you for:

1. **Resume**: Paste text directly or provide a PDF file path
2. **Job Description**: Paste text directly or provide a PDF file path
3. **Interview Type**: Choose from:
   - `Behavioral` - Focus on STAR format behavioral questions
   - `Technical` - Role-specific technical questions
   - `Mixed` - Combination of both (default)

### During the Interview

- Answer questions naturally
- Type `next` to skip to the next question
- Type `end` or `end interview` to finish and get your final report
- Type `help` to see available commands

### Scoring Rubric

Each answer is evaluated on:

- **Clarity** (1-10): How clear and well-articulated the response is
- **Communication** (1-10): Effectiveness of communication
- **STAR / Structure** (1-10): Use of structured response format (for behavioral questions)
- **Role Relevance** (1-10): How relevant the answer is to the target role
- **Technical Depth** (1-10): Technical knowledge and depth (for technical questions)
- **Overall Score** (1-10): Average of all categories

### Feedback Format

After each answer, you'll receive:

- **Strengths**: What you did well
- **Areas to Improve**: Specific improvement suggestions
- **Sample Improved Answer**: Example of a well-structured response

### Final Report

At the end of the interview, you'll receive:

- Average score across all answers
- Key strengths identified
- Key improvement areas
- Recommended practice topics
- Focus areas for next session

## Example Session

```
Interview Practice System - Multi-Agent Interview Simulator
======================================================================

Welcome! I'm your interview practice partner.

[Interviewer]: Tell me about yourself and why you're interested in this role.

Your answer: [Your response here]

**ASSESSMENT**
Clarity: 7.5/10
Communication: 8.0/10
...

**FEEDBACK**
Strengths:
• Clear and well-articulated response
• Effective communication with good detail
...
```

## Project Structure

```
Interview Partner/
├── agents/
│   ├── __init__.py
│   ├── interviewer.py    # Interviewer agent
│   ├── followup.py       # Follow-up question agent
│   ├── evaluator.py      # Scoring agent
│   ├── feedback.py       # Feedback agent
│   └── report.py         # Final report agent
├── utils/
│   ├── __init__.py
│   └── parser.py         # PDF/text parsing utilities
├── session.py            # Session manager
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Rules for Agents

- Ask ONE question at a time
- Do NOT provide evaluation until after the user answers
- Maintain natural, conversational tone
- Use resume + job description to personalize questions
- Support Behavioral (STAR format), Technical, and Situational questions
- Follow-up questions must be contextual
- Keep everything voice-friendly and concise

## Interview Question Patterns

The system supports:

- **Behavioral (STAR)**: Situation, Task, Action, Result format
- **Technical**: Role-specific technical questions
- **Situational**: What-if scenarios
- **Leadership/Teamwork**: Conflict resolution, collaboration
- **Project Deep Dives**: Based on resume experience

## Customization

You can customize the system by:

- Modifying question templates in `agents/interviewer.py`
- Adjusting scoring criteria in `agents/evaluator.py`
- Updating feedback templates in `agents/feedback.py`
- Adding new question types or patterns

## Requirements

- Python 3.7+
- PyPDF2 or pdfplumber (for PDF parsing)

## License

This project is provided as-is for interview practice purposes.

## Contributing

Feel free to extend the system with additional features:
- Voice input/output support
- Web interface
- Integration with LLM APIs for more sophisticated question generation
- Database storage for interview history
- Analytics and progress tracking

---

**Good luck with your interview practice!**

