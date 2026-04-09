import streamlit as st
from streamlit_mic_recorder import speech_to_text
from groq import Groq
from gtts import gTTS
import base64
import random

# 1. ESTO TIENE QUE IR PRIMERO: Configuración y Estilo Total
st.set_page_config(page_title="Yayobot Pro", page_icon="👵")

st.markdown("""
    <style>
    /* 1. CAMBIAR EL FONDO DE TODA LA PÁGINA */
    .stApp {
        background: linear-gradient(180deg, #E3F2FD 0%, #FFFFFF 100%) !important;
    }

    /* 2. TÍTULO EN ROJO Y GRANDE */
    .titulo-pro {
        color: #FF4B4B !important;
        font-size: 55px !important;
        font-weight: 800 !important;
        text-align: center !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-top: -40px;
    }

    /* 3. BURBUJAS DE CHAT ESTILO MODERNAS */
    .burbuja {
        padding: 20px;
        border-radius: 20px;
        margin: 15px 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        line-height: 1.5;
    }
    .user {
        background-color: #DCF8C6 !important; /* Verde WhatsApp */
        border-left: 10px solid #25D366 !important;
        color: #2c3e50;
    }
    .bot {
        background-color: #FFFFFF !important;
        border-left: 10px solid #FF4B4B !important;
        color: #2c3e50;
    }

    /* 4. BOTÓN DE GRABAR GIGANTE Y REDONDO */
    button[kind="secondary"] {
        background-color: #FF4B4B !important;
        color: white !important;
        border-radius: 50px !important;
        height: 80px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 8px 15px rgba(255, 75, 75, 0.4) !important;
    }
    
    /* Quitar menús feos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Cabecera
st.markdown("<h1 class='titulo-pro'>👵 Yayobot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Tu asistente inteligente y amigable</p>", unsafe_allow_html=True)

# 2. CONEXIÓN GROQ
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def hablar(texto):
    tts = gTTS(text=texto, lang='es', tld='es')
    id_audio = random.randint(1, 99999)
    archivo = f"v_{id_audio}.mp3"
    tts.save(archivo)
    with open(archivo, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

# 3. INTERFAZ DE USUARIO
st.write(" ")
text = speech_to_text(
    language='es',
    start_prompt="🎤 TOCA PARA HABLAR",
    stop_prompt="✅ ENVIAR",
    key='yayo_v3'
)

if text:
    # Burbuja del Usuario
    st.markdown(f"<div class='burbuja user'><b>Tú:</b><br>{text}</div>", unsafe_allow_html=True)
    
    mensajes = [
        {"role": "system", "content": "Eres Yayobot, un asistente amigable, educado y natural. No uses motes excesivos. Responde brevemente."},
        {"role": "user", "content": text}
    ]
    
    try:
        completion = client.chat.completions.create(
            messages=mensajes,
            model="llama-3.1-8b-instant",
        )
        respuesta = completion.choices[0].message.content
        
        # Burbuja del Bot
        st.markdown(f"<div class='burbuja bot'><b>Yayobot:</b><br>{respuesta}</div>", unsafe_allow_html=True)
        
        hablar(respuesta)
        
    except Exception as e:
        st.error(f"Error: {e}")
