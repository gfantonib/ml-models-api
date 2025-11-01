from typing import List

from src.objects.pythagorean_support_machine_objects import MainMatrix, Node


class ProbabilitiesUpdater:
    def __init__(self, matrix: MainMatrix):
        self.matrix = matrix

    def calculate_probability(
        self, distance: float, all_distances: List[float]
    ) -> float:
        cum_sum = sum((distance / d) ** 2 for d in all_distances)
        return cum_sum**-1

    def get_all_point_distances(self, point_idx: int) -> List[float]:
        return [node.points_status[point_idx].distance for node in self.matrix.nodes]

    def get_distance_to_centroid(self, node: Node, point_idx: int) -> float:
        return node.points_status[point_idx].distance

    def update_probability_for_point(
        self, node: Node, point_idx: int, all_distances: List[float]
    ):
        distance = self.get_distance_to_centroid(node, point_idx)
        new_prob = self.calculate_probability(distance, all_distances)
        node.points_status[point_idx].probability = new_prob

    def update_probabilities_for_point_across_nodes(self, point_idx: int):
        all_distances = self.get_all_point_distances(point_idx)
        for node in self.matrix.nodes:
            self.update_probability_for_point(node, point_idx, all_distances)

    def update_probabilities(self):
        n_points = len(self.matrix.nodes[0].points_status)
        for point_idx in range(n_points):
            self.update_probabilities_for_point_across_nodes(point_idx)
