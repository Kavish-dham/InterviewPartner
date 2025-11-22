"""
PDF and text parsing utilities
"""

import os
from typing import Optional


def parse_pdf(file_path: str) -> Optional[str]:
    """
    Parse PDF file and extract text content.
    Falls back to basic text extraction if PyPDF2 is not available.
    """
    if not os.path.exists(file_path):
        return None
    
    try:
        import PyPDF2
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
    except ImportError:
        # Fallback: try pdfplumber
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except ImportError:
            # If no PDF library available, return None
            return None
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return None


def parse_text(content: str) -> str:
    """
    Parse plain text content.
    For now, just returns the content as-is.
    Can be extended for cleaning/normalization.
    """
    return content.strip()

