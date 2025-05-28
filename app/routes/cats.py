from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
import httpx

router = APIRouter()

# TheCatAPI — валідація породи
async def validate_breed(breed: str):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.thecatapi.com/v1/breeds")
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch cat breeds")
        breeds = response.json()
        breed_names = [b["name"].lower() for b in breeds]
        if breed.lower() not in breed_names:
            raise HTTPException(status_code=400, detail=f"Breed '{breed}' is not valid")


@router.post("/", response_model=schemas.CatOut, status_code=status.HTTP_201_CREATED)
async def create_cat(cat: schemas.CatCreate, db: Session = Depends(get_db)):
    await validate_breed(cat.breed)
    return crud.create_cat(db, cat)


@router.get("/", response_model=list[schemas.CatOut])
def list_cats(db: Session = Depends(get_db)):
    return crud.get_cats(db)


@router.get("/{cat_id}", response_model=schemas.CatOut)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = crud.get_cat(db, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


@router.patch("/{cat_id}", response_model=schemas.CatOut)
def update_salary(cat_id: int, update: schemas.CatUpdate, db: Session = Depends(get_db)):
    return crud.update_cat_salary(db, cat_id, update.salary)


@router.delete("/{cat_id}")
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    return crud.delete_cat(db, cat_id)