from typing import List, Tuple

from src.ant_colony_model.objects import (
    CollectionOfAntsTrails,
    Point,
    Segment,
    Trail,
    TrailMatrix,
)
from src.ant_colony_model.params import AntColonyModelParams
from src.ant_colony_model.trail_manager import TrailMatrixManager
from src.ant_colony_model.utils import calc_distance, eject_object, random_points


class AntColonyModel:
    def __init__(self, points: List[tuple]):
        self.matrix = self._build_trail_matrix(points)
        self.model_params = AntColonyModelParams()

    def _build_trail_matrix(self, points: List[tuple]) -> TrailMatrix:
        point_objs = [Point(idx=i + 1, x=pt[0], y=pt[1]) for i, pt in enumerate(points)]
        trails = []
        for i, from_p in enumerate(point_objs):
            segments = []
            for j, to_p in enumerate(point_objs):
                if i != j:
                    distance = calc_distance(from_p, to_p)
                    segment = Segment(
                        from_p=from_p, to_p=to_p, distance=distance, pheromone=1
                    )
                    segments.append(segment)
            trail = Trail(segments=segments)
            trails.append(trail)

        return TrailMatrix(matrix=trails)

    def _get_min_trail(self, trails: TrailMatrix) -> Trail:
        min_trail = None
        min_distance = float("inf")
        for trail in trails.matrix:
            if trail.total_distance < min_distance:
                min_distance = trail.total_distance
                min_trail = trail
        return min_trail

    def run(self) -> Tuple[Trail, CollectionOfAntsTrails]:

        n_iterations = self.model_params.n_iterations
        collection_of_ants_trails = []
        first_trail = None

        manager = TrailMatrixManager(self.matrix)

        for i in range(n_iterations):
            manager.update_probabilities()

            chosen_trails = manager.choose_trails()

            shortest_trail = self._get_min_trail(chosen_trails)
            collection_of_ants_trails.append(shortest_trail)
            if i == 0:
                first_trail = shortest_trail

            manager.update_pheromones(chosen_trails)

        last_trail = collection_of_ants_trails[-1]

        return (
            first_trail,
            last_trail,
            CollectionOfAntsTrails(trails=collection_of_ants_trails),
        )


if __name__ == "__main__":
    points = random_points(4, 5)
    model = AntColonyModel(points)
    first_trail, last_trail, collection_of_ants_trails = model.run()
    eject_object(first_trail, "_first_trail")
    eject_object(last_trail, "_last_trail")
    eject_object(collection_of_ants_trails, "_collection_of_ants_trails")
