
# TrendPulse — Task 1: Data Collection
# Author: Abhishek Choudhary

import requests
import json
import os
import time
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {"User-Agent": "TrendPulse/1.0"}
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
STORY_DETAIL_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
MAX_IDS = 500
MAX_PER_CATEGORY = 25

CATEGORIES = {
    "technology":    ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM", "programming", "developer", "python", "open source", "startup", "model"],
    "worldnews":     ["war", "government", "country", "president", "election", "climate", "attack", "global", "china", "russia", "india", "policy", "trump", "law", "military", "treaty", "sanctions", "court", "minister", "nuclear", "border", "deal", "tax", "ban", "protest"],
    "sports":        ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship", "cricket", "tennis", "olympic", "tournament", "coach", "match", "score", "win", "loss", "EPL", "baseball", "hockey", "golf", "race", "athlete", "cup", "IPL", "wrestling"],
    "science":       ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome", "brain", "health", "cancer", "virus", "quantum", "planet", "scientist", "experiment", "medicine"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming", "youtube", "podcast", "artist", "actor", "series", "trailer", "release", "review"],
}

def fetch_top_story_ids():
    print("Fetching top story IDs...")
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        all_ids = response.json()
        print(f"  Got {len(all_ids)} IDs. Using first {MAX_IDS}.")
        return all_ids[:MAX_IDS]
    except requests.RequestException as e:
        print(f"  ERROR: {e}")
        return []

def assign_category(title):
    if not title:
        return None
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category
    return None

def fetch_story_details(story_id):
   
    for attempt in range(3):
        try:
            url = STORY_DETAIL_URL.format(story_id)
            response = requests.get(url, headers=HEADERS, timeout=15, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt < 2:
                time.sleep(2)  
                continue
            print(f"  WARNING: Could not fetch story {story_id} — {e}")
            return None

def collect_stories(story_ids):
    category_counts = {cat: 0 for cat in CATEGORIES}
    collected_stories = []
    collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\nFetching and categorising stories...\n")

    for story_id in story_ids:
        if all(count >= MAX_PER_CATEGORY for count in category_counts.values()):
            print("All categories full. Stopping.")
            break

        story = fetch_story_details(story_id)
        if not story or "title" not in story:
            continue

        title = story.get("title", "")
        category = assign_category(title)

        if category is None or category_counts[category] >= MAX_PER_CATEGORY:
            continue

        story_data = {
            "post_id":      story.get("id"),
            "title":        title,
            "category":     category,
            "score":        story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author":       story.get("by", "unknown"),
            "collected_at": collected_at,
        }

        collected_stories.append(story_data)
        category_counts[category] += 1

        if len(collected_stories) % 25 == 0:
            print(f"  {len(collected_stories)} stories collected so far...")
            time.sleep(2)

    print(f"\nCategory breakdown: {category_counts}")
    return collected_stories

def save_to_json(stories):
    os.makedirs("data", exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{today}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)
    print(f"\nCollected {len(stories)} stories. Saved to {filename}")
    return filename

if __name__ == "__main__":
    print("=== TrendPulse — Task 1: Data Collection ===\n")
    story_ids = fetch_top_story_ids()
    if not story_ids:
        print("No IDs fetched. Exiting.")
    else:
        stories = collect_stories(story_ids)
        if stories:
            save_to_json(stories)
        else:
            print("No stories collected.")
