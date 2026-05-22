import os
import sys

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def sistemi_hazirla():
    # 1. Yolları Tanımlıyoruz
    ana_dizin = r"C:\Users\HP\Desktop\Smart Dealer AI\Data"
    pdf_yolu = os.path.join(ana_dizin, "Sap_data.pdf")
    # Vektörlerin saklanacağı yeni klasör yolu
    db_yolu = os.path.join(ana_dizin, "Sap_Vector_DB")

    if not os.path.exists(pdf_yolu):
        print(f"❌ Hata: {pdf_yolu} bulunamadı! Lütfen PDF'in adını ve yerini kontrol et.")
        return

    print("🚀 Adım 1: PDF okunuyor...")
    loader = PyPDFLoader(pdf_yolu)
    sayfalar = loader.load()

    print("📦 Adım 2: Metinler küçük parçalara bölünüyor (Chunking)...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    parcalar = text_splitter.split_documents(sayfalar)

    print(f"🧠 Adım 3: {len(parcalar)} parça için sayısal karşılıklar (Embedding) üretiliyor...")
    # Not: Bu model internetten indirileceği için ilk seferde zaman alabilir
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    print(f"💾 Adım 4: Vektör veritabanı oluşturuluyor ve kaydediliyor...")
    print(f"📍 Kayıt Yeri: {db_yolu}")

    # persist_directory kısmını güncelledik
    vector_db = Chroma.from_documents(
        documents=parcalar,
        embedding=embeddings,
        persist_directory=db_yolu
    )

    print(f"✅ İşlem Başarılı! Vektör hafızası '{db_yolu}' klasörüne kaydedildi.")


if __name__ == "__main__":
    sistemi_hazirla()