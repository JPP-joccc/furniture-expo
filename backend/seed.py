import json

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models.product import Product
from app.models.user import Role, User
from app.utils.security import hash_password

DEMO_PASSWORD = "Demo12345"

SAMPLE_PRODUCTS = [
    {
        "name": "北欧布艺三人沙发",
        "description": "简约北欧风格，高密度海绵填充，可拆洗布艺外套，适合客厅使用。",
        "category": "沙发",
        "material": "布艺",
        "price": 3999,
        "images": ["/uploads/placeholder-sofa.jpg"],
    },
    {
        "name": "真皮电动功能沙发",
        "description": "头层牛皮，电动躺椅功能，USB充电接口，舒适居家体验。",
        "category": "沙发",
        "material": "真皮",
        "price": 8999,
        "images": ["/uploads/placeholder-sofa2.jpg"],
    },
    {
        "name": "实木双人床架",
        "description": "北美橡木打造，环保清漆，稳固承重，搭配储物抽屉设计。",
        "category": "床",
        "material": "实木",
        "price": 4599,
        "images": ["/uploads/placeholder-bed.jpg"],
    },
    {
        "name": "轻奢软包大床",
        "description": "高密度海绵软包头板，绒布面料，营造温馨卧室氛围。",
        "category": "床",
        "material": "绒布",
        "price": 5299,
        "images": ["/uploads/placeholder-bed2.jpg"],
    },
    {
        "name": "大理石餐桌椅组合",
        "description": "天然大理石台面，六人位餐桌椅套装，适合家庭聚餐。",
        "category": "餐桌",
        "material": "大理石",
        "price": 6800,
        "images": ["/uploads/placeholder-table.jpg"],
    },
    {
        "name": "实木伸缩餐桌",
        "description": "可伸缩设计，日常四人位，展开后容纳八人，节省空间。",
        "category": "餐桌",
        "material": "实木",
        "price": 3200,
        "images": ["/uploads/placeholder-table2.jpg"],
    },
    {
        "name": "现代简约书柜",
        "description": "多层开放式书架，E1级环保板材，适合书房与客厅展示。",
        "category": "柜子",
        "material": "板材",
        "price": 1899,
        "images": ["/uploads/placeholder-cabinet.jpg"],
    },
    {
        "name": "推拉门衣柜",
        "description": "2.4米宽推拉门设计，内部分区合理，镜面门板节省空间。",
        "category": "柜子",
        "material": "板材",
        "price": 4200,
        "images": ["/uploads/placeholder-wardrobe.jpg"],
    },
    {
        "name": "人体工学办公椅",
        "description": "网布透气靠背，腰托可调节，适合长时间办公使用。",
        "category": "桌椅",
        "material": "网布",
        "price": 1299,
        "images": ["/uploads/placeholder-chair.jpg"],
    },
    {
        "name": "岩板茶几",
        "description": "进口岩板台面，防刮耐磨，双层收纳设计，现代客厅必备。",
        "category": "桌椅",
        "material": "岩板",
        "price": 1599,
        "images": ["/uploads/placeholder-tea-table.jpg"],
    },
]


def seed():
    if not settings.allow_demo_seed:
        print("ALLOW_DEMO_SEED=false，跳过演示数据写入。")
        return

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == "merchant@demo.com").first():
            print("Seed data already exists, skipping.")
            print(f"演示密码（若无法登录请删除 furniture.db 后重跑）: {DEMO_PASSWORD}")
            return

        merchant = User(
            email="merchant@demo.com",
            password_hash=hash_password(DEMO_PASSWORD),
            name="雅致家居",
            role=Role.MERCHANT,
            shop_name="雅致家居旗舰店",
        )
        customer = User(
            email="customer@demo.com",
            password_hash=hash_password(DEMO_PASSWORD),
            name="张先生",
            role=Role.CUSTOMER,
        )
        db.add(merchant)
        db.add(customer)
        db.flush()

        for item in SAMPLE_PRODUCTS:
            product = Product(
                name=item["name"],
                description=item["description"],
                category=item["category"],
                material=item["material"],
                price=item["price"],
                images=json.dumps(item["images"]),
                status="active",
                merchant_id=merchant.id,
            )
            db.add(product)

        db.commit()
        print("Seed data created successfully.")
        print(f"Merchant: merchant@demo.com / {DEMO_PASSWORD}")
        print(f"Customer: customer@demo.com / {DEMO_PASSWORD}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
