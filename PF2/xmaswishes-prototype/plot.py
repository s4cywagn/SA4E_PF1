#!/usr/bin/env python3

import matplotlib.pyplot as plt

def main():
    # Data (using dots, no commas for thousands or decimals)
    requests = [
        159, 264, 462, 854, 1678, 3526, 7981,
        19601, 52664, 156195, 516457, 1924587.164,
        8180339.79, 40183566.3, 231447943.2, 1588176107
    ]
    durations = [
        0.081045866, 0.099644184, 0.140738726, 0.228533268, 0.516710281,
        0.820467234, 4.735725164, 8.982017517, 21.32693028, 50.39159656,
        154.3340766, 662.4313195, 2815.623725, 13830.94169, 79662.98915, 546640.6583
    ]
    
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Plot the data; marker='o' for circular points, linestyle='-' for a line
    ax.plot(requests, durations, marker='o', linestyle='-', color='blue', label='Requests vs Duration')
    
    # Optional: if the data spans large ranges, uncomment these lines:
    # ax.set_xscale('log')
    # ax.set_yscale('log')
    
    # Label the axes
    ax.set_xlabel("Requests")
    ax.set_ylabel("Duration (s)")
    ax.set_title("Requests vs. Duration")
    ax.legend(loc="upper left")
    
    # You can manually set x/y limits or ticks if desired, e.g.:
    # ax.set_xlim(0, 2e9)
    # ax.set_ylim(0, 6e5)
    # ax.set_xticks([1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9])
    # ax.set_yticks([1e-1, 1e0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6])
    
    ax.grid(True, which='both', linestyle='--', alpha=0.5)
    
    # Save the figure as a PNG file
    plt.savefig("requests_vs_duration.png", dpi=150, bbox_inches='tight')
    print("Chart saved as 'requests_vs_duration.png'.")
    
    # If you want to show the plot interactively, uncomment:
    # plt.show()

if __name__ == "__main__":
    main()
