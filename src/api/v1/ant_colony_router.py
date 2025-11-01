from fastapi import APIRouter

from src.objects.ant_colony_objects import AntColonyRequest, AntColonyResponse
from src.services.ant_colony_model.ant_colony_model import AntColonyModel

router = APIRouter()


@router.post("/ant-colony-model", response_model=AntColonyResponse)
def run_ant_colony_model(request: AntColonyRequest):
    model = AntColonyModel(request)
    response = model.run()
    return response
