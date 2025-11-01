from typing import List

from pydantic import BaseModel


class Point(BaseModel):
    coordinates: List[float]


class PythagoreanSupportMachineInput(BaseModel):
    points: List[Point]
    n_groups: int


class Group(BaseModel):
    points: List[Point]
    n_points: int
    centroid: Point


class PythagoreanSupportMachineOutput(BaseModel):
    groups: List[Group]
    n_dimensions: int


class PointStatus(BaseModel):
    probability: float
    distance: float
    point: Point


class Node(BaseModel):
    points_status: List[PointStatus]
    centroid: Point


class MainMatrix(BaseModel):
    nodes: List[Node]
