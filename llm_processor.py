import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise EnvironmentError("OPENAI_API_KEY not set. Please check your .env file.")

openai.api_key = openai_api_key

def generate_persona(posts, comments):
    context = "\n\n".join(
        [f"[Post: {p['id']}]\n{p['title']}\n{p.get('selftext', '')}" for p in posts] +
        [f"[Comment: {c['id']}]\n{c['body']}" for c in comments]
    )

    # Truncate if needed
    MAX_CONTEXT_CHARS = 15000
    context = context[:MAX_CONTEXT_CHARS]

    prompt = f"""
    Build a user persona from the following Reddit activity. For each insight, cite the source post/comment ID.

    {context}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0.7
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"[OpenAI Error: {e}]"
