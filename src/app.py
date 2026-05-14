import streamlit as st
import os
from datetime import datetime
from generator_service import cevap_uret, zamana_gore_selam

# Sayfa Yapilandirmasi
st.set_page_config(
    page_title="Smart Dealer AI - SAP Asistani",
    page_icon="🤖",
    layout="centered"
)

# CSS ile Stil Verme (Daha modern bir gorunum icin)
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# Yan Menu (Sidebar)
with st.sidebar:
    st.image("https://www.sap.com/dam/application/shared/logos/sap-logo-svg.svg", width=100)
    st.title("Proje Bilgileri")
    st.info("""
        **Smart Dealer AI**
        SAP dökümanlari uzerinde uzmanlasmis, RAG mimarisi ile calisan akilli asistan.
    """)
    st.write("---")
    st.write("🚀 **Teknoloji Yigini:**")
    st.code("Python\nLangChain\nChromaDB\nGroq (Llama-3.3)")
    st.write("---")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# Baslik ve Selamlama
selam = zamana_gore_selam()
st.title("🤖 Smart Dealer AI")
st.subheader(f"{selam}! Size nasil yardimci olabilirim?")

# Chat Gecmisi (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Gecmis mesajlari ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanici Girisi
if prompt := st.chat_input("SAP hakkinda bir soru sorun..."):
    # Kullanici mesajini ekle ve goster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Cevabi
    with st.chat_message("assistant"):
        with st.spinner("Arastiriliyor ve cevap üretiliyor..."):
            cevap = cevap_uret(prompt)
            st.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})

# Alt Bilgi
st.markdown("---")
st.caption("Smart Dealer AI - SAP Uzmanlik Sistemi | © 2024")
