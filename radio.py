from fetch_and_record import fetch_radio_stations, record_stream
from audio_entropy import calculate_entropy
import hashlib

def combine_audio_streams(audio1_bytes, audio2_bytes):
    # Ensure both byte arrays are the same length by truncating or padding
    min_length = min(len(audio1_bytes), len(audio2_bytes))
    combined_bytes = bytes([b1 ^ b2 for b1, b2 in zip(audio1_bytes[:min_length], audio2_bytes[:min_length])])
    return combined_bytes

def apply_sha3_512(data):
    # Hash the data using SHA3-512
    sha3_hash = hashlib.sha3_512(data).hexdigest()
    return sha3_hash

def get_sys_entropy_and_radio_seed():
    min_entropy_threshold = 7.90  # Set the minimum acceptable entropy value

    # Step 1: Fetch and shuffle radio stations once
    all_stations = fetch_radio_stations()
    if not all_stations or len(all_stations) < 2:
        print("Not enough stations available to proceed.")
        return

    # Step 2: Validate and record audio streams
    audio_data_list = []
    for i, station in enumerate(all_stations, start=1):
        while True:  # Keep trying for a valid stream with sufficient entropy
            print(f"\n--- Recording {i}: {station['name']} ---")
            stream_url = station['url_resolved']

            audio_data = record_stream(stream_url, duration=5)
            if not audio_data:
                print(f"Failed to record audio from {station['name']}. Trying next station...")
                break  # Move to the next station if recording fails

            print(f"Audio recorded successfully from {station['name']}.")
            audio_bytes = audio_data.getvalue()

            # Calculate entropy
            entropy = calculate_entropy(audio_bytes)
            print(f"Shannon Entropy of the audio from {station['name']}: {entropy}")

            if entropy >= min_entropy_threshold:
                audio_data_list.append(audio_bytes)
                break  # Exit loop when entropy is acceptable
            else:
                print(f"Entropy too low ({entropy}). Moving to next station...")
                break  # Move to the next station if entropy is too low

        # Stop early if we already have two valid streams
        if len(audio_data_list) == 2:
            break

    # Fallback: Use the last available stations if two high-entropy streams are not found
    if len(audio_data_list) < 2:
        print("Could not find two high-entropy streams. Using available streams.")
        # Fill with what you have, even if entropy is below the threshold
        for station in all_stations[len(audio_data_list):2]:  # Take remaining stations if available
            print(f"\n--- Using fallback station: {station['name']} ---")
            stream_url = station['url_resolved']
            audio_data = record_stream(stream_url, duration=5)
            if audio_data:
                audio_data_list.append(audio_data.getvalue())
            if len(audio_data_list) == 2:
                break

    if len(audio_data_list) < 2:
        print("Failed to obtain two valid audio streams.")
        return

    # Step 3: Combine the two audio streams
    combined_data = combine_audio_streams(audio_data_list[0], audio_data_list[1])
    combined_entropy = calculate_entropy(combined_data)
    print(f"Shannon Entropy of the combined audio streams: {combined_entropy}")

    # Step 4: Apply SHA3-512 Hash
    hash_result = apply_sha3_512(combined_data)
    print(f"SHA3-512 Hash of the combined audio streams: {hash_result}")
    return hash_result