from fetch_and_record import fetch_radio_stations, record_stream, pick_random_station
from audio_entropy import calculate_entropy
import hashlib
from concurrent.futures import ThreadPoolExecutor

def combine_audio_streams(audio1_bytes, audio2_bytes):
    """XOR two audio byte arrays for entropy mixing."""
    min_length = min(len(audio1_bytes), len(audio2_bytes))
    return bytes(b1 ^ b2 for b1, b2 in zip(audio1_bytes[:min_length], audio2_bytes[:min_length]))

def apply_sha3_512(data):
    """Apply SHA3-512 hash to the data."""
    return hashlib.sha3_512(data).digest()  # Return raw bytes instead of hex

def get_valid_station():
    """Try multiple stations until one works."""
    for _ in range(5):  # Try up to 5 different stations
        station, entropy = pick_random_station()
        if not station:
            continue
        print(f"Trying station: {station['name']} -> {station['url_resolved']}")

        audio_data = record_stream(station['url_resolved'], duration=5)
        if audio_data:
            return audio_data.getvalue(), entropy, station  # Return valid audio + entropy + station info
        print(f"Station {station['name']} failed. Trying another...")

    print("All attempts to fetch a valid station failed.")
    return None, 0, None  # No valid station found

def get_seed():
    """Generate a seed from two different radio streams."""
    min_entropy_threshold = 7.90  # Set minimum entropy value

    # Step 1: Fetch valid stations
    all_stations = fetch_radio_stations()
    if len(all_stations) < 2:
        print("Not enough stations available. Using fallback seed.")
        return b"fallback_seed_value"

    # Step 2: Find two working streams
    audio1, entropy1, station1 = get_valid_station()
    audio2, entropy2, station2 = get_valid_station()

    if not audio1 or not audio2:
        print("Failed to obtain two valid audio streams. Using fallback seed.")
        return b"fallback_seed_value"

    print("✅ Successfully retrieved two valid audio streams!")

    # Step 3: Combine audio and check entropy
    combined_data = combine_audio_streams(audio1, audio2)
    combined_entropy = calculate_entropy(combined_data)

    print(f"🔹 Combined entropy: {combined_entropy}")
    if combined_entropy < min_entropy_threshold:
        print("⚠️ Warning: Low entropy detected! Using fallback seed.")
        return b"fallback_seed_value"

    # Step 4: Print the final two selected stations
    print("\n🎵 Final selected stations for entropy:")
    print(f"📡 Station 1: {station1['name']} -> {station1['url_resolved']}")
    print(f"📡 Station 2: {station2['name']} -> {station2['url_resolved']}")

    # Step 5: Return secure SHA3-512 hash
    return apply_sha3_512(combined_data)
