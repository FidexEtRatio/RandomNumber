import requests
from io import BytesIO
from pyradios import RadioBrowser
import random

def fetch_radio_stations():
    rb = RadioBrowser()
    stations = rb.search(limit=10)  # Fetch a list of 10 random stations
    if stations:
        print("Available stations:")
        for station in stations:
            print(f"{station['name']}: {station['url_resolved']}")
        return stations
    else:
        print("No stations found.")
        return []

# Validate if a radio stream works
def validate_stream(stream_url):
    try:
        response = requests.get(stream_url, stream=True, timeout=5)  # Short timeout for validation
        response.raise_for_status()
        print(f"Stream {stream_url} is valid.")
        return True
    except Exception as e:
        print(f"Stream {stream_url} is invalid: {e}")
        return False

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

def fetch_two_working_radios():
    stations = fetch_radio_stations()
    working_stations = []

    for station in stations:
        if len(working_stations) == 2:  # Stop once we have two working stations
            break

        stream_url = station['url_resolved']
        if validate_stream(stream_url):  # Check if the stream works
            working_stations.append(station)

    if len(working_stations) < 2:
        print("Could not find two working stations.")
    else:
        print("\nSelected two working stations:")
        for ws in working_stations:
            print(f"{ws['name']}: {ws['url_resolved']}")

    return working_stations