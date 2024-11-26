import tkinter as tk
import threading
import time
import math
import random

# Parameter der Simulation
GRID_SIZE = 10  # 10x10 Gitter
SYNC_RATE = 0.1  # Einflussrate für die Synchronisation
CYCLE_TIME = 2.0  # Grundzykluszeit (in Sekunden)

class Firefly:
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.phase = random.uniform(0, 2 * math.pi)  # Zufällige Anfangsphase
        self.canvas = canvas
        self.rectangle = None
        self.neighbors = []
        self.running = True

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def update_phase(self):
        while self.running:
            # Phase entsprechend der Nachbarschaft und dem Kuramoto-Modell aktualisieren
            sync_effect = sum(math.sin(neighbor.phase - self.phase) for neighbor in self.neighbors)
            self.phase += SYNC_RATE * sync_effect
            self.phase %= 2 * math.pi  # Phase im Bereich [0, 2π] halten
            
            # Helligkeit basierend auf der Phase berechnen (sinusförmig für Aufleuchten)
            brightness = (1 + math.sin(self.phase)) / 2
            color = f'#{int(brightness * 255):02x}{int(brightness * 255):02x}00'
            
            # Rechteck im Canvas aktualisieren
            self.canvas.itemconfig(self.rectangle, fill=color)
            time.sleep(0.05)  # Kurze Pause für realistischere Animation

    def stop(self):
        self.running = False

class FireflySimulation:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.root = tk.Tk()
        self.root.title("Firefly Synchronization")
        self.canvas = tk.Canvas(self.root, width=grid_size*30, height=grid_size*30)
        self.canvas.pack()
        self.fireflies = []

        self.create_fireflies()
        self.connect_neighbors()

    def create_fireflies(self):
        for x in range(self.grid_size):
            row = []
            for y in range(self.grid_size):
                firefly = Firefly(x, y, self.canvas)
                rect = self.canvas.create_rectangle(
                    x * 30, y * 30, (x + 1) * 30, (y + 1) * 30, fill='black'
                )
                firefly.rectangle = rect
                row.append(firefly)
            self.fireflies.append(row)

    def connect_neighbors(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                firefly = self.fireflies[x][y]
                # Nachbarn in der Torus-Struktur finden (oben, unten, links, rechts)
                neighbors = [
                    self.fireflies[(x-1) % self.grid_size][y],  # oben
                    self.fireflies[(x+1) % self.grid_size][y],  # unten
                    self.fireflies[x][(y-1) % self.grid_size],  # links
                    self.fireflies[x][(y+1) % self.grid_size]   # rechts
                ]
                for neighbor in neighbors:
                    firefly.add_neighbor(neighbor)

    def start_simulation(self):
        # Threads für alle Glühwürmchen starten
        for row in self.fireflies:
            for firefly in row:
                threading.Thread(target=firefly.update_phase).start()

    def stop_simulation(self):
        for row in self.fireflies:
            for firefly in row:
                firefly.stop()

    def run(self):
        try:
            self.start_simulation()
            self.root.mainloop()
        finally:
            self.stop_simulation()

# Simulation starten
simulation = FireflySimulation(GRID_SIZE)
simulation.run()
