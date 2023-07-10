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
    topic: str,
    first_figure: str,
    second_figure: str,
    svc: Service = Depends(get_service),
):
    names = {
        first_figure: ["arxiv", "ddg-search", "wikipedia"],
        second_figure: ["arxiv", "ddg-search", "wikipedia"],
    }
    response = svc.openai_service.run_dialogue_simulation(
        topic=topic,
        names=names,
    )
    return response
