import numpy as np
from math import log2
from fetch_and_record import fetch_radio_stations, record_stream

# Calculate Shannon Entropy from byte data
def calculate_entropy(audio_bytes):
    # Convert bytes into integer data
    byte_array = np.frombuffer(audio_bytes, dtype=np.uint8)
    frequencies = np.bincount(byte_array)  # Count occurrences of each byte
    probabilities = frequencies / len(byte_array)  # Normalize to probabilities
    return -sum(p * log2(p) for p in probabilities if p > 0)