from fastapi import Request, Depends, status
from typing import List

from app.utils import AppModel

from ..service import Service, get_service

from . import router


class GenerateAitysRequest(AppModel):
    id: str
    topic: str
    first_figure: str
    second_figure: str

class GenerateAitysResponse(AppModel):
    replies: List[str]


@router.post("/{id}/response", status_code=status.HTTP_201_CREATED)
async def generate_aitys(
    input: GenerateAitysRequest,
    svc: Service = Depends(get_service),
):
    print("LOOK")
    print(input)
    names = {
        input.first_figure: ["arxiv", "ddg-search", "wikipedia"],
        input.second_figure: ["arxiv", "ddg-search", "wikipedia"],
    }
    response = svc.openai_service.run_dialogue_simulation(
        topic=input.topic,
        names=names,
    )
    return response
