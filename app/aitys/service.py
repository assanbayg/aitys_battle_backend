import os
from dotenv import getenv
from pydantic import BaseSettings

from app.config import database

from .adapters.jwt_service import JwtService
from .repository.repository import AuthRepository


class AuthConfig(BaseSettings):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_EXP: int = 10_800


config = AuthConfig()


class Service:
    def __init__(
        self,
        repository: AuthRepository,
        jwt_svc: JwtService,
    ):
        self.repository = repository
        self.jwt_svc = jwt_svc


def get_service():
    repository = AuthRepository(database)
    jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)

    svc = Service(repository, jwt_svc)
    return svc
