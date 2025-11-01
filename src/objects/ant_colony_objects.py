from typing import List, Optional

from pydantic import BaseModel


class Point(BaseModel):
    idx: int
    x: float
    y: float


class Segment(BaseModel):
    from_p: Point
    to_p: Point
    distance: float
    pheromone: Optional[float] = None
    probability: Optional[float] = None


class Trail(BaseModel):
    segments: List[Segment]
    total_distance: Optional[float] = None


class TrailMatrix(BaseModel):
    matrix: List[Trail]


class CollectionOfAntsTrails(BaseModel):
    trails: List[Trail]


class PointRequest(BaseModel):
    x: float
    y: float


class AntColonyRequest(BaseModel):
    points: List[PointRequest]


class AntColonyResponse(BaseModel):
    first_trail: Trail
    last_trail: Trail
    collection_of_ants_trails: CollectionOfAntsTrails
