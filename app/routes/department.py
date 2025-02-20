# routes/department.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.database.database import SessionLocal
from app.models.department import Department
import pandas as pd
import io

router = APIRouter(
    prefix="/departments",
    tags=["departments"]
)

# DependencyInyección de dependencias
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Mapeo department
@router.post("/upload")
async def upload_departments(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos CSV")
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Procesar en lotes de 1000
        for i in range(0, len(df), 1000):
            batch_df = df[i:i + 1000]
            departments = [
                Department(
                    id=row['id'],
                    department=row['department']
                )
                for _, row in batch_df.iterrows()
            ]
            db.bulk_save_objects(departments)
            db.commit()
            
        return {"message": f"Se procesaron {len(df)} departamentos"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))