from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Competency(Base):
    __tablename__ = "competencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(String(500))

    level_definitions = relationship(
        "CompetencyLevelDefinition", back_populates="competency", cascade="all, delete-orphan"
    )
    role_requirements = relationship(
        "RoleCompetencyRequirement", back_populates="competency", cascade="all, delete-orphan"
    )
    assessments = relationship("EmployeeCompetencyAssessment", back_populates="competency")
    activity_mappings = relationship(
        "DevelopmentActivityCompetencyMapping", back_populates="competency", cascade="all, delete-orphan"
    )


class CompetencyLevelDefinition(Base):
    __tablename__ = "competency_level_definitions"

    id = Column(Integer, primary_key=True, index=True)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
    level_name = Column(String(50), nullable=False)
    level_order = Column(Integer, nullable=False)
    description = Column(String(500))

    competency = relationship("Competency", back_populates="level_definitions")


class RoleCompetencyRequirement(Base):
    __tablename__ = "role_competency_requirements"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(100), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
    required_level_name = Column(String(50), nullable=False)

    competency = relationship("Competency", back_populates="role_requirements")
