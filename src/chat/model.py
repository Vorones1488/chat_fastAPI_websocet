from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text


class Users(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(unique=True)
    

class Messages(Base):
    __tablename__ = 'messages'
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(Text)