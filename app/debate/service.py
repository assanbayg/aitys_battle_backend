from pydantic import BaseSettings

from app.config import database
from .repository.repository import AitysRepository


class Service:
    def __init__(self):
        self.repository = AitysRepository(database)


def get_service():
    svc = Service()
    return svc
