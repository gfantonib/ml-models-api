from src.objects.pythagorean_support_machine_objects import (
    MainMatrix,
    Node,
    Point,
    PointStatus,
)
from src.services.pythagorean_support_machine_model.utils import calculate_centroid


class CentroidUpdater:
    def __init__(self, matrix: MainMatrix):
        self.matrix = matrix

    def update_centroids(self) -> MainMatrix:
        for node in self.matrix.nodes:
            node.centroid = calculate_centroid(
                node.points_status, len(node.points_status[0].point.coordinates)
            )
        return self.matrix
