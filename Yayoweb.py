import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2
import mediapipe as mp
from groq import Groq

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Yayobot Vision Pro", page_icon="👵")

# Estilo: Botón Blanco y Título Rojo
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #f0f2f6 !important; }
    h1 { color: #FF4B4B !important; text-align: center; }
    button {
        background-color: #ffffff !important;
        color: #FF4B4B !important;
        border: 2px solid #FF4B4B !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👵 Yayobot Pro")

# Inicializar MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        # Dibujar esqueleto azul
        mp_drawing.draw_landmarks(
            img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=3)
        )
        
        # Lógica de caída (Clavícula baja)
        h_izq = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
        if h_izq > 0.8:
            cv2.putText(img, "CAIDA!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="yayobot",
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False}
)
