"""Rule-based competency gap analysis and recommendation service."""
from collections import defaultdict
from typing import Dict, List

from sqlalchemy.orm import Session

from ..models import (
    CompetencyLevelDefinition,
    DevelopmentActivity,
    DevelopmentActivityCompetencyMapping,
    Employee,
    EmployeeCompetencyAssessment,
    RoleCompetencyRequirement,
)
from ..schemas.activity import DevelopmentActivityRead
from ..schemas.recommendation import (
    CompetencyGapRecommendation,
    DevelopmentJourneyStep,
    RecommendationResponse,
)

LEVEL_FALLBACK_ORDER = {
    "awareness": 1,
    "basic": 2,
    "intermediate": 3,
    "advanced": 4,
    "expert": 5,
}


def _normalize_level_name(name: str) -> str:
    return name.strip().lower()


def _level_order_map(levels: List[CompetencyLevelDefinition]) -> Dict[str, int]:
    return {
        _normalize_level_name(level.level_name): level.level_order
        for level in sorted(levels, key=lambda l: l.level_order)
    }


def _serialize_activity(activity: DevelopmentActivity) -> DevelopmentActivityRead:
    return DevelopmentActivityRead(
        id=activity.id,
        code=activity.code,
        name=activity.name,
        type=activity.type,
        modality=activity.modality,
        duration_hours=float(activity.duration_hours),
        provider=activity.provider,
        description=activity.description,
    )


def generate_recommendations_for_employee(db: Session, employee_id: int) -> RecommendationResponse:
    """Generate competency gap-based recommendations for the employee."""

    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise ValueError("Employee not found")

    # Query related data.
    requirements = (
        db.query(RoleCompetencyRequirement)
        .filter(RoleCompetencyRequirement.role_name == employee.role)
        .all()
    )
    assessments = (
        db.query(EmployeeCompetencyAssessment)
        .filter(EmployeeCompetencyAssessment.employee_id == employee.id)
        .all()
    )
    assessments_map = {assessment.competency_id: assessment for assessment in assessments}

    # Preload level orders per competency for quick gap calculations.
    competency_level_map: Dict[int, Dict[str, int]] = {}
    for req in requirements:
        if req.competency_id in competency_level_map:
            continue
        level_defs = (
            db.query(CompetencyLevelDefinition)
            .filter(CompetencyLevelDefinition.competency_id == req.competency_id)
            .all()
        )
        if level_defs:
            competency_level_map[req.competency_id] = _level_order_map(level_defs)

    # Preload activities by competency to avoid repetitive queries.
    mapping_rows = (
        db.query(DevelopmentActivityCompetencyMapping)
        .filter(
            DevelopmentActivityCompetencyMapping.competency_id.in_([req.competency_id for req in requirements])
        )
        .all()
    )
    activity_ids = {mapping.activity_id for mapping in mapping_rows}
    activities = (
        db.query(DevelopmentActivity)
        .filter(DevelopmentActivity.id.in_(activity_ids))
        .all()
    )
    activities_map = {activity.id: activity for activity in activities}

    mapping_by_competency: Dict[int, List[DevelopmentActivityCompetencyMapping]] = defaultdict(list)
    for mapping in mapping_rows:
        mapping_by_competency[mapping.competency_id].append(mapping)

    competency_gaps: List[CompetencyGapRecommendation] = []

    for requirement in requirements:
        level_orders = competency_level_map.get(requirement.competency_id)
        if not level_orders:
            continue
        target_level_order = level_orders.get(
            _normalize_level_name(requirement.required_level_name),
            LEVEL_FALLBACK_ORDER.get(_normalize_level_name(requirement.required_level_name), 0),
        )
        assessment = assessments_map.get(requirement.competency_id)
        current_level_order = (
            level_orders.get(_normalize_level_name(assessment.current_level_name)) if assessment else None
        )
        if current_level_order is not None and current_level_order >= target_level_order:
            continue

        gap_difference = target_level_order - (current_level_order or 0)
        awareness_activities: List[DevelopmentActivityRead] = []
        advanced_activities: List[DevelopmentActivityRead] = []
        journey_steps: List[DevelopmentJourneyStep] = []

        for mapping in mapping_by_competency.get(requirement.competency_id, []):
            activity = activities_map.get(mapping.activity_id)
            if not activity:
                continue
            serialized = _serialize_activity(activity)
            mapping_level_order = level_orders.get(
                _normalize_level_name(mapping.target_level_name),
                LEVEL_FALLBACK_ORDER.get(_normalize_level_name(mapping.target_level_name), 0),
            )
            if mapping_level_order <= 2:
                awareness_activities.append(serialized)
            else:
                advanced_activities.append(serialized)

        # Basic journey builder.
        journey_steps.append(
            DevelopmentJourneyStep(
                title="Step 1 - Awareness",
                description="Gain foundational knowledge before applying skills.",
                activities=awareness_activities[:2],
            )
        )
        journey_steps.append(
            DevelopmentJourneyStep(
                title="Step 2 - Practice",
                description="Apply learning through on-the-job assignments or projects.",
                activities=advanced_activities[:1],
            )
        )
        journey_steps.append(
            DevelopmentJourneyStep(
                title="Step 3 - Deep Expertise",
                description="Engage in advanced experiences, mentoring, or coaching.",
                activities=advanced_activities[1:3],
            )
        )

        competency_gaps.append(
            CompetencyGapRecommendation(
                competency_id=requirement.competency_id,
                competency_name=requirement.competency.name,
                current_level=assessment.current_level_name if assessment else None,
                target_level=requirement.required_level_name,
                gap_level_difference=gap_difference,
                awareness_activities=awareness_activities,
                advanced_activities=advanced_activities,
                journey=journey_steps,
            )
        )

    return RecommendationResponse(
        employee_id=employee.id,
        employee_name=f"{employee.first_name} {employee.last_name}",
        role=employee.role,
        department=employee.department,
        seniority_level=employee.seniority_level,
        competency_gaps=competency_gaps,
    )
