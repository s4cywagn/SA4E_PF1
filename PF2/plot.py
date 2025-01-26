#!/usr/bin/env python3

import matplotlib.pyplot as plt

def main():
    # Replace commas with dots in your data where needed and ensure numbers are floats.
    # Here’s the data from your table (converted to floating-point with dots):
    requests = [
        159, 264, 462, 854, 1678, 3526, 7981, 19601, 52664,
        156194.3162, 516454.1231, 1924575.371, 8180284.652,
        40183268.36, 231446055.5, 1.588161859e9
    ]
    durations = [
        0.73703742, 0.399532318, 0.448467731, 0.780230284, 1.438035488,
        2.593583584, 7.023740292, 17.60385537, 60.15636849,
        162.4618598, 537.1776602, 2001.801997, 8508.53149,
        41795.68546, 240733.1939, 1651889.362
    ]

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot as line with markers
    ax.plot(requests, durations, marker='o', linestyle='-', color='blue', label='Requests vs. Duration')

    # Label axes
    ax.set_xlabel("Requests")
    ax.set_ylabel("Duration (s)")
    ax.set_title("Requests vs Duration")

    # Optional: if data spans wide ranges, you might use a log scale
    # ax.set_xscale('log')
    # ax.set_yscale('log')

    ax.grid(True)
    ax.legend()

    # Save as PNG
    plt.savefig("requests_vs_duration.png", dpi=150, bbox_inches='tight')
    print("Chart saved to 'requests_vs_duration.png'.")

    # Show plot interactively (uncomment if you want a pop-up window)
    # plt.show()

if __name__ == "__main__":
    main()
