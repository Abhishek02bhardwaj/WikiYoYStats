from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List
import requests
import pandas as pd
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProjectData(BaseModel):
    projects: List[str]
    start_date: str
    end_date: str

def fetch_editors_data(project, editor_type, page_type, activity_level, granularity, start_date, end_date):
    """
    Fetch editor data from Wikimedia API for a specific time range and activity level.
    """
    url = f"https://wikimedia.org/api/rest_v1/metrics/editors/aggregate/{project}/{editor_type}/{page_type}/{activity_level}/{granularity}/{start_date}/{end_date}"
    headers = {"User-Agent": "WikiExplorer/0.1 (contact: abhishek02bhardwaj.er@gmail.com)"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "items" in data and data["items"]:
            editors = [
                {
                    "date": item["results"][i]["timestamp"][:10],  # Extract YYYY-MM-DD from timestamp
                    "editors": item["results"][i]["editors"]
                }
                for item in data["items"]
                for i in range(len(item["results"]))  # Iterate over the 'results' array
            ]
            return pd.DataFrame(editors)
        else:
            return pd.DataFrame()
    else:
        return pd.DataFrame()


def calculate_editors_more_than_five(editors_data_all, editors_data_1_to_5):
    """
    Calculate the number of editors with more than 5 edits.
    """
    merged_df = pd.merge(editors_data_all, editors_data_1_to_5, on="date", how="outer", suffixes=('_all', '_1_to_5'))
    merged_df['editors_more_than_5'] = merged_df['editors_all'] - merged_df['editors_1_to_5']
    merged_df['date'] = pd.to_datetime(merged_df['date'])
    return merged_df[['date', 'editors_more_than_5']].sort_values(by='date')


def get_rolling_average(project, date, editor_type, page_type):
    """
    Fetch data for the past 6 months and calculate the rolling average for active editors.
    """
    end_date = date
    start_date = (datetime.strptime(date, "%Y%m%d") - timedelta(days=180)).strftime("%Y%m%d")
    
    editors_data_all = fetch_editors_data(project, editor_type, page_type, "all-activity-levels", "monthly", start_date, end_date)
    editors_data_1_to_5 = fetch_editors_data(project, editor_type, page_type, "1..4-edits", "monthly", start_date, end_date)
    
    if not editors_data_all.empty and not editors_data_1_to_5.empty:
        active_editors_df = calculate_editors_more_than_five(editors_data_all, editors_data_1_to_5)
        return active_editors_df['editors_more_than_5'].mean()
    else:
        return None


def calculate_percentage_change(project, start_date, end_date, editor_type="all-editor-types", page_type="content"):
    """
    Calculate the percentage change in the number of editors between two dates.
    """
    # Get the rolling averages for the start and end dates
    start_avg = get_rolling_average(project, start_date, editor_type, page_type)
    end_avg = get_rolling_average(project, end_date, editor_type, page_type)
    
    if start_avg is not None and end_avg is not None:
        percentage_change = ((end_avg - start_avg) / start_avg) * 100
        return percentage_change
    else:
        return None

@app.post("/percentage_change/")
async def get_percentage_change(data: ProjectData):
    results = []

    for project in data.projects:
        try:
            percentage_change = calculate_percentage_change(
                project, data.start_date, data.end_date
            )
            if percentage_change is not None:
                results.append({
                    "metric": "Percentage Change",
                    "language": project.split(".")[0],
                    "value": round(percentage_change, 2),
                })
        except Exception as e:
            continue

    if not results:
        raise HTTPException(status_code=400, detail="No data available")

    return results
