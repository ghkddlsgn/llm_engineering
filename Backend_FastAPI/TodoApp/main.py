from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from routers import auth, todos

#init -------------------
@asynccontextmanager
async def lifespan(app:FastAPI):
    await todos.init_todos()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(todos.router)
    
if __name__ == "__main__":
    uvicorn.run("Backend_FastAPI.TodoApp.main:app", host="127.0.0.1", port=8000, reload=True)
