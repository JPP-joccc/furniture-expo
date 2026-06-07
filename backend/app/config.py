from pathlib import Path
from typing import List

from pydantic import model_validator
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # 开发模式（生产环境设为 false）
    debug: bool = True

    database_url: str = f"sqlite:///{BASE_DIR / 'furniture.db'}"
    secret_key: str = "dev-only-insecure-key-change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 小时
    upload_dir: Path = BASE_DIR / "uploads"

    # CORS：生产环境填写正式域名，逗号分隔
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    # 可选：正则匹配多个前端域名（CloudBase 静态托管推荐）
    cors_origin_regex: str = ""
    # 仅开发/局域网演示时设为 true
    allow_lan_access: bool = False
    # 生产环境关闭 Swagger 文档
    enable_api_docs: bool = True

    # 商家注册邀请码；留空则禁止自助注册商家（开发默认见 .env.example）
    merchant_invite_code: str = "dev-merchant-invite"

    # 是否允许 seed.py 写入演示账号（生产环境必须为 false）
    allow_demo_seed: bool = True

    class Config:
        env_file = ".env"

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @model_validator(mode="before")
    @classmethod
    def normalize_database_url(cls, data):
        if isinstance(data, dict):
            url = data.get("database_url") or data.get("DATABASE_URL")
            if url and str(url).startswith("postgres://"):
                data["database_url"] = str(url).replace(
                    "postgres://", "postgresql://", 1
                )
        return data

    @model_validator(mode="after")
    def validate_production_settings(self):
        if not self.debug:
            if self.secret_key == "dev-only-insecure-key-change-me":
                raise ValueError("生产环境必须设置 SECRET_KEY 环境变量")
            if self.allow_lan_access:
                raise ValueError("生产环境禁止 ALLOW_LAN_ACCESS=true")
            if self.allow_demo_seed:
                raise ValueError("生产环境禁止 ALLOW_DEMO_SEED=true")
            if self.enable_api_docs:
                raise ValueError("生产环境必须设置 ENABLE_API_DOCS=false")
            if self.merchant_invite_code in ("", "dev-merchant-invite"):
                raise ValueError("生产环境必须设置自定义 MERCHANT_INVITE_CODE")
        return self


settings = Settings()
settings.upload_dir.mkdir(parents=True, exist_ok=True)
