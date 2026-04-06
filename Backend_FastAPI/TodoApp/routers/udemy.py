from typing import Annotated
from fastapi import Depends, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status
from Backend_FastAPI.TodoApp.udemy_table import Prices
import Backend_FastAPI.TodoApp.models as models
from Backend_FastAPI.TodoApp.database import engine, SessionLocal,Base, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import APIRouter


router = APIRouter()
db_dependency = Annotated[AsyncSession, Depends(get_db)]

class PriceRequest(BaseModel):
    city:str = Field(min_length=1)
    price:int = Field(ge=0)

@router.get("/udemy/db/price/{city}")
async def read_price(db:db_dependency, city:str = Path(min_length=1)):
    price_model = await db.get(Prices, city)
    if price_model:
        return price_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid city name")

@router.post("/udemy/db/price")
async def create_city(db:db_dependency, price_request:PriceRequest):
    new_model = Prices(**price_request.model_dump())
    db.add(new_model)
    await db.commit()

@router.put("/udemy/db/price/{city}")
async def update_city(db:db_dependency, city:str = Path(min_length=1), price:int = Path(ge=0)):
    result = await db.execute(select(Prices).filter())