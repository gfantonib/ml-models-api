import json
import random
from typing import Any, List, Optional, Tuple

import numpy as np
from draft_plot import plot_first_and_last_trail, plot_total_distance_progression
from objects import (
    AntColonyModelInput,
    AntColonyModelParams,
    AntsTrails,
    AntTrail,
    Pheromone,
    PheromoneMatrix,
    Point,
    ProbabilityMatrix,
    Segment,
)


class AntColonyModel:
    def __init__(self, input: AntColonyModelInput):
        self.model_params = AntColonyModelParams()
        self._eject_object(self.model_params)
        self.points: List[Point] = self._get_points(input.points)
        self.probability_matrix: ProbabilityMatrix = self._build_probability_matrix()
        self._eject_object(self.probability_matrix)
        self.n_rows = len(self.probability_matrix.matrix)
        self.n_columns = len(self.probability_matrix.matrix[0])

    def _eject_object(self, object: Any, name: str = ""):
        path = object.__class__.__name__ + name + ".json"
        with open(path, "w") as f:
            json_str = object.model_dump_json()
            f.write(json_str)

    def _get_points(self, points: List[Tuple[float, float]]) -> List[Point]:
        return [Point(x=point[0], y=point[1], idx=i) for i, point in enumerate(points)]

    def _get_distance(self, point_a: Point, point_b: Point) -> float:
        a = np.array([point_a.x, point_a.y])
        b = np.array([point_b.x, point_b.y])
        return np.linalg.norm(a - b)

    def _build_probability_matrix(self) -> ProbabilityMatrix:
        rows = []
        points = self.points
        for i in range(len(points)):
            columns = []
            for j in range(len(points)):
                if i != j:
                    a = np.array([points[i].x, points[i].y])
                    b = np.array([points[j].x, points[j].y])
                    distance = np.linalg.norm(a - b)
                    distance_obj = Segment(
                        distance=distance,
                        point_a=points[i],
                        point_b=points[j],
                        probability=0,
                        pheromone=self.model_params.initial_pheromone,
                    )
                    columns.append(distance_obj)
            rows.append(columns)
        return ProbabilityMatrix(matrix=rows)

    def _is_segment_in_pheromone(self, segment: Segment, pheromone: Segment) -> bool:
        segment_point_a = segment.point_a
        segment_point_b = segment.point_b
        pheromone_point_a = pheromone.point_a
        pheromone_point_b = pheromone.point_b
        return (
            segment_point_a.idx == pheromone_point_a.idx
            and segment_point_b.idx == pheromone_point_b.idx
            or segment_point_a.idx == pheromone_point_b.idx
            and segment_point_b.idx == pheromone_point_a.idx
        )

    def _get_pheromone_diffusion(
        self, ants_trails: AntsTrails, pheromone: Segment
    ) -> int:
        diffusion = 0
        for ant_trail in ants_trails.trails:
            for segment in ant_trail.trail:
                if self._is_segment_in_pheromone(segment, pheromone):
                    diffusion += 1 / ant_trail.total_distance
        return diffusion

    def _update_pheromone(self, ants_trails: AntsTrails, i: int, j: int) -> float:
        pheromone_obj = self.probability_matrix.matrix[i][j]
        pheromone_diffusion = self._get_pheromone_diffusion(ants_trails, pheromone_obj)
        old_pheromone = pheromone_obj.pheromone

        new_pheromone = (
            1 - self.model_params.evaporation_rate
        ) * old_pheromone + pheromone_diffusion

        return new_pheromone

    def _update_pheromone_matrix(self, ants_trails: AntsTrails):
        for i in range(self.n_rows):
            for j in range(self.n_columns):
                if i != j:
                    self.probability_matrix.matrix[i][j].pheromone = (
                        self._update_pheromone(ants_trails, i, j)
                    )

    def _get_segment_probability(
        self, distance: float, pheromone: float, pheromone_density: float
    ) -> float:
        individual_pheromone_density = np.power(
            pheromone, self.model_params.alpha
        ) / np.power(distance, self.model_params.beta)
        probability = individual_pheromone_density / pheromone_density
        return probability

    def _get_pheromone_density(
        self, pheromone_list: List[Pheromone], distance_list: List[Segment]
    ) -> float:
        pheromone_density = 0
        for i in range(len(pheromone_list)):
            pheromone_density += np.power(
                pheromone_list[i].pheromone, self.model_params.alpha
            ) / np.power(distance_list[i].distance, self.model_params.beta)
        return pheromone_density

    def _update_probabilities(self):
        for i in range(self.n_rows):
            pheromone_list = self.mutable_pheromone_matrix.matrix[i]
            distance_list = self.probability_matrix.matrix[i]
            pheromone_density = self._get_pheromone_density(
                pheromone_list, distance_list
            )
            for j in range(self.n_columns):
                distance = distance_list[j].distance
                pheromone = pheromone_list[j].pheromone
                probability = self._get_segment_probability(
                    distance, pheromone, pheromone_density
                )
                self.probability_matrix.matrix[i][j].probability = probability

    def _get_tail_points(self, chosen_order: List[int]) -> List[Tuple[float, float]]:
        points = []
        for i in chosen_order:
            points.append(self.points[i])
        return points

    def _get_trail(self, ant_probable_trail: np.ndarray) -> List[int]:
        valid_indices = np.where(ant_probable_trail > 0)[0]
        valid_probs = ant_probable_trail[valid_indices].astype(float)

        chosen_order = []
        while len(valid_indices) > 0:
            valid_probs = valid_probs / valid_probs.sum()
            idx = np.random.choice(len(valid_indices), p=valid_probs)
            chosen_order.append(valid_indices[idx])

            valid_indices = np.delete(valid_indices, idx)
            valid_probs = np.delete(valid_probs, idx)

        return chosen_order

    def _get_idx(self, probs: List[float]) -> int:
        elements = list(range(len(probs)))
        choice = random.choices(elements, weights=probs, k=1)[0]
        return choice

    def exclude_at(self, lst: List[float], idx: int) -> List[float]:
        return lst[:idx] + lst[idx + 1 :]

    def _choose_trail(self, probable_trail: List[Segment]) -> List[Segment]:
        trail = []
        probs = [seg.probability for seg in probable_trail]
        idx = self._get_idx(probs)
        segment = probable_trail[idx]
        new_segment = Segment(
            distance=segment.distance,
            point_a=segment.point_a,
            point_b=segment.point_b,
        )
        trail.append(new_segment)
        probs = self.exclude_at(probs, idx)
        probs = [p / sum(probs) for p in probs]

        while len(probs) > 0:
            idx = self._get_idx(probs)
            segment = probable_trail[idx]
            distance = self._get_distance(segment.point_a, segment.point_b)
            new_segment = Segment(
                distance=distance,
                point_a=trail[-1].point_b,
                point_b=segment.point_b,
            )
            trail.append(new_segment)
            probs = self.exclude_at(probs, idx)
            probs = [p / sum(probs) for p in probs]

        return trail

    def _get_ants_trails(self) -> AntsTrails:
        ants = []
        i = 0
        for probable_trail in self.probability_matrix.matrix:
            trail: List[Segment] = self._choose_trail(probable_trail)
            total_distance = sum([seg.distance for seg in trail])
            ant = AntTrail(idx=i, trail=trail, total_distance=total_distance)
            ants.append(ant)
            i += 1
        return AntsTrails(trails=ants)

    def run(self):

        n_iterations = 1000
        collection_of_ants_trails = []
        first_trail = None

        for i in range(n_iterations):

            self._update_probabilities()

            ants_trail: AntsTrails = self._get_ants_trails()

            self._update_pheromone_matrix(ants_trail)

            shortest_trail = min(ants_trail.trails, key=lambda x: x.total_distance)

            if i == 0:
                first_trail = shortest_trail

            collection_of_ants_trails.append(shortest_trail)

        last_trail = collection_of_ants_trails[-1]

        return collection_of_ants_trails, first_trail, last_trail


def random_points(n_points: int, max_val: int) -> List[Tuple[int, int]]:
    return [
        (random.randint(0, max_val), random.randint(0, max_val))
        for _ in range(n_points)
    ]


def main():
    points = random_points(4, 5)
    input = AntColonyModelInput(points=points)
    model = AntColonyModel(input=input)
    collection_of_ants_trails, first_trail, last_trail = model.run()
    plot_total_distance_progression(collection_of_ants_trails)
    plot_first_and_last_trail(first_trail, last_trail)


if __name__ == "__main__":
    main()
