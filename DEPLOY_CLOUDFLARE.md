# Cloudflare 部署指南

## ⚠️ Cloudflare 后端部署限制

**重要说明**：Cloudflare 目前**不能直接部署 Python 后端**，原因如下：

1. **Cloudflare Workers**：
   - ✅ 支持：JavaScript/TypeScript（使用 V8 引擎）
   - ❌ 不支持：Python、Java、Go 等语言
   - ❌ 限制：CPU 时间限制（免费版 10ms，付费版 50ms-30s）
   - ❌ 限制：不支持长时间运行的进程
   - ❌ 限制：不支持安装大型依赖包（如 AI 模型）

2. **Cloudflare Pages**：
   - ✅ 支持：静态网站部署
   - ✅ 支持：全栈框架（Next.js、Nuxt.js 等，但后端代码会被编译为 JavaScript）
   - ❌ 不支持：独立的 Python 后端服务

3. **本项目需求**：
   - Python 后端（使用 `http.server`）
   - AI 模型（SentenceTransformer，需要下载 ~100MB+ 模型文件）
   - 长时间运行（处理文件上传、模型推理）
   - 持久化存储（知识库文件）

**结论**：本项目**必须使用混合部署方案**。

## 推荐部署方案

本项目采用混合部署方案：
- **前端**：部署到 Cloudflare Pages（静态托管）
- **后端**：部署到支持 Python 和 AI 模型的平台（推荐：Railway、Render 或 Fly.io）

## 方案一：前端 Cloudflare Pages + 后端 Railway/Render

### 第一步：部署后端到 Railway 或 Render

#### 选项 A：Railway 部署

1. **准备部署文件**

在项目根目录创建 `railway.json`（可选）：
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && python3 api_server.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

创建 `Procfile`（Railway 会自动识别）：
```
web: cd backend && python3 api_server.py
```

2. **在 Railway 上部署**

   - 访问 [Railway](https://railway.app/)
   - 使用 GitHub 登录
   - 点击 "New Project" → "Deploy from GitHub repo"
   - 选择你的仓库
   - Railway 会自动检测 Python 项目并开始构建
   - 等待部署完成，记下生成的域名（如：`your-app.railway.app`）

3. **配置环境变量**

   在 Railway 项目设置中添加环境变量：
   ```
   PORT=5000
   ```

4. **获取后端 URL**

   Railway 会自动分配一个 URL，格式如：`https://your-app.railway.app`

#### 选项 B：Render 部署

1. **准备部署文件**

创建 `render.yaml`：
```yaml
services:
  - type: web
    name: knowledge-base-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: cd backend && python3 api_server.py
    envVars:
      - key: PORT
        value: 5000
```

2. **在 Render 上部署**

   - 访问 [Render](https://render.com/)
   - 使用 GitHub 登录
   - 点击 "New" → "Web Service"
   - 连接你的 GitHub 仓库
   - 配置：
     - **Name**: `knowledge-base-backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `cd backend && python3 api_server.py`
   - 点击 "Create Web Service"
   - 等待部署完成，记下生成的域名

### 第二步：配置前端 API 地址

1. **修改前端 API 配置**

编辑 `frontend/src/services/api.ts`，将 API 基础 URL 改为环境变量：

```typescript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 30000,
})
```

2. **创建环境变量文件**

创建 `frontend/.env.production`：
```
VITE_API_URL=https://your-backend-url.railway.app/api
```

创建 `frontend/.env.development`（本地开发用）：
```
VITE_API_URL=http://127.0.0.1:5000/api
```

### 第三步：部署前端到 Cloudflare Pages

1. **构建前端**

```bash
cd frontend
npm install
npm run build
```

构建产物会在 `frontend/dist` 目录。

2. **通过 Cloudflare Dashboard 部署**

   - 访问 [Cloudflare Dashboard](https://dash.cloudflare.com/)
   - 登录你的账户
   - 点击左侧菜单 "Pages"
   - 点击 "Create a project"
   - 选择 "Upload assets"
   - 上传 `frontend/dist` 目录中的所有文件
   - 项目名称：`knowledge-base-frontend`
   - 点击 "Deploy site"

3. **通过 Git 连接部署（推荐）**

   - 在 Cloudflare Pages 中点击 "Create a project"
   - 选择 "Connect to Git"
   - 连接你的 GitHub 仓库
   - 配置构建设置：
     - **Framework preset**: `Vite`
     - **Build command**: `cd frontend && npm install && npm run build`
     - **Build output directory**: `frontend/dist`
     - **Root directory**: `/`（项目根目录）
   - 添加环境变量：
     - **Variable name**: `VITE_API_URL`
     - **Value**: `https://your-backend-url.railway.app/api`
   - 点击 "Save and Deploy"

4. **配置自定义域名（可选）**

   - 在 Cloudflare Pages 项目设置中
   - 点击 "Custom domains"
   - 添加你的域名
   - 按照提示配置 DNS 记录

### 第四步：配置 CORS

确保后端允许 Cloudflare Pages 的域名访问。

编辑 `backend/api_server.py` 中的 `send_cors_headers` 方法（约第 95 行）：

```python
def send_cors_headers(self):
    """发送CORS头"""
    origin = self.headers.get('Origin', '*')
    # 允许 Cloudflare Pages 域名
    allowed_origins = [
        'https://your-frontend.pages.dev',  # 替换为你的 Cloudflare Pages 域名
        'https://your-custom-domain.com',   # 替换为你的自定义域名（如果有）
        'http://localhost:3000',            # 本地开发
    ]
    
    # 允许所有 .pages.dev 域名（Cloudflare Pages 默认域名）
    if origin in allowed_origins or (origin and origin.endswith('.pages.dev')):
        self.send_header('Access-Control-Allow-Origin', origin)
    else:
        # 开发环境允许所有来源，生产环境建议限制
        self.send_header('Access-Control-Allow-Origin', '*')
    
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    self.send_header('Content-Type', 'application/json')
```

**注意**：如果使用环境变量管理允许的域名，可以这样配置：

```python
import os

def send_cors_headers(self):
    """发送CORS头"""
    origin = self.headers.get('Origin', '*')
    allowed_origins_str = os.getenv('ALLOWED_ORIGINS', '')
    allowed_origins = [o.strip() for o in allowed_origins_str.split(',') if o.strip()]
    
    if origin in allowed_origins or (origin and origin.endswith('.pages.dev')):
        self.send_header('Access-Control-Allow-Origin', origin)
    else:
        self.send_header('Access-Control-Allow-Origin', '*')
    
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    self.send_header('Content-Type', 'application/json')
```

然后在后端环境变量中添加：
```
ALLOWED_ORIGINS=https://your-frontend.pages.dev,https://your-custom-domain.com
```

### 第五步：测试部署

1. 访问 Cloudflare Pages 提供的 URL
2. 测试上传文件功能
3. 测试问答功能
4. 检查浏览器控制台是否有错误

## 方案二：使用 Cloudflare Workers 作为 API 代理（可选）

如果你想让所有流量都通过 Cloudflare，可以使用 Workers 作为**反向代理**（后端仍然部署在其他平台）：

### 优点
- ✅ 统一域名（前端和 API 都通过同一个域名）
- ✅ 利用 Cloudflare 的 CDN 和 DDoS 保护
- ✅ 隐藏后端真实地址

### 缺点
- ⚠️ 增加一层代理，可能有轻微延迟
- ⚠️ 大文件上传可能受 Workers 限制

### 实现步骤

1. **创建 Cloudflare Worker**

在 Cloudflare Dashboard 中创建新的 Worker，使用以下代码：

```javascript
// worker.js
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // 代理 API 请求到后端
    if (url.pathname.startsWith('/api')) {
      // 从环境变量读取后端 URL
      const backendUrl = env.BACKEND_URL || 'https://your-backend-url.railway.app';
      const newUrl = new URL(url.pathname + url.search, backendUrl);
      
      // 创建新请求
      const newRequest = new Request(newUrl, {
        method: request.method,
        headers: request.headers,
        body: request.body,
      });
      
      // 转发请求并返回响应
      const response = await fetch(newRequest);
      
      // 复制响应头（包括 CORS）
      const newResponse = new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: response.headers,
      });
      
      return newResponse;
    }
    
    // 其他请求（前端静态资源）由 Cloudflare Pages 处理
    // 这里可以返回 404 或重定向到 Pages
    return new Response('Not Found', { status: 404 });
  }
}
```

2. **配置环境变量**

在 Worker 设置中添加：
- **Variable name**: `BACKEND_URL`
- **Value**: `https://your-backend-url.railway.app`

3. **绑定到域名**

- 在 Worker 设置中点击 "Add route"
- 添加路由规则：`your-domain.com/api/*`
- 这样所有 `/api/*` 请求都会被 Worker 代理到后端

4. **更新前端配置**

前端不需要修改，因为 API 请求仍然发送到 `/api`，但会被 Worker 代理到后端。

### 注意事项

- Workers 有请求大小限制（免费版 100KB，付费版更大）
- 大文件上传可能需要直接访问后端，或使用分块上传
- 超时限制：免费版 10ms CPU 时间，付费版更长（但网络请求时间不受此限制）

## 注意事项

### 模型文件大小限制

- **Cloudflare Pages**: 单个文件最大 25MB，总大小无限制
- **Railway**: 免费版有存储限制，付费版更大
- **Render**: 免费版有存储限制

如果模型文件太大，考虑：
1. 使用外部模型服务（如 Hugging Face Inference API）
2. 使用 CDN 存储模型文件
3. 在部署时下载模型

### 环境变量管理

- **Cloudflare Pages**: 在项目设置中配置环境变量
- **Railway/Render**: 在服务设置中配置环境变量

### 持久化存储

知识库数据需要持久化存储：
- **Railway**: 使用 Volume 或外部数据库
- **Render**: 使用 Disk 或外部数据库
- 考虑使用外部存储（如 S3、Cloudflare R2）

### 性能优化

1. **启用 Cloudflare CDN**: 自动启用
2. **启用压缩**: 在 Cloudflare 设置中启用 Brotli 压缩
3. **缓存策略**: 配置适当的缓存头

## 故障排查

### 前端无法连接后端

1. 检查 `VITE_API_URL` 环境变量是否正确
2. 检查后端 CORS 配置
3. 检查后端是否正常运行

### 模型加载失败

1. 检查模型文件是否在部署环境中
2. 检查网络连接（需要访问 Hugging Face）
3. 考虑使用预下载的模型文件

### 上传文件失败

1. 检查文件大小限制
2. 检查后端存储空间
3. 检查权限设置

## 推荐配置

### 生产环境环境变量

**前端（Cloudflare Pages）**:
```
VITE_API_URL=https://your-backend.railway.app/api
```

**后端（Railway/Render）**:
```
PORT=5000
HF_HUB_DOWNLOAD_TIMEOUT=300
```

## 更新部署

### 更新前端

- 推送到 GitHub，Cloudflare Pages 会自动重新部署
- 或手动在 Cloudflare Dashboard 中触发部署

### 更新后端

- 推送到 GitHub，Railway/Render 会自动重新部署
- 或手动在平台中触发重新部署

## 成本估算

- **Cloudflare Pages**: 免费（有使用限制）
- **Railway**: 免费版 $5/月额度，超出后按使用付费
- **Render**: 免费版有限制，付费版 $7/月起

## 替代方案：全栈部署到单一平台

如果你希望前端和后端部署在同一个平台，可以考虑：

### 1. Fly.io（推荐）

- ✅ 支持 Python 后端
- ✅ 支持 Docker 部署
- ✅ 可以部署前端和后端
- ✅ 全球边缘节点
- ✅ 免费额度：3 个共享 CPU、256MB RAM

**部署步骤**：
1. 创建 `Dockerfile` 和 `fly.toml`
2. 使用 `flyctl` CLI 部署
3. 前端可以构建后作为静态文件服务

### 2. Railway

- ✅ 支持 Python 后端
- ✅ 可以部署前端和后端（使用多个服务）
- ✅ 自动 HTTPS
- ✅ 免费额度：$5/月

### 3. Render

- ✅ 支持 Python 后端
- ✅ 可以部署前端和后端
- ✅ 自动 HTTPS
- ⚠️ 免费版有休眠限制

### 4. DigitalOcean App Platform

- ✅ 支持 Python 后端
- ✅ 可以部署前端和后端
- ✅ 自动 HTTPS
- ⚠️ 最低 $5/月起

### 5. Vercel（仅前端）+ 后端其他平台

- ✅ Vercel 部署前端（免费）
- ✅ 后端部署到 Railway/Render
- ✅ 两者都支持自动部署

### 6. AWS/GCP/Azure（企业级）

- ✅ 完全控制
- ✅ 可扩展性强
- ⚠️ 配置复杂
- ⚠️ 成本较高

