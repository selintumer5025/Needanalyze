from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    seniority_level = Column(String(50), nullable=False)
    manager_name = Column(String(100))
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    assessments = relationship(
        "EmployeeCompetencyAssessment", back_populates="employee", cascade="all, delete-orphan"
    )
    plans = relationship(
        "EmployeeDevelopmentPlan", back_populates="employee", cascade="all, delete-orphan"
    )


class EmployeeCompetencyAssessment(Base):
    __tablename__ = "employee_competency_assessments"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
    current_level_name = Column(String(50), nullable=False)
    assessment_date = Column(Date, nullable=False)
    source = Column(String(50), nullable=False)

    employee = relationship("Employee", back_populates="assessments")
    competency = relationship("Competency", back_populates="assessments")


class EmployeeDevelopmentPlan(Base):
    __tablename__ = "employee_development_plans"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("development_activities.id"), nullable=False)
    status = Column(String(20), nullable=False, default="planned")
    planned_start_date = Column(Date)
    completion_date = Column(Date)

    employee = relationship("Employee", back_populates="plans")
    activity = relationship("DevelopmentActivity", back_populates="plans")
