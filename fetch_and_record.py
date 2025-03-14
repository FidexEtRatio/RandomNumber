import requests
from io import BytesIO
from pyradios import RadioBrowser
from GRN_for_radio import generate_random_number  # Import the custom random number generator

def deterministic_shuffle(stations):
    # Generate a "random-like" seed
    seed = generate_random_number()
    
    # Use the seed to create a deterministic sorting key for each station
    shuffled_stations = sorted(stations, key=lambda s: (seed + hash(s['name'])) % len(stations))
    return shuffled_stations

def fetch_radio_stations():
    rb = RadioBrowser()
    stations = rb.search(limit=20)  # Fetch more stations for diversity
    if stations:
        # Shuffle stations deterministically or once before returning
        shuffled_stations = deterministic_shuffle(stations)  # Only shuffle once
        print("Shuffled stations:")
        for station in shuffled_stations:
            print(f"{station['name']}: {station['url_resolved']}")
        return shuffled_stations
    else:
        print("No stations found.")
        return []



# Record audio from the stream
def record_stream(stream_url, duration=5):
    try:
        response = requests.get(stream_url, stream=True, timeout=10)  # Timeout after 10 seconds
        response.raise_for_status()
        audio_data = BytesIO()
        for chunk in response.iter_content(chunk_size=1024):
            audio_data.write(chunk)
            if audio_data.tell() >= duration * 44100 * 2:  # Approx. 5 seconds of audio
                break
        return audio_data
    except Exception as e:
        print(f"Error recording stream: {e}")
    return None


# Example usage of the new random generator
def pick_random_station():
    stations = fetch_radio_stations()
    if stations:
        random_index = generate_random_number() % len(stations)  # Use custom random number generator
        selected_station = stations[random_index]
        print(f"Selected station: {selected_station['name']}: {selected_station['url_resolved']}")
        return selected_station
    else:
        print("No stations available to pick from.")
        return None
