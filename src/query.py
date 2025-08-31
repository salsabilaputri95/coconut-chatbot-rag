import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Tambahkan direktori src ke path
src_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(src_dir))

from gemini_utils import get_gemini_embeddings, get_gemini_chat_model  # Gunakan underscore
load_dotenv()

class CoconutRAGSystem:
    def __init__(self):
        self.embeddings = get_gemini_embeddings()
        
        self.vector_store = Chroma(
            persist_directory=os.getenv("PERSIST_DIR"),
            collection_name="coconut_rag",
            embedding_function=self.embeddings
        )
        
        self.llm = get_gemini_chat_model()
        
        self.qa_chain = self._create_qa_chain()
    
    def _create_qa_chain(self):
        prompt_template = """
        Anda adalah asisten ahli untuk COCONUT Computer Club. Gunakan konteks berikut untuk menjawab pertanyaan.
        Jika jawaban tidak ditemukan dalam konteks, jelaskan dengan jujur bahwa Anda tidak tahu.
        
        Konteks:
        {context}
        
        Pertanyaan: {question}
        
        Berikan jawaban yang terstruktur dan informatif:
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_type="mmr",
                search_kwargs={"k": 5, "lambda_mult": 0.25}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
    
    def query(self, question: str):
        result = self.qa_chain({"query": question})
        return {
            "answer": result["result"],
            "sources": result["source_documents"]
        }
    
    def print_result(self, result):
        print("\n🤖 Jawaban:")
        print(result["answer"])
        print("\n🔍 Sumber Referensi:")
        for i, doc in enumerate(result["sources"]):
            print(f"{i+1}. {doc.metadata['source']}")
            print(f"   {doc.page_content[:150]}...")
            print()

if __name__ == "__main__":
    rag_system = CoconutRAGSystem()
    print("🔍 Sistem RAG siap. Ketik 'exit' untuk keluar")
    
    while True:
        query = input("\nPertanyaan Anda: ")
        if query.lower() in ['exit', 'quit']:
            break
        
        result = rag_system.query(query)
        rag_system.print_result(result)