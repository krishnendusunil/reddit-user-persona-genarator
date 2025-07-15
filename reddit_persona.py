# reddit_persona.py
import praw
import os
import sys
from dotenv import load_dotenv

from utils import get_username_from_url
from persona_generator import combine_text_for_analysis, generate_persona_with_llm, generate_basic_persona

load_dotenv()  # Load environment variables

# --- PRAW Initialization Function ---
def initialize_reddit() -> praw.Reddit | None:
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    user_agent = os.environ.get("REDDIT_USER_AGENT")

    if not all([client_id, client_secret, user_agent]):
        print("❌ Reddit API credentials are not set. Check your .env file.", file=sys.stderr)
        return None

    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        print("✅ PRAW initialized successfully (read-only mode)." if reddit.read_only else "✅ PRAW initialized (writable mode).")
        return reddit
    except Exception as e:
        print(f"❌ Error initializing PRAW: {e}", file=sys.stderr)
        return None

# --- Scraping Function ---
def scrape_redditor_content(reddit: praw.Reddit, username: str, limit: int = 100) -> tuple[list[dict], list[dict]]:
    comments_data, posts_data = [], []

    try:
        user = reddit.redditor(username)
        print(f"🔍 Scraping comments for u/{username}...")
        for comment in user.comments.top(limit=limit):
            comments_data.append({
                'type': 'comment',
                'id': comment.id,
                'body': comment.body,
                'score': comment.score,
                'created_utc': comment.created_utc,
                'permalink': f"https://www.reddit.com{comment.permalink}",
                'submission_title': getattr(comment.submission, 'title', 'N/A'),
                'submission_url': getattr(comment.submission, 'url', 'N/A')
            })
        print(f"📝 Found {len(comments_data)} comments.")

        print(f"🔍 Scraping posts for u/{username}...")
        for submission in user.submissions.top(limit=limit):
            posts_data.append({
                'type': 'post',
                'id': submission.id,
                'title': submission.title,
                'selftext': submission.selftext if submission.is_self else '',
                'url': submission.url,
                'score': submission.score,
                'created_utc': submission.created_utc,
                'permalink': f"https://www.reddit.com{submission.permalink}"
            })
        print(f"📰 Found {len(posts_data)} posts.")

    except Exception as e:
        print(f"❌ Error scraping content for u/{username}: {e}", file=sys.stderr)

    return comments_data, posts_data

# --- Save Output ---
def save_persona_to_file(username: str, persona_content: str, output_dir: str = "sample_output"):
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{username}_persona.txt")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(persona_content)
        print(f"✅ Persona saved to {filepath}")
    except Exception as e:
        print(f"❌ Error saving persona: {e}", file=sys.stderr)

# --- Main ---
def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️ Warning: OPENAI_API_KEY is missing. LLM generation will fail.")

    reddit = initialize_reddit()
    if not reddit:
        return

    # Read usernames from list or hardcode
    try:
        with open("reddit_users.txt") as f:
            reddit_user_urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        reddit_user_urls = [
            "https://www.reddit.com/user/kojied/",
            "https://www.reddit.com/user/Hungry-Move-6603/"
        ]

    for url in reddit_user_urls:
        username = get_username_from_url(url)
        if not username:
            print(f"⚠️ Invalid URL skipped: {url}")
            continue

        print(f"\n🧠 Processing user: {username}")
        comments, posts = scrape_redditor_content(reddit, username, limit=150)

        combined_text = combine_text_for_analysis(comments, posts)
        if not combined_text.strip():
            print(f"⚠️ No data found for u/{username}. Skipping.")
            continue

        # Only use LLM if user has more than 20 total items
        if len(comments) + len(posts) > 20:
            persona = generate_persona_with_llm(combined_text, comments, posts)
        else:
            persona = generate_basic_persona(combined_text, comments, posts)
        save_persona_to_file(username, persona)

        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()
