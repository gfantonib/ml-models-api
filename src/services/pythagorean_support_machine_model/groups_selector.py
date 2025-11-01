from typing import Dict, List

from src.objects.pythagorean_support_machine_objects import (
    Group,
    MainMatrix,
    Point,
    PythagoreanSupportMachineOutput,
)


class GroupsSelector:
    def __init__(self, matrix: MainMatrix):
        self.matrix = matrix

    def extract_all_points(self) -> List[Point]:
        return [ps.point for ps in self.matrix.nodes[0].points_status]

    def get_n_dimensions(self) -> int:
        return len(self.matrix.nodes[0].centroid.coordinates)

    def find_best_group_for_point(self, point_idx: int) -> int:
        return max(
            range(len(self.matrix.nodes)),
            key=lambda i: self.matrix.nodes[i].points_status[point_idx].probability,
        )

    def assign_points_to_groups(self, points: List[Point]) -> Dict[int, List[Point]]:
        assignments: Dict[int, List[Point]] = {
            i: [] for i in range(len(self.matrix.nodes))
        }
        for point_idx, point in enumerate(points):
            best_group_idx = self.find_best_group_for_point(point_idx)
            assignments[best_group_idx].append(point)
        return assignments

    def build_groups(self, assignments: Dict[int, List[Point]]) -> List[Group]:
        groups: List[Group] = []
        for i, node in enumerate(self.matrix.nodes):
            group_points = assignments[i]
            group_points = [p.model_dump() for p in group_points]
            centroid = node.centroid.model_dump()
            groups.append(
                Group(
                    points=group_points, n_points=len(group_points), centroid=centroid
                )
            )
        return groups

    def select_groups(self) -> PythagoreanSupportMachineOutput:
        points = self.extract_all_points()
        n_dimensions = self.get_n_dimensions()
        assignments = self.assign_points_to_groups(points)
        groups = self.build_groups(assignments)

        return PythagoreanSupportMachineOutput(groups=groups, n_dimensions=n_dimensions)
