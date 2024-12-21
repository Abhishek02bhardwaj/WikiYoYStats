import requests
import pandas as pd
from datetime import datetime

def fetch_edits_data(project, editor_type, page_type, activity_level, granularity, start_date, end_date):
    """
    Fetch total number of edits from the Wikimedia API for the given time range.
    """
    url = f"https://wikimedia.org/api/rest_v1/metrics/edited-pages/aggregate/{project}/{editor_type}/{page_type}/{activity_level}/{granularity}/{start_date}/{end_date}"
    headers = {"User-Agent": "WikiExplorer/0.1 (contact: abhishek02bhardwaj.er@gmail.com)"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if "items" in data and data["items"]:
            # Sum the number of edits for the specified range (total edits per month)
            total_edits = sum(item["results"][0]["edited_pages"] for item in data["items"] if item["results"])
            return total_edits
        else:
            print("No 'items' found in the response.")
            return 0
    else:
        print(f"Error {response.status_code}: {response.text}")
        return 0

def calculate_percentage_change(start_year, end_year, project="en.wikipedia.org", editor_type="all-editor-types", page_type="content"):
    """
    Calculate the percentage change in the number of edits YoY.
    """
    # Define the start and end dates for the two years
    start_date = f"{start_year}0101"  # Start of the start year
    end_date = f"{start_year}1231"    # End of the start year
    start_year_edits = fetch_edits_data(project, editor_type, page_type, "all-activity-levels", "monthly", start_date, end_date)
    print(start_year_edits)

    start_date_end_year = f"{end_year}0101"  # Start of the end year
    end_date_end_year = f"{end_year}1231"   # End of the end year
    end_year_edits = fetch_edits_data(project, editor_type, page_type, "all-activity-levels", "monthly", start_date_end_year, end_date_end_year)
    print(end_year_edits)

    # Calculate the percentage change
    if start_year_edits > 0:  # Avoid division by zero
        percentage_change = ((end_year_edits - start_year_edits) / start_year_edits) * 100
        return percentage_change
    else:
        print(f"No edits found in {start_year}. Cannot calculate percentage change.")
        return None

# Parameters
project = "en.wikipedia.org"
start_year = 2023
end_year = 2024

# Calculate the percentage change in number of edits YoY
percentage_change = calculate_percentage_change(start_year, end_year, project)

if percentage_change is not None:
    print(f"Percentage change in the number of edits from {start_year} to {end_year}: {percentage_change:.2f}%")
else:
    print("Could not calculate percentage change due to missing data.")
