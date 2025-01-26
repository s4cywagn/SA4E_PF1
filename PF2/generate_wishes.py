#!/usr/bin/env python3
import os

OUTPUT_DIR = "data/scanned-letters"
NUM_LETTERS = 10000

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for i in range(NUM_LETTERS):
        file_name = f"letter_{i+1}.txt"
        file_path = os.path.join(OUTPUT_DIR, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            # A simple sample text (could be from an OCR step)
            f.write(f"Hello Santa, I am letter number {i+1} and I want a gift!\n")
    print(f"Created {NUM_LETTERS} letters in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
