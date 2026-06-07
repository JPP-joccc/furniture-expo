from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_customer
from app.models.inquiry import Inquiry
from app.models.product import Product
from app.models.user import User
from app.schemas.inquiry import InquiryCreate, InquiryResponse

router = APIRouter(prefix="/api/inquiries", tags=["inquiries"])


@router.post("", response_model=InquiryResponse, status_code=status.HTTP_201_CREATED)
def create_inquiry(
    data: InquiryCreate,
    user: User = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    product = db.get(Product, data.product_id)
    if not product or product.status != "active":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")
    inquiry = Inquiry(
        message=data.message,
        contact=data.contact,
        user_id=user.id,
        product_id=product.id,
        merchant_id=product.merchant_id,
    )
    db.add(inquiry)
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
        user_name=user.name,
        product_name=product.name,
    )
