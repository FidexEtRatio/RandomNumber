import requests
from io import BytesIO
from pyradios import RadioBrowser
import httpcore  # For handling timeout exceptions
from concurrent.futures import ThreadPoolExecutor
import json
import os
import time
from system_entropy import get_hardware_seed

# Optimized Knuth hash function for better randomness
def knuth_hash(value, size):
    return ((value * 2654435761) % (2**32)) % size

# Parallel URL verification for efficiency
def verify_url_concurrently(stations):
    def verify(station):
        try:
            response = requests.head(station['url_resolved'], timeout=5)
            response.raise_for_status()
            return station  # Valid station
        except Exception:
            return None  # Invalid or unreachable

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(verify, stations)
    return [station for station in results if station]  # Filter valid stations

# Fetch and cache valid radio stations
def fetch_radio_stations():
    cache_file = "valid_stations.json"
    cache_timeout = 600  # Refresh every 10 minutes

    if os.path.exists(cache_file) and (time.time() - os.path.getmtime(cache_file) < cache_timeout):
        with open(cache_file, "r") as f:
            cached_stations = json.load(f)
            if any(station['url_resolved'].startswith("https") for station in cached_stations):
                return cached_stations  # Return cached stations only if they seem valid

    print("Fetching new station list...")
    rb = RadioBrowser()
    try:
        stations = rb.search(limit=200)
        valid_stations = [s for s in stations if s['url_resolved'].startswith("https")]

        if valid_stations:
            with open(cache_file, "w") as f:
                json.dump(valid_stations, f)
        return valid_stations

    except Exception as e:
        print(f"❌ Error fetching stations: {e}")
        return []


# Stream recording with adaptive timeouts
def record_stream(stream_url, duration=5):
    timeout = 5  # Start with 5s timeout

    for _ in range(2):  # Try twice with increasing timeouts
        try:
            response = requests.get(stream_url, stream=True, timeout=timeout)
            response.raise_for_status()

            audio_data = BytesIO()
            for chunk in response.iter_content(chunk_size=1024):
                audio_data.write(chunk)
                if audio_data.tell() >= duration * 44100 * 2:  # Approx. 5s of audio
                    break
            return audio_data

        except (httpcore.ReadTimeout, requests.exceptions.Timeout):
            timeout = 20  # Increase timeout on failure
        except Exception as e:
            print(f"Error recording stream: {e}")
            return None

    return None  # Failed to fetch audio
