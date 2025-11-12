from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from typing import List, Optional
from database import engine, get_db
from models import Base
import schemas
import crud
from api_client import fetch_nasa_asteroids
import uvicorn

#create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Asteroid Tracker API", description="API for tracking asteroids")

#CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to the Asteroid Tracker API"}

@app.get("/asteroids", response_model=List[schemas.Asteroid])
def get_asteroids(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[schemas.Asteroid]:
    try:
        asteroids = crud.get_all_asteroids(db, skip=skip, limit=limit)
        return asteroids
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get asteroids: {str(e)}")

@app.get(f"/asteroids/{id}", response_model=schemas.Asteroid)
def get_asteroid_by_id(id: int, db: Session = Depends(get_db)) -> schemas.Asteroid:
    try:
        asteroid = crud.get_asteroid_by_id(db, id)
        return asteroid
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get asteroid: {str(e)}")

@app.post("/asteroids", response_model=schemas.Asteroid)
def create_asteroid(asteroid: schemas.AsteroidCreate, db: Session = Depends(get_db)) -> schemas.Asteroid:
    try:
        _asteroid = crud.create_asteroid(db, asteroid)
        db.add(_asteroid)
        db.commit()
        db.refresh(_asteroid)
        return _asteroid
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create asteroid: {str(e)}")

@app.put("/asteroids/{id}", response_model=schemas.Asteroid)
def update_asteroid(id: int, asteroid: schemas.AsteroidUpdate, db: Session = Depends(get_db)) -> schemas.Asteroid:
    try:
        _asteroid = crud.update_asteroid(db, id, asteroid)
        db.commit()
        db.refresh(_asteroid)
        return _asteroid
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update asteroid: {str(e)}")


def delete_asteroid(id: int, db: Session = Depends(get_db)) -> schemas.AsteroidDelete:
    try:
        _asteroid = crud.delete_asteroid(db, id)
        db.commit()
        return _asteroid
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete asteroid: {str(e)}")

@app.get("/asteroids/filter/hazardous", response_model=List[schemas.Asteroid])
def get_hazardous_asteroids(db: Session = Depends(get_db)) -> List[schemas.Asteroid]:
    try:
        asteroids = crud.get_all_asteroids(db, hazardous=True)
        return asteroids
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get hazardous asteroids: {str(e)}")

@app.get("/asteroids/filter/not_hazardous", response_model=List[schemas.Asteroid])
def get_not_hazardous_asteroids(db: Session = Depends(get_db)) -> List[schemas.Asteroid]:
    try:
        asteroids = crud.get_all_asteroids(db, hazardous=False)
        return asteroids
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get not hazardous asteroids: {str(e)}")

@app.post("/asteroids/fetch", response_model=List[schemas.Asteroid])
def fetch_asteroids(start_date: str, end_date: str, db: Session = Depends(get_db)) -> List[schemas.Asteroid]:
    try:
        asteroids = fetch_nasa_asteroids(start_date, end_date)
        for asteroid in asteroids:
            _asteroid = crud.create_asteroid(db, asteroid)
            db.add(_asteroid)
        db.commit()
        return asteroids
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to fetch asteroids: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)