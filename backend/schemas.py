from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class AsteroidBase(BaseModel):
    name: str = Field(..., description="The name of the asteroid")
    nasa_jpl_url: str = Field(..., description="The NASA JPL URL of the asteroid")
    absolute_magnitude: float = Field(..., description="The absolute magnitude of the asteroid")
    is_potentially_hazardous: bool = Field(..., description="Whether the asteroid is potentially hazardous")
    estimated_diameter_min: float = Field(..., description="Estimated minimum diameter in kilometers")
    estimated_diameter_max: float = Field(..., description="Estimated maximum diameter in kilometers")
    close_approach_date: str = Field(..., description="The date of the closest approach to Earth")
    close_approach_date_full: str = Field(..., description="The full date of the closest approach to Earth")
    epoch_date_close_approach: int = Field(..., description="The epoch date of the closest approach to Earth")
    relative_velocity: float = Field(..., description="The relative velocity of the asteroid in km/s")
    miss_distance: float = Field(..., description="The miss distance of the asteroid in kilometers")
    orbiting_body: str = Field(..., description="The body the asteroid is orbiting")


class AsteroidCreate(AsteroidBase):
    pass


class AsteroidUpdate(BaseModel):
    name: Optional[str] = Field(None, description="The name of the asteroid")
    nasa_jpl_url: Optional[str] = Field(None, description="The NASA JPL URL of the asteroid")
    absolute_magnitude: Optional[float] = Field(None, description="The absolute magnitude of the asteroid")
    is_potentially_hazardous: Optional[bool] = Field(None, description="Whether the asteroid is potentially hazardous")
    estimated_diameter_min: Optional[float] = Field(None, description="Estimated minimum diameter in kilometers")
    estimated_diameter_max: Optional[float] = Field(None, description="Estimated maximum diameter in kilometers")
    close_approach_date: Optional[str] = Field(None, description="The date of the closest approach to Earth")
    close_approach_date_full: Optional[str] = Field(None, description="The full date of the closest approach to Earth")
    epoch_date_close_approach: Optional[int] = Field(None, description="The epoch date of the closest approach to Earth")
    relative_velocity: Optional[float] = Field(None, description="The relative velocity of the asteroid in km/s")
    miss_distance: Optional[float] = Field(None, description="The miss distance of the asteroid in kilometers")
    orbiting_body: Optional[str] = Field(None, description="The body the asteroid is orbiting")


class Asteroid(AsteroidBase):
    id: int = Field(..., description="The unique identifier of the asteroid")
    created_at: datetime = Field(..., description="The date and time the asteroid record was created")
    updated_at: datetime = Field(..., description="The date and time the asteroid record was last updated")

    class Config:
        from_attributes = True


class AsteroidDelete(BaseModel):
    id: int = Field(..., description="The unique identifier of the deleted asteroid")
    deleted_at: datetime = Field(..., description="Timestamp of when the asteroid was deleted")


class FetchRequest(BaseModel):
    start_date: date = Field(..., description="Start date for the NASA feed request")
    end_date: date = Field(..., description="End date for the NASA feed request")


AsteroidList = List[Asteroid]
