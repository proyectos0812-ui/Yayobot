import os
# FORZAMOS AL SISTEMA A USAR LA VERSIÓN COMPATIBLE
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import streamlit as st
import cv2
import mediapipe as mp
import av
from streamlit_webrtc import webrtc_streamer

# CONFIGURACIÓN VISUAL
st.set_page_config(page_title="Yayobot", page_icon="👵")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #f0f2f6 !important; }
    h1 { color: #FF4B4B !important; text-align: center; font-weight: bold; }
    button {
        background-color: #ffffff !important;
        color: #FF4B4B !important;
        border: 2px solid #FF4B4B !important;
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👵 Yayobot")

# CARGA SEGURA DE MODELOS
@st.cache_resource
def iniciar_ia():
    # Intentamos cargar por la vía directa
    try:
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
        mp_draw = mp.solutions.drawing_utils
        return mp_pose, pose, mp_draw
    except Exception as e:
        st.error(f"Error de IA: {e}")
        return None, None, None

mp_pose, pose, mp_draw = iniciar_ia()

def callback(frame):
    img = frame.to_ndarray(format="bgr24")
    
    if pose:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)

        if results.pose_landmarks:
            # Dibujamos esqueleto azul
            mp_draw.draw_landmarks(
                img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                mp_draw.DrawingSpec(color=(255, 255, 0), thickness=3)
            )
            
            # Alerta visual
            hombro = results.pose_landmarks.landmark[11].y
            if hombro > 0.8:
                cv2.putText(img, "ALERTA: CAIDA", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 4)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# LA CÁMARA
if mp_pose:
    webrtc_streamer(
        key="yayo-v4",
        video_frame_callback=callback,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": False}
    )
else:
    st.warning("La IA se está reiniciando. Espera un momento...")
