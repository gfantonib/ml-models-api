import random
from typing import Any, List, Tuple

import numpy as np
from objects import Point, Segment
from params import AntColonyModelParams


def calc_distance(a: Point, b: Point) -> float:
    dx = a.x - b.x
    dy = a.y - b.y
    return (dx**2 + dy**2) ** 0.5


def get_segment_pheromone_density(
    segment: Segment, model_params: AntColonyModelParams
) -> float:
    pheromone_density = np.power(segment.pheromone, model_params.alpha) / np.power(
        segment.distance, model_params.beta
    )
    return pheromone_density


def random_points(n_points: int, max_val: int) -> List[Tuple[int, int]]:
    points = set()
    while len(points) < n_points:
        p = (random.randint(0, max_val), random.randint(0, max_val))
        points.add(p)  # set automatically ignores duplicates
    return list(points)


def eject_object(object: Any, name: str = ""):
    path = object.__class__.__name__ + name + ".json"
    with open(path, "w") as f:
        f.write(object.model_dump_json())
