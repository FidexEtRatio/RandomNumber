import numpy as np
from scipy.stats import entropy, chisquare, pearsonr
import zlib
import os
import sys

def read_bytes(file_path):
    with open(file_path, 'rb') as f:
        return np.frombuffer(f.read(), dtype=np.uint8)

def hamming_distance(arr1, arr2):
    return np.sum(arr1 != arr2)

def calc_entropy(data):
    counts = np.bincount(data, minlength=256)
    probs = counts / np.sum(counts)
    return entropy(probs, base=2)

def compress_ratio(data):
    original_size = len(data)
    compressed = zlib.compress(data.tobytes())
    return len(compressed) / original_size

def compare_files(file1, file2):
    data1 = read_bytes(file1)
    data2 = read_bytes(file2)
    min_len = min(len(data1), len(data2))
    data1 = data1[:min_len]
    data2 = data2[:min_len]

    print(f"Hamming Distance: {hamming_distance(data1, data2)} / {min_len}")
    print(f"Entropy File 1: {calc_entropy(data1):.4f}")
    print(f"Entropy File 2: {calc_entropy(data2):.4f}")
    print(f"Compression Ratio File 1: {compress_ratio(data1):.4f}")
    print(f"Compression Ratio File 2: {compress_ratio(data2):.4f}")

    correlation, _ = pearsonr(data1, data2)
    print(f"Pearson Correlation: {correlation:.4f}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python histo.py <file1> <file2>")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    if not os.path.exists(file1):
        print(f"Error: {file1} not found.")
        sys.exit(1)

    if not os.path.exists(file2):
        print(f"Error: {file2} not found.")
        sys.exit(1)

    compare_files(file1, file2)

if __name__ == "__main__":
    main()
