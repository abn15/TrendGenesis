import praw
import openai
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time

# Load environment variables from .env file
load_dotenv()

# Load API keys from environment variables
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize Reddit API and OpenAI with loaded keys
CLIENT_ID = REDDIT_CLIENT_ID
CLIENT_SECRET = REDDIT_CLIENT_SECRET
USER_AGENT = 'trending_topic_fetcher'
openai.api_key = OPENAI_API_KEY

reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

# Function to fetch Reddit posts based on a topic, not older than a week
def fetch_recent_reddit_posts(topic, limit=10):
    subreddit = reddit.subreddit('all')  # Change to specific subreddit if needed
    posts = subreddit.search(topic, time_filter='week', limit=limit)
    return [(post.title, post.selftext) for post in posts]  # Return title and selftext of each post

# Function to scrape a webpage and extract paragraphs
def scrape_webpage(url):
    headers = {
        'User-Agent': USER_AGENT,
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    return '\n'.join([p.get_text() for p in paragraphs])

# Function to summarize text using OpenAI
def openai_summarize(text, prompt):
    response = openai.Completion.create(
        engine="davinci-002",
        prompt=prompt + "\n" + text,
        max_tokens=150  # Adjust as per your need for summary length
    )
    return response.choices[0].text.strip()


# Example usage:
if __name__ == "__main__":
    # Example usage:
    topic = 'fashion trends india'
    prompt = "Write me a summary on emerging fashion trends,likes and dislikes and ignore all other data not relevant to it."

    # Fetch recent Reddit posts based on the predefined topic
    posts = fetch_recent_reddit_posts(topic, limit=2)  # Fetch 5 posts for example
    
    for title, text in posts:
        summary = openai_summarize(text, prompt)
        print("Original Post - Title:\n", title)
        print("Original Post - Text:\n", text)
        print("Summary:\n", summary)
        print("-" * 50)

    