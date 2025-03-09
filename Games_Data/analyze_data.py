def analyze_data(data, data_type):
    """
    Analyze the fetched data based on the type.
    Args:
        data (dict): Data fetched from the API.
        data_type (str): The type of data ('stats').
    Returns:
        Any: Results of the analysis.
    """
    if data_type == "stats":
        # Example: Extract summoner level
        return {"summoner_name": data["name"], "summoner_level": data["summonerLevel"]}
    else:
        return {"error": "Unsupported data type"}
