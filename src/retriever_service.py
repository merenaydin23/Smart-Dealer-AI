import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 1. MODEL KATMANI (Embedding Modelini Hazırlayan Fonksiyon)
def model_yukle():
    """HuggingFace üzerinden multilingual embedding modelini başlatır."""
    model_adi = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_adi)
    return embeddings

# 2. VERİTABANI KATMANI (Vektör Deposunu Bağlayan Fonksiyon)
def veritabani_bagla(embeddings):
    """Diskteki .bin dosyalarını (ChromaDB) sisteme bağlar."""
    # Senin verdiğin klasör yapısına uygun yol
    db_yolu = r"C:\Users\HP\Desktop\Smart Dealer AI\Data\Sap_Vector_DB"

    if not os.path.exists(db_yolu):
        raise FileNotFoundError(f"⚠️ Vektör deposu bulunamadı: {db_yolu}")

    vector_db = Chroma(persist_directory=db_yolu, embedding_function=embeddings)
    return vector_db

# 3. KIYASLAMA VE GERİ ÇAĞIRMA KATMANI (k-NN Arama Fonksiyonu)
def benzerlik_aramasi(soru, vector_db, k=3):
    """
    Sorduğun soruyu alır, k-NN (k-Nearest Neighbors) algoritmasıyla 
    en yakın k tane parçayı bulur.
    """
    # k=3: En yakın 3 komşuyu (en benzer 3 metni) getirir
    sonuclar = vector_db.similarity_search(soru, k=k)
    return sonuclar

# 4. ANA SERVİS (Tüm parçaları birleştiren 'Bilgi Getir' fonksiyonu)
def bilgi_getir(soru):
    """Pipeline'ı sırasıyla çalıştıran ana fonksiyon."""
    # Adım A: Modeli çevir/yükle
    embeddings = model_yukle()

    # Adım B: Veritabanına bu modelle bağlan
    db = veritabani_bagla(embeddings)

    # Adım C: k-NN ile kıyasla ve sonuçları dön
    sonuclar = benzerlik_aramasi(soru, db)
    return sonuclar

# --- TEST BÖLÜMÜ ---
if __name__ == "__main__":
    soru = "Satış organizasyonu unsurları nelerdir?"
    print(f"🚀 Backend Sorgusu Başlatıldı: {soru}\n")

    try:
        cevaplar = bilgi_getir(soru)
        for i, doc in enumerate(cevaplar):
            print(f"📍 Sonuç {i+1} (Sayfa: {doc.metadata.get('page')}):")
            print(f"{doc.page_content[:200]}...\n")
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")