from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from src.query import CoconutRAGSystem
from dotenv import load_dotenv
import os
import logging
import traceback

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("COCONUT_RAG_SERVER")

app = Flask(__name__, static_folder='public')
CORS(app)  # Enable CORS for all routes

# Initialize RAG system
try:
    logger.info("Memulai inisialisasi sistem RAG...")
    rag_system = CoconutRAGSystem()
    logger.info("Sistem RAG berhasil diinisialisasi")
except Exception as e:
    logger.error(f"Gagal menginisialisasi sistem RAG: {str(e)}")
    logger.error(traceback.format_exc())
    rag_system = None

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('public', path)

@app.route('/query', methods=['POST'])
def handle_query():
    if rag_system is None:
        return jsonify({
            "error": "Sistem RAG belum diinisialisasi dengan benar"
        }), 500
    
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({
            "error": "Pertanyaan tidak boleh kosong"
        }), 400
    
    try:
        logger.info(f"Pertanyaan diterima: {question}")
        
        # Process the query
        result = rag_system.query(question)
        logger.info("Berhasil mendapatkan jawaban")
        
        # Format sources for the frontend
        sources = []
        for doc in result["sources"]:
            # Extract filename from source path
            source_name = os.path.basename(doc.metadata.get('source', 'unknown'))
            
            # Create content preview
            content_preview = doc.page_content[:150] + '...' if len(doc.page_content) > 150 else doc.page_content
            
            # Combine information
            sources.append(f"{source_name}: {content_preview}")
        
        return jsonify({
            "answer": result["answer"],
            "sources": sources
        })
        
    except Exception as e:
        logger.error(f"Error memproses pertanyaan: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": "Terjadi kesalahan dalam memproses pertanyaan"
        }), 500

@app.errorhandler(404)
def not_found(e):
    return send_from_directory('public', 'index.html')

if __name__ == "__main__":
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    
    logger.info(f"🌐 Server berjalan di http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)