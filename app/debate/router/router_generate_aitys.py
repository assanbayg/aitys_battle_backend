from fastapi import Depends, status
from typing import List

from app.utils import AppModel

from ..service import Service, get_service

from . import router


class GenerateAitysResponse(AppModel):
    replies: List[str]


@router.post("/{id}/response", status_code=status.HTTP_201_CREATED)
def generate_aitys(
    id: str,
    topic: str = "Revolution",
    first_figure: str = "Stalin",
    second_figure: str = "Lenin",
    svc: Service = Depends(get_service),
):
    response = svc.openai_serivce.run_dialogue_simulation()
    return response
