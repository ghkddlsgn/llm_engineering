from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status
from Backend_FastAPI.TodoApp.models import Todos
import Backend_FastAPI.TodoApp.models as models
from Backend_FastAPI.TodoApp.database import engine, SessionLocal, Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uvicorn
from contextlib import asynccontextmanager

#init -------------------
@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)    
    yield

app = FastAPI(lifespan=lifespan)

async def get_db():
    async with SessionLocal() as db:
        yield db

db_dependency = Annotated[AsyncSession, Depends(get_db)]

class TodoRequest(BaseModel):
    title:str = Field(min_length=3)
    description:str = Field(min_length=3, max_length=100)
    priority:int = Field(gt=0, lt=6)
    complete:bool

@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    result = await db.execute(select(Todos))
    return result.scalars().all()

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = await db.get(Todos, todo_id)
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')

@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_doto(db:db_dependency, todo_request:TodoRequest):
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    await db.commit()

@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency, todo_id:int, todo_request:TodoRequest):
    result = await db.execute(select(Todos).filter(Todos.id == todo_id))
    todo_model = result.scalars().first()
    if not todo_model:
        raise HTTPException(status_code=404, detail='Todo not found')
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    await db.commit()

@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency, todo_id:int = Path(gt=0)):
    result = await db.execute(select(Todos).filter(Todos.id == todo_id))
    todo_model = result.scalars().first()
    if not todo_model:
        raise HTTPException(status_code=404, detail='Todo not found')
    
    await db.delete(todo_model)
    await db.commit()
    
if __name__ == "__main__":
    uvicorn.run("Backend_FastAPI.TodoApp.main:app", host="127.0.0.1", port=8000, reload=True)
