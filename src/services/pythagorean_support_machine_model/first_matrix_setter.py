import random
from typing import List

from src.objects.pythagorean_support_machine_objects import (
    MainMatrix,
    Node,
    PointStatus,
    PythagoreanSupportMachineInput,
)
from src.services.pythagorean_support_machine_model.utils import calculate_centroid


class FirstMatrixSetter:
    def __init__(self, input: PythagoreanSupportMachineInput):
        self.input = input
        self.points = input.points
        self.n_groups = input.n_groups

    def get_first_points_status(self) -> List[List[PointStatus]]:
        nodes: List[List[PointStatus]] = [[] for _ in range(self.n_groups)]

        for point in self.points:
            raw_probs = [random.random() for _ in range(self.n_groups)]
            total = sum(raw_probs)

            normalized_probs = [p / total for p in raw_probs]

            for i, prob in enumerate(normalized_probs):
                nodes[i].append(
                    PointStatus(probability=prob, point=point.model_dump(), distance=0)
                )

        return nodes

    def set_first_matrix(self) -> MainMatrix:
        n_dimensions = len(self.points[0].coordinates)
        point_status_list = self.get_first_points_status()
        nodes = []
        for points_status in point_status_list:
            centroid = calculate_centroid(points_status, n_dimensions)
            nodes.append(Node(points_status=points_status, centroid=centroid))
        return MainMatrix(nodes=nodes)
