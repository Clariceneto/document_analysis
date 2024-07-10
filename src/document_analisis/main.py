import fitz  # PyMuPDF
import docx
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

# Configure OpenAI API key
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        raise ValueError('Unsupported file format')

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ''
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

async def identify_document_type(text):
    # Use the first 500 characters of the text to determine the document type
    initial_text = text[:500]
    prompt = f"Identify the type of document (e.g., report, article, contract) based on the following text:\n\n{initial_text}"
    try:
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL_NAME"),
            messages=[{"role": "user", "content": prompt}]
        )
        document_type = response.choices[0].message.content.strip()
        return document_type
    except Exception as e:
        return f"An error occurred: {str(e)}"

async def extract_theme(text):
    # Use the first 500 characters of the text to determine the theme
    initial_text = text[:500]
    prompt = f"Identify only the theme of the document:\n\n{initial_text}"
    try:
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL_NAME"),
            messages=[{"role": "user", "content": prompt}]
        )
        theme = response.choices[0].message.content.strip()
        return theme
    except Exception as e:
        return f"An error occurred: {str(e)}"

def generate_prompt(section, text):
    prompts = {
        "THEME": f"Identify theme of the document:\n\n{text[:1500]}",
        "OBJECTIVES": f"Summarize the main objectives of the document in two lines:\n\n{text}",
        "EVALUATION": f"Provide a critical evaluation of the document in two lines:\n\n{text}",
        "SUGGESTIONS": f"List improvement suggestions for the document in two lines:\n\n{text}",
        "CRITICISMS": f"Provide detailed criticisms of the document in two lines:\n\n{text}",
        "IMPROVEMENTS": f"Identify and suggest specific improvements for the document in two lines:\n\n{text}",
    }
    return prompts.get(section)

async def analyze_document(file_path):
    document_text = await extract_text(file_path)
    document_type = await identify_document_type(document_text)
    theme = await extract_theme(document_text)
    
    analysis = {
        "DOCUMENT_TYPE": document_type,
        "THEME": theme,
        "FILE": os.path.basename(file_path),
        "OBJECTIVES": "",
        "EVALUATION": "",
        "SUGGESTIONS": "",
        "CRITICISMS": "",
        "IMPROVEMENTS": ""
    }
    sections = ["OBJECTIVES", "EVALUATION", "SUGGESTIONS", "CRITICISMS", "IMPROVEMENTS"]
    
    for section in sections:
        prompt = generate_prompt(section, document_text)
        try:
            response = await client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL_NAME"),
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content.strip()
            # Ensure the summary is compact and concise
            analysis[section] = ' '.join(content.split())
        except Exception as e:
            analysis[section] = f"An error occurred: {str(e)}"
    
    return analysis
