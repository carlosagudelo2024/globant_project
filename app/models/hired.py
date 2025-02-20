from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Hired(Base):
    __tablename__ = "hired"
    # Declaración hired
    id = Column(Integer, primary_key=True)
    name_emp = Column(String(150), nullable = True)
    datet = Column(String(50), nullable = True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable = True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable = True)

    # Relaciones
    #department = relationship("Department", back_populates="hired")
    #job = relationship("Job", back_populates="hired")

    def __repr__(self):
        return f"Hired(id={self.id}, name={self.name_emp})"