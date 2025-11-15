from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Employee, EmployeeDevelopmentPlan
from ..schemas.plan import (
    EmployeeDevelopmentPlanCreate,
    EmployeeDevelopmentPlanRead,
    EmployeeDevelopmentPlanUpdate,
)
from ..schemas.recommendation import RecommendationResponse
from ..services.matching_service import generate_recommendations_for_employee

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/{employee_id}/recommendations", response_model=RecommendationResponse)
def get_employee_recommendations(employee_id: int, db: Session = Depends(get_db)):
    try:
        return generate_recommendations_for_employee(db, employee_id)
    except ValueError as exc:  # pragma: no cover - simple error mapping
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/{employee_id}/plan", response_model=List[EmployeeDevelopmentPlanRead])
def get_employee_plan(employee_id: int, db: Session = Depends(get_db)):
    plans = (
        db.query(EmployeeDevelopmentPlan)
        .options(joinedload(EmployeeDevelopmentPlan.activity))
        .filter(EmployeeDevelopmentPlan.employee_id == employee_id)
        .all()
    )
    return plans


@router.post("/{employee_id}/plan", response_model=EmployeeDevelopmentPlanRead, status_code=status.HTTP_201_CREATED)
def add_activity_to_plan(
    employee_id: int,
    payload: EmployeeDevelopmentPlanCreate,
    db: Session = Depends(get_db),
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    plan = EmployeeDevelopmentPlan(
        employee_id=employee_id,
        activity_id=payload.activity_id,
        status=payload.status,
        planned_start_date=payload.planned_start_date,
        completion_date=payload.completion_date,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.patch("/{employee_id}/plan/{plan_id}", response_model=EmployeeDevelopmentPlanRead)
def update_plan_entry(
    employee_id: int,
    plan_id: int,
    payload: EmployeeDevelopmentPlanUpdate,
    db: Session = Depends(get_db),
):
    plan = (
        db.query(EmployeeDevelopmentPlan)
        .options(joinedload(EmployeeDevelopmentPlan.activity))
        .filter(
            EmployeeDevelopmentPlan.employee_id == employee_id,
            EmployeeDevelopmentPlan.id == plan_id,
        )
        .first()
    )
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan entry not found")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(plan, field, value)
    db.commit()
    db.refresh(plan)
    return plan
