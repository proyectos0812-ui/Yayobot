import streamlit as st
import cv2
import mediapipe as mp
import av
from streamlit_webrtc import webrtc_streamer

st.set_page_config(page_title="Yayobot", page_icon="👵")
st.title("👵 Yayobot")

# Carga de IA ultra segura
@st.cache_resource
def load_ia():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils
    return mp_pose, pose, mp_draw

try:
    mp_pose, pose, mp_draw = load_ia()
    st.success("✅ ¡IA Lista!")
except Exception as e:
    st.error(f"Error cargando IA: {e}")

def callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)
    if results.pose_landmarks:
        mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="yayo-final",
    video_frame_callback=callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False}
)
