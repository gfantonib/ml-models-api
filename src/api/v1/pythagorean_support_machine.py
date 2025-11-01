from fastapi import APIRouter

from src.objects.pythagorean_support_machine_objects import (
    PythagoreanSupportMachineInput,
    PythagoreanSupportMachineOutput,
)
from src.services.pythagorean_support_machine_model.pythagorean_support_machine_model import (
    PythagoreanSupportMachineModel,
)

router = APIRouter()


@router.post(
    "/pythagorean-support-machine-model", response_model=PythagoreanSupportMachineOutput
)
def run_pythagorean_support_machine(request: PythagoreanSupportMachineInput):
    model = PythagoreanSupportMachineModel(request)
    response = model.run()
    return response
