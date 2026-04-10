import streamlit as st
from streamlit_mic_recorder import speech_to_text
from groq import Groq
from gtts import gTTS
import base64
import random

# 1. ESTILO RADICAL (Forzado al máximo)
st.set_page_config(page_title="Yayobot", page_icon="👵")

st.markdown("""
    <style>
    /* Forzar fondo azul en toda la pantalla */
    [data-testid="stAppViewContainer"] {
        background-color: #E3F2FD !important;
    }
    
    /* Forzar que el título sea rojo */
    h1 {
        color: #FF4B4B !important;
        text-align: center !important;
        font-size: 50px !important;
    }

    /* Estilo de las burbujas */
    .stMarkdown div p {
        font-size: 18px !important;
    }

    /* Hacer el botón de grabación ROJO Y GRANDE */
    button {
        background-color: #FF4B4B !important;
        color: white !important;
        border-radius: 20px !important;
        height: 60px !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👵 Yayobot")

# 2. CONFIGURACIÓN GROQ
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def hablar(texto):
    tts = gTTS(text=texto, lang='es', tld='es')
    nombre = f"temp_{random.randint(1,999)}.mp3"
    tts.save(nombre)
    with open(nombre, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

# 3. INTERFAZ
text = speech_to_text(language='es', start_prompt="🎤 HABLAR", stop_prompt="✅ ENVIAR", key='yayo_test')

if text:
    # Caja de texto para el usuario
    st.info(f"**Tú:** {text}")
    
    mensajes = [
        {"role": "system", "content": "Eres Yayobot, un asistente amigable. Responde corto."},
        {"role": "user", "content": text}
    ]
    
    completion = client.chat.completions.create(messages=mensajes, model="llama-3.1-8b-instant")
    respuesta = completion.choices[0].message.content
    
    # Caja de texto para el Bot (Rojo)
    st.success(f"**Yayobot:** {respuesta}")
    
    hablar(respuesta)
