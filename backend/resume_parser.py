import os
import logging
from typing import Optional
import PyPDF2
import docx
import re

# Configure logging
logger = logging.getLogger("api_logger")

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        str: Extracted text from the PDF.
    """
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")

def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file.
    
    Args:
        file_path (str): Path to the DOCX file.
        
    Returns:
        str: Extracted text from the DOCX.
    """
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        raise ValueError(f"Failed to extract text from DOCX: {str(e)}")

def extract_text_from_txt(file_path: str) -> str:
    """
    Extract text from a TXT file.
    
    Args:
        file_path (str): Path to the TXT file.
        
    Returns:
        str: Extracted text from the TXT.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error extracting text from TXT: {str(e)}")
        raise ValueError(f"Failed to extract text from TXT: {str(e)}")

def extract_text_from_file(file_path: str, original_filename: Optional[str] = None) -> str:
    """
    Extract text from a file based on its extension.
    
    Args:
        file_path (str): Path to the file.
        original_filename (str, optional): Original filename with extension.
        
    Returns:
        str: Extracted text from the file.
    """
    if original_filename:
        file_extension = os.path.splitext(original_filename)[1].lower()
    else:
        file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    elif file_extension == '.txt':
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def clean_resume_text(text: str) -> str:
    """
    Clean and normalize resume text.
    
    Args:
        text (str): Raw text extracted from a resume.
        
    Returns:
        str: Cleaned and normalized text.
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might interfere with analysis
    text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
    
    # Normalize line breaks
    text = text.replace('\n', ' ').strip()
    
    return text

def extract_sections_from_resume(text: str) -> dict:
    """
    Extract common sections from a resume.
    
    Args:
        text (str): Text extracted from a resume.
        
    Returns:
        dict: Dictionary with resume sections.
    """
    # This is a simplified implementation
    # A more robust implementation would use NLP techniques or regex patterns
    # to identify and extract specific sections
    
    sections = {
        'education': '',
        'experience': '',
        'skills': '',
        'summary': '',
        'full_text': text
    }
    
    # Simple pattern matching for common section headers
    education_patterns = [r'education', r'academic background', r'qualifications']
    experience_patterns = [r'experience', r'employment', r'work history', r'professional experience']
    skills_patterns = [r'skills', r'technical skills', r'competencies', r'expertise']
    summary_patterns = [r'summary', r'profile', r'objective', r'professional summary']
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Find sections based on patterns
    # This is a very simplified approach and might not work well for all resumes
    for pattern in education_patterns:
        match = re.search(r'\b' + pattern + r'\b', text_lower)
        if match:
            start_idx = match.start()
            # Extract text from the match to the next section or end of text
            next_section_idx = len(text)
            for p in experience_patterns + skills_patterns + summary_patterns:
                next_match = re.search(r'\b' + p + r'\b', text_lower[start_idx+len(pattern):])
                if next_match:
                    next_section_idx = min(next_section_idx, start_idx+len(pattern)+next_match.start())
            sections['education'] = text[start_idx:next_section_idx].strip()
    
    # Similar approach for other sections
    # (Implementation simplified for brevity)
    
    return sections

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            extracted_text = extract_text_from_file(file_path)
            print(f"Extracted {len(extracted_text)} characters from {file_path}")
            print("\nFirst 500 characters:")
            print(extracted_text[:500])
            
            cleaned_text = clean_resume_text(extracted_text)
            print("\nCleaned text (first 500 characters):")
            print(cleaned_text[:500])
            
            sections = extract_sections_from_resume(extracted_text)
            print("\nExtracted sections:")
            for section, content in sections.items():
                if section != 'full_text':
                    print(f"\n{section.upper()}:")
                    print(content[:200] + "..." if len(content) > 200 else content)
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("Please provide a file path as an argument.")
