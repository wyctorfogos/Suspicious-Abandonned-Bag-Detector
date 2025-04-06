import cv2
import supervision as sv
from models.detector import get_model
from utils.video_reader import get_video_capture
from utils.track_abandonment import update_abandonment_status
from utils.draw import draw_annotations
from config.settings import CONFIDENCE_THRESHOLD

model = get_model()
byte_tracker = sv.ByteTrack()
cap = get_video_capture()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Executa a detecção com o modelo
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)

    # Separa as detecções de pessoas
    persons = detections[[model.names[int(cls)] == 'person' for cls in detections.class_id]]

    # Separa objetos de interesse (mochilas, bolsas, malas)
    objects = detections[[model.names[int(cls)] in ['backpack', 'handbag', 'suitcase'] for cls in detections.class_id]]

    # Rastreia apenas os objetos de interesse
    tracked_objects = byte_tracker.update_with_detections(objects)

    # Coleta os centros das pessoas detectadas
    person_centers = [((x1 + x2) // 2, (y1 + y2) // 2) for x1, y1, x2, y2 in persons.xyxy]

    # Cria rótulos para desenhar nos objetos rastreados
    labels = [
        f"{model.names[int(cls)]} {tracker_id}"
        for cls, tracker_id in zip(tracked_objects.class_id, tracked_objects.tracker_id)
    ]

    # Verifica objetos abandonados com base na distância das pessoas
    alerts = update_abandonment_status(tracked_objects, person_centers)

    abandoned_ids = {alert["id"] for alert in alerts}  # collect abandoned IDs

    for alert in alerts:
        print(f"🚨 ALERTA: Objeto ID {alert['id']} abandonado por {alert['time']:.1f}s")

    # draw with highlights
    annotated = draw_annotations(frame, tracked_objects, labels, abandoned_ids)


    # Exibe o resultado
    cv2.imshow("Intelligent Surveillance", annotated)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
