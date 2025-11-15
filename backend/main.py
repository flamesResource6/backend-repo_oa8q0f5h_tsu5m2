from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
from schemas import Product
from database import db, create_document, get_documents

app = FastAPI(title="Toy Store API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
async def test():
    # simple db test: count products
    count = await db["product"].count_documents({})
    return {"status": "ok", "time": datetime.utcnow().isoformat(), "products": count}


@app.get("/products", response_model=List[Product])
async def list_products(category: str | None = None, limit: int = 12):
    filter_q = {"category": category} if category else {}
    docs = await get_documents("product", filter_q, limit)
    return [Product(**{k: v for k, v in d.items() if k in Product.__fields__}) for d in docs]


@app.post("/products", response_model=Product, status_code=201)
async def create_product(product: Product):
    data = product.dict()
    await create_document("product", data)
    return product
