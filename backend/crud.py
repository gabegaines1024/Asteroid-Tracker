from fastapi import HTTPException
from collections.abc import Iterable
from typing import Optional, List
from datetime import datetime

from sqlalchemy.orm import Session

from . import models, schemas
from .schemas import Asteroid

# ============================= Asteroid CRUD Operations =============================
# Create a new asteroid
def create_asteroid(db: Session, asteroid: schemas.AsteroidCreate) -> models.Asteroid:
    db_asteroid = models.Asteroid(
        name=asteroid.name,
        nasa_jpl_url=asteroid.nasa_jpl_url,
        absolute_magnitude=asteroid.absolute_magnitude,
        is_potentially_hazardous=asteroid.is_potentially_hazardous,
        close_approach_date=asteroid.close_approach_date,
        close_approach_date_full=asteroid.close_approach_date_full,
        epoch_date_close_approach=asteroid.epoch_date_close_approach,
        relative_velocity=asteroid.relative_velocity,
        miss_distance=asteroid.miss_distance,
        orbiting_body=asteroid.orbiting_body,
    )
    try:
        db.add(db_asteroid)
        db.commit()
        db.refresh(db_asteroid)
        #convert SQLAlchemy model to Pydantic model and return as Asteroid object
        return models.Asteroid.model_validate(db_asteroid)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create asteroid: {str(e)}")

# Get all asteroids
def get_all_asteroids(db: Session) -> models.AsteroidList:
    try:
        asteroids = db.query(models.Asteroid).all()
        #convert SQLAlchemy model to Pydantic model and return as list of Asteroid objects
        return models.AsteroidList(asteroids=[models.Asteroid.model_validate(asteroid) for asteroid in asteroids]) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get asteroids: {str(e)}")

# Get an asteroid by ID
def get_asteroid_by_id(db: Session, asteroid_id: int) -> models.Asteroid:
    try:
        asteroid = db.query(models.Asteroid).filter(models.Asteroid.id == asteroid_id).first()
        if not asteroid:
            raise HTTPException(status_code=404, detail=f"Asteroid with ID {asteroid_id} not found")
        #convert SQLAlchemy model to Pydantic model and return as Asteroid object
        return models.Asteroid.model_validate({"id": asteroid.id, 
                                                "name": asteroid.name, 
                                                "nasa_jpl_url": asteroid.nasa_jpl_url, 
                                                "absolute_magnitude": asteroid.absolute_magnitude, 
                                                "is_potentially_hazardous": asteroid.is_potentially_hazardous, 
                                                "close_approach_date": asteroid.close_approach_date, 
                                                "close_approach_date_full": asteroid.close_approach_date_full, 
                                                "epoch_date_close_approach": asteroid.epoch_date_close_approach, 
                                                "relative_velocity": asteroid.relative_velocity, 
                                                "miss_distance": asteroid.miss_distance, 
                                                "orbiting_body": asteroid.orbiting_body, 
                                                "created_at": asteroid.created_at, 
                                                "updated_at": asteroid.updated_at}
                                                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get asteroid: {str(e)}")

# Update an asteroid
def update_asteroid(db: Session, asteroid_id: int, asteroid: schemas.AsteroidUpdate) -> models.Asteroid:
    try:
        db_asteroid = db.query(models.Asteroid).filter(models.Asteroid.id == asteroid_id).first()
        if not db_asteroid:
            raise HTTPException(status_code=404, detail=f"Asteroid with ID {asteroid_id} not found")
        #update the asteroid with the new data
        db_asteroid.name = asteroid.name
        db_asteroid.nasa_jpl_url = asteroid.nasa_jpl_url
        db_asteroid.absolute_magnitude = asteroid.absolute_magnitude
        db_asteroid.is_potentially_hazardous = asteroid.is_potentially_hazardous
        db_asteroid.close_approach_date = asteroid.close_approach_date
        db_asteroid.close_approach_date_full = asteroid.close_approach_date_full
        db_asteroid.epoch_date_close_approach = asteroid.epoch_date_close_approach
        db_asteroid.relative_velocity = asteroid.relative_velocity
        db_asteroid.miss_distance = asteroid.miss_distance
        db_asteroid.orbiting_body = asteroid.orbiting_body
        db_asteroid.updated_at = datetime.now()
        db.commit()
        db.refresh(db_asteroid)
        #convert SQLAlchemy model to Pydantic model and return as Asteroid object
        return models.Asteroid.model_validate({"updated_id": db_asteroid.id, "updated_at": datetime.now()})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update asteroid: {str(e)}")
    
# Delete an asteroid
def delete_asteroid(db: Session, asteroid_id: int) -> models.Asteroid:
    try:
        db_asteroid = db.query(models.Asteroid).filter(models.Asteroid.id == asteroid_id).first()
        if not db_asteroid:
            raise HTTPException(status_code=404, detail=f"Asteroid with ID {asteroid_id} not found")
        db.delete(db_asteroid)
        db.commit()
        #convert SQLAlchemy model to Pydantic model and return as Asteroid object
        return models.Asteroid.model_validate({"deleted_id": db_asteroid.id, "deleted_at": datetime.now()})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete asteroid: {str(e)}")