from src.objects.pythagorean_support_machine_objects import MainMatrix, Node, Point


class DistancesUpdater:
    def __init__(self, matrix: MainMatrix):
        self.matrix = matrix

    def calculate_distance(self, point: Point, centroid: Point) -> float:
        distance = (
            sum((p - c) ** 2 for p, c in zip(point.coordinates, centroid.coordinates))
            ** 0.5
        )
        return distance

    def update_distances_for_node(self, node: Node) -> MainMatrix:
        for point in node.points_status:
            point.distance = self.calculate_distance(point.point, node.centroid)
        return node

    def update_distances(self):
        for node in self.matrix.nodes:
            self.update_distances_for_node(node)
