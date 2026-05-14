import requests
import os
from dotenv import load_dotenv
from retriever_service import bilgi_getir

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# --- YAPILANDIRMA ---
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

def cevap_uret(soru):
    """
    Retriever'dan gelen verileri alır ve Hugging Face API kullanarak 
    anlamlı bir cevap üretir.
    """
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

    # 4. API İsteği
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "temperature": 0.5,
            "return_full_text": False
        }
    }

    try:
        print("🤖 Model cevap üretiyor...")
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        # API bazen liste döner
        if isinstance(result, list):
            return result[0]['generated_text'].strip()
        return result['generated_text'].strip()
        
    except Exception as e:
        return f"❌ Hata: {str(e)}"

if __name__ == "__main__":
    print("--- SAP AKILLI ASİSTAN ---")
    while True:
        soru = input("\nSoru (Çıkış için 'q'): ")
        if soru.lower() == 'q':
            break
            
        cevap = cevap_uret(soru)
        print(f"\nAI CEVABI:\n{cevap}")
