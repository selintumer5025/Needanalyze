from datetime import date
from typing import Optional

from pydantic import BaseModel

from .activity import DevelopmentActivityRead


class EmployeeDevelopmentPlanBase(BaseModel):
    activity_id: int
    status: str = "planned"
    planned_start_date: Optional[date] = None
    completion_date: Optional[date] = None


class EmployeeDevelopmentPlanCreate(EmployeeDevelopmentPlanBase):
    pass


class EmployeeDevelopmentPlanUpdate(BaseModel):
    status: Optional[str]
    planned_start_date: Optional[date]
    completion_date: Optional[date]


class EmployeeDevelopmentPlanRead(EmployeeDevelopmentPlanBase):
    id: int
    activity: Optional[DevelopmentActivityRead]

    class Config:
        orm_mode = True
