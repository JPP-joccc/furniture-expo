from typing import Optional

from pydantic import BaseModel, Field


class InquiryCreate(BaseModel):
    product_id: int
    message: str = Field(min_length=1, max_length=1000)
    contact: str = Field(min_length=1, max_length=100)


class InquiryUpdate(BaseModel):
    status: str


class InquiryResponse(BaseModel):
    id: int
    message: str
    contact: str
    status: str
    user_id: int
    product_id: int
    merchant_id: int
    user_name: Optional[str] = None
    product_name: Optional[str] = None

    class Config:
        from_attributes = True
