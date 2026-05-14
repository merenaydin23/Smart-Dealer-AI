import os
from dotenv import load_dotenv, find_dotenv
from groq import Groq
from retriever_service import bilgi_getir

# .env dosyasını otomatik bul ve yükle
load_dotenv(find_dotenv())

# --- YAPILANDIRMA ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Groq üzerindeki en güçlü model Llama-3 (Türkçe desteği çok iyidir)
MODEL_ID = "llama-3.3-70b-versatile"

# Groq İstemcisini Başlat
client = Groq(api_key=GROQ_API_KEY)

def cevap_uret(soru):
    """
    Retriever'dan gelen verileri alır ve Groq API kullanarak 
    anlamlı bir cevap üretir.
    """
    try:
        # 1. Bilgi Getirme (Retrieval)
        ilgili_dokumanlar = bilgi_getir(soru)
        
        # 2. Bağlam Oluşturma
        baglam = ""
        for i, doc in enumerate(ilgili_dokumanlar):
            baglam += f"\n[Kaynak {i+1}]: {doc.page_content}\n"
        
        # 3. Prompt (Komut) Hazırlama
        prompt = f"""Sen yardımcı bir SAP uzmanısın. 
Aşağıdaki dokümanları (KAYNAKLAR) temel alarak kullanıcının sorusunu cevapla.
Eğer cevap dokümanlarda yoksa uydurma, 'Bu bilgiye sahip değilim' de.

KAYNAKLAR:
{baglam}

SORU: {soru}

CEVAP:"""

        # 4. Groq API İsteği
        print("🤖 Groq (Llama-3) cevap üretiyor...")
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=MODEL_ID,
            temperature=0.5,
            max_tokens=1024,
        )

        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"❌ Hata: {str(e)}"

if __name__ == "__main__":
    print("--- SAP AKILLI ASİSTAN (GROQ POWERED) ---")
    if not GROQ_API_KEY:
        print("⚠️ HATA: .env dosyasında GROQ_API_KEY bulunamadı!")
    else:
        while True:
            soru = input("\nSoru (Çıkış için 'q'): ")
            if soru.lower() == 'q':
                break
                
            cevap = cevap_uret(soru)
            print(f"\nAI CEVABI:\n{cevap}")
