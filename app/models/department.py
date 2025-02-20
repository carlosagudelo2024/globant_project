# models/department.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class Department(Base):
    __tablename__ = "departments"
    # Declaración departments
    id = Column(Integer, primary_key=True)
    department = Column(String(150))
    

    # Relación con hired
    #hired = relationship("Hired", back_populates="department")

    def __repr__(self):
        return f"Department(id={self.id}, department={self.department})"