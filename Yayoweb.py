import streamlit as st
from streamlit_mic_recorder import speech_to_text
from groq import Groq
from gtts import gTTS
import base64
import random

# 1. CONFIGURACIÓN DE LA PÁGINA (Título en la pestaña del navegador)
st.set_page_config(page_title="Yayobot Pro", page_icon="👵", layout="centered")

# 2. ESTILO CSS AVANZADO (Esto es lo que hace que se vea genial)
st.markdown("""
    <style>
    /* Fondo con degradado suave */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }
    
    /* Contenedor principal para centrar contenido */
    .main-container {
        max-width: 700px;
        margin: auto;
        padding: 20px;
    }

    /* Estilo del título principal */
    .main-title {
        color: #2c3e50;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        font-size: 3em;
        padding-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Subtítulo */
    .sub-title {
        color: #7f8c8d;
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 30px;
    }

    /* Ocultar el botón feo por defecto de Streamlit y estilizar el nuestro */
    div.stButton > button {
        background-color: #ff4b4b; /* Rojo Yayobot */
        color: white;
        border-radius: 50px;
        padding: 15px 30px;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
        transition: all 0.3s ease;
        width: 100%;
        font-size: 1.3em;
        font-weight: bold;
    }
    
    div.stButton > button:hover {
        background-color: #e04040;
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.5);
    }

    /* --- ESTILO DE BURBUJAS DE CHAT --- */
    .chat-bubble {
        padding: 15px 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        max-width: 80%;
        font-family: 'Segoe UI', sans-serif;
        line-height: 1.4;
        position: relative;
        clear: both;
    }
    
    /* Burbuja del Usuario (Tú) - Derecha y Azul */
    .user-bubble {
        background-color: #DCF8C6; /* Verde tipo WhatsApp */
        float: right;
        color: #303030;
        border-bottom-right-radius: 2px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Burbuja del Bot (Yayobot) - Izquierda y Blanca */
    .bot-bubble {
        background-color: #ffffff;
        float: left;
        color: #303030;
        border-bottom-left-radius: 2px;
        box-shadow: -2px 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Limpiar floats para que las burbujas no se superpongan */
    .clearfix::after {
        content: "";
        clear: both;
        display: table;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INTERFAZ VISUAL
st.markdown("<div class='main-container'>", unsafe_allow_html=True) # Inicio contenedor principal

st.markdown("<h1 class='main-title'>👵 Yayobot</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Tu asistente amigable. ¡Toca el botón y hablemos!</p>", unsafe_allow_html=True)
st.write("---") # Línea divisoria

# 4. CONEXIÓN CON GROQ (Secrets)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 5. FUNCIÓN DE VOZ (Se mantiene para que hable)
def hablar(texto):
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

# 6. ENTRADA DE VOZ (El Micrófono estilizado en una columna centrada)
col1, col2, col3 = st.columns([1,3,1]) # Centrar el botón
with col2:
    text = speech_to_text(
        language='es',
        start_prompt="🎤 Toca para hablar",
        stop_prompt="✅ Enviar mensaje",
        key='speech'
    )

# 7. LÓGICA DEL CHAT
st.markdown("<div class='clearfix'></div>", unsafe_allow_html=True) # Espaciador

if text:
    # Mostrar mensaje del usuario en burbuja verde a la derecha
    st.markdown(f"<div class='clearfix'><div class='chat-bubble user-bubble'><b>Tú:</b><br>{text}</div></div>", unsafe_allow_html=True)
    
    # Personalidad: Amigable y natural, sin motes dulces
    mensajes = [
        {
            "role": "system", 
            "content": "Eres Yayobot, un asistente amigable, cercano y educado. Responde de forma muy natural, como un amigo. No uses motes excesivamente dulces como 'mi sol' o 'tesoro'. Mantén las respuestas breves."
        },
        {"role": "user", "content": text}
    ]
    
    try:
        completion = client.chat.completions.create(
            messages=mensajes,
            model="llama-3.1-8b-instant",
        )
        respuesta = completion.choices[0].message.content
        
        # Mostrar respuesta de Yayobot en burbuja blanca a la izquierda
        st.markdown(f"<div class='clearfix'><div class='chat-bubble bot-bubble'><b>Yayobot:</b><br>{respuesta}</div></div>", unsafe_allow_html=True)
        
        # Activar la voz
        hablar(respuesta)
        
    except Exception as e:
        st.error(f"Error en la conexión: {e}")

st.markdown("</div>", unsafe_allow_html=True) # Fin contenedor principal
