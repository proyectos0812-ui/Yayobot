import streamlit as st
import av
import cv2
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Yayobot", page_icon="👵")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #f0f2f6 !important; }
    h1 { color: #FF4B4B !important; text-align: center; font-weight: 800 !important; }
    /* BOTÓN BLANCO */
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

st.title("👵 Yayobot") # Quitamos el Pro

# --- 2. CARGA SEGURA DE MEDIAPIPE ---
# Usamos soluciones directas para evitar el error de 'AttributeError'
Pose = mp.solutions.pose.Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose_frames = mp.solutions.pose

pose_tracker = Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# --- 3. PROCESAMIENTO DE VÍDEO ---
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # IA analiza la imagen
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose_tracker.process(img_rgb)

    if results.pose_landmarks:
        # Dibujamos las líneas azules (Cian)
        mp_drawing.draw_landmarks(
            img, results.pose_landmarks, mp_pose_frames.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=3)
        )
        
        # Detección de caída simple
        h_izq = results.pose_landmarks.landmark[mp_pose_frames.PoseLandmark.LEFT_SHOULDER].y
        if h_izq > 0.8:
            cv2.putText(img, "CAIDA!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- 4. CÁMARA ---
webrtc_streamer(
    key="yayobot-cam",
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False}
)

st.info("💡 Yayobot está listo. Si ves las líneas azules, la IA está funcionando.")
