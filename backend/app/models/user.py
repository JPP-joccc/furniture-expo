import enum
from typing import List, Optional

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Role(str, enum.Enum):
    CUSTOMER = "customer"
    MERCHANT = "merchant"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[Role] = mapped_column(Enum(Role))
    shop_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    products: Mapped[List["Product"]] = relationship(back_populates="merchant")
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="user")
    inquiries: Mapped[List["Inquiry"]] = relationship(
        back_populates="user", foreign_keys="Inquiry.user_id"
    )
