from src.ant_colony_model.objects import TrailMatrix
from src.ant_colony_model.params import AntColonyModelParams
from src.ant_colony_model.pheromone_updater import PheromoneUpdater
from src.ant_colony_model.probability_updater import ProbabilityUpdater
from src.ant_colony_model.trail_choser import TrailChooser


class TrailMatrixManager:
    def __init__(self, matrix: TrailMatrix):
        self.matrix: TrailMatrix = matrix
        self.model_params = AntColonyModelParams()

    def get_trail_matrix(self) -> TrailMatrix:
        return self.matrix

    def update_probabilities(self):
        updater = ProbabilityUpdater(self.matrix)
        return updater.update_probabilities()

    def choose_trails(self) -> TrailMatrix:
        trail_chooser = TrailChooser(self.matrix)
        new_trails = []
        for probable_trail in self.matrix.matrix:
            new_trail = trail_chooser.choose_trail(probable_trail)
            new_trails.append(new_trail)
        return TrailMatrix(matrix=new_trails)

    def update_pheromones(self, chosen_trails: TrailMatrix) -> TrailMatrix:
        updater = PheromoneUpdater(self.matrix)
        return updater.update_pheromones(chosen_trails)
