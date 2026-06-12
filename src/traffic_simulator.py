import tkinter as tk
from tkinter import messagebox

# ==========================================
# TRAFFIC SIGNAL CONTROLLER
# ==========================================

class TrafficSimulator:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "AI Emergency Vehicle Priority System"
        )

        self.root.geometry("900x900")

        # -------------------------
        # TITLE
        # -------------------------

        self.title = tk.Label(
            root,
            text="AI-Based Emergency Vehicle Priority System",
            font=("Arial", 20, "bold")
        )

        self.title.pack(pady=10)

        # -------------------------
        # CANVAS
        # -------------------------

        self.canvas = tk.Canvas(
            root,
            width=800,
            height=700,
            bg="white"
        )

        self.canvas.pack()

        self.draw_roads()
        self.draw_signals()

        # -------------------------
        # STATUS LABEL
        # -------------------------

        self.status_label = tk.Label(
            root,
            text="System Status: NORMAL OPERATION",
            font=("Arial", 14, "bold")
        )

        self.status_label.pack(pady=10)

        # -------------------------
        # CONTROL PANEL
        # -------------------------

        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        tk.Button(
            control_frame,
            text="🚑 Ambulance on Road A",
            command=lambda: self.emergency_detected("A")
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            control_frame,
            text="🚑 Ambulance on Road B",
            command=lambda: self.emergency_detected("B")
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            control_frame,
            text="🚑 Ambulance on Road C",
            command=lambda: self.emergency_detected("C")
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            control_frame,
            text="🚑 Ambulance on Road D",
            command=lambda: self.emergency_detected("D")
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            root,
            text="Reset System",
            command=self.reset_system,
            font=("Arial", 12)
        ).pack(pady=10)

    # ==========================================
    # DRAW ROADS
    # ==========================================

    def draw_roads(self):

        self.canvas.create_rectangle(
            350, 0, 450, 700,
            fill="gray"
        )

        self.canvas.create_rectangle(
            0, 300, 800, 400,
            fill="gray"
        )

        self.canvas.create_text(
            400, 50,
            text="Road A",
            font=("Arial", 16, "bold")
        )

        self.canvas.create_text(
            750, 350,
            text="Road B",
            font=("Arial", 16, "bold")
        )

        self.canvas.create_text(
            400, 650,
            text="Road C",
            font=("Arial", 16, "bold")
        )

        self.canvas.create_text(
            50, 350,
            text="Road D",
            font=("Arial", 16, "bold")
        )

    # ==========================================
    # DRAW SIGNALS
    # ==========================================

    def draw_signals(self):

        self.signal_A = self.canvas.create_oval(
            380, 100, 420, 140,
            fill="green"
        )

        self.signal_B = self.canvas.create_oval(
            650, 330, 690, 370,
            fill="red"
        )

        self.signal_C = self.canvas.create_oval(
            380, 560, 420, 600,
            fill="red"
        )

        self.signal_D = self.canvas.create_oval(
            100, 330, 140, 370,
            fill="red"
        )

        self.signals = {
            "A": self.signal_A,
            "B": self.signal_B,
            "C": self.signal_C,
            "D": self.signal_D
        }

    # ==========================================
    # SIGNAL CONTROL
    # ==========================================

    def set_green(self, road):

        for r in self.signals:
            self.canvas.itemconfig(
                self.signals[r],
                fill="red"
            )

        self.canvas.itemconfig(
            self.signals[road],
            fill="green"
        )

    # ==========================================
    # DECISION ENGINE
    # ==========================================

    def make_decision(
        self,
        vehicle_detected,
        siren_detected
    ):

        return (
            vehicle_detected
            and
            siren_detected
        )

    # ==========================================
    # EMERGENCY EVENT
    # ==========================================

    def emergency_detected(self, road):

        # ----------------------------------
        # REPLACE THESE LINES LATER WITH
        # YOUR REAL YOLO + SIREN OUTPUTS
        # ----------------------------------

        vehicle_detected = True
        siren_detected = True

        # ----------------------------------

        priority = self.make_decision(
            vehicle_detected,
            siren_detected
        )

        if priority:

            self.set_green(road)

            self.status_label.config(
                text=f"System Status: EMERGENCY ON ROAD {road}"
            )

            messagebox.showinfo(
                "Emergency Vehicle",
                f"Priority Granted to Road {road}"
            )

        else:

            self.status_label.config(
                text="System Status: NORMAL OPERATION"
            )
    def activate_emergency(self, road):

        self.root.after(
            0,
            lambda: self._activate_emergency(road)
        )

    def _activate_emergency(self, road):

        self.set_green(road)

        self.status_label.config(
            text=f"System Status: EMERGENCY ON ROAD {road}"
        )
    # ==========================================
    # RESET
    # ==========================================

    def reset_system(self):

        self.set_green("A")

        self.status_label.config(
            text="System Status: NORMAL OPERATION"
        )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    root = tk.Tk()

    app = TrafficSimulator(root)

    root.mainloop()