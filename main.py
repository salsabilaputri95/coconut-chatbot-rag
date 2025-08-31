from dotenv import load_dotenv
from src.query import CoconutRAGSystem
from src.gemini_utils import stream_response  
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

def main():
    print("\n" + "="*50)
    print("🥥 COCONUT Bluebook RAG Assistant")
    print("="*50)
    print("Tanyakan tentang Bluebook COCONUT Computer Club")
    print("Ketik 'exit' untuk keluar\n")
    
    rag_system = CoconutRAGSystem()
    
    while True:
        try:
            query = input("Pertanyaan Anda: ")
            if query.lower() in ['exit', 'quit']:
                break
            
            # Mode respons langsung (streaming)
            print("\n💡 Mode Respons Langsung:")
            for chunk in stream_response(query):
                print(chunk, end="", flush=True)
            
            # Mode RAG dengan sumber referensi
            print("\n\n🔎 Mode Jawaban Berdokumen:")
            result = rag_system.query(query)
            rag_system.print_result(result)
            
        except Exception as e:
            print(f"⚠️ Error: {str(e)}")
            print("Silakan coba pertanyaan lain")

if __name__ == "__main__":
    main()