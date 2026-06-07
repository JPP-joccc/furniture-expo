from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.schemas.favorite import FavoriteCreate, FavoriteResponse
from app.schemas.inquiry import InquiryCreate, InquiryResponse, InquiryUpdate
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

__all__ = [
    "RegisterRequest",
    "LoginRequest",
    "TokenResponse",
    "UserResponse",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "FavoriteCreate",
    "FavoriteResponse",
    "InquiryCreate",
    "InquiryResponse",
    "InquiryUpdate",
]
