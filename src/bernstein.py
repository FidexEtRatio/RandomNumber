def djb2(string, max):
    hash_value = 5381

    for elem in string:
        hash_value = ((hash_value << 5) + hash_value + elem) % max
    return hash_value