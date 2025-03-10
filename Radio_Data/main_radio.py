from fetch_and_record import fetch_two_working_radios, record_stream
from transform_calculate_entropy import calculate_entropy
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

def main():
    # Step 1: Fetch two working radio stations
    working_stations = fetch_two_working_radios()
    if len(working_stations) < 2:
        print("Not enough working radios to proceed.")
        return

    # Step 2: Record audio from the two stations
    audio_data_list = []
    for i, station in enumerate(working_stations, start=1):
        print(f"\n--- Recording {i}: {station['name']} ---")
        stream_url = station['url_resolved']

        audio_data = record_stream(stream_url, duration=5)
        if not audio_data:
            print(f"Failed to record audio from {station['name']}.")
            continue

        print(f"Audio recorded successfully from {station['name']}.")
        audio_data_list.append(audio_data.getvalue())

        # Calculate entropy for individual streams
        entropy = calculate_entropy(audio_data.getvalue())
        print(f"Shannon Entropy of the audio from {station['name']}: {entropy}")

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

if __name__ == "__main__":
    main()
