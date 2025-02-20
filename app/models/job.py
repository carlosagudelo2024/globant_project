# models/job.py
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database.database import Base

class Job(Base):
    __tablename__ = "jobs"
    # Declaración job
    id = Column(Integer, primary_key=True)
    job = Column(String(150))
    
    # Relación con employees
    #employees = relationship("Hired", back_populates="job")

    def __repr__(self):
        return f"Job(id={self.id}, job={self.job})"