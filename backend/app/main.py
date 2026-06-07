from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.database import Base, engine
from app.limiter import limiter
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.models import Favorite, Inquiry, Product, User  # noqa: F401
from app.routers import auth, favorites, inquiries, merchant, products, upload

app = FastAPI(
    title="家私家具展览系统",
    version="1.0.0",
    docs_url="/docs" if settings.enable_api_docs else None,
    redoc_url="/redoc" if settings.enable_api_docs else None,
    openapi_url="/openapi.json" if settings.enable_api_docs else None,
)


@app.on_event("startup")
def init_database():
    Base.metadata.create_all(bind=engine)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SecurityHeadersMiddleware)

if settings.allow_lan_access:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https?://.*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
elif settings.cors_origin_regex:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=settings.cors_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.mount("/uploads", StaticFiles(directory=str(settings.upload_dir)), name="uploads")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(favorites.router)
app.include_router(inquiries.router)
app.include_router(merchant.router)
app.include_router(upload.router)


@app.get("/")
def root():
    return {
        "name": "家私家具展览系统 API",
        "status": "running",
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}
