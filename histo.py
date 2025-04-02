import struct
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def gen_histo(file_path):

# Read the binary file and extract 2-byte numbers
    numbers = []
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(2)  # Read 2 bytes at a time
            if not data:
                break
            number = struct.unpack('<H', data)[0]  # '<H' for little-endian unsigned short (2 bytes)
            numbers.append(number)

    total_nums = len(numbers)

    # Plot the histogram
    plt.figure(figsize=(10, 5))
    plt.hist(numbers, bins=50, edgecolor='black', alpha=0.75)
    plt.xlabel('Number Value')
    plt.ylabel('Frequency')
    plt.title('Distribution of 2-Byte Numbers in Binary File')
    plt.grid(True)
    plt.text(
        1, 1, f'Total Numbers: {total_nums}', 
        transform=plt.gca().transAxes, 
        fontsize=12, color='black', 
        verticalalignment='top', horizontalalignment='right'
    )
    plt.savefig(file_path + ".png")

def main():
    if len(sys.argv) != 2:
        print("Usage: python randomness_tester.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print("Error: File not found.")
        sys.exit(1)
    
    gen_histo(file_path)

if __name__ == "__main__":
    main()