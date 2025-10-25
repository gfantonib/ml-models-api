import random
from copy import deepcopy
from typing import List

from src.objects.ant_colony_objects import Segment, Trail, TrailMatrix
from src.params.ant_colony_params import AntColonyModelParams
from src.services.ant_colony_model.utils import (
    calc_distance,
    get_segment_pheromone_density,
)


class TrailChooser:

    def __init__(self, matrix: TrailMatrix):
        self.matrix: TrailMatrix = matrix
        self.model_params = AntColonyModelParams()

    def _get_pheromone_from_matrix(self, segment: Segment) -> float:
        a_idx, b_idx = segment.from_p.idx, segment.to_p.idx

        for trail in self.matrix.matrix:
            for seg in trail.segments:
                seg_a, seg_b = seg.from_p.idx, seg.to_p.idx
                if {a_idx, b_idx} == {seg_a, seg_b}:
                    return seg.pheromone

        return 1.0

    def _compute_total_density(self, segments: List[Segment]) -> float:
        return sum(
            get_segment_pheromone_density(seg, self.model_params) for seg in segments
        )

    def _update_segment_probabilities(
        self, segments: List[Segment], total_density: float
    ):
        for seg in segments:
            seg_density = get_segment_pheromone_density(seg, self.model_params)
            seg.probability = (
                seg_density / total_density if total_density > 0 else 1 / len(segments)
            )

    def _choose_segment(self, segments: List[Segment]) -> Segment:
        rnd = random.random()
        cumulative = 0.0
        for seg in segments:
            cumulative += seg.probability
            if rnd <= cumulative:
                return seg
        return segments[-1]  # fallback

    def _update_remaining_segments(
        self, chosen_seg: Segment, remaining_segments: List[Segment]
    ):
        new_from_point = chosen_seg.to_p

        for seg in remaining_segments:
            seg.from_p = deepcopy(new_from_point)
            seg.distance = calc_distance(seg.from_p, seg.to_p)
            seg.pheromone = self._get_pheromone_from_matrix(seg)
            seg.probability = None

    def choose_trail(self, probable_trail: Trail) -> Trail:
        available_segments = deepcopy(probable_trail.segments)
        factual_segments = []

        while available_segments:
            # Step 1: Compute total pheromone density
            total_density = self._compute_total_density(available_segments)

            # Step 2: Update probabilities
            self._update_segment_probabilities(available_segments, total_density)

            # Step 3: Choose a segment probabilistically
            chosen_seg = self._choose_segment(available_segments)

            # Step 4: Add chosen segment to factual trail
            factual_seg = deepcopy(chosen_seg)
            factual_seg.probability = None
            factual_segments.append(factual_seg)

            # Step 5: Remove chosen segment
            available_segments.remove(chosen_seg)

            # Step 6: Stop if no segments left
            if not available_segments:
                break

            # Step 7: Update remaining segments (geometry + pheromone)
            self._update_remaining_segments(chosen_seg, available_segments)

            # Step 8: If only one segment remains, add it and stop
            if len(available_segments) == 1:
                last_seg = deepcopy(available_segments[0])
                last_seg.probability = None
                factual_segments.append(last_seg)
                break

        total_distance = sum(seg.distance for seg in factual_segments)
        factual_trail = Trail(segments=factual_segments, total_distance=total_distance)

        # Step 9: Return the new factual trail
        return factual_trail
