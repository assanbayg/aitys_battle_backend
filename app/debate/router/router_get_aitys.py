from typing import Any

from fastapi import Depends, status, HTTPException

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GetAitysRequest(AppModel):
    topic: str
    first_figure: str
    second_figure: str


@router.get("/{id: str}", status_code=status.HTTP_200_OK)
def get_aitys_by_id(id: str, svc: Service = Depends(get_service)):
    aitys = svc.repository.get_aitys_by_id(id)
    return {
        "id": id,
        "topics": aitys["topic"],
        "first_figure": aitys["first_figure"],
        "second_figure": aitys["second_figure"],
    }


@router.get("/", status_code=status.HTTP_200_OK)
def get_aitys(
    # input: GetAitysRequest,
    topic: str,
    svc: Service = Depends(get_service),
):
    aitys_data = svc.repository.get_aitys(input)
    if aitys_data:
        return aitys_data["replies"]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aitys not found",
        )
