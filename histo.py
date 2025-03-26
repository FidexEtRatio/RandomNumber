import struct
import matplotlib.pyplot as plt
import numpy as np

# Replace 'data.bin' with your actual file path
file_path = 'data.bin'

# Read the binary file and extract 2-byte numbers
numbers = []
with open(file_path, 'rb') as f:
    while True:
        data = f.read(2)  # Read 2 bytes at a time
        if not data:
            break
        number = struct.unpack('<H', data)[0]  # '<H' for little-endian unsigned short (2 bytes)
        numbers.append(number)

# Plot the histogram
plt.figure(figsize=(10, 5))
plt.hist(numbers, bins=50, edgecolor='black', alpha=0.75)
plt.xlabel('Number Value')
plt.ylabel('Frequency')
plt.title('Distribution of 2-Byte Numbers in Binary File')
plt.grid(True)
plt.show()
