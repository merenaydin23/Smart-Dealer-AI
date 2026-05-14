import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from groq import Groq
from retriever_service import bilgi_getir

# .env dosyasini otomatik bul ve yukle
load_dotenv(find_dotenv())

# --- YAPILANDIRMA ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_ID = "llama-3.3-70b-versatile"

# Groq Istemcisini Baslat
client = Groq(api_key=GROQ_API_KEY)

# Modelin sabit talimati (Sistem Promptu)
SISTEM_TALIMATI = """Sen "Smart Dealer AI" adinda, son derece bilgili ve profesyonel bir SAP uzmanissin. 
Kullanicilarin sorularina detayli, aciklayici ve cozum odakli cevaplar ver.

KURALLAR:
1. DIL VE TON: Resmi, kibar ve guven verici bir Turkce kullan. "Siz" hitabini kullan.
2. DETAYLI CEVAP: Sorulari yuzeysel gecistirme. Kavramlari acikla, surecleri adim adim anlat ve mumkunse kaynaklardaki verileri sentezleyerek derinlik kat.
3. BILGI SINIRI: Yalnizca sana verilen KAYNAKLAR icerisindeki bilgileri kullan. Bilgin olmayan konularda uydurma, "Bu konuda dökümanlarimda yeterli veri yok" diyerek yardim iste.
4. GORSEL DUZEN: Cevaplarinda basliklar, madde işaretleri ve onemli terimler icin **kalin yazim** kullanarak okunabilirligi artir.
"""

def zamana_gore_selam():
    """Gunun saatine gore uygun selamlama mesajini dondurur."""
    saat = datetime.now().hour
    if 5 <= saat < 12:
        donem = "Gunaydın"
    elif 12 <= saat < 18:
        donem = "Iyi gunler"
    elif 18 <= saat < 22:
        donem = "Iyi aksamlar"
    else:
        donem = "Iyi geceler"
    return donem

def giris_mesaji():
    """Chatbot acilisinda kullaniciya zamana gore selam verir."""
    selam = zamana_gore_selam()
    print("\n" + "="*55)
    print("   SMART DEALER AI | SAP Akilli Asistan")
    print("="*55)
    print(f"\n{selam}! Ben Smart Dealer AI, SAP konularinda size")
    print("yardimci olmak icin buradayim.\n")
    print("-"*55)

def cevap_uret(soru):
    """
    Retriever'dan gelen verileri alir ve Groq API kullanarak
    anlamli bir cevap uretir.
    """
    try:
        # 1. Bilgi Getirme (Retrieval)
        ilgili_dokumanlar = bilgi_getir(soru)

        # 2. Baglam Olusturma
        baglam = ""
        for i, doc in enumerate(ilgili_dokumanlar):
            baglam += f"\n[Kaynak {i+1}]: {doc.page_content}\n"

        # 3. Prompt (Komut) Hazirlama
        kullanici_mesaji = f"""KAYNAKLAR:
{baglam}

SORU: {soru}

CEVAP:"""

        # 4. Groq API Istegi (Sistem promptu ayri olarak gonderiliyor)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SISTEM_TALIMATI,
                },
                {
                    "role": "user",
                    "content": kullanici_mesaji,
                }
            ],
            model=MODEL_ID,
            temperature=0.4,
            max_tokens=1024,
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Hata: {str(e)}"

def devam_sorusu():
    """Cevaptan sonra baska soru olup olmadigini sorar."""
    print("\nBaska sormak istediginiz bir konu var mi?")
    cevap = input("(Evet/Hayir veya sorunuzu yazin): ").strip().lower()
    return cevap

def veda_mesaji():
    """Kullanici cikinca veda eder."""
    selam = zamana_gore_selam()
    print("\n" + "-"*55)
    print("Tesekkur ederim, iyi calismalar dilerim!")
    print(f"{selam}!")
    print("="*55 + "\n")

if __name__ == "__main__":
    if not GROQ_API_KEY:
        print("HATA: .env dosyasinda GROQ_API_KEY bulunamadi!")
    else:
        giris_mesaji()

        ilk_soru = True
        while True:
            if ilk_soru:
                girdi = input("Sorunuz: ").strip()
                ilk_soru = False
            else:
                girdi = devam_sorusu()

            # Cikis kontrolleri
            if girdi.lower() in ['q', 'hayir', 'yok', 'hayır', 'h', 'n', 'no']:
                veda_mesaji()
                break

            if not girdi:
                print("Lutfen bir soru girin.")
                ilk_soru = True
                continue

            print("\nArastiriliyor, lutfen bekleyin...")
            cevap = cevap_uret(girdi)
            print(f"\n{cevap}")
            print("\n" + "-"*55)
