from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

# ============================= Asteroid Schemas =============================
class AsteroidBase(BaseModel): 
    name: str = Field(..., description="The name of the asteroid")
    nasa_jpl_url: str = Field(..., description="The NASA JPL URL of the asteroid")
    absolute_magnitude: float = Field(..., description="The absolute magnitude of the asteroid")
    is_potentially_hazardous: bool = Field(..., description="Whether the asteroid is potentially hazardous")
    close_approach_date: str = Field(..., description="The date of the closest approach to Earth")
    close_approach_date_full: str = Field(..., description="The full date of the closest approach to Earth")
    epoch_date_close_approach: int = Field(..., description="The epoch date of the closest approach to Earth")
    relative_velocity: float = Field(..., description="The relative velocity of the asteroid")
    miss_distance: float = Field(..., description="The miss distance of the asteroid")
    orbiting_body: str = Field(..., description="The body the asteroid is orbiting")
    created_at: datetime = Field(..., description="The date and time the asteroid was created")
    updated_at: datetime = Field(..., description="The date and time the asteroid was updated")

class AsteroidCreate(AsteroidBase): #input schema for creating a new asteroid
    pass

class Asteroid(AsteroidBase): #output schema for a single asteroid
    id: int = Field(..., description="The unique identifier of the asteroid")

    class Config: 
        from_attributes = True

class AsteroidList(BaseModel): #output schema for a list of asteroids
    asteroids: List[Asteroid] = Field(..., description="The list of asteroids")

class AsteroidUpdate(AsteroidBase): #input schema for updating an existing asteroid
    pass

class AsteroidDelete(BaseModel): #input schema for deleting an existing asteroid
    id: int = Field(..., description="The unique identifier of the asteroid to delete")