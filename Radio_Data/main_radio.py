from fetch_and_record import fetch_radio_station, record_stream
from transform_calculate_entropy import calculate_entropy

def main():
    # Step 1: Fetch the radio stream URL
    stream_url = fetch_radio_station()
    if not stream_url:
        print("Failed to fetch a valid radio stream URL. Exiting program.")
        return

    print(f"Using stream URL: {stream_url}")
    
    # Step 2: Record audio from the stream
    audio_data = record_stream(stream_url, duration=5)
    if not audio_data:
        print("Failed to record audio from the stream. Exiting program.")
        return

    print("Audio recorded successfully.")
    
    # Step 3: Calculate Shannon Entropy from the audio data
    audio_bytes = audio_data.getvalue()
    entropy = calculate_entropy(audio_bytes)
    print(f"Shannon Entropy of the audio: {entropy}")

if __name__ == "__main__":
    main()
