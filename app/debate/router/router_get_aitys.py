from typing import Any

from fastapi import Depends, status
from pydantic import Field

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GetAitysResponse(AppModel):
    id: Any = Field(alias="_id")
    topic: str = ""
    first_figure: str = ""
    second_figure: str = ""


@router.get(
    "/aitys/{id: str}",
    response_model=GetAitysResponse,
    status_code=status.HTTP_200_OK,
)
def get_aitys(id: str, svc: Service = Depends(get_service)):
    aitys = svc.repository.get_aitys_by_id(id)
    return aitys
