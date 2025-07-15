# utils.py
from urllib.parse import urlparse

def get_username_from_url(url: str) -> str | None:
    """
    Extracts the Reddit username from a user profile URL.

    Args:
        url: The full Reddit user profile URL (e.g., "https://www.reddit.com/user/kojied/").

    Returns:
        The username as a string, or None if the URL is not a valid user profile URL.
    """
    parsed_url = urlparse(url)
    # Split the path by '/' and filter out empty strings (due to leading/trailing slashes)
    path_segments = [segment for segment in parsed_url.path.split('/') if segment]

    # A typical user URL path is like /user/username/
    if len(path_segments) >= 2 and path_segments[0].lower() == 'user':
        return path_segments[1]
    return None

if __name__ == "__main__":
    # Example usage for testing utils.py
    print("Testing get_username_from_url:")
    url1 = "https://www.reddit.com/user/kojied/"
    print(f"Username for '{url1}': {get_username_from_url(url1)}")

    url2 = "https://www.reddit.com/user/Hungry-Move-6603/"
    print(f"Username for '{url2}': {get_username_from_url(url2)}")

    url3 = "https://www.reddit.com/r/python/"
    print(f"Username for '{url3}' (invalid): {get_username_from_url(url3)}")

    url4 = "https://www.reddit.com/user/testuser" # No trailing slash
    print(f"Username for '{url4}': {get_username_from_url(url4)}")