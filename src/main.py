import cv2
import tkinter as tk
import threading

from vehicle_detector import detect_vehicle
from siren_detector import detect_siren
from decision_engine import priority_decision

from traffic_simulator import TrafficSimulator
def ai_loop(simulator):

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        if not ret:
            continue
        cv2.imshow("Live Camera", frame)

        if cv2.waitKey(1) == 27:
            break
        vehicle_detected, vehicle_conf, road = detect_vehicle(
            frame
        )
        
        if vehicle_detected:
            print(
            f"Vehicle={vehicle_detected}, "
            f"Road={road}"
            )
            print(
                "Checking siren..."
            )

            siren_detected, siren_conf = detect_siren()
            print(
            f"Siren={siren_detected}"
            )
            priority = priority_decision(
                vehicle_detected,
                siren_detected
            )
            print(
            f"Priority={priority}"
            )
            if priority and road:

                simulator.activate_emergency(
                    road
                )



root = tk.Tk()

simulator = TrafficSimulator(
        root
    )

thread = threading.Thread(
        target=ai_loop,
        args=(simulator,),
        daemon=True
    )

thread.start()

root.mainloop()