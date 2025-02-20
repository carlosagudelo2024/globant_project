# routes/job.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.database.database import SessionLocal
from app.models.job import Job
import pandas as pd
import io

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mapeo job
@router.post("/upload")
async def upload_jobs(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos CSV")
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Procesar en lotes de 1000
        for i in range(0, len(df), 1000):
            batch_df = df[i:i + 1000]
            jobs = [
                Job(
                    id=row['id'],
                    job=row['job']
                )
                for _, row in batch_df.iterrows()
            ]
            db.bulk_save_objects(jobs)
            db.commit()
            
        return {"message": f"Se procesaron {len(df)} trabajos"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))