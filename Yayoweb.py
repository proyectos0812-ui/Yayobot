import streamlit as st
from streamlit_mic_recorder import speech_to_text
from groq import Groq
from gtts import gTTS
import base64
import random

# Configuración inicial
st.set_page_config(page_title="Yayobot", page_icon="👵")

# ESTILO PARA CAMBIAR EL BOTÓN A BLANCO
st.markdown("""
    <style>
    /* Cambiar el fondo de la app para que el botón blanco se vea */
    [data-testid="stAppViewContainer"] {
        background-color: #f0f2f6 !important;
    }

    /* EL BOTÓN: Fondo blanco, texto rojo y bordes redondeados */
    button {
        background-color: #ffffff !important;
        color: #FF4B4B !important;
        border: 2px solid #FF4B4B !important;
        border-radius: 25px !important;
        height: 60px !important;
        width: 100% !important;
        font-weight: bold !important;
        font-size: 18px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }
    
    /* Efecto al pasar el ratón por encima */
    button:hover {
        background-color: #FF4B4B !important;
        color: white !important;
    }

    h1 {
        color: #FF4B4B !important;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👵 Yayobot")

# Conexión Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def hablar(texto):
    tts = gTTS(text=texto, lang='es', tld='es')
    nombre = f"v_{random.randint(1,999)}.mp3"
    tts.save(nombre)
    with open(nombre, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

# Interfaz
text = speech_to_text(language='es', start_prompt="🎤 TOCA PARA HABLAR", stop_prompt="✅ ENVIAR", key='yayo_blanco')

if text:
    st.info(f"**Tú:** {text}")
    
    mensajes = [
        {"role": "system", "content": "Eres Yayobot, un asistente amigable. Responde corto."},
        {"role": "user", "content": text}
    ]
    
    completion = client.chat.completions.create(messages=mensajes, model="llama-3.1-8b-instant")
    respuesta = completion.choices[0].message.content
    
    st.success(f"**Yayobot:** {respuesta}")
    hablar(respuesta)
