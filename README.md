# COCONUT Bluebook RAG System

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Framework](https://img.shields.io/badge/Framework-LangChain-orange)
![LLM](https://img.shields.io/badge/LLM-Gemini%201.5%20Flash-purple)

## 📖 Overview

COCONUT Bluebook RAG (Retrieval Augmented Generation) adalah sistem tanya-jawab berbasis AI yang dibangun untuk menyediakan informasi akurat tentang COCONUT Computer Club. Sistem ini menggunakan dokumen Bluebook sebagai sumber pengetahuan dan teknologi RAG untuk memberikan jawaban yang tepat dan relevan.

Dikembangkan oleh: **rockmind** 🚀

## ⚙️ Arsitektur Sistem

Sistem ini dibangun dengan arsitektur RAG (Retrieval Augmented Generation) yang menggabungkan kemampuan retrieval dan generasi untuk menghasilkan jawaban yang akurat dan relevan.

### Komponen Utama

```
┌─────────────────┐     ┌──────────────┐     ┌────────────────┐
│ User Question   │────>│  Embeddings  │────>│  Vector Store  │
└─────────────────┘     └──────────────┘     └────────┬───────┘
                                                      │
┌─────────────────┐     ┌──────────────┐     ┌────────▼───────┐
│    Response     │<────│ LLM (Gemini) │<────│ Context Chunks │
└─────────────────┘     └──────────────┘     └────────────────┘
```

### Teknologi

| Komponen | Teknologi | Deskripsi |
| --- | --- | --- |
| **Backend** | Flask | Web framework Python untuk API dan serving |
| **LLM Pipeline** | LangChain | Framework untuk mengembangkan aplikasi berbasis LLM |
| **Generative AI** | Google Gemini | Model generatif Gemini 1.5 Flash untuk menjawab pertanyaan |
| **Embedding** | Google Embedding API | Model embedding-001 untuk vektorisasi teks |
| **Vector Database** | ChromaDB | Database vektor lokal untuk menyimpan embedding |
| **Frontend** | HTML, JS, TailwindCSS | Interface web dengan komponen chat interaktif |

## 🚀 Fitur Utama

- **Retrieval Akurat**: Menggunakan MMR (Maximum Marginal Relevance) untuk mengambil konteks paling relevan dan beragam
- **Responsif**: Antarmuka web yang responsif dengan streaming respons untuk pengalaman pengguna yang baik
- **Referensi Sumber**: Menampilkan sumber referensi dari dokumen Bluebook untuk setiap jawaban
- **Mode Streaming**: Jawaban ditampilkan secara streaming untuk pengalaman real-time
- **Contextual Memory**: Mempertahankan konteks percakapan untuk follow-up questions

## 🛠️ Teknis Implementasi

### Embedding Model
- **Model**: Google Generative AI Embedding (`models/embedding-001`)
- **Dimensi**: 768 dimensi vektor
- **Keunggulan**: Mampu menangkap semantik dalam konteks bahasa Indonesia dengan baik

### Teknik Chunking & Preprocessing
- Dokumen dipecah dengan `RecursiveCharacterTextSplitter` dengan parameter:
  - `chunk_size`: 512 karakter
  - `chunk_overlap`: 100 karakter
  - Pemisah: "\n\n", "\n", " ", ""

### Metode Retrieval
- **Algoritma**: MMR (Maximum Marginal Relevance)
- **Parameter**:
  - `k`: 5 (jumlah dokumen yang diambil)
  - `lambda_mult`: 0.25 (parameter untuk menyeimbangkan relevansi dan diversitas)

### LLM
- **Model**: Gemini 1.5 Flash
- **Parameter**:
  - `temperature`: 0.3 (memastikan jawaban konsisten dan faktual)
  - `top_p`: 0.95 (variasi yang wajar tanpa mengorbankan kualitas)
  - `max_output_tokens`: 2048 (panjang jawaban yang memadai)

## 📊 Evaluasi Performa

Sistem ini telah dievaluasi menggunakan berbagai metrik untuk retrieval dan generasi. Berikut adalah ringkasan hasil evaluasi:

### Metrik Retrieval:
- **Precision@1**: 0.85 - Tingkat keakuratan dokumen paling relevan
- **Precision@3**: 0.78 - Rasio dokumen relevan dalam 3 hasil teratas
- **Recall@5**: 0.92 - Persentase dokumen relevan yang berhasil ditemukan dalam 5 hasil teratas

### Metrik Generasi:
- **ROUGE-L**: 0.76 - Kesamaan struktural dan linguistik dengan jawaban referensi
- **BLEU**: 0.62 - Presisi n-gram jawaban dibanding dengan referensi
- **Semantic Similarity**: 0.85 - Kesamaan makna menggunakan model embedding

Evaluasi lengkap dapat dilihat dalam notebook `percobaan 2/evaluasi.ipynb`.

## 🔧 Struktur Proyek

```
coconut-bluebook-rag/
├── rag_implementation.ipynb    # Notebook implementasi awal RAG
├── percobaan 2/
│   ├── data/
│   │   ├── evaluation_dataset.json    # Dataset untuk evaluasi
│   │   ├── processed/
│   │   │   └── bluebook_coconut_optimized.md   # Dokumen yang sudah preprocessing
│   │   └── raw/
│   │       └── bluebook_coconut.md   # Dokumen sumber asli
│   ├── evaluasi.ipynb          # Evaluasi komprehensif sistem
│   ├── main.py                 # Entry point untuk aplikasi CLI
│   ├── public/
│   │   └── index.html          # Antarmuka web
│   ├── requirements.txt        # Dependensi Python
│   ├── server.py               # Server Flask
│   ├── src/
│   │   ├── gemini_utils.py     # Utilitas untuk Google Gemini API
│   │   ├── ingest.py           # Script untuk ingesti dokumen
│   │   ├── preprocess.py       # Script untuk preprocessing dokumen
│   │   └── query.py            # Logic RAG dan query
│   └── storage/                # Penyimpanan ChromaDB
└── README.md                   # Dokumentasi proyek ini
```

## 🏁 Cara Menjalankan

### Prasyarat

- Python 3.9+
- Google AI API Key
- ChromaDB

### Langkah-langkah

1. **Clone repository**

2. **Setup environment**
   ```bash
   # Buat virtual environment
   python -m venv venv
   
   # Aktifkan virtual environment
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   
   # Install dependencies
   pip install -r percobaan\ 2/requirements.txt
   ```

3. **Setup API key**
   ```
   # Buat file .env di folder percobaan 2/
   echo "GOOGLE_API_KEY=your_api_key_here" > percobaan\ 2/.env
   ```

4. **Preproses dokumen (jika diperlukan)**
   ```bash
   cd percobaan\ 2
   python src/preprocess.py --input data/raw/bluebook_coconut.md --output data/processed/bluebook_coconut_optimized.md
   ```

5. **Ingest dokumen ke ChromaDB**
   ```bash
   cd percobaan\ 2
   python src/ingest.py --input_dir data/processed --collection_name coconut_rag
   ```

6. **Jalankan server**
   ```bash
   cd percobaan\ 2
   python server.py
   ```


## 📝 Evaluasi

Untuk menjalankan evaluasi sistem:

1. **Jalankan notebook evaluasi**
   ```bash
   cd percobaan\ 2
   jupyter notebook evaluasi.ipynb
   ```

2. **Jalankan semua sel** di notebook untuk melihat hasil evaluasi lengkap

## 📚 Referensi

- LangChain Documentation: https://python.langchain.com/
- Google Gemini API: https://ai.google.dev/
- ChromaDB: https://www.trychroma.com/
- RAG Papers: https://arxiv.org/abs/2005.11401

## 👤 Kontributor

- **rockmind** - *Pengembang Utama* - [GitHub](https://github.com/salsabilaputri95)

---

Dibuat dengan ❤️ oleh **rockmind** untuk COCONUT Computer Club
