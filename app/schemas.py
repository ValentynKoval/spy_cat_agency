from pydantic import BaseModel, Field
from typing import Optional, List


# ---------- Target ----------
class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = None
    is_completed: bool = False


class TargetCreate(TargetBase):
    pass


class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_completed: Optional[bool] = None


class TargetOut(TargetBase):
    id: int

    class Config:
        orm_mode = True


# ---------- Mission ----------
class MissionBase(BaseModel):
    is_completed: bool = False


class MissionCreate(MissionBase):
    targets: List[TargetCreate]


class MissionAssign(BaseModel):
    cat_id: int


class MissionOut(MissionBase):
    id: int
    cat_id: Optional[int]
    targets: List[TargetOut]

    class Config:
        orm_mode = True


# ---------- Cat ----------
class CatBase(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: float


class CatCreate(CatBase):
    pass


class CatUpdate(BaseModel):
    salary: float


class CatOut(CatBase):
    id: int

    class Config:
        orm_mode = True