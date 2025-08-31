import re
import os
import argparse
import logging
from pathlib import Path

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("doc_preprocessor")

def process_markdown(input_path: str, output_path: str) -> str:
    """Langkah preprocessing dokumen lengkap"""
    logger.info(f"Memproses: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 1. Normalisasi karakter khusus
    text = re.sub(r'\u2013|\u2014', '-', text)
    text = re.sub(r'\u2018|\u2019', "'", text)
    
    # 2. Standarisasi heading
    text = re.sub(r'(\n#+ [^\n]+)\n([^\n#])', r'\1\n\n\2', text)
    
    # 3. Proteksi komponen kritis
    critical_sections = [
        "Indikator Keberhasilan",
        "Tujuan",
        "Output yang Diharapkan",
        "Komponen Tes",
        "Tahapan"
    ]
    
    for section in critical_sections:
        pattern = fr'({section}[\s\S]*?)(?=\n#|\Z)'
        text = re.sub(
            pattern, 
            f'<!-- CRITICAL_START:{section} -->\n\\1\n<!-- CRITICAL_END:{section} -->', 
            text,
            flags=re.IGNORECASE
        )
    
    # 4. Perbaiki tabel
    text = re.sub(r'(\|.*?)\n(\s*\|)', r'\1\2', text)
    
    # 5. Simpan hasil
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    logger.info(f"Output disimpan di: {output_path}")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Optimasi dokumen untuk RAG')
    parser.add_argument('--input', required=True, help='Path file input')
    parser.add_argument('--output', required=True, help='Path file output')
    args = parser.parse_args()
    
    process_markdown(args.input, args.output)