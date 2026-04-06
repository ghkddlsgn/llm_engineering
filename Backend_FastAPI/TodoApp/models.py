from Backend_FastAPI.TodoApp.database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email:Mapped[str] = mapped_column(String, unique=True)
    username:Mapped[str] = mapped_column(String)
    username:Mapped[str] = mapped_column(String)
    hashed_password:Mapped[str] = mapped_column(String)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True)
    role:Mapped[str] = mapped_column(String)



class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title:Mapped[str] = mapped_column(String)
    description:Mapped[str] = mapped_column(String)
    priority:Mapped[int] = mapped_column(Integer)
    complete:Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id:Mapped[int] = mapped_column(Integer)

