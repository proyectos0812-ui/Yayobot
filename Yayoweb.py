import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import mediapipe as mp
import cv2
import random
from groq import Groq
from gtts import gTTS
import base64

# --- CONFIGURACIÓN DE IA ---
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

st.set_page_config(page_title="Yayobot Vision", page_icon="👵")

# --- ESTILO (Botón Blanco y Título Rojo) ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6 !important; }
    h1 { color: #FF4B4B !important; text-align: center; }
    /* BOTÓN BLANCO */
    button {
        background-color: #ffffff !important;
        color: #FF4B4B !important;
        border: 2px solid #FF4B4B !important;
        border-radius: 20px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👵 Yayobot Pro")

# --- PROCESAMIENTO DE VÍDEO ---
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        # DIBUJAR LÍNEAS AZULES (Clavículas y Torso)
        mp_drawing.draw_landmarks(
            img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=3, circle_radius=3), # Puntos azules
            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=3) # Líneas cian/azul
        )

        # DETECTAR CAÍDA (Si los hombros bajan del 80% de la pantalla)
        h_izq = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
        h_der = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
        
        if h_izq > 0.8 or h_der > 0.8:
            cv2.putText(img, "¡CAIDA!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- CÁMARA ---
st.write("### 🎥 Vigilancia activa")
webrtc_streamer(
    key="yayovision", 
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

st.info("Yayobot te avisará si detecta una caída analizando tu clavícula.")
