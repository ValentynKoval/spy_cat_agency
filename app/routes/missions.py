from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.MissionOut, status_code=status.HTTP_201_CREATED)
def create_mission(mission: schemas.MissionCreate, db: Session = Depends(get_db)):
    return crud.create_mission(db, mission)


@router.get("/", response_model=list[schemas.MissionOut])
def list_missions(db: Session = Depends(get_db)):
    return crud.get_missions(db)


@router.get("/{mission_id}", response_model=schemas.MissionOut)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = crud.get_mission(db, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@router.delete("/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    return crud.delete_mission(db, mission_id)


@router.post("/{mission_id}/assign", response_model=schemas.MissionOut)
def assign_cat(mission_id: int, assignment: schemas.MissionAssign, db: Session = Depends(get_db)):
    return crud.assign_cat_to_mission(db, mission_id, assignment.cat_id)


@router.patch("/targets/{target_id}", response_model=schemas.TargetOut)
def update_target(target_id: int, update: schemas.TargetUpdate, db: Session = Depends(get_db)):
    return crud.update_target(db, target_id, update)