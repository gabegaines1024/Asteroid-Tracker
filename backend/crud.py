from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas


def create_asteroid(db: Session, asteroid: schemas.AsteroidCreate) -> schemas.Asteroid:
    db_asteroid = models.Asteroid(
        name=asteroid.name,
        nasa_jpl_url=asteroid.nasa_jpl_url,
        absolute_magnitude=asteroid.absolute_magnitude,
        is_potentially_hazardous=asteroid.is_potentially_hazardous,
        estimated_diameter_min=asteroid.estimated_diameter_min,
        estimated_diameter_max=asteroid.estimated_diameter_max,
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
        return schemas.Asteroid.model_validate(db_asteroid)
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create asteroid: {exc}") from exc


def get_all_asteroids(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    hazardous: Optional[bool] = None,
) -> List[schemas.Asteroid]:
    query = db.query(models.Asteroid)

    if hazardous is not None:
        query = query.filter(models.Asteroid.is_potentially_hazardous == hazardous)

    asteroids = query.offset(skip).limit(limit).all()
    return [schemas.Asteroid.model_validate(asteroid) for asteroid in asteroids]


def get_asteroid_by_id(db: Session, asteroid_id: int) -> schemas.Asteroid:
    asteroid = db.query(models.Asteroid).filter(models.Asteroid.id == asteroid_id).first()
    if not asteroid:
        raise HTTPException(status_code=404, detail=f"Asteroid with ID {asteroid_id} not found")
    return schemas.Asteroid.model_validate(asteroid)


def update_asteroid(db: Session, asteroid_id: int, asteroid: schemas.AsteroidUpdate) -> schemas.Asteroid:
    db_asteroid = db.query(models.Asteroid).filter(models.Asteroid.id == asteroid_id).first()
    if not db_asteroid:
        raise HTTPException(status_code=404, detail=f"Asteroid with ID {asteroid_id} not found")

    update_data = asteroid.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_asteroid, field, value)

    db_asteroid.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(db_asteroid)
        return schemas.Asteroid.model_validate(db_asteroid)
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update asteroid: {exc}") from exc


def delete_asteroid(db: Session, asteroid_id: int) -> schemas.AsteroidDelete:
    db_asteroid = db.query(models.Asteroid).filter(models.Asteroid.id == asteroid_id).first()
    if not db_asteroid:
        raise HTTPException(status_code=404, detail=f"Asteroid with ID {asteroid_id} not found")

    try:
        db.delete(db_asteroid)
        db.commit()
        return schemas.AsteroidDelete(id=asteroid_id, deleted_at=datetime.utcnow())
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete asteroid: {exc}") from exc
