from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("POSTGRES_USERNAME")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOSTNAME")
port = os.getenv("POSTGRES_PORT")
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{username}:{password}"
    f"@{host}:{port}/todos"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as db:
        yield db
