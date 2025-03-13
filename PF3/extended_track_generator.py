#!/usr/bin/env python3
import sys
import json
import random

def generate_tracks(num_tracks: int,
                    length_of_track: int,
                    caesar_indices=None,
                    bottleneck_indices=None,
                    allow_splits=False,
                    max_splits=2):
    """
    Erzeugt eine Datenstruktur mit 'num_tracks' Rennbahnen, die jeweils 'length_of_track'
    Segmente enthalten. Neben den bisherigen Segmenttypen werden auch 'caesar' und 'bottleneck'
    unterstützt. Außerdem lässt sich optional aktivieren, dass Segmente sich auf mehrere
    Folgesegmente aufspalten können (allow_splits=True).
    
    :param num_tracks: Anzahl der Rennbahnen (z.B. 1, 2, 3, ...)
    :param length_of_track: Anzahl der Segmente pro Bahn
    :param caesar_indices: Liste von Segmentpositionen, an denen ein 'caesar'-Segment eingefügt werden soll
    :param bottleneck_indices: Liste von Segmentpositionen, an denen ein 'bottleneck'-Segment eingefügt werden soll
    :param allow_splits: Falls True, können manche Segmente mehrere nextSegments besitzen
    :param max_splits: Bis zu wie viele verschiedene nächste Segmente ein Segment im Split-Fall haben kann
    :return: Ein Dictionary, das in JSON serialisiert werden kann
    """
    if caesar_indices is None:
        caesar_indices = []
    if bottleneck_indices is None:
        bottleneck_indices = []

    all_tracks = []

    for t in range(1, num_tracks + 1):
        track_id = str(t)
        segments = []

        # 1) Startsegment anlegen
        start_segment_id = f"start-and-goal-{t}"
        if length_of_track == 1:
            # Spezialfall: nur 1 Segment => es verweist auf sich selbst
            next_segments = [start_segment_id]
        else:
            next_segments = [f"segment-{t}-1"]

        start_segment = {
            "segmentId": start_segment_id,
            "type": "start-goal",
            "nextSegments": next_segments
        }
        segments.append(start_segment)

        # 2) Normale Segmente + ggf. Caesar- / Bottleneck-Segmente
        for c in range(1, length_of_track):
            seg_id = f"segment-{t}-{c}"

            # Letztes Segment verweist zurück auf 'start-and-goal-t'
            # (geschlossene Kreisbahn)
            if c == length_of_track - 1:
                base_next = [start_segment_id]
            else:
                # Standard: verweise auf das nächste Segment
                base_next = [f"segment-{t}-{c + 1}"]

            # Falls allow_splits=True, fügen wir evtl. weitere Next-Segments hinzu
            if allow_splits and c < length_of_track - 1:
                # Beispiel: mit gewisser Wahrscheinlichkeit Split generieren
                if random.random() < 0.3:  # 30% Chance auf eine Aufspaltung
                    # Maximal 'max_splits' mögliche Ziele (z.B. 2)
                    num_possible_next = random.randint(2, max_splits)
                    extra_next = []
                    for _ in range(num_possible_next):
                        # Wähle zufällig ein Segment, das noch vor dem letzten liegt
                        next_index = random.randint(c + 1, length_of_track - 1)
                        next_seg_id = f"segment-{t}-{next_index}"
                        # Vermeide Duplikate
                        if next_seg_id not in extra_next:
                            extra_next.append(next_seg_id)
                    # Kombiniere mit dem Basis-Nachfolger
                    base_next = list(set(base_next + extra_next))

            # Segmenttyp bestimmen:
            # - falls c in caesar_indices => type='caesar'
            # - falls c in bottleneck_indices => type='bottleneck'
            # - sonst => type='normal'
            if c in caesar_indices:
                seg_type = "caesar"
            elif c in bottleneck_indices:
                seg_type = "bottleneck"
            else:
                seg_type = "normal"

            segment = {
                "segmentId": seg_id,
                "type": seg_type,
                "nextSegments": base_next
            }

            # Beispiel für weitere Eigenschaften, z.B. Wartezeit bei bottleneck
            if seg_type == "bottleneck":
                # Füge ein zufälliges Delay-Feld hinzu
                segment["delayRangeMs"] = [200, 1000]  # 200-1000 ms, Beispiel

            segments.append(segment)

        track_definition = {
            "trackId": track_id,
            "segments": segments
        }
        all_tracks.append(track_definition)

    return {"tracks": all_tracks}


def main():
    """
    Usage:
      ./extended_track_generator.py <num_tracks> <length_of_track> <output_file>
      [--caesar "1,5,10"] [--bottleneck "2,3"] [--splits]

    Beispiel:
      ./extended_track_generator.py 2 12 tracks.json --caesar 3,7 --bottleneck 5 --splits

    Erzeugt 2 Tracks mit jeweils 12 Segmenten. In jedem Track sind:
      - Segment 3 und 7 vom Typ 'caesar'
      - Segment 5 vom Typ 'bottleneck'
      - Mit 30% Chance Aufspaltungen an zufälligen Positionen
    """
    # Standard-Parameter parsen
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <num_tracks> <length_of_track> <output_file> [--caesar \"x,y\"] [--bottleneck \"a,b\"] [--splits]")
        sys.exit(1)

    num_tracks = int(sys.argv[1])
    length_of_track = int(sys.argv[2])
    output_file = sys.argv[3]

    # Defaults
    caesar_indices = []
    bottleneck_indices = []
    allow_splits = False

    # Zusätzliche Argumente verarbeiten
    extra_args = sys.argv[4:]
    i = 0
    while i < len(extra_args):
        arg = extra_args[i]
        if arg == "--caesar" and i + 1 < len(extra_args):
            caesar_indices = [int(x.strip()) for x in extra_args[i+1].split(",") if x.strip().isdigit()]
            i += 2
        elif arg == "--bottleneck" and i + 1 < len(extra_args):
            bottleneck_indices = [int(x.strip()) for x in extra_args[i+1].split(",") if x.strip().isdigit()]
            i += 2
        elif arg == "--splits":
            allow_splits = True
            i += 1
        else:
            i += 1

    tracks_data = generate_tracks(num_tracks,
                                  length_of_track,
                                  caesar_indices=caesar_indices,
                                  bottleneck_indices=bottleneck_indices,
                                  allow_splits=allow_splits,
                                  max_splits=2)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(tracks_data, f, indent=2)
        f.write('\n')
    print(f"Successfully generated {num_tracks} track(s) of length {length_of_track} into '{output_file}'")
    print(f"  Caesar segments: {caesar_indices}")
    print(f"  Bottleneck segments: {bottleneck_indices}")
    print(f"  Splits enabled: {allow_splits}")

if __name__ == "__main__":
    main()
