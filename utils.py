import re

def get_username_from_url(url: str) -> str | None:
    """
    Extracts the Reddit username from a profile URL.
    Supports URLs like:
      - https://www.reddit.com/user/username/
      - https://reddit.com/user/username
      - https://old.reddit.com/user/username/
      - https://www.reddit.com/u/username/
      - https://reddit.com/u/username
    Returns the username as a string, or None if not found.
    """
    match = re.search(r"reddit\.com/(?:user|u)/([A-Za-z0-9_-]+)/?", url)
    if match:
        return match.group(1)
    return None

# Optional: test block
if __name__ == "__main__":
    test_urls = [
        "https://www.reddit.com/user/kojied/",
        "https://reddit.com/user/Hungry-Move-6603",
        "https://old.reddit.com/user/test_user/",
        "https://www.reddit.com/u/anotheruser/",
        "https://reddit.com/u/yetanotheruser"
    ]
    for url in test_urls:
        print(f"URL: {url} -> Username: {get_username_from_url(url)}") 