from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.dependencies import get_current_customer
from app.models.favorite import Favorite
from app.models.product import Product
from app.models.user import User
from app.schemas.favorite import FavoriteCreate, FavoriteResponse
from app.schemas.product import ProductResponse

router = APIRouter(prefix="/api/favorites", tags=["favorites"])


@router.get("", response_model=List[FavoriteResponse])
def list_favorites(
    user: User = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    favorites = db.scalars(
        select(Favorite)
        .options(joinedload(Favorite.product).joinedload(Product.merchant))
        .where(Favorite.user_id == user.id)
        .order_by(Favorite.id.desc())
    ).unique().all()
    return [
        FavoriteResponse(
            id=fav.id,
            product=ProductResponse.from_orm_product(fav.product, is_favorited=True),
        )
        for fav in favorites
        if fav.product and fav.product.status == "active"
    ]


@router.post("", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
def add_favorite(
    data: FavoriteCreate,
    user: User = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    product = db.get(Product, data.product_id)
    if not product or product.status != "active":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")
    existing = db.scalar(
        select(Favorite).where(
            Favorite.user_id == user.id, Favorite.product_id == data.product_id
        )
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="已收藏")
    favorite = Favorite(user_id=user.id, product_id=data.product_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    product = db.scalar(
        select(Product)
        .options(joinedload(Product.merchant))
        .where(Product.id == data.product_id)
    )
    return FavoriteResponse(
        id=favorite.id,
        product=ProductResponse.from_orm_product(product, is_favorited=True),
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    product_id: int,
    user: User = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    favorite = db.scalar(
        select(Favorite).where(
            Favorite.user_id == user.id, Favorite.product_id == product_id
        )
    )
    if not favorite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未收藏")
    db.delete(favorite)
    db.commit()
