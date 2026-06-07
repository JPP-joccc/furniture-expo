from pydantic import BaseModel

from app.schemas.product import ProductResponse


class FavoriteCreate(BaseModel):
    product_id: int


class FavoriteResponse(BaseModel):
    id: int
    product: ProductResponse

    class Config:
        from_attributes = True
