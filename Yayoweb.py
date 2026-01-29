import streamlit as st
from streamlit_mic_recorder import speech_to_text
from groq import Groq
from gtts import gTTS
import base64
import random  # Necesario para que el audio no se bloquee

# 1. CONFIGURACIÓN E INTERFAZ
st.set_page_config(page_title="Yayobot", page_icon="👵")

# Estilo para el botón gigante y colores más amigables
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 3em;
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        background-color: #ff4b4b;
        color: white;
        border-radius: 15px;
    }
    .stApp {
        background-color: #f5f7f9;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👵 Yayobot")
st.write("¡Hola cariño! Pulsa el botón, cuéntame algo y espera a que te conteste.")

# 2. CLIENTE DE GROQ (Usando tus Secrets de Streamlit)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. FUNCIÓN DE VOZ MEJORADA (Ya no se queda muda)
def hablar(texto):
    tts = gTTS(text=texto, lang='es', tld='es')
    # Generamos un nombre único para que el navegador no se confunda
    id_audio = random.randint(1, 999999)
    archivo_audio = f"voz_{id_audio}.mp3"
    tts.save(archivo_audio)
    
    with open(archivo_audio, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        # El autoplay ahora detectará un contenido "nuevo" siempre
        md = f"""
            <audio autoplay="true" key="{id_audio}">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

# 4. EL MICRÓFONO
text = speech_to_text(
    language='es',
    start_prompt="🎤 PULSAR PARA HABLAR",
    stop_prompt="🛑 PARAR Y ENVIAR",
    key='speech'
)

# 5. LÓGICA DE RESPUESTA
if text:
    st.info(f"Tú: {text}")
    
    mensajes = [
        {"role": "system", "content": "Eres Yayobot, un asistente muy cariñoso para personas mayores. Habla de forma muy breve (máximo 2 frases), con mucha ternura y usa palabras como 'mi sol', 'cariño' o 'tesoro'."},
        {"role": "user", "content": text}
    ]
    
    try:
        completion = client.chat.completions.create(
            messages=mensajes,
            model="llama-3.1-8b-instant",
        )
        respuesta = completion.choices[0].message.content
        st.success(f"Yayobot: {respuesta}")
        
        # Activar la voz corregida
        hablar(respuesta)
        
    except Exception as e:
        st.error(f"¡Ay! Me he despistado un poco: {e}")
