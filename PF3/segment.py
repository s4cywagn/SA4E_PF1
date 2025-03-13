#!/usr/bin/env python3
import os
import time
import json
import random
from confluent_kafka import Consumer, Producer

def create_consumer(kafka_bootstrap_servers, group_id, topic):
    """Erzeugt einen Kafka Consumer, der genau ein Topic abonniert."""
    consumer_conf = {
        'bootstrap.servers': kafka_bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])
    return consumer

def create_producer(kafka_bootstrap_servers):
    """Erzeugt einen Kafka Producer."""
    producer_conf = {
        'bootstrap.servers': kafka_bootstrap_servers
    }
    producer = Producer(producer_conf)
    return producer

def segment_logic(segment_type):
    """
    Diese Funktion kann segment-spezifische Logik abbilden.
    Z.B. Wartezeiten, Caesar-Gruß o.Ä.
    """
    if segment_type == "bottleneck":
        # Beispiel: zufälliges Delay zwischen 0.2 und 1 Sekunde
        delay = random.uniform(0.2, 1.0)
        time.sleep(delay)  
    elif segment_type == "caesar":
        # Beispiel: Log-Ausgabe, oder man trackt, dass Caesar gegrüßt wurde
        print("[INFO] Caesar-Segment betreten. Gruß registriert!")
        # Keine Wartezeit an dieser Stelle, aber das könnte man anpassen
    elif segment_type == "start-goal":
        # Hier könnte man bei Empfang des 'Start' Tokens etwas Besonderes tun
        # oder am 'Ziel' die Zeit nehmen.
        pass
    else:
        # normal-Segment => keine besondere Logik
        pass

def main():
    # Lies die nötigen Parameter z.B. aus Umgebungsvariablen (oder argparse/Datei)
    kafka_bootstrap = os.getenv('KAFKA_BOOTSTRAP', 'localhost:9092')
    segment_id = os.getenv('SEGMENT_ID', 'segment-unknown')
    segment_type = os.getenv('SEGMENT_TYPE', 'normal')
    next_segments_json = os.getenv('NEXT_SEGMENTS', '[]')
    next_segments = json.loads(next_segments_json)  # Liste von Strings

    group_id = f"group_{segment_id}"  # Eindeutige consumer group pro Segment

    consumer = create_consumer(kafka_bootstrap, group_id, topic=segment_id)
    producer = create_producer(kafka_bootstrap)

    print(f"[{segment_id}] started. Type={segment_type}, Next={next_segments}")

    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Warte auf Nachricht
            if msg is None:
                # Keine neue Nachricht
                continue
            if msg.error():
                print(f"[{segment_id}] Consumer error: {msg.error()}")
                continue

            # Wir haben eine Token-Nachricht erhalten
            token_value = msg.value().decode('utf-8')
            print(f"[{segment_id}] received token: {token_value}")

            # Führe segment-spezifische Logik aus (Wartezeit etc.)
            segment_logic(segment_type)

            # Leite Token an alle Next-Segments weiter
            for nxt in next_segments:
                producer.produce(nxt, key=None, value=token_value)
                producer.flush()
                print(f"[{segment_id}] forwarded token to -> {nxt}")

            # Falls es das Zielsegment (start-goal) ist, könnte man hier
            # (wenn z.B. Runden abgeschlossen sind) Messungen vornehmen.
            # => Abhängig von deinem Rennlogik-Design
    except KeyboardInterrupt:
        print(f"[{segment_id}] Shutting down...")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
