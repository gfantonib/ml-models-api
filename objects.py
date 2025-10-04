from typing import List, Optional, Tuple

from pydantic import BaseModel, confloat


class AntColonyModelInput(BaseModel):
    points: List[Tuple[float, float]]


class AntColonyModelOutput(BaseModel):
    path: List[Tuple[float, float]]
    distance: float


class AntColonyModelParams(BaseModel):
    alpha: float = 3.0
    beta: float = 2.0
    evaporation_rate: confloat(gt=0, lt=1) = 0.5
    initial_pheromone: float = 1.0


class Point(BaseModel):
    idx: int
    x: float
    y: float


class Segment(BaseModel):
    idx: int
    distance: float
    point_a: Point
    point_b: Point
    probability: Optional[float] = None
    marks: Optional[int] = None


class ProbabilityMatrix(BaseModel):
    matrix: List[List[Segment]]


class AntTrail(BaseModel):
    idx: int
    trail: List[Segment]
    total_distance: float


class AntsTrails(BaseModel):
    trails: List[AntTrail]


class Pheromone(BaseModel):
    idx: int
    pheromone: float
    point_a: Point
    point_b: Point


class PheromoneMatrix(BaseModel):
    matrix: List[List[Pheromone]]
