from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class CompetencyBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None


class CompetencyCreate(CompetencyBase):
    pass


class CompetencyUpdate(BaseModel):
    name: Optional[str]
    category: Optional[str]
    description: Optional[str]


class CompetencyLevelDefinitionBase(BaseModel):
    level_name: str
    level_order: int
    description: Optional[str] = None


class CompetencyLevelDefinitionCreate(CompetencyLevelDefinitionBase):
    competency_id: int


class CompetencyLevelDefinitionRead(CompetencyLevelDefinitionBase):
    id: int

    class Config:
        orm_mode = True


class CompetencyRead(CompetencyBase):
    id: int
    level_definitions: List[CompetencyLevelDefinitionRead] = []

    class Config:
        orm_mode = True


class RoleCompetencyRequirementBase(BaseModel):
    role_name: str
    competency_id: int
    required_level_name: str


class RoleCompetencyRequirementRead(RoleCompetencyRequirementBase):
    id: int

    class Config:
        orm_mode = True


class EmployeeCompetencyAssessmentBase(BaseModel):
    competency_id: int
    current_level_name: str
    assessment_date: date
    source: str


class EmployeeCompetencyAssessmentRead(EmployeeCompetencyAssessmentBase):
    id: int

    class Config:
        orm_mode = True
