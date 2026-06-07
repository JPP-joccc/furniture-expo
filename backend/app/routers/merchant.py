import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.dependencies import get_current_merchant
from app.models.inquiry import Inquiry
from app.models.product import Product
from app.models.user import User
from app.schemas.inquiry import InquiryResponse, InquiryUpdate
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/api/merchant", tags=["merchant"])


@router.get("/stats")
def get_stats(
    merchant: User = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    product_count = db.scalar(
        select(func.count()).select_from(Product).where(Product.merchant_id == merchant.id)
    )
    pending_inquiries = db.scalar(
        select(func.count())
        .select_from(Inquiry)
        .where(Inquiry.merchant_id == merchant.id, Inquiry.status == "pending")
    )
    return {
        "product_count": product_count or 0,
        "pending_inquiries": pending_inquiries or 0,
    }


@router.get("/products", response_model=List[ProductResponse])
def list_merchant_products(
    merchant: User = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    products = db.scalars(
        select(Product)
        .options(joinedload(Product.merchant))
        .where(Product.merchant_id == merchant.id)
        .order_by(Product.id.desc())
    ).unique().all()
    return [ProductResponse.from_orm_product(p) for p in products]


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    merchant: User = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    product = Product(
        name=data.name,
        description=data.description,
        category=data.category,
        material=data.material,
        price=data.price,
        images=json.dumps(data.images),
        status=data.status,
        merchant_id=merchant.id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    product = db.scalar(
        select(Product)
        .options(joinedload(Product.merchant))
        .where(Product.id == product.id)
    )
    return ProductResponse.from_orm_product(product)


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    merchant: User = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)
    if not product or product.merchant_id != merchant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")
    update_data = data.model_dump(exclude_unset=True)
    if "images" in update_data and update_data["images"] is not None:
        update_data["images"] = json.dumps(update_data["images"])
    for key, value in update_data.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    product = db.scalar(
        select(Product)
        .options(joinedload(Product.merchant))
        .where(Product.id == product.id)
    )
    return ProductResponse.from_orm_product(product)


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    merchant: User = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)
    if not product or product.merchant_id != merchant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")
    db.delete(product)
    db.commit()


@router.get("/inquiries", response_model=List[InquiryResponse])
def list_inquiries(
    merchant: User = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    inquiries = db.scalars(
        select(Inquiry)
        .options(joinedload(Inquiry.user), joinedload(Inquiry.product))
        .where(Inquiry.merchant_id == merchant.id)
        .order_by(Inquiry.id.desc())
    ).unique().all()
    result = []
    for inquiry in inquiries:
        result.append(
            InquiryResponse(
                id=inquiry.id,
                message=inquiry.message,
                contact=inquiry.contact,
                status=inquiry.status,
                user_id=inquiry.user_id,
                product_id=inquiry.product_id,
                merchant_id=inquiry.merchant_id,
                user_name=inquiry.user.name if inquiry.user else None,
                product_name=inquiry.product.name if inquiry.product else None,
            )
        )
    return result


@router.patch("/inquiries/{inquiry_id}", response_model=InquiryResponse)
def update_inquiry(
    inquiry_id: int,
    data: InquiryUpdate,
    merchant: User = Depends(get_current_merchant),
    db: Session = Depends(get_db),
):
    if data.status not in ("pending", "replied"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="无效状态")
    inquiry = db.scalar(
        select(Inquiry)
        .options(joinedload(Inquiry.user), joinedload(Inquiry.product))
        .where(Inquiry.id == inquiry_id, Inquiry.merchant_id == merchant.id)
    )
    if not inquiry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="咨询不存在")
    inquiry.status = data.status
    db.commit()
    db.refresh(inquiry)
    return InquiryResponse(
        id=inquiry.id,
        message=inquiry.message,
        contact=inquiry.contact,
        status=inquiry.status,
        user_id=inquiry.user_id,
        product_id=inquiry.product_id,
        merchant_id=inquiry.merchant_id,
        user_name=inquiry.user.name if inquiry.user else None,
        product_name=inquiry.product.name if inquiry.product else None,
    )
