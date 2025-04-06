from ultralytics import YOLO
from config.settings import YOLO_MODEL_PATH, CONFIDENCE_THRESHOLD

# Classes de interesse
TARGET_CLASSES = {"backpack", "handbag", "suitcase", "person"}

model = YOLO(YOLO_MODEL_PATH)

def detect_objects(frame):
    results = model(frame)[0]
    detections = []

    for result in results.boxes:
        conf = float(result.conf.item())
        if conf < CONFIDENCE_THRESHOLD:
            continue

        cls_id = int(result.cls.item())
        label = model.names[cls_id]

        # Filtro apenas objetos desejados
        if label not in TARGET_CLASSES:
            continue

        box = result.xyxy[0].cpu().numpy().astype(int)

        detections.append({
            "label": label,
            "confidence": conf,
            "bbox": box
        })

    return detections
