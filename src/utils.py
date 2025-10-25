import csv
import os
import gspread
from google.oauth2.service_account import Credentials

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
    

def append_to_google_sheet(all_analytics, spreadsheet_id="166iro0j2OPew8fA78w2NQIELgpaZWcmpTR2gXl9I0Sg", worksheet_name="posts"):
    """
    Append LinkedIn analytics to Google Sheet without headers.
    """
    SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), "service_account.json")
    spreadsheet_id = "17oBPHGxD64iSdVp1pK72MItARyOdfLIRZO6DQipNs9U"
    worksheet_name = "posts"

    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,scopes=["https://www.googleapis.com/auth/spreadsheets"])
    
    if not all_analytics:
        print("⚠️ No analytics data to append.")
        return

    headers_order = ["URL", "Impressions", "Likes", "Comments", "Followers", "Reposts", "Saves", "Sends"]

    client = gspread.authorize(creds)

    # Open sheet
    sheet = client.open_by_key(spreadsheet_id).worksheet(worksheet_name)

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

    headers_order = ["URL", "Impressions", "Likes", "Comments", "Followers", "Reposts", "Saves", "Sends"]

    # Prepare rows with proper mapping
    rows = []
    for post in all_analytics:
        mapped_post = {new_key: post.get(orig_key, "") for orig_key, new_key in field_mapping.items()}
        rows.append([mapped_post.get(col, "") for col in headers_order])

    # Append rows without headers
    sheet.append_rows(rows, value_input_option="USER_ENTERED")
    print(f"✅ Appended {len(rows)} rows to Google Sheet '{worksheet_name}'.")