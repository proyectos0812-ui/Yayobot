import streamlit as st
from streamlit_mic_recorder import speech_to_text
from groq import Groq
from gtts import gTTS
import base64
import random

# 1. CONFIGURACIÓN E INTERFAZ
st.set_page_config(page_title="AmigoBot", page_icon="💬")

# Estilo visual moderno
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 3em;
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
    }
    .stApp {
        background-color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💬 AmigoBot")
st.write("¡Hola! ¿Qué tal todo? Pulsa el botón y charlamos un rato.")

# 2. CONEXIÓN SEGURA CON GROQ
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. FUNCIÓN DE VOZ MEJORADA
def hablar(texto):
    # Usamos 'es' con tld 'es' para un acento de España más natural
    tts = gTTS(text=texto, lang='es', tld='es')
    id_audio = random.randint(1, 999999)
    archivo_audio = f"voz_{id_audio}.mp3"
    tts.save(archivo_audio)
    
    with open(archivo_audio, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true" key="{id_audio}">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

# 4. EL MICRÓFONO
text = speech_to_text(
    language='es',
    start_prompt="🎤 HABLAR",
    stop_prompt="🛑 ENVIAR",
    key='speech'
)

# 5. LÓGICA DE RESPUESTA (Nueva personalidad)
if text:
    st.info(f"Tú: {text}")
    
    mensajes = [
        {
            "role": "system", 
            "content": "Eres una persona amigable, cercana y educada. Habla de forma natural, como un amigo hablaría con otro. No uses motes excesivamente dulces como 'mi sol' o 'tesoro'. Mantén las respuestas breves y directas."
        },
        {"role": "user", "content": text}
    ]
    
    try:
        completion = client.chat.completions.create(
            messages=mensajes,
            model="llama-3.1-8b-instant",
        )
        respuesta = completion.choices[0].message.content
        st.success(f"AmigoBot: {respuesta}")
        
        hablar(respuesta)
        
    except Exception as e:
        st.error(f"Error: {e}")
