import requests

def fetch_edits_data(project, editor_type, page_type, activity_level, granularity, start_date, end_date):
    """
    Fetch total number of edits from the Wikimedia API for the given time range.
    """
    url = f"https://wikimedia.org/api/rest_v1/metrics/edited-pages/aggregate/{project}/{editor_type}/{page_type}/{activity_level}/{granularity}/{start_date}/{end_date}"
    headers = {"User-Agent": "WikiExplorer/0.1 (contact: your-email@example.com)"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if "items" in data and data["items"]:
            # Sum the number of edits for the specified range (total edits per month)
            total_edits = sum(item["results"][0]["edited_pages"] for item in data["items"] if item["results"])
            return total_edits
        else:
            print(f"No 'items' found in the response for project: {project}.")
            return 0
    else:
        print(f"Error {response.status_code} for project {project}: {response.text}")
        return 0

def edits_percent_change(project, start_date, end_date, editor_type="all-editor-types", page_type="content"):
    """
    Calculate the percentage change in the total number of edits between two dates.
    """
    # Fetch total edits for the start date range
    start_edits = fetch_edits_data(
        project, editor_type, page_type, "all-activity-levels", "monthly",
        f"{start_date[:4]}0101", f"{start_date[:4]}1231"
    )
    
    # Fetch total edits for the end date range
    end_edits = fetch_edits_data(
        project, editor_type, page_type, "all-activity-levels", "monthly",
        f"{end_date[:4]}0101", f"{end_date[:4]}1231"
    )
    
    if start_edits > 0:
        percentage_change = ((end_edits - start_edits) / start_edits) * 100
    else:
        percentage_change = None  # Handle case where start edits are zero
    
    return {
        "percentage": percentage_change,
        "start_avg_edits": start_edits,
        "end_avg_edits": end_edits
    }
