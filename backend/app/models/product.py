from typing import List, Optional

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50), index=True)
    material: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    images: Mapped[str] = mapped_column(Text, default="[]")
    status: Mapped[str] = mapped_column(String(20), default="active", index=True)
    merchant_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    merchant: Mapped["User"] = relationship(back_populates="products")
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="product")
    inquiries: Mapped[List["Inquiry"]] = relationship(back_populates="product")
