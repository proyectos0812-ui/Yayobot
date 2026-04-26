import streamlit as st
import av
import cv2
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Yayobot", page_icon="👵")

# Estilo: Fondo claro, Título rojo y Botón blanco
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #f0f2f6 !important; }
    h1 { color: #FF4B4B !important; text-align: center; font-weight: 800 !important; }
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

st.title("👵 Yayobot")

# --- CARGA SEGURA DE IA ---
# Usamos el importador de soluciones de forma directa para evitar el AttributeError
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose_detector = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# --- PROCESAMIENTO DE VÍDEO ---
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # MediaPipe necesita RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose_detector.process(img_rgb)

    if results.pose_landmarks:
        # Dibujamos las líneas de la clavícula y cuerpo en AZUL
        mp_drawing.draw_landmarks(
            img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2), # Puntos
            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=3) # Líneas (Azul/Cian)
        )
        
        # Detección de caída (Hombro por debajo del 80%)
        h_izq = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
        if h_izq > 0.8:
            cv2.putText(img, "¡CAIDA!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- COMPONENTE DE CÁMARA ---
webrtc_streamer(
    key="yayocam",
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False}
)

st.info("💡 Haz clic en 'Start' y colócate frente a la cámara para ver el esqueleto azul.")
