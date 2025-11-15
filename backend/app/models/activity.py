from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from ..database import Base


class DevelopmentActivity(Base):
    __tablename__ = "development_activities"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)
    modality = Column(String(50), nullable=False)
    duration_hours = Column(Numeric(6, 2), nullable=False)
    provider = Column(String(100), nullable=False)
    description = Column(String(500))

    competency_mappings = relationship(
        "DevelopmentActivityCompetencyMapping",
        back_populates="activity",
        cascade="all, delete-orphan",
    )
    plans = relationship("EmployeeDevelopmentPlan", back_populates="activity")


class DevelopmentActivityCompetencyMapping(Base):
    __tablename__ = "development_activity_competency_mappings"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("development_activities.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
    target_level_name = Column(String(50), nullable=False)

    activity = relationship("DevelopmentActivity", back_populates="competency_mappings")
    competency = relationship("Competency", back_populates="activity_mappings")
