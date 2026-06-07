import json
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str
    category: str = Field(max_length=50)
    material: Optional[str] = Field(default=None, max_length=100)
    price: Optional[float] = Field(default=None, ge=0)
    images: List[str] = Field(default_factory=list)
    status: str = "active"

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in ("active", "inactive"):
            raise ValueError("status must be active or inactive")
        return v


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(default=None, max_length=50)
    material: Optional[str] = Field(default=None, max_length=100)
    price: Optional[float] = Field(default=None, ge=0)
    images: Optional[List[str]] = None
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ("active", "inactive"):
            raise ValueError("status must be active or inactive")
        return v


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    category: str
    material: Optional[str]
    price: Optional[float]
    images: List[str]
    status: str
    merchant_id: int
    merchant_name: Optional[str] = None
    shop_name: Optional[str] = None
    is_favorited: bool = False

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_product(cls, product, is_favorited: bool = False) -> "ProductResponse":
        images = json.loads(product.images) if product.images else []
        merchant = product.merchant
        return cls(
            id=product.id,
            name=product.name,
            description=product.description,
            category=product.category,
            material=product.material,
            price=product.price,
            images=images,
            status=product.status,
            merchant_id=product.merchant_id,
            merchant_name=merchant.name if merchant else None,
            shop_name=merchant.shop_name if merchant else None,
            is_favorited=is_favorited,
        )
