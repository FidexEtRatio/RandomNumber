from fetch_data import fetch_data
from analyze_data import analyze_data
from delay import apply_rate_limit  # delay function


# at the moment i have a problem with fetching the data
# Error fetching data: 403 - {"status":{"message":"Forbidden","status_code":403}}


# API Details
API_URL = "https://euw1.api.riotgames.com"  # Riot Games API base URL
API_KEY = "RGAPI-6b6f6c81-e2a3-4ab3-b423-bffe0d9ec120"

# Rate limit settings
REQUEST_LIMIT_1S = 20  # 20 requests per 1 second
REQUEST_LIMIT_120S = 100  # 100 requests per 2 minutes
REQUEST_WINDOW_1S = 1  # Time window for 1-second limit
REQUEST_WINDOW_120S = 120  # Time window for 2-minute limit
requests_made = 0  # Counter for requests made in the current session

# User-specified type
data_type = "stats"

if data_type == "stats":
    endpoint = "lol/summoner/v4/summoners/by-name/florentinivan10"  # Endpoint for summoner stats

    # Loop for multiple requests or testing
    while True:
        # Apply rate limits
        apply_rate_limit(REQUEST_LIMIT_1S, REQUEST_WINDOW_1S, requests_made % REQUEST_LIMIT_1S)
        apply_rate_limit(REQUEST_LIMIT_120S, REQUEST_WINDOW_120S, requests_made % REQUEST_LIMIT_120S)

        # Fetch data
        data = fetch_data(API_URL, API_KEY, endpoint)
        if data:
            results = analyze_data(data, data_type)
            print(f"Analysis Results for {data_type}: {results}")
        # Increment request counter
        requests_made += 1

        # Stop the loop after one request for demo purposes (you can remove this for continuous requests)
        break
else:
    print("Invalid data type! Only 'stats' is supported.")
