from typing import Optional
from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    price: float = Field(..., ge=0)
    category: str = Field(..., min_length=1, max_length=60)
    image: str = Field(..., min_length=1)
    rating: float = Field(4.5, ge=0, le=5)
    description: Optional[str] = Field(None, max_length=500)
