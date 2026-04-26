import streamlit as st
import os

# Esto corrige fallos de memoria en servidores compartidos
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import cv2
import av
from streamlit_webrtc import webrtc_streamer

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Yayobot", page_icon="👵")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #f0f2f6 !important; }
    h1 { color: #FF4B4B !important; text-align: center; }
    button {
        background-color: #ffffff !important;
        color: #FF4B4B !important;
        border: 2px solid #FF4B4B !important;
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👵 Yayobot")

# --- CARGA SEGURA DE MEDIAPIPE ---
try:
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
except Exception as e:
    st.error(f"Error al cargar la IA: {e}. Reintentando...")
    st.stop()

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        # Dibujamos en AZUL
        mp_drawing.draw_landmarks(
            img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=3)
        )
        
        # Lógica de caída: hombro (punto 11) muy abajo
        y_hombro = results.pose_landmarks.landmark[11].y
        if y_hombro > 0.8:
            cv2.putText(img, "CAIDA DETECTADA", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 4)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- LA CÁMARA ---
webrtc_streamer(
    key="yayobot-final-v5",
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)

st.info("💡 Haz clic en Start para activar la cámara. Si ves líneas azules, todo está OK.")
