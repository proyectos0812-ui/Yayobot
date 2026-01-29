import streamlit as st
from streamlit_mic_recorder import speech_to_text
from groq import Groq
from gtts import gTTS
import base64

# 1. CONFIGURACIÓN E INTERFAZ
st.set_page_config(page_title="Yayobot", page_icon="👵")

# Estilo para el botón gigante
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 3em;
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        background-color: #ff4b4b;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👵 Yayobot")
st.write("Pulsa el botón, habla y espera a que te conteste.")

# 2. CLIENTE DE GROQ (Usando Secretos seguros)
# Esto ya no dará error en GitHub
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. FUNCIÓN PARA GENERAR VOZ
def hablar(texto):
    tts = gTTS(text=texto, lang='es', tld='es')
    tts.save("temp.mp3")
    with open("temp.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        # HTML para que el audio suene solo
        md = f"""
            <audio autoplay="true">
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

# 5. LÓGICA
if text:
    st.info(f"Tú: {text}")
    
    mensajes = [
        {"role": "system", "content": "Eres Yayobot, un asistente cariñoso para abuelos. Habla muy breve, máximo 2 frases, y usa palabras dulces como 'cariño'."},
        {"role": "user", "content": text}
    ]
    
    try:
        completion = client.chat.completions.create(
            messages=mensajes,
            model="llama-3.1-8b-instant",
        )
        respuesta = completion.choices[0].message.content
        st.success(f"Yayobot: {respuesta}")
        
        # Activar la voz
        hablar(respuesta)
        
    except Exception as e:
        st.error(f"Fallo en el cerebro: {e}")