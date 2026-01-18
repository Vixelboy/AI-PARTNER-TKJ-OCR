import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import base64

# --- SETTING LAYOUT & HIDE MENU ---
st.set_page_config(page_title="Guru TKJ AI", page_icon="💻")
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>""", unsafe_allow_html=True)

# --- KONFIGURASI AI (API KEY GEMINI IKBAL) ---
API_KEY_IKBAL = "AIzaSyD90ywjHCFLSZPhMb4n0tjZZPSoHesyd5I"
genai.configure(api_key=API_KEY_IKBAL)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- FUNGSI SUARA (TTS) ---
def play_voice(text):
    try:
        clean_text = text[:300].replace('*', '').replace('#', '')
        tts = gTTS(text=clean_text, lang='id')
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(md, unsafe_allow_html=True)
    except:
        pass

# --- TAMPILAN UTAMA ---
st.title("🤖 Kelas Digital Pak Guru TKJ")
st.info("Halo Bal! Chatbot Gemini kamu sudah aktif. Bisa baca Gambar, PDF, dan Suara.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR UPLOAD ---
with st.sidebar:
    st.header("📁 Media & Dokumen")
    uploaded_file = st.file_uploader("Upload Gambar/File Materi", type=['png', 'jpg', 'jpeg', 'pdf', 'txt'])
    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# Menampilkan Riwayat Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT CHAT ---
if prompt := st.chat_input("Tanya apa hari ini, Bal?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    input_data = [prompt]
    if uploaded_file:
        if uploaded_file.type.startswith('image'):
            img = Image.open(uploaded_file)
            input_data.append(img)
            st.image(img, caption="Gambar dari Murid", width=250)
        else:
            text_data = uploaded_file.read().decode('utf-8', errors='ignore')
            input_data.append(f"\nReferensi: {text_data[:5000]}")

    with st.chat_message("assistant"):
        try:
            with st.spinner("Lagi mikir..."):
                response = model.generate_content(input_data)
                st.markdown(response.text)
                play_voice(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error pada sistem: {e}")
