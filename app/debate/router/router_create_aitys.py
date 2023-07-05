from fastapi import Depends, status
from typing import Optional

from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router


class CreateAitysRequest(AppModel):
    topic: str
    first_figure: str
    second_figure: str


class CreateAitysResponse(AppModel):
    id: Optional[str]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_aitys(
    input: CreateAitysRequest,
    # jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    created_aitys_id = svc.repository.create_aitys(
        # jwt_data.user_id,
        input.dict(),
    )
    return CreateAitysResponse(id=created_aitys_id)
