from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from .competency import EmployeeCompetencyAssessmentRead
from .plan import EmployeeDevelopmentPlanRead


class EmployeeBase(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    department: str
    role: str
    seniority_level: str
    manager_name: Optional[str] = None
    location: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: int

    class Config:
        orm_mode = True


class EmployeeWithAssessments(EmployeeRead):
    assessments: List[EmployeeCompetencyAssessmentRead] = []
    plans: List[EmployeeDevelopmentPlanRead] = []
