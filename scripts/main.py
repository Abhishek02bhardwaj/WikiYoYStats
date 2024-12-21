from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from editCounts import edits_percent_change
from numEditors import editors_percent_change
from numPages import pages_percent_change

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
    project_types: List[str]
    start_date: str
    end_date: str
    comparison_metric: str


    
@app.post("/percentage_change/")
async def get_percentage_change(data: ProjectData):
    results = []

    for project in data.projects:
        for project_type in data.project_types:
            full_project_name = f"{project}.{project_type}.org"
            try:
                if data.comparison_metric == "edits":
                    percentage_change = edits_percent_change(
                        full_project_name, data.start_date, data.end_date
                    )
                elif data.comparison_metric == "editors":
                    percentage_change = editors_percent_change(
                        full_project_name, data.start_date, data.end_date
                    )
                elif data.comparison_metric == "articles":
                    percentage_change = pages_percent_change(
                        full_project_name, data.start_date, data.end_date
                    )
                else:
                    raise HTTPException(
                        status_code=400, detail=f"Invalid comparison metric: {data.comparison_metric}"
                    )

                if percentage_change is not None:
                    results.append({
                        "metric": f"Percentage change in {data.comparison_metric}",
                        "language": project.split(".")[0],
                        "project_type": project_type,
                        "value": round(percentage_change, 2),
                    })
            except Exception as e:
                continue

    if not results:
        raise HTTPException(status_code=400, detail="No data available")

    return results