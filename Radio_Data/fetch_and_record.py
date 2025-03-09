import requests
from io import BytesIO
from pyradios import RadioBrowser
import random

def fetch_radio_station():
    rb = RadioBrowser()
    stations = rb.search(name="BBC Radio 1", name_exact=True)  # Example: Search for a specific station
    if stations:
        print(f"Station Name: {stations[0]['name']}")
        print(f"Stream URL: {stations[0]['url_resolved']}")
        return stations[0]['url_resolved']
    else:
        print("No stations found.")
        return None

# Record audio from the stream
def record_stream(stream_url, duration=5):
    try:
        response = requests.get(stream_url, stream=True)
        response.raise_for_status()
        audio_data = BytesIO()
        for chunk in response.iter_content(chunk_size=1024):
            audio_data.write(chunk)
            if audio_data.tell() >= duration * 44100 * 2:  # 5 seconds of audio (approx)
                break
        return audio_data
    except Exception as e:
        print(f"Error recording stream: {e}")
        return None
