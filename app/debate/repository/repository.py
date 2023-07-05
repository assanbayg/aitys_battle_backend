from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AitysRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_aitys(self, user_id: str, data: dict):
        data["user_id"] = ObjectId(user_id)
        result = self.database["aitys"].insert_one(data)
        created_aitys_id = str(result.inserted_id)
        return created_aitys_id

    # def get_user_by_id(self, user_id: str) -> Optional[dict]:
    #     user = self.database["users"].find_one(
    #         {
    #             "_id": ObjectId(user_id),
    #         }
    #     )
    #     return user

    # def get_user_by_email(self, email: str) -> Optional[dict]:
    #     user = self.database["users"].find_one(
    #         {
    #             "email": email,
    #         }
    #     )
    #     return user
