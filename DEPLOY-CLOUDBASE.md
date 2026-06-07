# 免费上线：Vercel + Neon + 腾讯云 CloudBase

## 架构

```
用户浏览器
    ↓
Vercel（前端 Vue）
    ↓ API
CloudBase 云托管（后端 FastAPI，端口 8080）
    ↓
Neon（PostgreSQL 数据库）
```

## 第 1 步：Neon 数据库

1. 打开 https://neon.tech 注册
2. **New Project** 创建项目
3. 复制 **Connection string**（`postgresql://...`）
4. 保存为 `DATABASE_URL`

## 第 2 步：代码推到 GitHub

```powershell
cd d:\cursor\cursor\furniture-expo
git add .
git commit -m "CloudBase 部署"
git push
```

## 第 3 步：开通 CloudBase 云托管

1. 打开 https://cloud.tencent.com/product/tcb
2. 注册 / 登录腾讯云
3. 进入 **云开发控制台** → **创建环境**
4. 选择 **按量计费**（新用户通常有免费额度）
5. 左侧菜单 → **云托管**

## 第 4 步：部署后端

1. 点击 **新建服务**
2. 服务名称：`furniture-api`
3. 部署方式：**上传代码包** 或 **从 Git 仓库拉取**
4. 若从 GitHub 拉取：
   - 授权 GitHub
   - 选择 `furniture-expo` 仓库
   - **目标目录**：`backend`
5. 端口：**8080**
6. Dockerfile 名称：`Dockerfile`（默认）

### 环境变量（服务设置 → 环境变量）

| 变量名 | 值 |
|--------|-----|
| `DEBUG` | `false` |
| `SECRET_KEY` | 随机长字符串 |
| `ALLOW_LAN_ACCESS` | `false` |
| `ENABLE_API_DOCS` | `false` |
| `ALLOW_DEMO_SEED` | `false` |
| `MERCHANT_INVITE_CODE` | 如 `JiaJu2026` |
| `DATABASE_URL` | Neon 连接字符串 |
| `CORS_ORIGINS` | 先填 `https://temp.vercel.app`，第 6 步再改 |

生成随机密钥：

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

7. 点击 **创建并等待部署**（约 5–10 分钟）
8. 部署完成后，在 **服务详情 → 默认域名** 复制地址，例如：

```
https://furniture-api-xxx.sh.run.tcloudbase.com
```

9. 浏览器测试：

```
https://你的CloudBase地址/api/health
```

应返回 `{"status":"ok"}`

## 第 5 步：Vercel 部署前端

1. 打开 https://vercel.com → 导入 `furniture-expo`
2. Root Directory：`frontend`
3. 环境变量：

| Name | Value |
|------|-------|
| `VITE_API_BASE_URL` | CloudBase 后端地址（无末尾 `/`） |

4. Deploy，记下地址，如 `https://furniture-expo.vercel.app`

## 第 6 步：连接前后端

回到 CloudBase → `furniture-api` → **环境变量**：

把 `CORS_ORIGINS` 改成 Vercel 地址：

```
https://furniture-expo.vercel.app
```

保存后会自动重新部署。

## 第 7 步：验收

- [ ] Vercel 首页能打开
- [ ] 注册 / 登录正常
- [ ] Neon 控制台能看到数据表
- [ ] 商家注册需要邀请码

## 免费额度说明

- CloudBase 新用户有云托管 / 云函数免费试用额度
- 小流量演示一般够用
- 超出后按量计费，可在控制台设置预算告警

## 注意事项

- **上传的图片**存在容器临时磁盘，重新部署后可能丢失；正式运营建议接对象存储（COS）
- 改代码后：推 GitHub → CloudBase 重新部署；Vercel 自动部署

## 常见问题

**部署失败 / 构建超时**

- 确认目标目录是 `backend`，且其中有 `Dockerfile`
- 查看 CloudBase **部署日志**

**前端能开，API 失败**

- 检查 Vercel 的 `VITE_API_BASE_URL`
- 检查 CloudBase 的 `CORS_ORIGINS` 是否包含 Vercel 完整地址

**数据库连接失败**

- 确认 `DATABASE_URL` 是 Neon 的 `postgresql://` 格式
- Neon 项目需允许外网连接（默认允许）
