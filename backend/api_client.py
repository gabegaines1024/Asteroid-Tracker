import os
from typing import List

import requests
from dotenv import load_dotenv

import schemas

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_API_URL = "https://api.nasa.gov/neo/rest/v1/feed"


def _safe_float(value: str | float | None) -> float:
    try:
        return float(value) if value is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


def fetch_nasa_asteroids(start_date: str, end_date: str) -> List[schemas.AsteroidCreate]:
    if not start_date or not end_date:
        raise ValueError("Start and end dates are required")
    if start_date > end_date:
        raise ValueError("Start date must be before end date")
    if not NASA_API_KEY:
        raise ValueError("NASA API key is not set")

    params = {
        "start_date": start_date,
        "end_date": end_date,
        "api_key": NASA_API_KEY,
    }

    try:
        response = requests.get(NASA_API_URL, params=params, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ValueError(f"Failed to reach NASA API: {exc}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise ValueError("NASA API returned invalid JSON") from exc

    near_earth_objects = data.get("near_earth_objects", {})

    asteroids: List[schemas.AsteroidCreate] = []
    for asteroid_date, asteroid_list in near_earth_objects.items():
        for asteroid in asteroid_list:
            close_approaches = asteroid.get("close_approach_data", [])
            close_approach = close_approaches[0] if close_approaches else {}

            relative_velocity_data = close_approach.get("relative_velocity", {})
            miss_distance_data = close_approach.get("miss_distance", {})

            diameter_data = asteroid.get("estimated_diameter", {}).get("kilometers", {})

            asteroids.append(
                schemas.AsteroidCreate(
                    name=asteroid.get("name", "Unknown"),
                    nasa_jpl_url=asteroid.get("nasa_jpl_url", ""),
                    absolute_magnitude=_safe_float(asteroid.get("absolute_magnitude_h")),
                    is_potentially_hazardous=asteroid.get("is_potentially_hazardous_asteroid", False),
                    estimated_diameter_min=_safe_float(diameter_data.get("estimated_diameter_min")),
                    estimated_diameter_max=_safe_float(diameter_data.get("estimated_diameter_max")),
                    close_approach_date=close_approach.get("close_approach_date", asteroid_date),
                    close_approach_date_full=close_approach.get("close_approach_date_full", ""),
                    epoch_date_close_approach=int(close_approach.get("epoch_date_close_approach", 0) or 0),
                    relative_velocity=_safe_float(relative_velocity_data.get("kilometers_per_second")),
                    miss_distance=_safe_float(miss_distance_data.get("kilometers")),
                    orbiting_body=close_approach.get("orbiting_body", ""),
                )
            )

    return asteroids
