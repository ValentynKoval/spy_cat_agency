from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app import models, schemas


# ---------- CAT ----------
def create_cat(db: Session, cat: schemas.CatCreate):
    db_cat = models.Cat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


def get_cats(db: Session):
    return db.query(models.Cat).all()


def get_cat(db: Session, cat_id: int):
    return db.query(models.Cat).filter(models.Cat.id == cat_id).first()


def update_cat_salary(db: Session, cat_id: int, salary: float):
    cat = get_cat(db, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    cat.salary = salary
    db.commit()
    db.refresh(cat)
    return cat


def delete_cat(db: Session, cat_id: int):
    cat = get_cat(db, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    db.delete(cat)
    db.commit()
    return {"ok": True}


# ---------- MISSION ----------
def create_mission(db: Session, mission: schemas.MissionCreate):
    if not (1 <= len(mission.targets) <= 3):
        raise HTTPException(status_code=400, detail="Mission must have 1 to 3 targets")

    db_mission = models.Mission(is_completed=False)
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)

    for target_data in mission.targets:
        target = models.Target(**target_data.dict(), mission_id=db_mission.id)
        db.add(target)
    db.commit()
    db.refresh(db_mission)
    return db_mission


def assign_cat_to_mission(db: Session, mission_id: int, cat_id: int):
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    cat = get_cat(db, cat_id)

    if not mission or not cat:
        raise HTTPException(status_code=404, detail="Mission or Cat not found")

    if mission.cat_id:
        raise HTTPException(status_code=400, detail="Mission already assigned")

    mission.cat_id = cat_id
    db.commit()
    db.refresh(mission)
    return mission


def get_missions(db: Session):
    return db.query(models.Mission).all()


def get_mission(db: Session, mission_id: int):
    return db.query(models.Mission).filter(models.Mission.id == mission_id).first()


def delete_mission(db: Session, mission_id: int):
    mission = get_mission(db, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if mission.cat_id:
        raise HTTPException(status_code=400, detail="Cannot delete mission assigned to a cat")
    db.delete(mission)
    db.commit()
    return {"ok": True}


# ---------- TARGET ----------
def update_target(db: Session, target_id: int, target_data: schemas.TargetUpdate):
    target = db.query(models.Target).filter(models.Target.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    if target.is_completed or target.mission.is_completed:
        raise HTTPException(status_code=400, detail="Cannot update a completed target or mission")

    if target_data.notes is not None:
        target.notes = target_data.notes
    if target_data.is_completed is not None:
        target.is_completed = target_data.is_completed
    db.commit()
    db.refresh(target)
    return target