import requests
from io import BytesIO
from pyradios import RadioBrowser
import httpcore  # For handling specific timeout exceptions
from concurrent.futures import ThreadPoolExecutor
import json
import os
import time

# Verify URLs in parallel for speed optimization
def verify_url_concurrently(stations):
    def verify(station):
        try:
            response = requests.head(station['url_resolved'], timeout=5)
            response.raise_for_status()  # Valid URL
            return station
        except Exception:
            return None  # Invalid or unreachable

    with ThreadPoolExecutor(max_workers=10) as executor:  # Limit number of threads
        results = executor.map(verify, stations)
    return [station for station in results if station is not None]  # Filter valid stations


# Deterministic shuffling with dynamic seeding
def deterministic_shuffle(stations):
    # Import get_hardware_seed() from the external file
    from system_entropy import get_hardware_seed

    # Use the seed to create a deterministic sorting key for each station
    seed = get_hardware_seed()
    shuffled_stations = sorted(stations, key=lambda s: (seed + hash(s['name'])) % len(stations))
    return shuffled_stations


# Fetch radio stations with caching and error handling
def fetch_radio_stations():
    cache_file = "valid_stations.json"
    cache_timeout = 3600  # Refresh cache every 1 hour
    rb = RadioBrowser()

    # Attempt to load stations from cache
    try:
        if os.path.exists(cache_file):
            last_modified = os.path.getmtime(cache_file)
            if time.time() - last_modified < cache_timeout:
                with open(cache_file, "r") as f:
                    valid_stations = json.load(f)
                    return valid_stations
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # Cache doesn't exist or is invalid, proceed to fetch fresh stations

    # Fetch stations and update cache if necessary
    try:
        stations = rb.search(limit=100)  # Fetch up to 100 stations
        if stations:
            shuffled_stations = deterministic_shuffle(stations)
            valid_stations = verify_url_concurrently(shuffled_stations)
            if valid_stations:
                with open(cache_file, "w") as f:
                    json.dump(valid_stations, f)
                return valid_stations
        return []
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error while fetching stations: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while fetching stations: {e}")
        return []


# Verify individual URLs
def verify_url(stream_url):
    try:
        response = requests.head(stream_url, timeout=5)  # Use a HEAD request for quick verification
        response.raise_for_status()  # Raise an error for HTTP response codes >= 400
        return True
    except requests.exceptions.RequestException:
        return False


# Record audio from the stream with adaptive timeout
def record_stream(stream_url, duration=5):
    timeout = 5  # Start with a default 5-second timeout

    for attempt in range(2):  # Attempt twice: once with 5s, then with 20s
        try:
            response = requests.get(stream_url, stream=True, timeout=timeout)
            response.raise_for_status()
            audio_data = BytesIO()
            for chunk in response.iter_content(chunk_size=1024):
                audio_data.write(chunk)
                if audio_data.tell() >= duration * 44100 * 2:  # Approx. 5 seconds of audio
                    break
            return audio_data
        except (httpcore.ReadTimeout, requests.exceptions.Timeout):
            timeout = 20  # Increase timeout for the next attempt
        except Exception as e:
            print(f"Error recording stream: {e}")
            return None

    print(f"Stream timed out for URL: {stream_url}. Moving to the next station...")
    return None


# Randomly select a station with entropy influence
def pick_random_station(last_entropy=0):
    # Import get_hardware_seed() from the external file
    from system_entropy import get_hardware_seed

    stations = fetch_radio_stations()
    if stations:
        # Combine hardware seed and entropy from the last station
        random_index = (get_hardware_seed() + int(last_entropy)) % len(stations)
        selected_station = stations[random_index]

        # Update last_entropy dynamically based on the selected station's name
        last_entropy = sum(map(ord, selected_station['name'])) % 100  # Example: Sum of character codes mod 100

        print(f"Selected station: {selected_station['name']}: {selected_station['url_resolved']}")
        print(f"Updated last_entropy: {last_entropy}")

        return selected_station, last_entropy
    else:
        print("No stations available to pick from.")
        return None, last_entropy
