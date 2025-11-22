"""
Example client for voice-based interview system
Demonstrates WebSocket usage for real-time voice interaction
"""

import asyncio
import websockets
import json
import base64
import httpx
import sys

API_GATEWAY_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"


async def voice_interview_example():
    """Example of voice-based interview flow"""
    
    async with httpx.AsyncClient() as client:
        # 1. Create session
        print("Creating interview session...")
        session_response = await client.post(
            f"{API_GATEWAY_URL}/api/sessions",
            json={
                "resume": "Software Engineer with 5 years of experience in Python and cloud technologies.",
                "job_description": "Senior Software Engineer role requiring Python, AWS, and microservices experience.",
                "interview_type": "Mixed"
            }
        )
        session_data = session_response.json()
        session_id = session_data["session_id"]
        print(f"Session created: {session_id}")
        
        # 2. Start interview
        print("\nStarting interview...")
        start_response = await client.post(f"{API_GATEWAY_URL}/api/sessions/{session_id}/start")
        question_data = start_response.json()
        print(f"Question: {question_data['question']}")
        
        # 3. Connect via WebSocket for voice interaction
        print("\nConnecting via WebSocket for voice interaction...")
        
        async with websockets.connect(f"{WS_URL}/ws/{session_id}") as websocket:
            # Receive welcome message
            welcome = await websocket.recv()
            print(f"Received: {json.loads(welcome)}")
            
            # Example: Send audio (in real app, this would be from microphone)
            # For demo, we'll use text commands
            print("\nYou can now interact via voice commands:")
            print("  - Send audio data via WebSocket")
            print("  - Use 'next_question' command")
            print("  - Use 'end_interview' command")
            
            # Simulate sending a command
            await websocket.send(json.dumps({
                "type": "command",
                "command": "next_question"
            }))
            
            # Receive response
            response = await websocket.recv()
            print(f"\nResponse: {json.loads(response)}")
            
            # End interview
            print("\nEnding interview...")
            await websocket.send(json.dumps({
                "type": "command",
                "command": "end_interview"
            }))
            
            final_response = await websocket.recv()
            report = json.loads(final_response)
            print(f"\nFinal Report: {json.dumps(report, indent=2)}")


async def rest_api_example():
    """Example using REST API (text-based)"""
    
    async with httpx.AsyncClient() as client:
        # 1. Create session
        session_response = await client.post(
            f"{API_GATEWAY_URL}/api/sessions",
            json={
                "resume": "Software Engineer with 5 years of experience.",
                "job_description": "Senior Software Engineer role.",
                "interview_type": "Technical"
            }
        )
        session_id = session_response.json()["session_id"]
        print(f"Session ID: {session_id}")
        
        # 2. Start interview
        start_response = await client.post(f"{API_GATEWAY_URL}/api/sessions/{session_id}/start")
        question = start_response.json()["question"]
        print(f"\nQuestion: {question}")
        
        # 3. Submit answer
        answer = "I have extensive experience with Python and microservices architecture."
        answer_response = await client.post(
            f"{API_GATEWAY_URL}/api/sessions/{session_id}/submit-answer",
            params={"collect_mode": True},
            json={"answer": answer}
        )
        print(f"Answer submitted: {answer_response.json()}")
        
        # 4. Get next question
        next_response = await client.post(f"{API_GATEWAY_URL}/api/sessions/{session_id}/next-question")
        print(f"\nNext Question: {next_response.json()['question']}")
        
        # 5. Evaluate all and end
        eval_response = await client.post(f"{API_GATEWAY_URL}/api/sessions/{session_id}/evaluate-all")
        print(f"\nEvaluations: {eval_response.json()}")
        
        end_response = await client.post(f"{API_GATEWAY_URL}/api/sessions/{session_id}/end")
        print(f"\nFinal Report: {json.dumps(end_response.json(), indent=2)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "voice":
        asyncio.run(voice_interview_example())
    else:
        print("Running REST API example...")
        print("Use 'python client-example.py voice' for WebSocket example")
        asyncio.run(rest_api_example())

