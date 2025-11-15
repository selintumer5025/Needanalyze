from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Competency, DevelopmentActivity
from ..schemas.activity import (
    DevelopmentActivityCreate,
    DevelopmentActivityRead,
    DevelopmentActivityUpdate,
)
from ..schemas.competency import CompetencyCreate, CompetencyRead, CompetencyUpdate

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/competencies", response_model=List[CompetencyRead])
def list_competencies(db: Session = Depends(get_db)):
    return db.query(Competency).all()


@router.post("/competencies", response_model=CompetencyRead, status_code=status.HTTP_201_CREATED)
def create_competency(payload: CompetencyCreate, db: Session = Depends(get_db)):
    competency = Competency(**payload.dict())
    db.add(competency)
    db.commit()
    db.refresh(competency)
    return competency


@router.put("/competencies/{competency_id}", response_model=CompetencyRead)
def update_competency(competency_id: int, payload: CompetencyUpdate, db: Session = Depends(get_db)):
    competency = db.query(Competency).filter(Competency.id == competency_id).first()
    if not competency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competency not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(competency, field, value)
    db.commit()
    db.refresh(competency)
    return competency


@router.delete("/competencies/{competency_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_competency(competency_id: int, db: Session = Depends(get_db)):
    competency = db.query(Competency).filter(Competency.id == competency_id).first()
    if not competency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competency not found")
    db.delete(competency)
    db.commit()


@router.get("/activities", response_model=List[DevelopmentActivityRead])
def list_activities(db: Session = Depends(get_db)):
    return db.query(DevelopmentActivity).all()


@router.post("/activities", response_model=DevelopmentActivityRead, status_code=status.HTTP_201_CREATED)
def create_activity(payload: DevelopmentActivityCreate, db: Session = Depends(get_db)):
    activity = DevelopmentActivity(**payload.dict())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


@router.put("/activities/{activity_id}", response_model=DevelopmentActivityRead)
def update_activity(activity_id: int, payload: DevelopmentActivityUpdate, db: Session = Depends(get_db)):
    activity = db.query(DevelopmentActivity).filter(DevelopmentActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(activity, field, value)
    db.commit()
    db.refresh(activity)
    return activity


@router.delete("/activities/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(DevelopmentActivity).filter(DevelopmentActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    db.delete(activity)
    db.commit()
