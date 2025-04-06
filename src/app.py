from models.detector import detect_objects
from utils.video_reader import get_video_capture
from utils.draw import draw_detections
import cv2

def main():
    cap = get_video_capture()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detections = detect_objects(frame)
        frame = draw_detections(frame, detections)

        cv2.imshow("Detected Objects", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()