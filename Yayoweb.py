import streamlit as st
import os

# Forzamos compatibilidad de sistema
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

st.set_page_config(page_title="Yayobot", page_icon="👵")
st.title("👵 Yayobot")

try:
    import cv2
    import mediapipe as mp
    import av
    from streamlit_webrtc import webrtc_streamer
    
    # Cargamos el modelo de pose
    mp_pose = mp.solutions.pose
    mp_draw = mp.solutions.drawing_utils
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    st.success("✅ ¡Sistema operativo e IA listos!")

    def callback(frame):
        img = frame.to_ndarray(format="bgr24")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)
        
        if results.pose_landmarks:
            # Dibujamos el esqueleto en AZUL
            mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                 mp_draw.DrawingSpec(color=(255,0,0), thickness=2),
                                 mp_draw.DrawingSpec(color=(255,255,0), thickness=2))
            
            # Detectar si el hombro baja mucho (caída)
            hombro_y = results.pose_landmarks.landmark[11].y
            if hombro_y > 0.8:
                cv2.putText(img, "CAIDA DETECTADA", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                
        return av.VideoFrame.from_ndarray(img, format="bgr24")

    webrtc_streamer(
        key="yayobot-v6",
        video_frame_callback=callback,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": False}
    )

except Exception as e:
    st.error(f"Fallo de sistema: {e}")
    st.info("Revisa que packages.txt tenga: libgl1, libglib2.0-0 y libgthread-2.0-0")
