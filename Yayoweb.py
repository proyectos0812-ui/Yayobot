import streamlit as st

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO (Primero para evitar errores visuales) ---
st.set_page_config(page_title="Yayobot Vision Pro", page_icon="👵")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #f0f2f6 !important; }
    h1 { color: #FF4B4B !important; text-align: center; font-weight: 800 !important; }
    /* BOTÓN DE CÁMARA BLANCO */
    button {
        background-color: #ffffff !important;
        color: #FF4B4B !important;
        border: 2px solid #FF4B4B !important;
        border-radius: 20px !important;
        height: 50px !important;
        width: 100% !important;
        font-weight: bold !important;
    }
    button:hover {
        background-color: #FF4B4B !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. IMPORTACIONES DE LIBRERÍAS ---
from streamlit_webrtc import webrtc_streamer
import av
import cv2
import mediapipe as mp
from groq import Groq

# Intentamos cargar MediaPipe con seguridad
try:
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
except AttributeError:
    st.error("Error crítico: Parece que hay un archivo llamado 'mediapipe.py' en tu carpeta. Por favor, cámbiale el nombre para que la IA funcione.")

# --- 3. LÓGICA DE LA IA (Groq) ---
# Asegúrate de tener GROQ_API_KEY en los Secrets de Streamlit
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.warning("⚠️ No se encontró la clave de Groq en los Secrets.")

# --- 4. PROCESAMIENTO DE VÍDEO (Las líneas azules) ---
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # Conversión necesaria para que la IA lea la imagen
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        # DIBUJAMOS EL ESQUELETO AZUL/CIAN
        mp_drawing.draw_landmarks(
            img, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2), # Puntos
            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=3) # Líneas Cian (Azul claro)
        )

        # DETECCIÓN DE CAÍDA (Si la clavícula baja mucho)
        # El hombro izquierdo es el punto 11, el derecho el 12
        h_izq = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
        h_der = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
        
        # 0.8 significa el 80% de la pantalla hacia abajo
        if h_izq > 0.8 or h_der > 0.8:
            cv2.putText(img, "!!! CAIDA DETECTADA !!!", (30, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- 5. INTERFAZ DE USUARIO ---
st.title("👵 Yayobot Pro")
st.write("Haz clic en **Start** para activar la vigilancia de clavículas.")

webrtc_streamer(
    key="yayovision", 
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False}
)

st.info("💡 Consejo: Asegúrate de que se vea bien tu torso para que Yayobot pueda dibujar las líneas de la clavícula.")
