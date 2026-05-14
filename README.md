# 🤖 Smart Dealer AI: SAP Akilli Asistan

Smart Dealer AI, kurumsal SAP dökümanlari uzerinde uzmanlasmis, **RAG (Retrieval-Augmented Generation)** mimarisi ile calisan profesyonel bir yapay zeka asistanidir. Kullanicilarin karmasik SAP sureclerine dair sorularini, sirketin kendi dökümanlarina dayanarak saniyeler icinde yanitlar.

## 🚀 Ozellikler

- **Gelismiş RAG Mimarisi:** Sirket dökümanlarini (PDF) akilli parcalara boler ve anlamli arama (Semantic Search) yapar.
- **Yuksek Hizli Inference:** Groq LPU altyapisini kullanarak Llama-3.3-70B modeli ile isik hizinda cevap uretir.
- **RAM Caching (Singleton):** Embedding modelleri ve veritabani baglantilari RAM'de sabitlenerek sorgu suresi %90 oraninda iyilestirilmistir.
- **Profesyonel Kisilik:** Zamana gore selamlama, resmi/kibar hitap ve detayli SAP cozumleri sunan ozellestirilmis sistem talimatlari.
- **Modern Web Arayuzu:** Streamlit tabanli, chat gecmisini tutan ve kullanici dostu bir panel.

## 🛠 Teknoloji Yigini

- **Dil Modeli (LLM):** Llama-3.3-70B-Versatile (via Groq Cloud)
- **Vektor Veritabani:** ChromaDB
- **Framework:** LangChain
- **Embedding:** sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- **Arayuz:** Streamlit
- **Guvenlik:** python-dotenv (Environment Variables)

## 📂 Proje Yapisi

```text
Smart Dealer AI/
├── Data/
│   └── Sap_Vector_DB/    # Vektorize edilmis SAP hafizasi
├── src/
│   ├── app.py            # Streamlit Web Arayuzu
│   ├── retriever_service.py # Bilgi geri cagirma (Search) katmani
│   ├── generator_service.py # LLM ve Prompt yonetimi katmani
│   └── vector_repository.py # PDF isleme ve DB olusturma betigi
├── .env                  # API anahtarlari (Gizli)
└── requirements.txt      # Gerekli kutuphaneler
```

## ⚙️ Kurulum ve Calistirma

1. **Bagimliliklari Yukleyin:**
   ```bash
   pip install -r requirements.txt
   ```

2. **API Anahtarini Ekleyin:**
   `.env` dosyasi olusturun ve Groq API anahtarinizi ekleyin:
   ```text
   GROQ_API_KEY=gsk_your_key_here
   ```

3. **Sistemi Baslatin:**
   ```bash
   streamlit run src/app.py
   ```

## 🎓 Akademik Kapsam
Bu proje, 5 haftalik LLM ve Generative AI egitimi kapsaminda; veri isleme, embedding uretimi, vektor veritabanlari, prompt engineering ve model optimizasyonu konularini pratik etmek amaciyla gelistirilmistir.

---
**Gelistirici:** [Meren Aydin]  
**Mimari:** RAG (Retrieval Augmented Generation)
