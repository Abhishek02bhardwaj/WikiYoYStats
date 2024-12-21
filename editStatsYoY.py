import requests
import pandas as pd

def fetch_language_codes():
    """
    Fetch language codes for all Wikipedia projects from the sitematrix API.
    """
    url = "https://meta.wikimedia.org/w/api.php"
    params = {
        "action": "sitematrix",
        "smlangprop": "code|name|localname",
        "smtype": "language",
        "format": "json"
    }
    
    try:
        response = requests.get(url, params=params)
        print(response)
        
        # Check if the response is valid
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code} from the API.")
            print(f"Response text: {response.text}")
            return []
        
        # Attempt to parse JSON
        try:
            data = response.json()
            print(data)
        except requests.exceptions.JSONDecodeError:
            print("Error: Unable to decode JSON response.")
            print(f"Response content: {response.text}")
            return []
        
        # Process the data
        if "sitematrix" in data:
            language_codes = []
            for key, value in data["sitematrix"].items():
                if key.isdigit():  # Only process numeric keys (language entries)
                    language_code = value.get("code")
                    if language_code:
                        language_codes.append(language_code)
            print(language_codes)
            return language_codes
        else:
            print("No 'sitematrix' found in the response.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return []


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
            print(f"No 'items' found in the response for project: {project}.")
            return 0
    else:
        print(f"Error {response.status_code} for project {project}: {response.text}")
        return 0

def calculate_percentage_change_per_language(start_year, end_year):
    """
    Calculate the percentage change in edits for all Wikipedia language projects.
    """
    language_codes = fetch_language_codes()
    results = []
    
    for code in language_codes:
        project = f"{code}.wikipedia.org"
        print(f"Processing project: {project}...")  # Track progress
        
        # Fetch edits data for start year
        start_date = f"{start_year}0101"
        end_date = f"{start_year}1231"
        start_year_edits = fetch_edits_data(project, "all-editor-types", "content", "all-activity-levels", "monthly", start_date, end_date)
        
        # Fetch edits data for end year
        start_date_end_year = f"{end_year}0101"
        end_date_end_year = f"{end_year}1231"
        end_year_edits = fetch_edits_data(project, "all-editor-types", "content", "all-activity-levels", "monthly", start_date_end_year, end_date_end_year)
        
        # Calculate percentage change
        if start_year_edits > 0:
            percentage_change = ((end_year_edits - start_year_edits) / start_year_edits) * 100
        else:
            percentage_change = None  # No valid data to calculate percentage change
        
        # Append results
        results.append({
            "language": code,
            "start_year_edits": start_year_edits,
            "end_year_edits": end_year_edits,
            "percentage_change": percentage_change
        })
    
    # Convert results to DataFrame for easier analysis
    return pd.DataFrame(results)

# Parameters
start_year = 2023
end_year = 2024

# Calculate percentage change for all Wikipedia language projects
results_df = calculate_percentage_change_per_language(start_year, end_year)

# Display or save results
print(results_df)
# results_df.to_csv("wikipedia_edits_percentage_change.csv", index=False)
