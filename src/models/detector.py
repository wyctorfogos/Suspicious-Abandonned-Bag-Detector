from ultralytics import YOLO
import supervision as sv
from config.settings import YOLO_MODEL_PATH, CONFIDENCE_THRESHOLD

# Classes de interesse
TARGET_CLASSES = {"backpack", "handbag", "suitcase", "person"}

model = YOLO(YOLO_MODEL_PATH)

def detect_objects(frame):
    # Realiza a detecção
    results = model(frame)[0]

    # Filtra as detecções pelas classes de interesse e confiança
    detections = sv.Detections.from_ultralytics(results)
    detections = detections[detections.confidence > CONFIDENCE_THRESHOLD]
    detections = detections[[model.names[int(cls)] in TARGET_CLASSES for cls in detections.class_id]]
    
    return detections

def get_model():
    return model