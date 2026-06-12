from ultralytics import YOLO

MODEL_PATH = r"C:\Users\HEMANTH KUMAR K\Desktop\ambulance_detector\YOLOv8_ambulance_setector\emergency_vehicle_detector-4\weights\best.pt"

model = YOLO(MODEL_PATH)

def detect_vehicle(frame):

    results = model(
        frame,
        conf=0.3,
        verbose=False
    )

    vehicle_detected = False
    best_conf = 0

    road = None

    h, w = frame.shape[:2]

    for box in results[0].boxes:

        conf = float(box.conf[0])

        if conf > best_conf:
            best_conf = conf

        if conf >= 0.3:

            vehicle_detected = True

            x1, y1, x2, y2 = box.xyxy[0]

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            if center_x < w/2 and center_y < h/2:
                road = "A"

            elif center_x >= w/2 and center_y < h/2:
                road = "B"

            elif center_x >= w/2 and center_y >= h/2:
                road = "C"

            else:
                road = "D"

    return vehicle_detected, best_conf, road

if __name__ == "__main__":

    import cv2

    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    if ret:

        vehicle_detected, conf, road = detect_vehicle(frame)

        print("Detected:", vehicle_detected)
        print("Confidence:", conf)
        print("Road:", road)

    cap.release()