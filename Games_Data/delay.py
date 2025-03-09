import time

def apply_rate_limit(request_count, time_window, requests_made):
    """
    Applies rate limiting by ensuring requests do not exceed a defined limit.
    Args:
        request_count (int): Maximum number of requests allowed in the given time window.
        time_window (float): Time window in seconds (e.g., 1 second or 120 seconds).
        requests_made (int): Number of requests already made in the current window.
    Returns:
        None: Pauses the program execution if the limit is about to be exceeded.
    """
    if requests_made >= request_count:
        time.sleep(time_window)
