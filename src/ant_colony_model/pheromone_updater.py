from src.ant_colony_model.objects import Segment, Trail, TrailMatrix
from src.ant_colony_model.params import AntColonyModelParams


class PheromoneUpdater:
    def __init__(self, matrix: TrailMatrix):
        self.matrix: TrailMatrix = matrix
        self.model_params = AntColonyModelParams()

    def _is_segment_in_trail(self, segment: Segment, trail: Trail) -> bool:
        for seg in trail.segments:
            if (
                seg.from_p.idx == segment.from_p.idx
                and seg.to_p.idx == segment.to_p.idx
            ) or (
                seg.from_p.idx == segment.to_p.idx
                and seg.to_p.idx == segment.from_p.idx
            ):
                return True
        return False

    def _update_pheromone(self, segment: Segment, chosen_trails: TrailMatrix) -> float:
        current_pheromone = segment.pheromone
        scattered_factor_sum = 0
        for chosen_trail in chosen_trails.matrix:
            if self._is_segment_in_trail(segment, chosen_trail):
                scattered_factor_sum += 1 / chosen_trail.total_distance

        new_pheromone = (
            current_pheromone * (1 - self.model_params.evaporation_rate)
            + scattered_factor_sum
        )
        return new_pheromone

    def update_pheromones(self, chosen_trails: TrailMatrix) -> TrailMatrix:
        for trail in self.matrix.matrix:
            for segment in trail.segments:
                segment.pheromone = self._update_pheromone(segment, chosen_trails)
