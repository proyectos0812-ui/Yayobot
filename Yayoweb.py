import streamlit as st
import os

# Forzamos compatibilidad
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import cv2
import av
from streamlit_webrtc import webrtc_streamer

st.set_page_config(page_title="Yayobot", page_icon="👵")

st.title("👵 Yayobot")

# INTENTO DE CARGA DESESPERADO
try:
    import mediapipe as mp
    # Si mp.solutions falla, intentamos recargar el módulo
    if not hasattr(mp, 'solutions'):
        import importlib
        importlib.reload(mp)
    
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    st.success("¡IA Cargada correctamente!")
except Exception as e:
    st.error(f"Error crítico: {e}. Por favor, reinicia la app en el panel de Streamlit.")
    st.stop()

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="yayo-final",
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False}
)
