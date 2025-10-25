from typing import List

from pydantic import BaseModel

from src.objects.ant_colony_objects import CollectionOfAntsTrails, Trail


class PointRequest(BaseModel):
    x: float
    y: float


class AntColonyRequest(BaseModel):
    points: List[PointRequest]


class AntColonyResponse(BaseModel):
    first_trail: Trail
    last_trail: Trail
    collection_of_ants_trails: CollectionOfAntsTrails
