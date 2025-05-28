from fastapi import FastAPI
from app.routes import cats, missions
from app.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(cats.router, prefix="/cats", tags=["Cats"])
app.include_router(missions.router, prefix="/missions", tags=["Missions"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
