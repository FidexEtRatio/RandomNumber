from fetch_and_record import fetch_radio_stations, record_stream, knuth_hash
from audio_entropy import calculate_entropy
from concurrent.futures import ThreadPoolExecutor
from system_entropy import get_hardware_seed

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


# Get valid station and audio
def get_valid_station():
    for _ in range(5):  # Try up to 5 times
        station, entropy = pick_random_station()
        if not station:
            print("❌ No valid station found.")
            continue

        print(f"🎵 Trying to record from station: {station['name']} ({station['url_resolved']})")
        audio_data = record_stream(station['url_resolved'], duration=5)

        if audio_data:
            print(f"✅ Successfully recorded audio from {station['name']}")
            return audio_data.getvalue(), entropy, station  
        else:
            print(f"⚠️ Failed to record from {station['name']} ({station['url_resolved']})")

    print("❌ All attempts to record audio failed.")
    return None, 0, None  


# Generate a high-entropy seed
def get_data_for_seed():

    all_stations = fetch_radio_stations()
    if len(all_stations) < 2:
        return b"fallback_seed_value"

    # Fetch two streams in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: get_valid_station(), range(2)))

    audio1, _ , _ = results[0]
    audio2, _ , _ = results[1]

    if not audio1 or not audio2:
        return b"fallback_seed_value"

    # Step 1: Combine two streams using XOR
    combined_data = combine_audio_streams(audio1, audio2)
    return combined_data