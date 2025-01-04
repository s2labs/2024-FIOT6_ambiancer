import time

def get_timestamp_string():
    """
    Generates a timestamp string in the format YYYYMMDDHHMMSS.

    Returns:
        str: The current timestamp as a string.
    """
    return time.strftime("%Y%m%d%H%M%S", time.localtime())