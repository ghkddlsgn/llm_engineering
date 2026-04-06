from sqlalchemy import Float, String
from Backend_FastAPI.TodoApp.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Prices(Base):
    __tablename__ = 'prices'
    city: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    price: Mapped[float] = mapped_column(Float)