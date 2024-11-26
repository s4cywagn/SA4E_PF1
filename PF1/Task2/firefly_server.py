import grpc
import time
import math
import threading
from concurrent import futures
import sys
import threading
import random
from firefly_pb2 import PhaseMessage, AckMessage, Empty
import firefly_pb2_grpc

# Parameters
SYNC_RATE = 0.1
CYCLE_TIME = 2.0

class Firefly(firefly_pb2_grpc.FireflyServicer):
    def __init__(self, port, neighbors):
        self.phase = random.uniform(0, 2 * math.pi)  # Random initial phase
        self.neighbors = neighbors
        self.port = port
        self.running = True

    def SendPhase(self, request, context):
        # Update phase based on received phase
        self.phase += SYNC_RATE * math.sin(request.phase - self.phase)
        self.phase %= 2 * math.pi
        return AckMessage(status="Phase updated")

    def RequestPhase(self, request, context):
        # Return the current phase
        return PhaseMessage(phase=self.phase)

    def run_server(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        firefly_pb2_grpc.add_FireflyServicer_to_server(self, server)
        server.add_insecure_port(f'[::]:{self.port}')
        server.start()
        print(f"Firefly server running on port {self.port}")
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop(0)

    def communicate_with_neighbors(self):
        # Communicate periodically with neighbors to synchronize
        while self.running:
            for neighbor_port in self.neighbors:
                try:
                    with grpc.insecure_channel(f'localhost:{neighbor_port}') as channel:
                        stub = firefly_pb2_grpc.FireflyStub(channel)
                        phase_message = stub.RequestPhase(Empty())
                        self.SendPhase(phase_message, None)
                except grpc.RpcError:
                    pass  # Handle neighbors not being available
            time.sleep(0.05)  # Delay for periodic communication


if __name__ == "__main__":
    port = int(sys.argv[1])
    neighbors = list(map(int, sys.argv[2].split(',')))

    firefly = Firefly(port, neighbors)

    # Run server and communication threads
    server_thread = threading.Thread(target=firefly.run_server)
    communication_thread = threading.Thread(target=firefly.communicate_with_neighbors)

    server_thread.start()
    communication_thread.start()

    server_thread.join()
    communication_thread.join()