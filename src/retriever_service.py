import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# --- SINGLETON PATTERN (Modelleri hafizada tutmak icin) ---
_embeddings = None
_vector_db = None

def model_yukle():
    """HuggingFace uzerinden multilingual embedding modelini baslatir (Hafizada tutar)."""
    global _embeddings
    if _embeddings is None:
        logging.info("Embedding modeli ilk kez RAM'e yukleniyor...")
        model_adi = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        _embeddings = HuggingFaceEmbeddings(model_name=model_adi)
    return _embeddings

def veritabani_bagla(embeddings):
    """Diskteki ChromaDB'ye baglanir (Baglantiyi hafizada tutar)."""
    global _vector_db
    if _vector_db is None:
        logging.info("Vektor veritabanina baglaniliyor...")
        db_yolu = r"C:\Users\HP\Desktop\Smart Dealer AI\Data\Sap_Vector_DB"
        if not os.path.exists(db_yolu):
            raise FileNotFoundError(f"Vektor deposu bulunamadi: {db_yolu}")
        _vector_db = Chroma(persist_directory=db_yolu, embedding_function=embeddings)
    return _vector_db

def benzerlik_aramasi(soru, vector_db, k=5): # k degeri 3'ten 5'e cikarildi (Daha fazla bilgi icin)
    """k-NN ile en yakin metin parcalarini bulur."""
    return vector_db.similarity_search(soru, k=k)

def bilgi_getir(soru):
    """Pipeline'i calistiran ana fonksiyon (Hizli calisir)."""
    embeddings = model_yukle()
    db = veritabani_bagla(embeddings)
    return benzerlik_aramasi(soru, db)