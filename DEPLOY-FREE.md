# 免费上线指南（Vercel + Render + Neon）

不买服务器，用免费平台部署家具展览系统。

## 架构

```
用户浏览器
    ↓
Vercel（前端网页）  ──API 请求──→  Render（后端 API）
                                      ↓
                                 Neon（PostgreSQL 数据库）
```

## 第 1 步：把代码推到 GitHub

1. 注册 [GitHub](https://github.com)
2. 新建仓库 `furniture-expo`（Public 或 Private 均可）
3. 在本机 PowerShell 执行：

```powershell
cd d:\cursor\cursor\furniture-expo
git init
git add .
git commit -m "准备免费部署"
git branch -M main
git remote add origin https://github.com/你的用户名/furniture-expo.git
git push -u origin main
```

## 第 2 步：创建免费数据库（Neon）

> 跳过这步也能跑，但 Render 重启后 SQLite 数据会丢。正式演示建议用 Neon。

1. 打开 [https://neon.tech](https://neon.tech) 注册
2. **New Project** → 创建项目
3. 在 **Connection string** 复制 PostgreSQL 地址，形如：
   `postgresql://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require`
4. 保存备用（这是 `DATABASE_URL`）

## 第 3 步：部署后端到 Render

1. 打开 [https://render.com](https://render.com) 注册（可用 GitHub 登录）
2. 点击 **New +** → **Blueprint**
3. 连接 GitHub 仓库 `furniture-expo`
4. Render 会读取根目录的 `render.yaml`，点击 **Apply**

### 手动填写 3 个环境变量

在 Render 服务 **Environment** 里设置：

| 变量名 | 填什么 |
|--------|--------|
| `MERCHANT_INVITE_CODE` | 商家注册邀请码，如 `JiaJu2026` |
| `CORS_ORIGINS` | 先填 `https://placeholder.vercel.app`，第 5 步再改 |
| `DATABASE_URL` | 第 2 步 Neon 的连接字符串（没 Neon 可先不填，用 SQLite） |

`SECRET_KEY` 由 Render 自动生成。

5. 等待部署完成（约 3–5 分钟）
6. 记下后端地址，例如：`https://furniture-api-xxxx.onrender.com`
7. 浏览器打开 `https://你的后端地址.onrender.com/api/health`，应看到 `{"status":"ok"}`

## 第 4 步：部署前端到 Vercel

1. 打开 [https://vercel.com](https://vercel.com) 注册（可用 GitHub 登录）
2. **Add New → Project** → 导入 `furniture-expo` 仓库
3. 配置：

| 项 | 值 |
|----|-----|
| Framework Preset | Vite |
| Root Directory | `frontend` |
| Build Command | `npm run build` |
| Output Directory | `dist` |

4. 展开 **Environment Variables**，添加：

| Name | Value |
|------|-------|
| `VITE_API_BASE_URL` | `https://你的后端地址.onrender.com`（不要末尾斜杠） |

5. 点击 **Deploy**，等待完成
6. 记下 Vercel 地址，例如：`https://furniture-expo.vercel.app`

## 第 5 步：把前后端连起来

回到 **Render** → 你的后端服务 → **Environment**：

把 `CORS_ORIGINS` 改成你的 Vercel 地址：

```
https://furniture-expo.vercel.app
```

保存后 Render 会自动重新部署。

## 第 6 步：验收

在 Vercel 地址打开网站，检查：

- [ ] 首页能打开
- [ ] 可以注册客户账号
- [ ] 商家注册需要邀请码（第 3 步设的 `MERCHANT_INVITE_CODE`）
- [ ] 商家能上传商品
- [ ] 第一次打开若很慢（30–60 秒），是 Render 免费版从休眠唤醒，属正常

## 免费版限制（要知道）

| 项目 | 说明 |
|------|------|
| 冷启动 | Render 15 分钟无人访问会休眠，下次打开要等一会 |
| 图片 | 上传图片存在 Render 磁盘，**重新部署后可能丢失** |
| 流量 | 免费版有 monthly 限额，小流量演示够用 |

## 以后更新网站

改完代码后：

```powershell
cd d:\cursor\cursor\furniture-expo
git add .
git commit -m "更新内容"
git push
```

Render 和 Vercel 会自动重新部署（约 2–5 分钟）。

## 常见问题

**前端能开，登录/加载失败**
- 检查 Vercel 的 `VITE_API_BASE_URL` 是否正确
- 检查 Render 的 `CORS_ORIGINS` 是否包含 Vercel 地址（含 `https://`）

**后端部署失败**
- 在 Render **Logs** 查看报错
- 确认 `DEBUG=false` 时已设置 `MERCHANT_INVITE_CODE` 和 `SECRET_KEY`

**图片不显示**
- 确认 `VITE_API_BASE_URL` 已设置并重新 Deploy 前端
