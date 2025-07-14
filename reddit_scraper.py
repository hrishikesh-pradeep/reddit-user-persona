import os
import sys
import time
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
import praw
import openai

# ==========================
# Load Environment Variables
# ==========================
load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ==========================
# Configure Logging
# ==========================
logging.basicConfig(
    filename='reddit_persona.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ==========================
# Initialize APIs
# ==========================
openai.api_key = GROQ_API_KEY
openai.api_base = "https://api.groq.com/openai/v1"

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent="RedditUserPersonaScript/1.0 (by u/yourusername)"
)

# ==========================
# Fetch User Content
# ==========================
def fetch_user_data(username, max_items=100):
    logging.info(f"Fetching posts/comments for u/{username}")
    try:
        user = reddit.redditor(username)
        posts = []
        comments = []

        for i, post in enumerate(user.submissions.new(limit=max_items)):
            posts.append({
                "type": "post",
                "subreddit": post.subreddit.display_name,
                "title": post.title,
                "text": post.selftext,
                "score": post.score,
                "url": f"https://www.reddit.com{post.permalink}",
                "created_utc": datetime.utcfromtimestamp(post.created_utc).isoformat()
            })

        for i, comment in enumerate(user.comments.new(limit=max_items)):
            comments.append({
                "type": "comment",
                "subreddit": comment.subreddit.display_name,
                "text": comment.body,
                "score": comment.score,
                "url": f"https://www.reddit.com{comment.permalink}",
                "created_utc": datetime.utcfromtimestamp(comment.created_utc).isoformat()
            })

        return posts, comments

    except Exception as e:
        logging.error(f"Error fetching data for u/{username}: {str(e)}")
        raise RuntimeError(f"Unable to fetch data: {str(e)}")

# ==========================
# Run LLaMA 3 Analysis (Groq)
# ==========================
def analyze_content_with_groq(posts, comments):
    logging.info("Analyzing content using LLaMA 3 (Groq)")

    all_content = "\n\n".join(
        [f"[r/{p['subreddit']} - {p['created_utc']}] {p.get('title', '')} {p['text']}" for p in posts] +
        [f"[r/{c['subreddit']} - {c['created_utc']}] {c['text']}" for c in comments]
    )

    system_prompt = (
        "You are a researcher generating detailed user personas from Reddit activity. "
        "Use the Big Five personality model, values, interests, and communication style. "
        "Each trait must include: value, confidence score (0–100%), supporting evidence (quote or paraphrase), subreddit, and timestamp. "
        "Include summary stats like most active subreddits and themes."
    )

    response = openai.ChatCompletion.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": all_content[:16000]}  # Keep content within model token limit
        ],
        temperature=0.5
    )

    return response['choices'][0]['message']['content']

# ==========================
# Generate Output File
# ==========================
def generate_output_file(username, posts, comments, persona_report):
    output_file = f"{username}_persona.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"[User Persona: {username}]\n")
        f.write("="*40 + "\n\n")
        f.write("## Basic Profile\n")
        f.write(f"- Username: {username}\n")
        f.write(f"- Analysis Date: {datetime.utcnow().isoformat()} UTC\n")
        f.write(f"- Content Analyzed: {len(posts)} posts, {len(comments)} comments\n\n")
        f.write(persona_report)
        f.write("\n\n## Disclaimer\n")
        f.write("This analysis is based only on publicly available Reddit data.\n")
        f.write("It does not store or track personal information and is intended for research or educational use only.\n")
    logging.info(f"User persona saved to {output_file}")

# ==========================
# Main Execution
# ==========================
def main():
    if len(sys.argv) != 2:
        print("Usage: python reddit_persona.py <reddit_username>")
        return

    username = sys.argv[1]
    logging.info(f"Starting analysis for user: {username}")

    try:
        posts, comments = fetch_user_data(username)
        if not posts and not comments:
            print("No content found for this user.")
            return

        report = analyze_content_with_groq(posts, comments)
        generate_output_file(username, posts, comments, report)
        print(f"Persona generated in 'user_persona.txt'.")

    except Exception as e:
        logging.error(f"Fatal error: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
