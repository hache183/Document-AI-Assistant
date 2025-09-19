import os
import PyPDF2
from docx import Document as DocxDocument
from django.conf import settings
import openai

# Configura OpenAI
openai.api_key = settings.OPENAI_API_KEY

def extract_text_from_file(file_path, document_type):
    """Estrae testo da diversi tipi di documento"""
    try:
        if document_type == 'pdf':
            return extract_text_from_pdf(file_path)
        elif document_type == 'docx':
            return extract_text_from_docx(file_path)
        elif document_type == 'txt':
            return extract_text_from_txt(file_path)
        else:
            return "Tipo di documento non supportato"
    except Exception as e:
        return f"Errore nell'estrazione: {str(e)}"

def extract_text_from_pdf(file_path):
    """Estrae testo da PDF"""
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(file_path):
    """Estrae testo da DOCX"""
    doc = DocxDocument(file_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return "\n".join(text).strip()

def extract_text_from_txt(file_path):
    """Estrae testo da TXT"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def generate_summary(text, max_length=200):
    """Genera un riassunto usando OpenAI"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei un assistente che crea riassunti concisi e informativi."},
                {"role": "user", "content": f"Crea un riassunto di massimo {max_length} caratteri del seguente testo:\n\n{text[:2000]}"}
            ],
            max_tokens=100,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Errore nella generazione del riassunto: {str(e)}"

def query_document_with_ai(document_text, query):
    """Interroga il documento usando OpenAI"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei un assistente che risponde a domande basandoti esclusivamente sul contenuto del documento fornito."},
                {"role": "user", "content": f"Documento:\n{document_text[:3000]}\n\nDomanda: {query}\n\nRispondi basandoti solo sul contenuto del documento."}
            ],
            max_tokens=300,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Errore nella query AI: {str(e)}"