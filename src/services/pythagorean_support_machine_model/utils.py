from typing import List

from src.objects.pythagorean_support_machine_objects import Point, PointStatus


def calculate_centroid_coordinate(
    probabilities: List[PointStatus], dimension: int
) -> float:
    coordinate_numerator = 0
    coordinate_denominator = 0
    for probability in probabilities:
        coordinate_numerator += (
            probability.point.coordinates[dimension] * (probability.probability) ** 2
        )
        coordinate_denominator += (probability.probability) ** 2
    return coordinate_numerator / coordinate_denominator


def calculate_centroid(probabilities: List[PointStatus], n_dimensions: int) -> Point:
    coordinates = []
    for i in range(n_dimensions):
        coordinate = calculate_centroid_coordinate(probabilities, i)
        coordinates.append(coordinate)
    return Point(coordinates=coordinates)
