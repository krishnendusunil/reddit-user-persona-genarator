# Reddit User Persona Generator

## 🔍 Overview
This script generates a user persona from a Reddit user's public posts and comments using the Reddit API and OpenAI GPT-3.5 (if available).

## 🧰 Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/krishnendusunil/reddit-user-persona-generator.git
    cd reddit-user-persona-generator
    ```

2. **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows (PowerShell):
    .\venv\Scripts\Activate.ps1
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Download NLTK data:**
    ```bash
    python
    >>> import nltk
    >>> nltk.download('stopwords')
    >>> nltk.download('punkt')
    >>> nltk.download('punkt_tab')
    >>> exit()
    ```

5. **Obtain Reddit API Credentials:**
    - Go to [Reddit Apps](https://www.reddit.com/prefs/apps) and create a `script` app.
    - Note your `client ID`, `client secret`, and set a user agent.

6. **Set Environment Variables:**
    - Create a `.env` file in your project root with:
      ```
      REDDIT_CLIENT_ID=your_reddit_client_id
      REDDIT_CLIENT_SECRET=your_reddit_client_secret
      REDDIT_USER_AGENT=YourAppName/1.0 by YourRedditUsername
      OPENAI_API_KEY=your_openai_api_key  # Optional, for LLM persona generation
      ```

## 🚀 How to Run

1. **Add Reddit user URLs:**
    - Create a file named `reddit_users.txt` (one URL per line), e.g.:
      ```
      https://www.reddit.com/user/kojied/
      https://www.reddit.com/user/Hungry-Move-6603/
      ```
    - If `reddit_users.txt` is missing, the script will use a default list in the code.

2. **Run the script:**
    ```bash
    python reddit_persona.py
    ```

3. **Output:**
    - Persona files will be saved in the `sample_output/` directory, e.g. `sample_output/kojied_persona.txt`.

## 📝 Adding New Reddit Profiles

- Add new Reddit user URLs to `reddit_users.txt` (one per line).
- Re-run the script to generate personas for the new users.

## 📦 Sample Output

- Example persona files for the sample users are included in `sample_output/`.

## 🛠 Technologies Used

- Python 3.x
- PRAW (Reddit API)
- NLTK (text processing)
- OpenAI GPT-3.5 (for advanced persona generation, optional)
- python-dotenv (for environment variable management)

## ⚠️ Notes

- If `OPENAI_API_KEY` is not set, the script will use a basic keyword-based persona generator.
- All output files are saved as `.txt` in the `sample_output/` directory.

## Features

* **Scraping:** Retrieves comments and submissions (posts) for a given Reddit user.
* **Persona Generation:** Analyzes scraped text to form a user persona.
    * Includes a basic keyword-based persona generation with content citations.
    * (Optional but encouraged) Supports integration with Large Language Models (LLMs) like OpenAI GPT for more advanced, nuanced persona generation with detailed citations.
* **Output:** Saves the generated user persona to a text file (`.txt`) within a `sample_output` directory.

## Technologies Used

* **Python 3.x**
* **PRAW** (Python Reddit API Wrapper) for interacting with Reddit's API.
* **NLTK** (Natural Language Toolkit) for basic text processing (tokenization, stop words).
* **(Optional)** `openai` library for OpenAI GPT integration.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourGitHubUsername/your-repo-name.git](https://github.com/YourGitHubUsername/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment (highly recommended):**
    Open your terminal (PowerShell on Windows, Terminal on macOS/Linux) **as Administrator** if on Windows.

    ```powershell
    # Create the virtual environment
    python -m venv venv

    # Activate the virtual environment
    # On macOS/Linux:
    # source venv/bin/activate
    # On Windows (PowerShell):
    .\venv\Scripts\Activate.ps1
    # On Windows (Command Prompt):
    # venv\Scripts\activate.bat
    ```
    Your terminal prompt should change (e.g., `(venv) PS C:\...` or `(venv) user@host:...`) indicating the virtual environment is active.

3.  **Install dependencies:**
    With your virtual environment activated:
    ```bash
    pip install -r requirements.txt
    ```
    *(You will create `requirements.txt` in the next step)*

4.  **Download NLTK data:**
    Still with the virtual environment activated, open a Python interpreter:
    ```bash
    python
    ```
    Then, within the Python interpreter, run:
    ```python
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')
    exit() # Type this and press Enter to exit
    ```

5.  **Obtain Reddit API Credentials:**
    To use the Reddit API, you need to register your application:
    * Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps).
    * Scroll to the bottom and click "create app" or "create another app".
    * Select `script` as the app type.
    * Provide a `name` (e.g., "MyPersonaGenApp").
    * Set `redirect uri` to `http://localhost:8080` (this is a placeholder for script apps and doesn't need to be a real URL).
    * Click "create app".
    * Once created, you will see your `client ID` (under "personal use script") and your `client secret`. Note these down.

6.  **Set Environment Variables for API Keys:**
    The script reads API credentials from environment variables for security.

    * **Reddit Credentials:**
        * `REDDIT_CLIENT_ID`: Your Reddit app's client ID.
        * `REDDIT_CLIENT_SECRET`: Your Reddit app's client secret.
        * `REDDIT_USER_AGENT`: A unique user agent string (e.g., `YourAppName/1.0 by YourRedditUsername`). Replace `YourAppName` and `YourRedditUsername` with your actual app name and Reddit username.

    * **OpenAI (or other LLM) API Key (Optional):**
        * If you enable LLM integration in `persona_generator.py`, you'll also need:
            * `OPENAI_API_KEY`: Your OpenAI API key.

    **How to set environment variables (for the current terminal session):**

    * **On macOS/Linux:**
        ```bash
        export REDDIT_CLIENT_ID="your_reddit_client_id"
        export REDDIT_CLIENT_SECRET="your_reddit_client_secret"
        export REDDIT_USER_AGENT="YourAppName/1.0 by YourRedditUsername"
        export OPENAI_API_KEY="your_openai_api_key" # If using OpenAI
        ```
    * **On Windows (PowerShell):**
        ```powershell
        $env:REDDIT_CLIENT_ID="your_reddit_client_id"
        $env:REDDIT_CLIENT_SECRET="your_reddit_client_secret"
        $env:REDDIT_USER_AGENT="YourAppName/1.0 by YourRedditUsername"
        $env:OPENAI_API_KEY="your_openai_api_key" # If using OpenAI
        ```
    * **On Windows (Command Prompt):**
        ```cmd
        set REDDIT_CLIENT_ID="your_reddit_client_id"
        set REDDIT_CLIENT_SECRET="your_reddit_client_secret"
        set REDDIT_USER_AGENT="YourAppName/1.0 by YourRedditUsername"
        set OPENAI_API_KEY="your_openai_api_key" # If using OpenAI
        ```
    **Important:** These variables will only last for the current terminal session. For a more permanent solution, add them to your system's environment variables or your shell's profile script (e.g., `.bashrc`, `.zshrc`).

## How to Execute

1.  **Ensure your virtual environment is active** (as shown in Step 2 of Setup).
2.  **Ensure your environment variables for API keys are set** (as shown in Step 6 of Setup).
3.  **Run the main script:**
    ```bash
    python reddit_persona.py
    ```

The script will process the hardcoded URLs in `reddit_persona.py`, scrape their content, generate personas, and save them in the `sample_output` directory.

## Adding New Reddit Profiles

To generate a persona for a new Reddit profile, simply open `reddit_persona.py` and modify the `reddit_user_urls` list in the `main()` function:

```python
# In reddit_persona.py

def main():
    reddit_user_urls = [
        "[https://www.reddit.com/user/kojied/](https://www.reddit.com/user/kojied/)",
        "[https://www.reddit.com/user/Hungry-Move-6603/](https://www.reddit.com/user/Hungry-Move-6603/)",
        "[https://www.reddit.com/user/AnotherRedditUser/](https://www.reddit.com/user/AnotherRedditUser/)" # Add new URLs here
        # ... and so on
    ]
    # ... rest of the main function ...
```