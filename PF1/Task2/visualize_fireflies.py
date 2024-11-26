import tkinter as tk
import math
import random
import threading
import time
import grpc
from firefly_pb2 import Empty
import firefly_pb2_grpc

# Define the grid and ports
GRID_SIZE = 5
FIREFLY_PORTS = [5000 + i for i in range(GRID_SIZE * GRID_SIZE)]  # Ports for fireflies

class FireflyVisualizer:
    def __init__(self, grid_size, firefly_ports):
        self.grid_size = grid_size
        self.firefly_ports = firefly_ports
        self.root = tk.Tk()
        self.root.title("Firefly Synchronization (Decentralized)")
        self.canvas = tk.Canvas(self.root, width=grid_size * 50, height=grid_size * 50)
        self.canvas.pack()

        self.fireflies = {}
        for idx, port in enumerate(self.firefly_ports):
            x, y = idx % grid_size, idx // grid_size
            rect = self.canvas.create_rectangle(
                x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill="black"
            )
            initial_brightness = random.uniform(0, 1)  # Random brightness (0-1)
            initial_phase = random.uniform(0, 2 * math.pi)  # Random phase (0-2π)
            self.fireflies[port] = {"rect": rect, "phase": initial_phase, "brightness": initial_brightness}

        self.synchronized = False

    def update_firefly_phases(self):
        while True:
            phases = []
            for port in self.firefly_ports:
                try:
                    with grpc.insecure_channel(f"localhost:{port}") as channel:
                        stub = firefly_pb2_grpc.FireflyStub(channel)
                        phase_message = stub.RequestPhase(Empty())
                        self.fireflies[port]["phase"] = phase_message.phase
                        phases.append(phase_message.phase)
                except grpc.RpcError:
                    pass  # If a firefly is unreachable, just skip updating its phase
            
            # Check if all fireflies are synchronized
            if len(phases) > 0 and all(abs(phases[0] - phase) < 0.1 for phase in phases):
                self.synchronized = True
            
            time.sleep(0.1)

    def update_canvas(self):
        while True:
            for port, firefly in self.fireflies.items():
                phase = firefly["phase"]
                if phase is not None:
                    # Smooth transition to target brightness
                    target_brightness = (1 + math.sin(phase)) / 2
                    firefly["brightness"] += (target_brightness - firefly["brightness"]) * 0.1  # Smooth transition
                    brightness = firefly["brightness"]
                    
                    # Determine color based on brightness (black to yellow)
                    if self.synchronized:
                        brightness = 1.0  # Lock to full brightness when synchronized
                    color = f'#{int(brightness * 255):02x}{int(brightness * 255):02x}00'  # Black to yellow
                    self.canvas.itemconfig(firefly["rect"], fill=color)
            self.canvas.update()
            time.sleep(0.05)

    def run(self):
        threading.Thread(target=self.update_firefly_phases, daemon=True).start()
        threading.Thread(target=self.update_canvas, daemon=True).start()
        self.root.mainloop()

if __name__ == "__main__":
    visualizer = FireflyVisualizer(GRID_SIZE, FIREFLY_PORTS)
    visualizer.run()
