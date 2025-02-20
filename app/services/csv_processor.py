# app/services/csv_processor.py
import pandas as pd
import numpy as np
from typing import List
import os
from dotenv import load_dotenv
from app.database.database import SessionLocal
from app.models.department import Department
from app.models.job import Job
from app.models.hired import Hired

load_dotenv()

class CSVProcessor:
    def __init__(self):
        self.upload_dir = os.getenv("CSV_UPLOAD_DIR", "./uploads")
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_csv(self, file) -> str:
        file_path = os.path.join(self.upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        return file_path

    def process_batch(self, file_path: str, model_type: str):
        df = pd.read_csv(file_path)
        
         #Manejo de vacios
        if model_type == "hired":
            # Valores nulos
            df = df.replace({np.nan: None})
            # Convertir columnas numéricas, reemplazando NaN con 0
            df['department_id'] = pd.to_numeric(df['department_id'], errors='coerce').fillna(0).astype(int)
            df['job_id'] = pd.to_numeric(df['job_id'], errors='coerce').fillna(0).astype(int)
            
            
        records = df.to_dict('records')
        
        db = SessionLocal()
        try:
            for batch in self._batch_generator(records, 1000):
                db_items = []  # Definicion db_items 
                
                if model_type == "departments":
                    db_items = [
                        Department(
                            id=record['id'],
                            department=record['department']
                        ) for record in batch
                    ]
                elif model_type == "jobs":
                    db_items = [
                        Job(
                            id=record['id'],
                            job=record['job']
                        ) for record in batch
                    ]
                elif model_type == "hired":
                    db_items = [
                        Hired(
                            id=int(record['id']),
                            name_emp=str(record['name_emp']),
                            datet=str(record['datet']),
                            department_id=int(record['department_id']),
                            job_id=int(record['job_id'])
                        ) for record in batch
                    ]
                
                if db_items:  # Solo si hay items para guardar
                    db.bulk_save_objects(db_items)
                    db.commit()
                    
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def _batch_generator(self, items, batch_size):
        for i in range(0, len(items), batch_size):
            yield items[i:i + batch_size]