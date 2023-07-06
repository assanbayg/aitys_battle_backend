from fastapi import Depends, status
from typing import List

from app.utils import AppModel

from ..service import Service, get_service

from . import router


class GenerateAitysRequest(AppModel):
    topic: str
    first_figure: str
    second_figure: str


class GenerateAitysResponse(AppModel):
    replies: List[str]


@router.post("/{id}/response", status_code=status.HTTP_201_CREATED)
def generate_aitys(
    id: str,
    input: GenerateAitysRequest,
    svc: Service = Depends(get_service),
):
    response = svc.openai_service.run_dialogue_simulation(input)
    print("LOOK", response)
    return "OK"
