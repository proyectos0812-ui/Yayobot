import streamlit as st
import sys

# FORZAR COMPATIBILIDAD AL MÁXIMO
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

st.set_page_config(page_title="Yayobot", page_icon="👵")
st.title("👵 Yayobot")

# Intentar importar las librerías una por una para ver dónde explota
try:
    import cv2
    import mediapipe as mp
    import av
    from streamlit_webrtc import webrtc_streamer
    
    # Si llega aquí, es que las librerías básicas están
    mp_pose = mp.solutions.pose
    mp_draw = mp.solutions.drawing_utils
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    st.success("✅ ¡IA lista para vigilar!")
    
    def callback(frame):
        img = frame.to_ndarray(format="bgr24")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)
        if results.pose_landmarks:
            mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

    webrtc_streamer(
        key="yayo-final-final",
        video_frame_callback=callback,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": False}
    )

except ImportError as e:
    st.error(f"❌ Fallo de instalación: {e}")
    st.info("💡 Consejo: Asegúrate de que en 'Advanced Settings' has puesto Python 3.11.")
except Exception as e:
    st.error(f"❌ Error inesperado: {e}")
