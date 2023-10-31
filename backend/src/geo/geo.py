from pydantic import BaseModel
from geopy import distance

class Point(BaseModel):
    latitude: float
    longitude: float

def get_distance_between_two_points(point_a: Point, point_b: Point) -> float:
    return distance.distance(
        (point_a.latitude, point_a.longitude), 
        (point_b.latitude, point_b.longitude)
    ).miles