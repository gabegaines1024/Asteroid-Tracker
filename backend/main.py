from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import schemas
from api_client import fetch_nasa_asteroids
from database import engine, get_db
from models import Base

# create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Asteroid Tracker API", description="API for tracking asteroids")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Asteroid Tracker API"}


@app.get("/asteroids", response_model=List[schemas.Asteroid])
def get_asteroids(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[schemas.Asteroid]:
    try:
        return crud.get_all_asteroids(db, skip=skip, limit=limit)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to get asteroids: {exc}") from exc


@app.get("/asteroids/{asteroid_id}", response_model=schemas.Asteroid)
def get_asteroid_by_id(asteroid_id: int, db: Session = Depends(get_db)) -> schemas.Asteroid:
    try:
        return crud.get_asteroid_by_id(db, asteroid_id)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to get asteroid: {exc}") from exc


@app.post("/asteroids", response_model=schemas.Asteroid, status_code=201)
def create_asteroid(asteroid: schemas.AsteroidCreate, db: Session = Depends(get_db)) -> schemas.Asteroid:
    try:
        return crud.create_asteroid(db, asteroid)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to create asteroid: {exc}") from exc


@app.put("/asteroids/{asteroid_id}", response_model=schemas.Asteroid)
def update_asteroid(
    asteroid_id: int, asteroid: schemas.AsteroidUpdate, db: Session = Depends(get_db)
) -> schemas.Asteroid:
    try:
        return crud.update_asteroid(db, asteroid_id, asteroid)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to update asteroid: {exc}") from exc


@app.delete("/asteroids/{asteroid_id}", response_model=schemas.AsteroidDelete)
def delete_asteroid(asteroid_id: int, db: Session = Depends(get_db)) -> schemas.AsteroidDelete:
    try:
        return crud.delete_asteroid(db, asteroid_id)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to delete asteroid: {exc}") from exc


@app.get("/asteroids/filter/hazardous", response_model=List[schemas.Asteroid])
def get_hazardous_asteroids(db: Session = Depends(get_db)) -> List[schemas.Asteroid]:
    try:
        return crud.get_all_asteroids(db, hazardous=True)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to get hazardous asteroids: {exc}") from exc


@app.get("/asteroids/filter/not_hazardous", response_model=List[schemas.Asteroid])
def get_not_hazardous_asteroids(db: Session = Depends(get_db)) -> List[schemas.Asteroid]:
    try:
        return crud.get_all_asteroids(db, hazardous=False)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to get non-hazardous asteroids: {exc}") from exc


@app.post("/asteroids/fetch", response_model=List[schemas.Asteroid])
def fetch_asteroids(payload: schemas.FetchRequest, db: Session = Depends(get_db)) -> List[schemas.Asteroid]:
    try:
        asteroids_to_create = fetch_nasa_asteroids(payload.start_date.isoformat(), payload.end_date.isoformat())
        created_asteroids: List[schemas.Asteroid] = []
        for asteroid in asteroids_to_create:
            created_asteroids.append(crud.create_asteroid(db, asteroid))
        return created_asteroids
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch asteroids: {exc}") from exc


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
