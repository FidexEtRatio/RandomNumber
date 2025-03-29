from fetch_and_record import fetch_radio_stations, record_stream, knuth_hash
from audio_entropy import calculate_entropy
import hashlib
from concurrent.futures import ThreadPoolExecutor
from system_entropy import get_hardware_seed

# DJB2 Hash Function (Bernstein)
def bernstein_djb2(data):
    hash_val = 5381
    for byte in data:
        hash_val = ((hash_val << 5) + hash_val) + byte  # hash * 33 + byte
    return hash_val & 0xFFFFFFFF  # Keep within 32-bit range

# Pick a radio station using Knuth's hash
def pick_random_station(last_entropy=0):
    stations = fetch_radio_stations()
    if not stations:
        print("No stations available!")
        return None, last_entropy

    seed = get_hardware_seed() + last_entropy
    index = knuth_hash(seed, len(stations))  
    selected_station = stations[index]
    last_entropy = sum(map(ord, selected_station['name'])) % 100  

    print(f"🎵 Selected station: {selected_station['name']} -> {selected_station['url_resolved']}")
    return selected_station, last_entropy

# XOR two audio streams
def combine_audio_streams(audio1_bytes, audio2_bytes):
    min_length = min(len(audio1_bytes), len(audio2_bytes))
    return bytes(b1 ^ b2 for b1, b2 in zip(audio1_bytes[:min_length], audio2_bytes[:min_length]))

# Secure SHA3-512 Hash
def apply_sha3_512(data):
    return hashlib.sha3_512(data).digest()

# Get valid station and audio
def get_valid_station():
    for _ in range(5):  # Try up to 5 times
        station, entropy = pick_random_station()
        if not station:
            continue

        print(f"Trying station: {station['name']}")
        audio_data = record_stream(station['url_resolved'], duration=5)
        if audio_data:
            return audio_data.getvalue(), entropy, station  

    return None, 0, None  

# Extract high-entropy segments using a sliding window
def extract_entropy_with_sliding_window(data, window_size=256, stride=64, min_entropy=7.9):
    high_entropy_sections = []
    
    for start in range(0, len(data) - window_size + 1, stride):
        window = data[start:start + window_size]
        entropy = calculate_entropy(window)
        if entropy >= min_entropy:
            high_entropy_sections.append(window)
            print(f"Window starting at {start}: Entropy = {entropy}")
    
    return high_entropy_sections


# Aggregate entropy segments into a single data blob
def aggregate_entropy_segments(segments):
    return b"".join(segments)


# Generate a high-entropy seed
def get_seeds(num_seeds=5, min_entropy_threshold=7.90):
    """
    Generate multiple high-entropy seeds.
    """
    all_stations = fetch_radio_stations()
    if len(all_stations) < 2:
        return [b"fallback_seed_value"] * num_seeds

    # Collect seeds
    seeds = []
    while len(seeds) < num_seeds:
        # Fetch two streams in parallel
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(lambda _: get_valid_station(), range(2)))

        audio1, entropy1, station1 = results[0]
        audio2, entropy2, station2 = results[1]

        if not audio1 or not audio2:
            seeds.append(b"fallback_seed_value")
            continue

        # Step 1: Combine two streams using XOR
        combined_data = combine_audio_streams(audio1, audio2)

        # Step 2: Extract multiple high-entropy portions
        high_entropy_segments = extract_entropy_with_sliding_window(combined_data, min_entropy=min_entropy_threshold)
        if not high_entropy_segments:
            seeds.append(b"fallback_seed_value")
            continue

        # Step 3: Aggregate high-entropy segments
        aggregated_data = aggregate_entropy_segments(high_entropy_segments)

        # Step 4: Rotate bits for better dispersion
        def rotate_left(byte, shift):
            return ((byte << shift) | (byte >> (8 - shift))) & 0xFF

        modified_data = bytearray(aggregated_data)
        for i in range(len(modified_data)):
            modified_data[i] = rotate_left(modified_data[i], (i % 7) + 1)

        # Step 5: XOR with hardware entropy
        for i in range(len(modified_data)):
            modified_data[i] ^= (get_hardware_seed() >> (i % 8)) & 0xFF

        # Step 6: Measure entropy before hashing
        final_entropy = calculate_entropy(modified_data)
        print(f"🔹 Final Entropy before SHA3-512: {final_entropy}")

        # Step 7: Apply SHA3-512 for final randomness
        hashed_seed = apply_sha3_512(modified_data)

        # Step 8: Measure entropy after hashing
        post_hash_entropy = calculate_entropy(hashed_seed)
        print(f"🔹 Entropy after SHA3-512: {post_hash_entropy}")

        # Add to seeds list
        seeds.append(hashed_seed)

    return seeds