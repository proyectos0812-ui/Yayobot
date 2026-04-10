import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import mediapipe as mp
import cv2
import random
from groq import Groq
from gtts import gTTS
import base64

# --- 1. CONFIGURACIÓN DE IA Y VISIÓN ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# --- 2. CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(page_title="Yayobot Vision Pro", page_icon="👵")

st.markdown("""
    <style>
    /* Fondo claro */
    [data-testid="stAppViewContainer"] {
        background-color: #f0f2f6 !important;
    }
    /* Título Yayobot en Rojo */
    h1 {
        color: #FF4B4B !important;
        text-align: center !important;
        font-weight: 800 !important;
    }
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

st.title("👵 Yayobot Pro")
st.write("### 🎥 Vigilancia de Clavículas Activa")

# --- 3. PROCESAMIENTO DE VÍDEO (Líneas Azules) ---
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # MediaPipe necesita RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        # Dibujamos el esqueleto con líneas azules/cian
        mp_drawing.draw_landmarks(
            img, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2), # Puntos
            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=3) # Líneas (Cian)
        )

        # Lógica de detección de caída (Hombros/Clavícula)
        # El punto Y va de 0.0 (arriba) a 1.0 (abajo)
        h_izq = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
        h_der = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
        
        # Si los hombros bajan del 80% de la pantalla
        if h_izq > 0.8 or h_der > 0.8:
            cv2.putText(img, "!!! CAIDA DETECTADA !!!", (30, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- 4. COMPONENTE DE VÍDEO ---
webrtc_streamer(
    key="yayovision", 
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False}
)

st.info("💡 Yayobot está analizando tu postura en tiempo real. Si detecta que tus hombros bajan demasiado, saltará la alerta.")
