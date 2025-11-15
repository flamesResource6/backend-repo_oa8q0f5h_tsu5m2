import os
from typing import Any, Dict, List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "app_db")

_client: AsyncIOMotorClient = AsyncIOMotorClient(DATABASE_URL)
db: AsyncIOMotorDatabase = _client[DATABASE_NAME]


async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.utcnow()
    payload = {**data, "created_at": now, "updated_at": now}
    await db[collection_name].insert_one(payload)
    return payload


async def get_documents(collection_name: str, filter_dict: Dict[str, Any] | None = None, limit: int = 20) -> List[Dict[str, Any]]:
    filter_dict = filter_dict or {}
    cursor = db[collection_name].find(filter_dict).limit(limit)
    docs: List[Dict[str, Any]] = []
    async for d in cursor:
        d.pop("_id", None)
        docs.append(d)
    return docs
