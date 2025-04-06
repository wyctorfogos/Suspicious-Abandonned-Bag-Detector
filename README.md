# Suspicious-Abandonned-Bag-Detector

It is a system with focus to detect abandonned bags.


Creation of the virtual enviroment:
`conda create -n forgeted-bagged`

Enviroment activation:
`conda activate forgeted-bagged`

Settings:

It is important to verify the settings before putting the app online. You can change the data on the script 'src/config/settins.py':

VIDEO_SOURCE: int = 0  # or RTSP
YOLO_MODEL_PATH: str = "yolov8l.pt" # Object detection model
CONFIDENCE_THRESHOLD: float = 0.5 # Threashold value

