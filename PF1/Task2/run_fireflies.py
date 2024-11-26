import os
import subprocess

# Define a grid of fireflies with neighbors
GRID_SIZE = 5
BASE_PORT = 5000

# Generate neighbor mapping
fireflies = {}
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        port = BASE_PORT + x * GRID_SIZE + y
        neighbors = [
            BASE_PORT + ((x - 1) % GRID_SIZE) * GRID_SIZE + y,  # Top
            BASE_PORT + ((x + 1) % GRID_SIZE) * GRID_SIZE + y,  # Bottom
            BASE_PORT + x * GRID_SIZE + (y - 1) % GRID_SIZE,    # Left
            BASE_PORT + x * GRID_SIZE + (y + 1) % GRID_SIZE     # Right
        ]
        fireflies[port] = neighbors

# Launch firefly servers
processes = []
for port, neighbors in fireflies.items():
    neighbors_str = ','.join(map(str, neighbors))
    process = subprocess.Popen(
        ['python', 'firefly_server.py', str(port), neighbors_str]
    )
    processes.append(process)

# Wait for all processes to finish
while True:
    try:
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
