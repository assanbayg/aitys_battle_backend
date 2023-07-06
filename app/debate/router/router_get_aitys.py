from typing import Any

from fastapi import Depends, status

from app.utils import AppModel

from ..service import Service, get_service
from . import router


@router.get("/{id: str}", status_code=status.HTTP_200_OK)
def get_aitys(id: str, svc: Service = Depends(get_service)):
    aitys = svc.repository.get_aitys_by_id(id)
    return {
        "id": id,
        "topics": aitys["topic"],
        "first_figure": aitys["first_figure"],
        "second_figure": aitys["second_figure"],
    }
