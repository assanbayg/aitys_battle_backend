from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database


class AitysRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_aitys(
        self,
        data: dict,
    ):
        result = self.database["aitys"].insert_one(data)
        # created_aitys_id = str(result.inserted_id)
        return data["replies"]

    def get_aitys_by_id(self, id) -> Optional[dict]:
        aitys = self.database["aitys"].find_one({"_id": ObjectId(id)})
        return aitys
