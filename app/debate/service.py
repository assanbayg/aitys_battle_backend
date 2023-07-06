from pydantic import BaseSettings

from app.config import database
from .repository.repository import AitysRepository
from .adapters.openai_serivce import LLMService


class Service:
    def __init__(self):
        self.repository = AitysRepository(database)
        self.openai_serivce = LLMService()


def get_service():
    svc = Service()
    return svc
