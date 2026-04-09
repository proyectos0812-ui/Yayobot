import streamlit as st
from streamlit_mic_recorder import speech_to_text
from groq import Groq
from gtts import gTTS
import base64
import random

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Yayobot v2", page_icon="👵", layout="centered")

# 2. DISEÑO CSS AVANZADO
st.markdown("""
    <style>
    /* Fondo y tipografía */
    .stApp {
        background: linear-gradient(180deg, #f0f2f6 0%, #ffffff 100%);
    }
    
    /* Estilo del título */
    .main-title {
        color: #2c3e50;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        padding-bottom: 20px;
    }

    /* Botón de grabación */
    div.stButton > button {
        background-color: #4A90E2;
        color: white;
        border-radius: 50px;
        padding: 15px 30px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        width: 100%;
        font-size: 1.2em;
    }
    
    div.stButton > button:hover {
        background-color: #357ABD;
        transform: translateY(-2px);
    }

    /* Burbujas de chat */
    .chat-bubble {
        padding: 15px;
        border-radius: 20px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .user-bubble {
        background-color: #e1f5fe;
        margin-left: auto;
        color: #01579b;
        border-bottom-right-radius: 2px;
    }
    .bot-bubble {
        background-color: #ffffff;
        margin-right: auto;
        color: #333;
        border-bottom-left-radius: 2px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>👵 Yayobot</h1>", unsafe_allow_html=True)
st.write("---")

# 3. CONEXIÓN CON GROQ
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def hablar(texto):
    # Intentamos mejorar la velocidad para que suene menos pausado
    tts = gTTS(text=texto, lang='es', tld='es')
    id_audio = random.randint(1, 999999)
    archivo_audio = f"voz_{id_audio}.mp3"
    tts.save(archivo_audio)
    
    with open(archivo_audio, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true" style="display:none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

# 4. INTERFAZ DE USUARIO
col1, col2, col3 = st.columns([1,2,1])
with col2:
    text = speech_to_text(
        language='es',
        start_prompt="🎤 Toca para hablar",
        stop_prompt="✅ Enviar mensaje",
        key='speech'
    )

if text:
    # Mostrar mensaje del usuario
    st.markdown(f"<div class='chat-bubble user-bubble'><b>Tú:</b> {text}</div>", unsafe_allow_html=True)
    
    mensajes = [
        {
            "role": "system", 
            "content": "Eres Yayobot, un asistente amigable, educado y cercano. Responde de forma natural, sin ser excesivamente empalagoso. Usa frases cortas y claras."
        },
        {"role": "user", "content": text}
    ]
    
    try:
        completion = client.chat.completions.create(
            messages=mensajes,
            model="llama-3.1-8b-instant",
        )
        respuesta = completion.choices[0].message.content
        
        # Mostrar respuesta del bot
        st.markdown(f"<div class='chat-bubble bot-bubble'><b>Yayobot:</b> {respuesta}</div>", unsafe_allow_html=True)
        
        hablar(respuesta)
        
    except Exception as e:
        st.error(f"Error en la conexión: {e}")
