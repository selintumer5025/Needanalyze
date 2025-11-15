from typing import List, Optional

from pydantic import BaseModel

from .activity import DevelopmentActivityRead


class DevelopmentJourneyStep(BaseModel):
    title: str
    description: str
    activities: List[DevelopmentActivityRead]


class CompetencyGapRecommendation(BaseModel):
    competency_id: int
    competency_name: str
    current_level: Optional[str]
    target_level: str
    gap_level_difference: int
    awareness_activities: List[DevelopmentActivityRead]
    advanced_activities: List[DevelopmentActivityRead]
    journey: List[DevelopmentJourneyStep]


class RecommendationResponse(BaseModel):
    employee_id: int
    employee_name: str
    role: str
    department: str
    seniority_level: str
    competency_gaps: List[CompetencyGapRecommendation]
