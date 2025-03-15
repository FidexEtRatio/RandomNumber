import requests
from io import BytesIO
from pyradios import RadioBrowser
from system_entropy import get_hardware_seed  # Import the custom random number generator

def deterministic_shuffle(stations):
    # Generate a "random-like" seed
    seed = get_hardware_seed()
    
    # Use the seed to create a deterministic sorting key for each station
    shuffled_stations = sorted(stations, key=lambda s: (seed + hash(s['name'])) % len(stations))
    return shuffled_stations

def fetch_radio_stations():
    rb = RadioBrowser()
    stations = rb.search(limit=50)  # Fetch more stations for diversity
    if stations:
        # Shuffle stations deterministically or once before returning
        shuffled_stations = deterministic_shuffle(stations)  # Only shuffle once
        print(f"Found #{len(shuffled_stations)} stations. Checking entropy for each...")
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
        random_index = get_hardware_seed() % len(stations)  # Use custom random number generator
        selected_station = stations[random_index]
        print(f"Selected station: {selected_station['name']}: {selected_station['url_resolved']}")
        return selected_station
    else:
        print("No stations available to pick from.")
        return None
