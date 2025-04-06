import cv2
from config import settings

def get_video_capture():
    print("[DEBUG] Criando VideoCapture")
    return cv2.VideoCapture(settings.VIDEO_SOURCE)
