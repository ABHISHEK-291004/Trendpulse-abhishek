
# TrendPulse — Task 3: Analysis with Pandas & NumPy
# Name: Abhishek Choudhary
#
# NumPy handles the number-crunching, Pandas handles the structure.
# At the end we add two new columns and save a new CSV for Task 4.

import pandas as pd
import numpy as np


# STEP 1 — LOAD AND EXPLORE THE DATA
# ─────────────────────────────────────────────

# Read in the cleaned CSV that Task 2 produced
df = pd.read_csv("data/trends_clean.csv")

print(f"Loaded data: {df.shape}")   # (rows, columns)
print()

# Show first 5 rows so we can visually confirm it looks right
print("First 5 rows:")
print(df.head(5).to_string(index=False))
print()

avg_score    = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"Average score   : {avg_score:.2f}")
print(f"Average comments: {avg_comments:.2f}")


# STEP 2 — NUMPY STATS
# ─────────────────────────────────────────────
# We pull the score column out as a plain NumPy array

print("\n--- NumPy Stats ---")

scores = df["score"].to_numpy()

# Mean, median, std give us a picture of how scores are distributed.
# On HN a small number of stories get huge upvotes — so mean > median usually.
mean_score   = np.mean(scores)
median_score = np.median(scores)
std_score    = np.std(scores)

print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")

# Max and min tell us the range — how viral did the top story get?
max_score = np.max(scores)
min_score = np.min(scores)

print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

# value_counts() returns categories sorted by frequency automatically
top_category       = df["category"].value_counts().idxmax()
top_category_count = df["category"].value_counts().max()

print(f"\nMost stories in: {top_category} ({top_category_count} stories)")

# Find the row where num_comments is highest using idxmax()
# then pull out just the title and comment count from that row
most_commented_idx   = df["num_comments"].idxmax()
most_commented_title = df.loc[most_commented_idx, "title"]
most_commented_count = df.loc[most_commented_idx, "num_comments"]

print(f"\nMost commented story: \"{most_commented_title}\"  — {most_commented_count} comments")


# STEP 3 — ADD NEW COLUMNS
# ─────────────────────────────────────────────

# engagement: how much discussion a story generates per upvote.
# for any edge-case stories that somehow have a score of 0.
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Round to 4 decimal places so the CSV stays readable
df["engagement"] = df["engagement"].round(4)

# We already computed avg_score above — reuse it here.
df["is_popular"] = df["score"] > avg_score

print(f"\nNew columns added: engagement, is_popular")
print(f"Popular stories (above avg score of {avg_score:.1f}): {df['is_popular'].sum()} out of {len(df)}")

# Quick preview of the two new columns alongside score
print()
print(df[["title", "score", "engagement", "is_popular"]].head(5).to_string(index=False))


# STEP 4 — SAVE THE UPDATED DATAFRAME
# ─────────────────────────────────────────────

# Write out a new CSV — Task 4 will load this one for visualisation.
# index=False so pandas doesn't write its own row numbers into the file.
output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"\nSaved to {output_path}")
print(f"Final shape: {df.shape}  (original 7 columns + 2 new ones = 9 total)")
