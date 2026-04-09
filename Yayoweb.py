import streamlit as st
from streamlit_mic_recorder import speech_to_text
from groq import Groq
from gtts import gTTS
import base64
import random

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Yayobot Pro", page_icon="👵")

# 2. ESTILO CSS PARA QUE SE VEA INCREÍBLE
st.markdown("""
    <style>
    /* Fondo de la app */
    .stApp {
        background-color: #f8f9fa;
    }
    /* Título principal */
    .titulo-yayobot {
        color: #ff4b4b;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 50px;
        font-weight: bold;
        margin-top: -50px;
    }
    /* Burbujas de chat */
    .bubble {
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .user-bubble {
        background-color: #e3f2fd;
        border-left: 8px solid #2196f3;
        margin-left: 50px;
    }
    .bot-bubble {
        background-color: #ffffff;
        border-left: 8px solid #ff4b4b;
        margin-right: 50px;
    }
    /* Estilo del botón de grabación */
    div.stButton > button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 50px;
        border: none;
        height: 60px;
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(255, 75, 75, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# Título visual en la pantalla
st.markdown("<div class='titulo-yayobot'>👵 Yayobot</div>", unsafe_allow_html=True)
st.write("---")

# 3. CLIENTE GROQ
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 4. FUNCIÓN DE VOZ
def hablar(texto):
    tts = gTTS(text=texto, lang='es', tld='es')
    id_audio = random.randint(1, 100000)
    archivo_audio = f"v_{id_audio}.mp3"
    tts.save(archivo_audio)
    
    with open(archivo_audio, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        audio_html = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)

# 5. EL MICRO (Interfaz de grabación)
text = speech_to_text(
    language='es',
    start_prompt="🎤 PULSA PARA HABLAR",
    stop_prompt="✅ ENVIAR AHORA",
    key='yayo_input'
)

# 6. LÓGICA DE RESPUESTA
if text:
    # Burbuja del usuario
    st.markdown(f"<div class='bubble user-bubble'><b>Tú:</b><br>{text}</div>", unsafe_allow_html=True)
    
    # Personalidad: Amigable y natural
    mensajes = [
        {"role": "system", "content": "Eres Yayobot, un asistente amigable y cercano. Habla de forma natural como un amigo, responde brevemente y con educación. No uses motes excesivos."},
        {"role": "user", "content": text}
    ]
    
    try:
        completion = client.chat.completions.create(
            messages=mensajes,
            model="llama-3.1-8b-instant",
        )
        respuesta = completion.choices[0].message.content
        
        # Burbuja de Yayobot
        st.markdown(f"<div class='bubble bot-bubble'><b>Yayobot:</b><br>{respuesta}</div>", unsafe_allow_html=True)
        
        # Activar audio
        hablar(respuesta)
        
    except Exception as e:
        st.error(f"¡Ups! Algo ha fallado: {e}")
