from sqlalchemy import text
from typing import List, Dict
from app.database.database import SessionLocal

class MetricsService:
    @staticmethod
    def get_quarterly_hires():
        db = SessionLocal()
        try:
            query = text("""
                SELECT 
                    d.department,
                    j.job,
                    COALESCE(SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(SUBSTRING(h.datet, 1, 19) AS timestamp)) = 1 THEN 1 ELSE 0 END), 0) as Q1,
                    COALESCE(SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(SUBSTRING(h.datet, 1, 19) AS timestamp)) = 2 THEN 1 ELSE 0 END), 0) as Q2,
                    COALESCE(SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(SUBSTRING(h.datet, 1, 19) AS timestamp)) = 3 THEN 1 ELSE 0 END), 0) as Q3,
                    COALESCE(SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(SUBSTRING(h.datet, 1, 19) AS timestamp)) = 4 THEN 1 ELSE 0 END), 0) as Q4
                FROM test_globant.hired h
                JOIN test_globant.departments d ON h.department_id = d.id
                JOIN test_globant.jobs j ON h.job_id = j.id
                WHERE length(h.datet) = 20
                    AND EXTRACT(YEAR FROM CAST(SUBSTRING(h.datet, 1, 19) AS timestamp)) = 2021
                GROUP BY d.department, j.job
                ORDER BY d.department, j.job;
            """)
            
            result = db.execute(query)
            rows = result.fetchall()
            return [
                {
                    "department": row[0],
                    "job": row[1],
                    "Q1": int(row[2]),
                    "Q2": int(row[3]),
                    "Q3": int(row[4]),
                    "Q4": int(row[5])
                }
                for row in rows
            ]
        finally:
            db.close()

    @staticmethod
    def get_departments_above_mean():
        db = SessionLocal()
        try:
            query = text("""
                WITH dept_hires AS (
                    SELECT 
                        d.id,
                        d.department,
                        COUNT(*) as hired
                    FROM test_globant.hired h
                    JOIN test_globant.departments d ON h.department_id = d.id
                    WHERE length(h.datet) = 20 
                        AND EXTRACT(YEAR FROM to_timestamp(h.datet, 'YYYY-MM-DD"T"HH24:MI:SSZ')) = 2021
                    GROUP BY d.id, d.department
                ),
                mean_hires AS (
                    SELECT AVG(hired) as mean_hired
                    FROM dept_hires
                )
                SELECT 
                    id,
                    department,
                    hired
                FROM dept_hires
                WHERE hired > (SELECT mean_hired FROM mean_hires)
                ORDER BY hired DESC;
            """)
            
            result = db.execute(query)
            rows = result.fetchall()
            return [
                {
                    "id": row[0],
                    "department": row[1],
                    "hired": int(row[2])
                }
                for row in rows
            ]
        finally:
            db.close()