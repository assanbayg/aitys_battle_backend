from fastapi import Depends, status
from typing import Optional, List

from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router


class CreateAitysRequest(AppModel):
    topic: str
    first_figure: str
    second_figure: str
    replies: List = []


class CreateAitysResponse(AppModel):
    replies: List


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_aitys(
    input: CreateAitysRequest,
    svc: Service = Depends(get_service),
):
    names = {
        input.first_figure: ["arxiv", "ddg-search", "wikipedia"],
        input.second_figure: ["arxiv", "ddg-search", "wikipedia"],
    }
    response = svc.openai_service.run_dialogue_simulation(
        topic=input.topic,
        names=names,
    )
    updated_input = CreateAitysRequest(
        topic=input.topic,
        first_figure=input.first_figure,
        second_figure=input.second_figure,
        replies=response,
    )
    created_aitys_id = svc.repository.create_aitys(
        updated_input.dict(),
    )
    return CreateAitysResponse(replies=created_aitys_id)
