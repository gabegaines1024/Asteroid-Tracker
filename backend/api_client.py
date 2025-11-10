import os
import requests
from typing import List, Dict
from dotenv import load_dotenv
import schemas

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_API_URL = "https://api.nasa.gov/neo/rest/v1/feed"

def fetch_nasa_asteroids(start_date: str, end_date: str) -> List[schemas.Asteroid]:
    #validate the input dates
    if not start_date or not end_date:
        raise ValueError("Start and end dates are required")
    if start_date > end_date:
        raise ValueError("Start date must be before end date")
    if not NASA_API_KEY:
        raise ValueError("NASA API key is not set")
    #fetch the asteroids from the NASA API
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "api_key": NASA_API_KEY,
    }
    try:
        #make the API request
        response = requests.get(NASA_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        asteroids = []
        #extract the close approach data data (get first approach)
        near_earth_objects = data.get({"near_earth_objects"}, {})

        #extract diameter data
        for asteroid_date, asteroid_data in near_earth_objects.items():
            for asteroid in asteroid_data:
                close_approach = asteroid.get("close_approach_data", [{}])[0]
                diameter = close_approach.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_max", 0)

                asteroid_create = schemas.AsteroidCreate(
                    name=asteroid.get("name", ""),
                    nasa_jpl_url=asteroid.get("nasa_jpl_url", ""),
                    absolute_magnitude=asteroid.get("absolute_magnitude", 0),
                    is_potentially_hazardous=asteroid.get("is_potentially_hazardous", False),
                    close_approach_date=asteroid_date,
                    close_approach_date_full=close_approach.get("close_approach_date_full", ""),
                    epoch_date_close_approach=close_approach.get("epoch_date_close_approach", 0),
                    relative_velocity=close_approach.get("relative_velocity", 0),
                    miss_distance=close_approach.get("miss_distance", 0),
                    orbiting_body=asteroid.get("orbiting_body", ""),
                )
                asteroids.append(asteroid_create)
        return asteroids
    except Exception as e:
        raise ValueError(f"Failed to fetch asteroids from NASA API: {str(e)}")
