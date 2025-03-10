from fetch_and_record import fetch_two_working_radios, record_stream
from transform_calculate_entropy import calculate_entropy

def main():
    # Step 1: Fetch two working radio stations
    working_stations = fetch_two_working_radios()
    if len(working_stations) < 2:
        print("Not enough working radios to proceed.")
        return

    # Step 2: Record audio and calculate Shannon Entropy for each station
    for i, station in enumerate(working_stations, start=1):
        print(f"\n--- Recording {i}: {station['name']} ---")
        stream_url = station['url_resolved']

        # Record audio from the stream
        audio_data = record_stream(stream_url, duration=5)
        if not audio_data:
            print(f"Failed to record audio from {station['name']}.")
            continue

        print(f"Audio recorded successfully from {station['name']}.")

        # Calculate Shannon Entropy
        audio_bytes = audio_data.getvalue()
        entropy = calculate_entropy(audio_bytes)
        print(f"Shannon Entropy of the audio from {station['name']}: {entropy}")

if __name__ == "__main__":
    main()
