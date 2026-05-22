import os
import sys
import contextlib

# HuggingFace progress bar ve uyarilari kapat
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# --- SINGLETON PATTERN (Modelleri hafizada tutmak icin) ---
_embeddings = None
_vector_db = None


def _sessiz_calistir(fn):
    """stdout ve stderr'i susturarak fonksiyonu calistirir (Errno 22 onlemi)."""
    devnull = open(os.devnull, "w", encoding="utf-8")
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    try:
        sys.stdout = devnull
        sys.stderr = devnull
        return fn()
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        devnull.close()


def model_yukle():
    """HuggingFace uzerinden multilingual embedding modelini baslatir (Hafizada tutar)."""
    global _embeddings
    if _embeddings is None:
        model_adi = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        _embeddings = _sessiz_calistir(
            lambda: HuggingFaceEmbeddings(model_name=model_adi)
        )
    return _embeddings


def veritabani_bagla(embeddings):
    """Diskteki ChromaDB'ye baglanir (Baglantiyi hafizada tutar)."""
    global _vector_db
    if _vector_db is None:
        db_yolu = r"C:\Users\HP\Desktop\Smart Dealer AI\Data\Sap_Vector_DB"
        if not os.path.exists(db_yolu):
            raise FileNotFoundError(f"Vektor deposu bulunamadi: {db_yolu}")
        _vector_db = _sessiz_calistir(
            lambda: Chroma(persist_directory=db_yolu, embedding_function=embeddings)
        )
    return _vector_db


def benzerlik_aramasi(soru, vector_db, k=5):
    """k-NN ile en yakin metin parcalarini bulur."""
    return _sessiz_calistir(lambda: vector_db.similarity_search(soru, k=k))


def bilgi_getir(soru):
    """Pipeline'i calistiran ana fonksiyon (Hizli calisir)."""
    embeddings = model_yukle()
    db = veritabani_bagla(embeddings)
    return benzerlik_aramasi(soru, db)