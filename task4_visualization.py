
# TrendPulse — Task 4: Visualizations
# Name: Abhishek Choudhary
#
# Final step of the pipeline. We take the analysed CSV from Task 3
# and turn the numbers into 3 charts + a combined dashboard.
# Everything is saved as PNG files — nothing needs to pop up on screen.

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # non-interactive backend — saves files without needing a display
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# ─────────────────────────────────────────────
# STEP 1 — SETUP
# ─────────────────────────────────────────────

# Load the CSV that Task 3 produced (99 rows, 9 columns)
df = pd.read_csv("data/trends_analysed.csv")
print(f"Loaded {len(df)} rows from data/trends_analysed.csv")

# Create the outputs/ folder if it isn't there yet
os.makedirs("outputs", exist_ok=True)

# Colour palette — one distinct colour per category so charts
# look consistent with each other across the whole dashboard
CATEGORY_COLOURS = {
    "technology":    "#4C72B0",
    "worldnews":     "#DD8452",
    "sports":        "#55A868",
    "science":       "#C44E52",
    "entertainment": "#8172B2",
}

# Helper: shorten a title so long ones don't overflow the y-axis
def shorten(title, limit=50):
    return title[:limit] + "..." if len(title) > limit else title


# ─────────────────────────────────────────────
# CHART 1 — TOP 10 STORIES BY SCORE
# Horizontal bar chart so the titles are readable
# ─────────────────────────────────────────────

# Sort descending, grab the top 10
top10 = df.sort_values("score", ascending=False).head(10).copy()
top10["short_title"] = top10["title"].apply(shorten)

# Reverse so the highest score is at the top of the chart
top10 = top10.iloc[::-1]

fig1, ax1 = plt.subplots(figsize=(12, 7))

# Colour each bar according to its category
bar_colours = [CATEGORY_COLOURS.get(cat, "#999999") for cat in top10["category"]]
bars = ax1.barh(top10["short_title"], top10["score"], color=bar_colours, edgecolor="white", linewidth=0.6)

# Add score labels at the end of each bar — easier to read than the axis alone
for bar, score in zip(bars, top10["score"]):
    ax1.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
             str(score), va="center", fontsize=9, color="#333333")

ax1.set_title("Top 10 HackerNews Stories by Score", fontsize=14, fontweight="bold", pad=15)
ax1.set_xlabel("Score (Upvotes)", fontsize=11)
ax1.set_ylabel("Story Title", fontsize=11)
ax1.tick_params(axis="y", labelsize=8)

# Add a small legend so we know which colour = which category
legend_patches = [mpatches.Patch(color=c, label=cat) for cat, c in CATEGORY_COLOURS.items()]
ax1.legend(handles=legend_patches, loc="lower right", fontsize=8, title="Category")

plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png", dpi=150)
plt.close(fig1)     # close so it doesn't bleed into the next chart
print("Saved: outputs/chart1_top_stories.png")


# ─────────────────────────────────────────────
# CHART 2 — STORIES PER CATEGORY
# Plain bar chart with each category in its own colour
# ─────────────────────────────────────────────

# Count how many stories we have per category
cat_counts = df["category"].value_counts().sort_values(ascending=False)

fig2, ax2 = plt.subplots(figsize=(9, 6))

colours = [CATEGORY_COLOURS.get(cat, "#999999") for cat in cat_counts.index]
bars2 = ax2.bar(cat_counts.index, cat_counts.values, color=colours, edgecolor="white", linewidth=0.8, width=0.6)

# Put the count number on top of each bar
for bar, count in zip(bars2, cat_counts.values):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
             str(count), ha="center", va="bottom", fontsize=11, fontweight="bold")

ax2.set_title("Number of Stories per Category", fontsize=14, fontweight="bold", pad=15)
ax2.set_xlabel("Category", fontsize=11)
ax2.set_ylabel("Number of Stories", fontsize=11)
ax2.set_ylim(0, cat_counts.max() + 4)    # a bit of headroom above the tallest bar
ax2.tick_params(axis="x", labelsize=10)

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png", dpi=150)
plt.close(fig2)
print("Saved: outputs/chart2_categories.png")


# ─────────────────────────────────────────────
# CHART 3 — SCORE vs COMMENTS (SCATTER)
# Popular vs non-popular shown in different colours
# ─────────────────────────────────────────────

# Split into two groups based on the is_popular column Task 3 added
popular     = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

fig3, ax3 = plt.subplots(figsize=(10, 7))

# Plot non-popular first so popular dots layer on top visually
ax3.scatter(not_popular["score"], not_popular["num_comments"],
            color="#A8C6E3", alpha=0.75, s=60, label="Not Popular", edgecolors="#6A9EC2", linewidth=0.5)

ax3.scatter(popular["score"], popular["num_comments"],
            color="#E3724A", alpha=0.85, s=90, label="Popular (above avg score)", edgecolors="#B84F27", linewidth=0.5)

ax3.set_title("Score vs Number of Comments", fontsize=14, fontweight="bold", pad=15)
ax3.set_xlabel("Score (Upvotes)", fontsize=11)
ax3.set_ylabel("Number of Comments", fontsize=11)
ax3.legend(fontsize=10)

# Light grid in the background makes the scatter easier to read
ax3.grid(True, linestyle="--", alpha=0.4, color="#cccccc")
ax3.set_axisbelow(True)    # grid lines behind the dots, not on top

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png", dpi=150)
plt.close(fig3)
print("Saved: outputs/chart3_scatter.png")


# ─────────────────────────────────────────────
# BONUS — COMBINED DASHBOARD
# All 3 charts side by side in one figure
# ─────────────────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(24, 8))
fig.suptitle("TrendPulse Dashboard", fontsize=20, fontweight="bold", y=1.01)

# --- Panel 1: Top 10 horizontal bar (reuse same data) ---
ax = axes[0]
bar_colours = [CATEGORY_COLOURS.get(cat, "#999999") for cat in top10["category"]]
ax.barh(top10["short_title"], top10["score"], color=bar_colours, edgecolor="white", linewidth=0.5)
ax.set_title("Top 10 Stories by Score", fontsize=12, fontweight="bold")
ax.set_xlabel("Score")
ax.tick_params(axis="y", labelsize=7)

# --- Panel 2: Stories per category ---
ax = axes[1]
ax.bar(cat_counts.index, cat_counts.values,
       color=[CATEGORY_COLOURS.get(c, "#999999") for c in cat_counts.index],
       edgecolor="white", width=0.6)
for bar, count in zip(ax.patches, cat_counts.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
            str(count), ha="center", va="bottom", fontsize=9, fontweight="bold")
ax.set_title("Stories per Category", fontsize=12, fontweight="bold")
ax.set_xlabel("Category")
ax.set_ylabel("Count")
ax.set_ylim(0, cat_counts.max() + 4)
ax.tick_params(axis="x", labelsize=8)

# --- Panel 3: Scatter plot ---
ax = axes[2]
ax.scatter(not_popular["score"], not_popular["num_comments"],
           color="#A8C6E3", alpha=0.75, s=50, label="Not Popular", edgecolors="#6A9EC2", linewidth=0.4)
ax.scatter(popular["score"], popular["num_comments"],
           color="#E3724A", alpha=0.85, s=70, label="Popular", edgecolors="#B84F27", linewidth=0.4)
ax.set_title("Score vs Comments", fontsize=12, fontweight="bold")
ax.set_xlabel("Score")
ax.set_ylabel("Comments")
ax.legend(fontsize=8)
ax.grid(True, linestyle="--", alpha=0.4, color="#cccccc")
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("outputs/dashboard.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("Saved: outputs/dashboard.png")

print("\nAll done! Charts saved in the outputs/ folder:")
print("  outputs/chart1_top_stories.png")
print("  outputs/chart2_categories.png")
print("  outputs/chart3_scatter.png")
print("  outputs/dashboard.png  (bonus)")
