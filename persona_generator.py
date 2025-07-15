import os
from dotenv import load_dotenv
load_dotenv()

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import google.generativeai as genai
import openai


def combine_text_for_analysis(comments: list[dict], posts: list[dict]) -> str:
    all_text_parts = []
    for comment in comments:
        if 'body' in comment and comment['body']:
            all_text_parts.append(comment['body'])
    for post in posts:
        if 'selftext' in post and post['selftext']:
            all_text_parts.append(post['selftext'])
        elif 'title' in post and post['title']:
            all_text_parts.append(post['title'])
    return " ".join(all_text_parts)


def generate_persona_with_openai(text_data: str, comments: list[dict], posts: list[dict]) -> str:
    try:
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        openai.api_key = openai_api_key

        prompt = f"""
        You are an expert in user profiling, specifically for online forum users.
        Analyze the following Reddit comments and posts to create a detailed user persona.

        **Persona Characteristics to Identify:**
        - Interests/Hobbies
        - Profession/Occupation (if hinted)
        - Communication Style
        - General Tone/Sentiment
        - Values/Beliefs
        - Demographic clues (if strongly hinted only)

        **Citation Format (Strict):**
        * **Characteristic Name:** Description
            * *Citation 1:* "[Excerpt]" (Permalink: [Full URL])
            * *Citation 2:* "[Excerpt]" (Permalink: [Full URL])

        **Reddit Text:**
        {text_data[:15000]}

        Format the output in clean markdown and start directly with the persona.
        """
        print("Attempting to generate persona with OpenAI GPT-3.5...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0.7
        )
        persona_output = response.choices[0].message["content"]
        print("OpenAI GPT-3.5 persona generated.")
        return persona_output
    except Exception as e:
        print(f"Error calling OpenAI GPT-3.5 API: {e}. Falling back to basic persona generation.")
        return generate_basic_persona(text_data, comments, posts)


def generate_persona_with_llm(text_data: str, comments: list[dict], posts: list[dict]) -> str:
    try:
        # Prefer OpenAI if API key is set
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if openai_api_key:
            return generate_persona_with_openai(text_data, comments, posts)

        google_api_key = os.environ.get("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")

        genai.configure(api_key=google_api_key)

        # ✅ Correct Gemini usage
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

        prompt = f"""
        You are an expert in user profiling, specifically for online forum users.
        Analyze the following Reddit comments and posts to create a detailed user persona.

        **Persona Characteristics to Identify:**
        - Interests/Hobbies
        - Profession/Occupation (if hinted)
        - Communication Style
        - General Tone/Sentiment
        - Values/Beliefs
        - Demographic clues (if strongly hinted only)

        **Citation Format (Strict):**
        * **Characteristic Name:** Description
            * *Citation 1:* "[Excerpt]" (Permalink: [Full URL])
            * *Citation 2:* "[Excerpt]" (Permalink: [Full URL])

        **Reddit Text:**
        {text_data[:15000]}

        Format the output in clean markdown and start directly with the persona.
        """

        print("Attempting to generate persona with Google Gemini LLM...")
        response = model.generate_content(prompt)
        persona_output = response.text
        print("Google Gemini LLM persona generated.")
        return persona_output

    except ValueError as e:
        print(f"LLM API key error: {e}. Falling back to basic persona generation.")
        return generate_basic_persona(text_data, comments, posts)
    except Exception as e:
        print(f"Error calling Google Gemini LLM API: {e}. Falling back to basic persona generation.")
        return generate_basic_persona(text_data, comments, posts)


def generate_basic_persona(text_data: str, comments: list[dict], posts: list[dict]) -> str:
    persona_lines = ["--- Basic User Persona (Generated without LLM) ---"]

    stop_words = set(stopwords.words('english'))
    reddit_stop_words = {
        'r', 'subreddit', 'post', 'comment', 'like', 'know', 'think', 'get', 'would',
        'really', 'people', 'one', 'good', 'just', 'see', 'also', 'op', 'thread'
    }
    stop_words.update(reddit_stop_words)

    words = word_tokenize(text_data.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    word_freq = Counter(filtered_words)

    persona_lines.append("\n* **Potential Interests/Top Keywords:**")
    if word_freq:
        for word, freq in word_freq.most_common(7):
            persona_lines.append(f"    - **{word}** (Appears {freq} times)")
    else:
        persona_lines.append("    - No significant keywords found.")

    persona_lines.append("\n* **Sample Communication & Content (from comments):**")
    if comments:
        sampled_comments = sorted(comments, key=lambda x: x.get('score', 0), reverse=True)[:min(5, len(comments))]
        for comment in sampled_comments:
            preview = comment['body'][:200].replace('\n', ' ')
            persona_lines.append(f"    - \"{preview.strip()}...\" (Permalink: {comment['permalink']})")
    else:
        persona_lines.append("    - No comments found.")

    persona_lines.append("\n* **Sample Post Topics & Content:**")
    if posts:
        sampled_posts = sorted(posts, key=lambda x: x.get('score', 0), reverse=True)[:min(5, len(posts))]
        for post in sampled_posts:
            title_preview = post['title'].replace('\n', ' ')
            content_preview = post['selftext'][:100].replace('\n', ' ') if post['selftext'] else ""
            if content_preview:
                persona_lines.append(
                    f"    - Title: \"{title_preview.strip()}\" (Content: \"{content_preview.strip()}...\") (Permalink: {post['permalink']})"
                )
            else:
                persona_lines.append(
                    f"    - Title: \"{title_preview.strip()}\" (Permalink: {post['permalink']})"
                )
    else:
        persona_lines.append("    - No posts found.")

    persona_lines.append("\n--- End Basic Persona ---")
    return "\n".join(persona_lines)


# --- Testing Block ---
if __name__ == "__main__":
    print("Testing persona_generator.py (basic functionality without scraping/LLM)...")

    sample_comments = [
        {'type': 'comment', 'id': 'c1', 'body': 'I love coding in Python for data analysis.', 'score': 10,
         'permalink': 'https://reddit.com/r/python/comments/abcde/c1'},
        {'type': 'comment', 'id': 'c2', 'body': 'Just finished Project Hail Mary. Amazing sci-fi!', 'score': 5,
         'permalink': 'https://reddit.com/r/books/comments/fghijk/c2'},
        {'type': 'comment', 'id': 'c3', 'body': 'Ethereum is exciting. DeFi is the future.', 'score': 20,
         'permalink': 'https://reddit.com/r/ethereum/comments/lmnop/c3'},
    ]

    sample_posts = [
        {'type': 'post', 'id': 'p1', 'title': 'New AI build with RTX 4090', 'selftext': 'Running fast!', 'score': 15,
         'permalink': 'https://reddit.com/r/MachineLearning/comments/aijklm/p1'},
        {'type': 'post', 'id': 'p2', 'title': 'Crypto trends', 'selftext': '', 'url': 'https://crypto.com', 'score': 8,
         'permalink': 'https://reddit.com/r/CryptoCurrency/comments/bcdefg/p2'},
    ]

    combined_text = combine_text_for_analysis(sample_comments, sample_posts)
    print("\n--- Combined Text Sample ---")
    print(combined_text[:300])

    print("\n--- Generated Persona (LLM or Fallback) ---")
    persona_output = generate_persona_with_llm(combined_text, sample_comments, sample_posts)
    print(persona_output)
