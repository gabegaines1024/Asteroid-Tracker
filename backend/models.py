from datetime import datetime
from sqlalchemy import Mapped, mapped_column,  Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func 
from database import Base

class Asteroid(Base):
    __tablename__ = "asteroids"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    nasa_jpl_url: Mapped[str] = mapped_column(String, index=True)
    absolute_magnitude: Mapped[float] = mapped_column(Float)
    is_potentially_hazardous: Mapped[bool] = mapped_column(Boolean)
    close_approach_date: Mapped[str] = mapped_column(String, index=True)
    close_approach_date_full: Mapped[str] = mapped_column(String, index=True)
    epoch_date_close_approach: Mapped[int] = mapped_column(Integer, index=True)
    relative_velocity: Mapped[float] = mapped_column(Float)
    miss_distance: Mapped[float] = mapped_column(Float)
    orbiting_body: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
