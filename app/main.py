# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.services.csv_processor import CSVProcessor  
from app.services.metrics import MetricsService
from typing import List, Dict
import uvicorn

app = FastAPI(title="Data Migration API")
csv_processor = CSVProcessor()
metrics_service = MetricsService() 

@app.post("/api/upload/csv/{table_type}")
async def upload_csv(table_type: str, file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    if table_type not in ["departments", "jobs", "hired"]:
        raise HTTPException(status_code=400, detail="Invalid table type")
    
    try:
        file_path = await csv_processor.save_csv(file)
        csv_processor.process_batch(file_path, table_type)
        return {"message": f"Successfully processed {table_type} data"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)  

@app.get("/metrics/quarterly-hires", tags=["metrics"])
async def get_quarterly_hires():
    """
    Get number of employees hired for each job and department in 2021 by quarter.
    Returns data ordered alphabetically by department and job.
    """
    try:
        return metrics_service.get_quarterly_hires()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics/departments-above-mean", tags=["metrics"])
async def get_departments_above_mean():
    """
    Get departments that hired more employees than the mean in 2021.
    Returns data ordered by number of employees hired (descending).
    """
    try:
        return metrics_service.get_departments_above_mean()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))