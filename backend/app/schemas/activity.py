from typing import List, Optional

from pydantic import BaseModel


class DevelopmentActivityBase(BaseModel):
    code: str
    name: str
    type: str
    modality: str
    duration_hours: float
    provider: str
    description: Optional[str] = None


class DevelopmentActivityCreate(DevelopmentActivityBase):
    pass


class DevelopmentActivityUpdate(BaseModel):
    code: Optional[str]
    name: Optional[str]
    type: Optional[str]
    modality: Optional[str]
    duration_hours: Optional[float]
    provider: Optional[str]
    description: Optional[str]


class DevelopmentActivityRead(DevelopmentActivityBase):
    id: int

    class Config:
        orm_mode = True


class DevelopmentActivityCompetencyMappingBase(BaseModel):
    activity_id: int
    competency_id: int
    target_level_name: str


class DevelopmentActivityCompetencyMappingRead(DevelopmentActivityCompetencyMappingBase):
    id: int

    class Config:
        orm_mode = True
