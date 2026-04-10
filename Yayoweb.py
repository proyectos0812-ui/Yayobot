import streamlit as st
from streamlit_mic_recorder import speech_to_text
from groq import Groq
from gtts import gTTS
import base64
import random

# 1. CONFIGURACIÓN Y ESTILO (Todo el diseño en un solo bloque)
st.set_page_config(page_title="Yayobot Pro", page_icon="👵")

st.markdown("""
    <style>
    /* Fondo con degradado azulado */
    .stApp {
        background: linear-gradient(180deg, #E3F2FD 0%, #FFFFFF 100%) !important;
    }

    /* Título Yayobot en Rojo */
    .titulo-yayobot {
        color: #FF4B4B !important;
        font-size: 50px !important;
        font-weight: 800 !important;
        text-align: center !important;
        margin-top: -30px;
        font-family: 'Arial', sans-serif;
    }

    /* Burbujas de Chat */
    .chat-bubble {
        padding: 15px 20px;
        border-radius: 20px;
        margin: 10px 0;
        font-family: 'Arial', sans-serif;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
        max-width: 85%;
    }
    .user {
        background-color: #DCF8C6 !important; /* Verde estilo WhatsApp */
        border-left: 8px solid #25D366 !important;
        margin-left: auto;
    }
    .bot {
        background-color: #FFFFFF !important;
        border-left: 8px solid #FF4B4B !important;
        margin-right: auto;
    }

    /* Botón de hablar grande y rojo */
    button[kind="secondary"] {
        background-color: #FF4B4B !important;
        color: white !important;
        border-radius: 50px !important;
        height: 70px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Título en pantalla
st.markdown("<h1 class='titulo-yayobot'>👵 Yayobot</h1>", unsafe_allow_html=True)

# 2. CONEXIÓN CON GROQ
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. FUNCIÓN PARA QUE HABLE
def hablar(texto):
    tts = gTTS(text=texto, lang='es', tld='es')
    id_audio = random.randint(1, 9999)
    nombre_archivo = f"audio_{id_audio}.mp3"
    tts.save(nombre_archivo)
    
    with open(nombre_archivo, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        audio_html = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)

# 4. INTERFAZ (Botón de micrófono)
text = speech_to_text(
    language='es',
    start_prompt="🎤 TOCA PARA HABLAR",
    stop_prompt="✅ ENVIAR",
    key='yayo_vfinal'
)

# 5. LÓGICA DEL CHAT
if text:
    # Mensaje del Usuario
    st.markdown(f"<div class='chat-bubble user'><b>Tú:</b><br>{text}</div>", unsafe_allow_html=True)
    
    try:
        # Llamada a la IA
        mensajes = [
            {"role": "system", "content": "Eres Yayobot, un asistente amigable, cercano y natural. Responde de forma breve y clara."},
            {"role": "user", "content": text}
        ]
        
        completion = client.chat.completions.create(
            messages=mensajes,
            model="llama-3.1-8b-instant",
        )
        respuesta = completion.choices[0].message.content
        
        # Mensaje de Yayobot
        st.markdown(f"<div class='chat-bubble bot'><b>Yayobot:</b><br>{respuesta}</div>", unsafe_allow_html=True)
        
        # Audio
        hablar(respuesta)
        
    except Exception as e:
        st.error(f"Hubo un error: {e}")
