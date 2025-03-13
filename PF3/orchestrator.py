#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import time
from confluent_kafka import Producer

def start_segment_process(kafka_bootstrap, seg_config):
    """
    Startet einen einzelnen Segment-Prozess (segment.py) mit den nötigen Umgebungsvariablen.
    """
    seg_id = seg_config["segmentId"]
    seg_type = seg_config["type"]
    next_segs = seg_config.get("nextSegments", [])

    env = os.environ.copy()
    env["KAFKA_BOOTSTRAP"] = kafka_bootstrap
    env["SEGMENT_ID"] = seg_id
    env["SEGMENT_TYPE"] = seg_type
    env["NEXT_SEGMENTS"] = json.dumps(next_segs)

    # Starte segment.py als Subprozess (im Hintergrund)
    # Achtung: Pfad anpassen, wo 'segment.py' liegt
    p = subprocess.Popen(["python3", "segment.py"], env=env)
    print(f"Started segment {seg_id} (type={seg_type}) with PID {p.pid}")
    return p

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <tracks.json> <kafka_bootstrap_servers>")
        sys.exit(1)

    tracks_file = sys.argv[1]
    kafka_bootstrap = sys.argv[2]

    # JSON-Datei einlesen
    with open(tracks_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Starte alle Segmente
    processes = []
    for track in data["tracks"]:
        for seg in track["segments"]:
            p = start_segment_process(kafka_bootstrap, seg)
            processes.append(p)

    # Warte etwas, damit alle Consumer/Prozesse laufen
    time.sleep(3)

    # Optional: Sende ein "Start"-Token an alle start-goal-Segmente
    # (In der Praxis könnte man das besser steuern, z.B. nur an track 1 oder so)
    producer = Producer({'bootstrap.servers': kafka_bootstrap})

    for track in data["tracks"]:
        for seg in track["segments"]:
            if seg["type"] == "start-goal":
                seg_id = seg["segmentId"]
                token_value = f"{{'event':'start','segment':'{seg_id}'}}"
                producer.produce(seg_id, value=token_value.encode('utf-8'))
                producer.flush()
                print(f"Sent start token to {seg_id}")

    # Jetzt laufen die Segment-Prozesse im Hintergrund
    # und verschieben die Tokens durch die Topics.
    # In der Praxis: Wir könnten hier warten oder beenden,
    # je nachdem wie deine Logik das Ende erkennt.
    print("All segments are running. Press CTRL+C to stop.")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping all segment processes...")
        for p in processes:
            p.terminate()
        print("Done.")

if __name__ == "__main__":
    main()
