from src.objects.pythagorean_support_machine_objects import (
    PythagoreanSupportMachineInput,
    PythagoreanSupportMachineOutput,
)
from src.services.pythagorean_support_machine_model.centroid_updater import (
    CentroidUpdater,
)
from src.services.pythagorean_support_machine_model.distances_updater import (
    DistancesUpdater,
)
from src.services.pythagorean_support_machine_model.first_matrix_setter import (
    FirstMatrixSetter,
)
from src.services.pythagorean_support_machine_model.groups_selector import (
    GroupsSelector,
)
from src.services.pythagorean_support_machine_model.probabilities_updater import (
    ProbabilitiesUpdater,
)


class PythagoreanSupportMachineModel:
    def __init__(self, input: PythagoreanSupportMachineInput):
        self.input = input
        first_matrix_setter = FirstMatrixSetter(input)
        self.main_matrix = first_matrix_setter.set_first_matrix()

    def run(self, max_iterations: int = 10) -> PythagoreanSupportMachineOutput:
        distances_updater = DistancesUpdater(self.main_matrix)
        probabilities_updater = ProbabilitiesUpdater(self.main_matrix)
        centroid_updater = CentroidUpdater(self.main_matrix)
        for i in range(max_iterations):
            distances_updater.update_distances()
            probabilities_updater.update_probabilities()
            centroid_updater.update_centroids()
        groups_selector = GroupsSelector(self.main_matrix)
        return groups_selector.select_groups()
