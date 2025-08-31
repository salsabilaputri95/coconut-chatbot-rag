import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY tidak ditemukan di file .env")
    
    genai.configure(api_key=api_key)
    return genai

def get_gemini_embeddings():
    try:
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
    except Exception as e:
        print(f"Error membuat embeddings: {str(e)}")
        raise

def get_gemini_chat_model():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.3,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

def stream_response(prompt):
    genai = init_gemini()
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    response = model.generate_content(
        prompt,
        stream=True
    )
    
    for chunk in response:
        yield chunk.text