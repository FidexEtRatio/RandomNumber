import requests
from io import BytesIO
from pyradios import RadioBrowser
import httpcore  # For handling specific timeout exceptions
from concurrent.futures import ThreadPoolExecutor
import json
import os
import time
from system_entropy import get_hardware_seed

# Verify URLs in parallel for speed optimization
def verify_url_concurrently(stations):
    def verify(station):
        try:
            response = requests.head(station['url_resolved'], timeout=5)
            response.raise_for_status()  # Valid URL
            return station
        except Exception:
            return None  # Invalid or unreachable

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(verify, stations)
    return [station for station in results if station is not None]  # Filter valid stations

# Fetch radio stations with caching and error handling
def fetch_radio_stations():
    cache_file = "valid_stations.json"
    cache_timeout = 600  # Refresh every 10 minutes

    # Check if cache exists and is still valid
    if os.path.exists(cache_file):
        last_modified = os.path.getmtime(cache_file)
        if time.time() - last_modified < cache_timeout:
            with open(cache_file, "r") as f:
                return json.load(f)  # Use cached data

    # If cache is too old, refresh it
    if os.path.exists(cache_file):
        os.remove(cache_file)
        print("Cache cleared! Fetching fresh stations.")

    rb = RadioBrowser()
    try:
        stations = rb.search(limit=200)  # Fetch up to 200 stations
        https_stations = [s for s in stations if s['url_resolved'].startswith("https")]

        if https_stations:
            valid_stations = verify_url_concurrently(https_stations)

            if valid_stations:
                with open(cache_file, "w") as f:
                    json.dump(valid_stations, f)
                return valid_stations

        return []
    except Exception as e:
        print(f"Error fetching stations: {e}")
        return []


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

# Select a station based on entropy-derived index
def pick_random_station(last_entropy=0):
    stations = fetch_radio_stations()
    if stations:
        seed = get_hardware_seed() + last_entropy
        index = seed % len(stations)  # Use entropy to select an index
        # if you want a better index. in test time 
        # time_entropy = int(time.time()) % 100  # Adds a constantly changing factor
        # seed = get_hardware_seed() + last_entropy + time_entropy
        # index = (seed * (last_entropy + 1) + 23) % len(stations)  # Enhanced variation
        selected_station = stations[index]
        last_entropy = sum(map(ord, selected_station['name'])) % 100  # Update entropy factor

        print(f"Selected station: {selected_station['name']}: {selected_station['url_resolved']}")
        print(f"Updated last_entropy: {last_entropy}")

        return selected_station, last_entropy
    else:
        print("No stations available to pick from.")
        return None, last_entropy