import time
from collections import defaultdict
from config.settings import ABANDONMENT_TIME

object_entry_time = defaultdict(lambda: None)
IGNORED_IDS = set()

def is_close(obj_center, person_centers, threshold=100):
    for pc in person_centers:
        dx = obj_center[0] - pc[0]
        dy = obj_center[1] - pc[1]
        distance = (dx**2 + dy**2)**0.5
        if distance < threshold:
            return True
    return False

def update_abandonment_status(tracked_detections, person_centers):
    current_time = time.time()
    alerts = []

    for i, tracker_id in enumerate(tracked_detections.tracker_id):
        box = tracked_detections.xyxy[i]
        center_x = int((box[0] + box[2]) / 2)
        center_y = int((box[1] + box[3]) / 2)
        center = (center_x, center_y)

        if is_close(center, person_centers):
            object_entry_time[tracker_id] = None
            IGNORED_IDS.discard(tracker_id)
            continue

        if object_entry_time[tracker_id] is None:
            object_entry_time[tracker_id] = current_time
        else:
            time_in_scene = current_time - object_entry_time[tracker_id]
            if time_in_scene >= ABANDONMENT_TIME and tracker_id not in IGNORED_IDS:
                alerts.append({
                    "id": tracker_id,
                    "time": time_in_scene
                })
                #  If you want to ignore the alert, just uncomment the line below
                # IGNORED_IDS.add(tracker_id)

    return alerts
