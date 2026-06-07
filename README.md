# 家私家具展览系统

基于 **FastAPI + Vue 3** 的前后端分离家具展览平台，支持客户浏览收藏与商家商品管理，暂不包含支付功能。

## 功能概览

### 客户端
- 首页分类浏览与精选商品
- 产品列表（分类、关键词、价格筛选）
- 产品详情（多图、收藏、咨询）
- 我的收藏
- 注册 / 登录

### 商家端
- 仪表盘统计
- 商品 CRUD（含图片上传）
- 咨询管理

## 快速启动

### 环境要求
- Python 3.8+
- Node.js 18+

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload --port 8000
```

API 文档：http://localhost:8000/docs

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

访问：http://localhost:5173

## 手机访问（同一 WiFi）

电脑和手机连**同一个 WiFi** 时，手机可通过局域网链接访问。

### 1. 查电脑局域网 IP

Windows PowerShell：

```powershell
ipconfig
```

找到当前 WiFi 的 **IPv4 地址**，例如 `192.168.1.105`。

### 2. 启动服务（需监听局域网）

```bash
# 后端 — 注意加 --host 0.0.0.0
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 前端（已配置 --host，会暴露到局域网）
cd frontend
npm run dev
```

### 3. 手机浏览器打开

把 `192.168.1.105` 换成你的实际 IP：

```
http://192.168.1.105:5173
```

把这个链接发给同 WiFi 下的用户即可访问。Vite 会把 `/api` 请求转发到你电脑上的后端，手机无需单独配置。

### 4. 若手机打不开，检查

- 电脑和手机是否同一 WiFi（手机不要用 4G/5G）
- Windows 防火墙是否放行 5173、8000 端口
- IP 地址是否填对（不要用 `127.0.0.1`，那是本机地址）

---

## 公网访问（任何人、任何地点）

局域网链接**只有同一 WiFi 的人能访问**。要让外地客户通过链接进入，需要部署到公网：

| 方案 | 适用场景 | 说明 |
|------|----------|------|
| **云服务器** | 正式上线 | 买阿里云/腾讯云服务器，绑定域名，配置 HTTPS |
| **内网穿透** | 快速演示 | 用 [ngrok](https://ngrok.com)、花生壳等，获得临时公网链接 |
| **静态托管 + API** | 小规模 | 前端部署 Vercel/Netlify，后端部署 Railway/Render |

正式上线推荐：Nginx 反向代理，一个域名同时服务前端页面和 `/api` 接口。

## 演示账号

| 角色 | 邮箱 | 密码 |
|------|------|------|
| 商家 | merchant@demo.com | Demo12345 |
| 客户 | customer@demo.com | Demo12345 |

> 若演示账号无法登录，删除 `backend/furniture.db` 后重新执行 `python seed.py`。

## 生产环境安全配置

复制 `backend/.env.example` 为 `backend/.env`，生产环境至少设置：

```env
DEBUG=false
SECRET_KEY=<openssl rand -hex 32 生成的随机值>
ALLOW_LAN_ACCESS=false
ENABLE_API_DOCS=false
ALLOW_DEMO_SEED=false
MERCHANT_INVITE_CODE=<自定义商家邀请码>
CORS_ORIGINS=https://www.你的域名.com
```

已内置的安全措施：
- JWT 密钥强制从环境变量读取（生产模式）
- 登录/注册接口限流（5次/分钟、3次/分钟）
- 密码至少 8 位且含字母和数字
- 商家注册需邀请码
- 图片上传真实类型校验（Pillow）
- 安全响应头（HSTS、X-Frame-Options 等）
- 生产环境自动关闭 Swagger 文档

## 项目结构

```
furniture-expo/
├── backend/          # FastAPI 后端
│   ├── app/
│   │   ├── routers/    # API 路由
│   │   ├── models/     # SQLAlchemy 模型
│   │   └── schemas/    # Pydantic 校验
│   ├── seed.py         # 种子数据
│   └── requirements.txt
└── frontend/         # Vue 3 前端
    └── src/
        ├── views/customer/   # 客户端页面
        ├── views/merchant/   # 商家端页面
        └── api/              # API 封装
```
