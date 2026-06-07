import json
from typing import List, Optional, Set

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.dependencies import get_optional_user
from app.models.favorite import Favorite
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductResponse

router = APIRouter(prefix="/api/products", tags=["products"])


def _favorited_ids(db: Session, user: Optional[User]) -> Set[int]:
    if not user:
        return set()
    rows = db.scalars(select(Favorite.product_id).where(Favorite.user_id == user.id)).all()
    return set(rows)


@router.get("", response_model=List[ProductResponse])
def list_products(
    category: Optional[str] = None,
    q: Optional[str] = None,
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    stmt = (
        select(Product)
        .options(joinedload(Product.merchant))
        .where(Product.status == "active")
    )
    if category:
        stmt = stmt.where(Product.category == category)
    if q:
        stmt = stmt.where(
            or_(Product.name.contains(q), Product.description.contains(q))
        )
    if min_price is not None:
        stmt = stmt.where(Product.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Product.price <= max_price)
    products = db.scalars(stmt.order_by(Product.id.desc())).unique().all()
    fav_ids = _favorited_ids(db, user)
    return [
        ProductResponse.from_orm_product(p, is_favorited=p.id in fav_ids)
        for p in products
    ]


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    product = db.scalar(
        select(Product)
        .options(joinedload(Product.merchant))
        .where(Product.id == product_id)
    )
    if not product or product.status != "active":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")
    fav_ids = _favorited_ids(db, user)
    return ProductResponse.from_orm_product(
        product, is_favorited=product.id in fav_ids
    )
