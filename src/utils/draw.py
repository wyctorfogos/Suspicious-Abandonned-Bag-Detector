import supervision as sv

bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

def draw_annotations(frame, detections, labels):
    frame = bounding_box_annotator.annotate(scene=frame.copy(), detections=detections)
    frame = label_annotator.annotate(scene=frame, detections=detections, labels=labels)
    return frame
