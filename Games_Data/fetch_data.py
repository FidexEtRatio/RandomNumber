import requests

def fetch_data(api_url, api_key, endpoint):
    """
    Fetch data from the Riot Games API for the given endpoint.
    Args:
        api_url
        api_key
        endpoint
    Returns:
        dict: JSON response from the API if successful, None otherwise.
    """
    headers = {"X-Riot-Token": api_key}  # Riot API requires this header for authentication
    full_url = f"{api_url}/{endpoint}"  # Combine base URL and endpoint
    response = requests.get(full_url, headers=headers)  # Send GET request
    
    if response.status_code == 200:
        return response.json()  # Return the JSON data
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return None
