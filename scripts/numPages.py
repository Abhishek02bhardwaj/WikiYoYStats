import requests
import pandas as pd

def fetch_new_pages_data(project, editor_type, year, page_type, granularity):
    """
    Fetches the number of new pages created from the API for a given year.

    Parameters:
        project (str): Wikimedia project (e.g., "en.wikipedia.org").
        editor_type (str): Editor type ('user' or 'anonymous').
        page_type (str): Page type (e.g., "content").
        granularity (str): Data granularity (e.g., "monthly").
        year (int): Year for which data is fetched.

    Returns:
        DataFrame: DataFrame containing date and new pages data.
    """
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
                        else:
                            print(f"Warning: Missing 'timestamp' or 'new_pages' in result: {result}")
                else:
                    print(f"Warning: Missing 'results' key in item: {item}")
            
            return pd.DataFrame(pages_data)
        else:
            print("No data found in the 'items' section of the response.")
            return pd.DataFrame()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return pd.DataFrame()

def calculate_yearly_total(pages_data_user, pages_data_anonymous):
    """
    Calculates the total number of new pages created per year by combining 'user' and 'anonymous' data.

    Parameters:
        pages_data_user (DataFrame): DataFrame for 'user' editor type.
        pages_data_anonymous (DataFrame): DataFrame for 'anonymous' editor type.

    Returns:
        int: Total number of new pages created for the year.
    """
    # Combine user and anonymous data
    combined_df = pd.concat([pages_data_user, pages_data_anonymous], ignore_index=True)
    total_new_pages = combined_df['new_pages'].sum()
    return total_new_pages

def pages_percent_change(project, start_date, end_date):
    """
    Calculates the percentage change in new pages created between two years.

    Parameters:
        yearly_data (dict): Total new pages for each year.

    Returns:
        float: Percentage change in new pages created between the two years.
    """
    pages_data_user_1 = fetch_new_pages_data(project, "user", start_date, page_type = "content", granularity = "monthly")
    pages_data_anonymous_1 = fetch_new_pages_data(project, "anonymous", start_date, page_type = "content", granularity = "monthly")

    pages_data_user_2 = fetch_new_pages_data(project, "user", end_date, page_type = "content", granularity = "monthly")
    pages_data_anonymous_2 = fetch_new_pages_data(project, "anonymous", end_date, page_type = "content", granularity = "monthly")

    # Calculate yearly totals by combining user and anonymous data
    yearly_total_1 = calculate_yearly_total(pages_data_user_1, pages_data_anonymous_1)
    yearly_total_2 = calculate_yearly_total(pages_data_user_2, pages_data_anonymous_2)

    # Combine yearly totals into a dictionary
    yearly_data = {start_date: yearly_total_1, end_date: yearly_total_2}
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