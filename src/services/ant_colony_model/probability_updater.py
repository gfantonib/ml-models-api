from src.objects.ant_colony_objects import Segment, Trail, TrailMatrix
from src.params.ant_colony_params import AntColonyModelParams
from src.services.ant_colony_model.utils import get_segment_pheromone_density


class ProbabilityUpdater:
    def __init__(self, matrix: TrailMatrix):
        self.matrix: TrailMatrix = matrix
        self.model_params = AntColonyModelParams()

    def _get_segment_probability(
        self, segment: Segment, trail_pheromone_density: float
    ) -> float:
        segment_pheromone_density = get_segment_pheromone_density(
            segment, self.model_params
        )
        probability = segment_pheromone_density / trail_pheromone_density
        return probability

    def _get_trail_pheromone_density(self, trail: Trail) -> float:
        pheromone_density = 0
        for segment in trail.segments:
            pheromone_density += get_segment_pheromone_density(
                segment, self.model_params
            )
        return pheromone_density

    def update_probabilities(self) -> TrailMatrix:
        for trail in self.matrix.matrix:
            trail_pheromone_density = self._get_trail_pheromone_density(trail)
            for segment in trail.segments:
                segment.probability = self._get_segment_probability(
                    segment, trail_pheromone_density
                )
        return self.matrix
