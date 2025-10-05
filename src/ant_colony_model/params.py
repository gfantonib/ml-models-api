from pydantic import BaseModel, confloat


class AntColonyModelParams(BaseModel):
    alpha: float = 3.0
    beta: float = 2.0
    evaporation_rate: confloat(gt=0, lt=1) = 0.5
    initial_pheromone: float = 1.0
    n_iterations: int = 10
