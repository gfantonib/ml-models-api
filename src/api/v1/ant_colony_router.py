from fastapi import APIRouter

from src.contracts.ant_colony_contracts import AntColonyRequest, AntColonyResponse
from src.services.ant_colony_model.ant_colony_model import AntColonyModel

router = APIRouter()


@router.post("/ant-colony-model", response_model=AntColonyResponse)
def run_ant_colony_model(request: AntColonyRequest):
    model = AntColonyModel(request)
    response = model.run()
    return response
