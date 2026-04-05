
# TrendPulse — Task 2: Data Cleaning & CSV Export
# Name: Abhishek Choudhary
# We load the raw JSON file, clean it up step by step,
# and save a tidy CSV that Task 3 can work with directly.

import os
import glob
import json
import pandas as pd


# STEP 1 — FIND AND LOAD THE JSON FILE
# ─────────────────────────────────────────────

# Task 1 saves files named like data/trends_YYYYMMDD.json
# We use glob to find whichever date file is present
# instead of hardcoding a filename — more flexible this way.
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("ERROR: No trends JSON file found in data/ folder.")
    print("Please run task1_data_collection.py first.")
    exit()

# If somehow multiple files exist, take the most recent one
json_files.sort()
json_path = json_files[-1]

print(f"Loading data from: {json_path}\n")

# Open and parse the JSON into a list of dicts
with open(json_path, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Convert directly to a DataFrame — one row per story
df = pd.DataFrame(raw_data)

print(f"Loaded {len(df)} stories from {json_path}")
print(f"Columns found: {list(df.columns)}\n")


# STEP 2 — CLEAN THE DATA
# ─────────────────────────────────────────────
# We apply four cleaning rules in sequence and
# see exactly how much data each step removes.

# --- 2a: Remove duplicate post IDs ---
# Same story can sometimes slip in twice if it matched
# multiple category keywords or was fetched more than once.
before = len(df)
df = df.drop_duplicates(subset="post_id")
after = len(df)
print(f"After removing duplicates: {after}  (removed {before - after})")

# --- 2b: Drop rows with missing critical fields ---
# A story is useless to us without an ID, a title, or a score.
# We require all three to be non-null before keeping a row.
before = len(df)
df = df.dropna(subset=["post_id", "title", "score"])
after = len(df)
print(f"After removing nulls:      {after}  (removed {before - after})")

# --- 2c: Fix data types ---
# JSON doesn't enforce types — score and num_comments
# might have come in as floats (e.g. 45.0) instead of ints.
# We cast them now so downstream numeric operations work cleanly.
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)
# post_id should also be an integer, not a float
df["post_id"] = df["post_id"].astype(int)

# --- 2d: Remove low-quality / spam-like stories ---
# Stories with a score below 5 are basically invisible on HN.
# They tend to be self-promotional posts with no engagement,
# so we drop them to keep the dataset meaningful.
before = len(df)
df = df[df["score"] >= 5]
after = len(df)
print(f"After removing low scores: {after}  (removed {before - after})")

# --- 2e: Strip extra whitespace from titles ---
# Some titles in the raw JSON have leading/trailing spaces.
# .str.strip() cleans that up in one shot.
df["title"] = df["title"].str.strip()

print(f"\nCleaning complete. {len(df)} rows remaining.\n")


# STEP 3 — SAVE THE CLEANED DATA AS A CSV
# ─────────────────────────────────────────────

# Make sure the data/ folder exists (it should from Task 1,
# but we check anyway to be safe).
os.makedirs("data", exist_ok=True)

output_path = "data/trends_clean.csv"

# index=False — we don't want pandas to write its own row numbers
# into the CSV; the post_id is already our unique identifier.
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"Saved {len(df)} rows to {output_path}")


print("\nStories per category:")
category_counts = df["category"].value_counts()
for category, count in category_counts.items():
    # Pad the category name to 15 chars for alignment
    print(f"  {category:<15} {count}")
