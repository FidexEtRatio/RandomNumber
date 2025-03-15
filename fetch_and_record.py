import requests
from io import BytesIO
from pyradios import RadioBrowser
from system_entropy import get_hardware_seed  # Import the custom random number generator
import httpcore  # For handling specific timeout exceptions

def deterministic_shuffle(stations):
    # Generate a "random-like" seed
    seed = get_hardware_seed()
    
    # Use the seed to create a deterministic sorting key for each station
    shuffled_stations = sorted(stations, key=lambda s: (seed + hash(s['name'])) % len(stations))
    return shuffled_stations

import requests

def fetch_radio_stations():
    rb = RadioBrowser()  # Initialize the RadioBrowser client
    try:
        # Fetch stations using the RadioBrowser API
        stations = rb.search(limit=50)  # Fetch up to 50 stations
        if stations:
            # Shuffle stations deterministically before returning
            shuffled_stations = deterministic_shuffle(stations)
            print(f"Found #{len(shuffled_stations)} stations. Verifying URLs...")

            valid_stations = []  # List to store stations with valid URLs
            for station in shuffled_stations:
                try:
                    # Verify the URL of each station
                    response = requests.head(station['url_resolved'], timeout=5)  # Use HEAD for quick check
                    response.raise_for_status()  # Raise exception for invalid status codes
                    print(f"URL verified: {station['url_resolved']}")
                    valid_stations.append(station)  # Add valid station to the list
                except Exception as e:
                    # Log and skip any station with an invalid or unreachable URL
                    print(f"Skipping station due to URL error: {e}. Moving to the next one.")

            if valid_stations:
                return valid_stations  # Return the list of valid stations
            else:
                print("No valid stations found after URL verification.")
                return []
        else:
            print("No stations found.")
            return []
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (e.g., 502 Bad Gateway)
        print(f"HTTP error while fetching stations: {e}")
        return []
    except Exception as e:
        # Handle unexpected errors
        print(f"An unexpected error occurred while fetching stations: {e}")
        return []

def verify_url(stream_url):
    try:
        response = requests.head(stream_url, timeout=5)  # Use a HEAD request for quick verification
        response.raise_for_status()  # Raise an error for HTTP response codes >= 400
        return True
    except requests.exceptions.RequestException as e:
        return False

# Record audio from the stream
def record_stream(stream_url, duration=5):
    if not verify_url(stream_url):
        print("Skipping this station due to verification failure.")
        return None

    try:
        response = requests.get(stream_url, stream=True, timeout=20)  # Increased timeout for slower stations
        response.raise_for_status()
        audio_data = BytesIO()
        for chunk in response.iter_content(chunk_size=1024):
            audio_data.write(chunk)
            if audio_data.tell() >= duration * 44100 * 2:  # Approx. 5 seconds of audio
                break
        return audio_data
    except httpcore.ReadTimeout:
        print(f"Stream timed out for URL: {stream_url}. Moving to the next station...")
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
