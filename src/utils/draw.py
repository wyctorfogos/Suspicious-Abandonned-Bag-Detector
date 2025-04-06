import cv2

def draw_annotations(frame, detections, labels, abandoned_ids=set()):
    annotated_frame = frame.copy()
    for i, tracker_id in enumerate(detections.tracker_id):
        # Obtém as coordenadas da caixa delimitadora
        box = detections.xyxy[i]
        x1, y1, x2, y2 = map(int, box)
        # Define a cor: vermelho se abandonado, verde caso contrário
         
        if tracker_id in abandoned_ids:
            color = (0, 0, 255)
            # Desenha a caixa e o rótulo
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(annotated_frame, "Abandoned object: "+labels[i], (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        else:
            color = (0, 255, 0)
            # Desenha a caixa e o rótulo
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(annotated_frame, labels[i], (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
    return annotated_frame
