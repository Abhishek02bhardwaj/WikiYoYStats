import requests
import pandas as pd
import numpy as np  # For NaN

def fetch_new_pages_data(project, editor_type, page_type, granularity, year):
    start_date = f"{year}0101"
    end_date = f"{year}1231"
    
    url = f"https://wikimedia.org/api/rest_v1/metrics/edited-pages/new/{project}/{editor_type}/{page_type}/{granularity}/{start_date}/{end_date}"
    headers = {"User-Agent": "WikiExplorer/0.1 (contact: abhishek02bhardwaj.er@gmail.com)"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        if "items" in data:
            pages_data = []
            for item in data["items"]:
                if "results" in item:
                    for result in item["results"]:
                        if "timestamp" in result and "new_pages" in result:
                            pages_data.append({
                                "date": result["timestamp"][:10],  # Extract YYYY-MM-DD from timestamp
                                "new_pages": result["new_pages"]
                            })
            if pages_data:  # If there's data to return
                return pd.DataFrame(pages_data)
            else:
                print(f"No new pages data found for {project} ({editor_type}, {page_type}, {granularity}, {year})")
                return pd.DataFrame()  # Return empty DataFrame if no data found
        else:
            print(f"No 'items' in response for project {project}")
            return pd.DataFrame()
    
    elif response.status_code == 404:
        print(f"Error 404: Data not found for project {project} ({editor_type}, {page_type}, {granularity}, {year}). Returning NaN.")
        return pd.DataFrame({'date': [None], 'new_pages': [np.nan]})  # Return NaN for 404 errors
    else:
        print(f"Error {response.status_code} for project {project}: {response.text}")
        return pd.DataFrame()

def calculate_yearly_total(pages_data_user, pages_data_anonymous):
    combined_df = pd.concat([pages_data_user, pages_data_anonymous], ignore_index=True)
    if 'new_pages' in combined_df.columns:  # Check if the column exists before summing
        total_new_pages = combined_df['new_pages'].sum()
        return total_new_pages
    else:
        print("Error: 'new_pages' column not found in the combined data.")
        return 0  # Return 0 if no data

def calculate_percentage_change(yearly_data):
    if len(yearly_data) != 2:
        print("Data must contain exactly two years for comparison.")
        return None

    years = sorted(yearly_data.keys())
    year1, year2 = years[0], years[1]
    value1, value2 = yearly_data[year1], yearly_data[year2]

    if value1 != 0:
        percentage_change = ((value2 - value1) / value1) * 100
        return percentage_change
    else:
        print(f"Year {year1} has zero new pages, cannot calculate percentage change.")
        return None

def fetch_language_codes():
    url = "https://meta.wikimedia.org/w/api.php"
    params = {
        "action": "sitematrix",
        "smlangprop": "code|name|localname",
        "smtype": "language",
        "format": "json"
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code} from the API.")
            return []
        
        data = response.json()
        
        if "sitematrix" in data:
            language_codes = []
            for key, value in data["sitematrix"].items():
                if key.isdigit():  # Only process numeric keys (language entries)
                    language_code = value.get("code")
                    if language_code:
                        language_codes.append(language_code)
            return language_codes
        else:
            print("No 'sitematrix' found in the response.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return []

# Parameters
page_type = "content"
granularity = "monthly"

# Specify the two years
year_1 = 2021
year_2 = 2024

# Fetch language codes for all Wikipedia projects
language_codes = fetch_language_codes()

# Dictionary to store percentage changes for all languages
percentage_changes = {}

# Loop through each language project and calculate the percentage change
for language_code in language_codes:
    project = f"{language_code}.wikipedia.org"

    # Fetch data for both years and both editor types (user, anonymous)
    pages_data_user_1 = fetch_new_pages_data(project, "user", page_type, granularity, year_1)
    pages_data_anonymous_1 = fetch_new_pages_data(project, "anonymous", page_type, granularity, year_1)

    pages_data_user_2 = fetch_new_pages_data(project, "user", page_type, granularity, year_2)
    pages_data_anonymous_2 = fetch_new_pages_data(project, "anonymous", page_type, granularity, year_2)

    # If no data found, skip this project
    if pages_data_user_1.empty and pages_data_anonymous_1.empty and pages_data_user_2.empty and pages_data_anonymous_2.empty:
        print(f"Skipping project {project} due to missing data.")
        continue

    # Calculate yearly totals for both years by combining user and anonymous data
    yearly_total_1 = calculate_yearly_total(pages_data_user_1, pages_data_anonymous_1)
    yearly_total_2 = calculate_yearly_total(pages_data_user_2, pages_data_anonymous_2)

    # Combine yearly totals into a dictionary
    yearly_data = {year_1: yearly_total_1, year_2: yearly_total_2}

    # Calculate the percentage change for this language project
    percentage_change = calculate_percentage_change(yearly_data)

    if percentage_change is not None:
        percentage_changes[language_code] = percentage_change
        print(f"{language_code}: {percentage_change:.2f}% change in new pages (Year {year_1} and Year {year_2})")

# Output the final results for all languages
if percentage_changes:
    print("\nPercentage change for all languages:")
    for language, change in percentage_changes.items():
        print(f"{language}: {change:.2f}%")
else:
    print("No percentage changes calculated.")
