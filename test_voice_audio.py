#!/usr/bin/env python3
"""
Test script for voice transcription with real audio
"""
import requests
import base64
import json

# Test transcription endpoint
def test_transcription():
    print("Testing voice transcription endpoint...")
    
    # Create a simple test audio (silence) - in real use, this would be actual audio
    # For testing, we'll use a minimal valid WAV file header
    # This is a 1-second silent WAV file (44.1kHz, 16-bit, mono)
    wav_header = bytes([
        0x52, 0x49, 0x46, 0x46,  # "RIFF"
        0x24, 0x08, 0x00, 0x00,  # File size
        0x57, 0x41, 0x56, 0x45,  # "WAVE"
        0x66, 0x6D, 0x74, 0x20,  # "fmt "
        0x10, 0x00, 0x00, 0x00,  # Subchunk1Size
        0x01, 0x00,              # AudioFormat (PCM)
        0x01, 0x00,              # NumChannels (mono)
        0x44, 0xAC, 0x00, 0x00,  # SampleRate (44100)
        0x88, 0x58, 0x01, 0x00,  # ByteRate
        0x02, 0x00,              # BlockAlign
        0x10, 0x00,              # BitsPerSample (16)
        0x64, 0x61, 0x74, 0x61,  # "data"
        0x00, 0x08, 0x00, 0x00,  # Subchunk2Size
    ])
    # Add silence data
    silence = bytes([0x00, 0x00] * 8820)  # 1 second of silence
    wav_data = wav_header + silence
    
    base64_audio = base64.b64encode(wav_data).decode('utf-8')
    
    try:
        response = requests.post(
            'http://localhost:8000/api/voice/transcribe',
            json={
                'audio_data': base64_audio,
                'audio_format': 'wav'
            },
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Transcription successful!")
            print(f"  Text: {data.get('text', '')}")
            print(f"  Confidence: {data.get('confidence', 0)}")
        else:
            print(f"✗ Transcription failed")
            
    except Exception as e:
        print(f"✗ Error: {e}")

# Test PDF parsing endpoint
def test_pdf_parsing():
    print("\nTesting PDF parsing endpoint...")
    
    # Create a minimal valid PDF
    pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Test PDF Content) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000306 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
395
%%EOF"""
    
    base64_pdf = base64.b64encode(pdf_content).decode('utf-8')
    
    try:
        response = requests.post(
            'http://localhost:8000/api/parse-pdf',
            json={
                'file_data': base64_pdf,
                'file_name': 'test.pdf'
            },
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ PDF parsing successful!")
            print(f"  Extracted text length: {len(data.get('text', ''))}")
            print(f"  Text preview: {data.get('text', '')[:100]}...")
        else:
            print(f"✗ PDF parsing failed")
            
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == '__main__':
    print("=" * 50)
    print("Testing Voice and PDF Endpoints")
    print("=" * 50)
    test_transcription()
    test_pdf_parsing()
    print("\n" + "=" * 50)
    print("Tests completed")
    print("=" * 50)

