import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tambahkan direktori src ke path
src_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(src_dir))

from gemini_utils import get_gemini_embeddings

load_dotenv()

def clean_metadata(metadata):
    """Bersihkan metadata untuk memastikan kompatibilitas dengan ChromaDB"""
    cleaned = {}
    for key, value in metadata.items():
        # Konversi semua nilai ke string
        cleaned[key] = str(value)
    return cleaned

def main(input_dir: str, collection_name: str):
    logger.info("🚀 Memulai proses indexing...")
    
    loader = DirectoryLoader(
        input_dir, 
        glob="**/*.md",
        loader_cls=TextLoader,
        show_progress=True,
        use_multithreading=True
    )
    documents = loader.load()
    logger.info(f"Memuat {len(documents)} dokumen")
    
    # Bersihkan metadata
    for doc in documents:
        doc.metadata = clean_metadata(doc.metadata)
    
    # Konfigurasi splitter dengan chunk size lebih kecil
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,  
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""],
        length_function=len,
        is_separator_regex=False
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Memecah menjadi {len(chunks)} chunks")
    
    # Log contoh chunk pertama
    if chunks:
        logger.info(f"Contoh chunk pertama: {chunks[0].page_content[:100]}...")
        logger.info(f"Metadata: {chunks[0].metadata}")
    
    try:
        embeddings = get_gemini_embeddings()
        logger.info("Berhasil memuat embeddings")
        
        # Simpan ke Chroma
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=os.getenv("PERSIST_DIR"),
            collection_name=collection_name
        )
        vector_store.persist()
        logger.info(f"{len(chunks)} chunks tersimpan di {os.getenv('PERSIST_DIR')}")
    except Exception as e:
        logger.error(f"Gagal menyimpan ke Chroma: {str(e)}")
        # Log detail error
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', default='data/processed', help='Direktori input')
    parser.add_argument('--collection_name', default='coconut_rag', help='Nama koleksi Chroma')
    args = parser.parse_args()
    main(args.input_dir, args.collection_name)