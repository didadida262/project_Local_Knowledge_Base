# 后端部署替代方案（Railway 不可用时）

由于 Railway 免费计划有 "Limited Access" 限制，以下是推荐的替代方案：

## 🚀 方案一：Render（最简单，推荐新手）

### 优点
- ✅ 免费计划可用
- ✅ 界面友好，配置简单
- ✅ 自动 HTTPS
- ✅ 支持 GitHub 自动部署

### 缺点
- ⚠️ 免费版有休眠限制（15分钟无活动后休眠，首次访问需要等待启动）

**休眠机制详解**：
- **什么是休眠**：如果服务在 15 分钟内没有任何请求，Render 会自动停止（休眠）你的服务以节省资源
- **首次访问等待**：当服务休眠后，第一次访问时 Render 需要重新启动服务，这个过程通常需要 30-60 秒
- **后续访问**：服务启动后，在 15 分钟内有请求时，服务会保持运行，响应速度正常
- **影响**：如果用户访问时服务正在休眠，会看到较长的加载时间（等待服务启动）
- **解决方案**：
  1. 升级到付费计划（$7/月起）可避免休眠
  2. 使用定时任务定期访问服务保持活跃（但可能违反服务条款）
  3. 使用 Fly.io 等无休眠限制的平台

### 部署步骤

1. **访问 Render**
   - 打开 https://render.com/
   - 使用 GitHub 登录

2. **创建 Web Service**
   - 点击 "New" → "Web Service"
   - 连接你的 GitHub 仓库

3. **配置服务**
   - **Name**: `knowledge-base-backend`
   - **Environment**: `Python 3`
   - **Region**: 选择离你最近的区域
   - **Branch**: `main` 或 `master`
   - **Root Directory**: 留空（项目根目录）
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && python3 api_server.py`
   - **Plan**: 选择 "Free"（免费，有休眠）或 "Starter"（$7/月，无休眠）

4. **环境变量**
   在 "Environment" 标签页添加：
   ```
   PORT=5000
   HOST=0.0.0.0
   HF_HUB_DOWNLOAD_TIMEOUT=300
   ```

5. **部署**
   - 点击 "Create Web Service"
   - 等待构建和部署完成（首次部署可能需要 5-10 分钟）
   - 记下生成的 URL（如：`https://knowledge-base-backend.onrender.com`）

## 🚀 方案二：Fly.io（推荐，无休眠限制）

### 优点
- ✅ 免费额度充足（3 个共享 CPU、256MB RAM）
- ✅ **无休眠限制**（服务一直运行）
- ✅ 全球边缘节点，速度快
- ✅ 支持 Docker 部署

### 缺点
- ⚠️ 需要安装 CLI 工具
- ⚠️ 配置稍复杂

### 部署步骤

1. **安装 Fly CLI**

```bash
# macOS
curl -L https://fly.io/install.sh | sh

# 或使用 Homebrew
brew install flyctl

# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

2. **登录 Fly.io**

```bash
flyctl auth login
```

3. **初始化项目**

```bash
cd backend
flyctl launch
```

按提示配置：
- **App name**: `knowledge-base-backend`（或自定义，需全局唯一）
- **Region**: 选择离你最近的区域（如 `sjc` 旧金山）
- **PostgreSQL**: 选择 `No`（本项目不需要数据库）
- **Redis**: 选择 `No`

4. **检查配置文件**

确保 `backend/fly.toml` 存在且配置正确（项目已包含此文件）

5. **部署**

```bash
flyctl deploy
```

首次部署会：
- 构建 Docker 镜像
- 上传到 Fly.io
- 启动服务

6. **获取 URL**

部署完成后，Fly.io 会显示服务 URL，格式如：
```
https://knowledge-base-backend.fly.dev
```

7. **查看日志**

```bash
flyctl logs
```

8. **查看服务状态**

```bash
flyctl status
```

## 🚀 方案三：Zeabur（新平台，类似 Railway）

### 优点
- ✅ 免费计划可用
- ✅ 界面类似 Railway
- ✅ 支持多种语言

### 部署步骤

1. 访问 https://zeabur.com/
2. 使用 GitHub 登录
3. 点击 "New Project"
4. 选择你的仓库
5. 自动检测 Python 项目
6. 配置环境变量并部署

## 🚀 方案四：DigitalOcean App Platform

### 优点
- ✅ 稳定可靠
- ✅ 自动 HTTPS
- ✅ 支持 GitHub 自动部署

### 缺点
- ⚠️ 最低 $5/月

### 部署步骤

1. 访问 https://www.digitalocean.com/products/app-platform
2. 创建新应用
3. 连接 GitHub 仓库
4. 配置构建和启动命令
5. 部署

## 🚀 方案五：本地服务器 + Cloudflare Tunnel（免费但需要服务器）

如果你有自己的服务器（VPS），可以使用 Cloudflare Tunnel：

1. 在服务器上部署后端
2. 使用 Cloudflare Tunnel 暴露服务
3. 获得免费的 HTTPS 和 CDN

## 推荐选择

- **新手/快速部署**: 使用 **Render**（最简单）
- **需要无休眠**: 使用 **Fly.io**（推荐）
- **预算充足**: 使用 **DigitalOcean**（最稳定）

## 部署后配置

无论使用哪个平台，部署完成后：

1. **获取后端 URL**
   - Render: `https://your-app.onrender.com`
   - Fly.io: `https://your-app.fly.dev`
   - 其他平台类似

2. **更新前端环境变量**
   在 Cloudflare Pages 的环境变量中设置：
   ```
   VITE_API_URL=https://your-backend-url.onrender.com/api
   ```

3. **测试部署**
   - 访问前端 URL
   - 测试上传文件
   - 测试问答功能

## 故障排查

### Render 部署问题

- **构建失败**: 检查 `requirements.txt` 是否正确
- **启动失败**: 检查 `PORT` 环境变量是否设置
- **休眠问题**: 免费版会休眠，首次访问需要等待 30-60 秒

### Fly.io 部署问题

- **CLI 未安装**: 按照官方文档安装
- **部署失败**: 检查 `Dockerfile` 是否正确
- **服务无法访问**: 检查 `fly.toml` 配置

### 通用问题

- **CORS 错误**: 检查后端 CORS 配置
- **模型加载失败**: 检查网络连接和超时设置
- **文件上传失败**: 检查文件大小限制

