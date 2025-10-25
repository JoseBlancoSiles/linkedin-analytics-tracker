import csv
import os

def convert_to_csv(all_analytics, filename="posts-analytics.csv", folder="data"):
    """
    Save LinkedIn post analytics to CSV with filtered and renamed fields
    for Google Sheets ingestion.
    
    Desired CSV structure:
    URL, Impressions, Likes, Comments, Followers, Reposts, Saves, Sends
    """
    if not all_analytics:
        print("⚠️ No analytics data to save.")
        return

    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)

    # Mapping original keys -> desired CSV headers
    field_mapping = {
        "url": "URL",
        "Impressions": "Impressions",
        "Reactions": "Likes",
        "Comments": "Comments",
        "Followers gained from this post": "Followers",
        "Reposts": "Reposts",
        "Saves": "Saves",
        "Sends on LinkedIn": "Sends"
    }

    # Filter and rename the data
    processed_data = []
    for post in all_analytics:
        filtered_post = {new_key: post.get(orig_key, "") for orig_key, new_key in field_mapping.items()}
        processed_data.append(filtered_post)

    # Write to CSV
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=field_mapping.values())
        writer.writeheader()
        writer.writerows(processed_data)

    print(f"✅ Post analytics saved to CSV: {path}")