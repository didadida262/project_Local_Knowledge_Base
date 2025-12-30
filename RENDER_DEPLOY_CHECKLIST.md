# Render 部署检查清单

## ✅ 配置文件检查

### 后端配置
- [x] `render.yaml` - Render 部署配置
- [x] `requirements.txt` - Python 依赖
- [x] `backend/api_server.py` - 支持环境变量 PORT 和 HOST
- [x] 后端代码支持从环境变量读取端口和主机

### 前端配置
- [x] `frontend/src/services/api.ts` - 支持环境变量 VITE_API_URL
- [x] 前端构建配置正常

## 📋 Render 部署步骤

### 第一步：在 Render 上创建服务

1. **访问 Render**
   - 打开 https://render.com/
   - 使用 GitHub 账号登录

2. **创建 Web Service**
   - 点击右上角 "New" → "Web Service"
   - 选择 "Build and deploy from a Git repository"
   - 连接你的 GitHub 账号（如果还没连接）
   - 选择你的仓库：`project_Local_Knowledge_Base`

3. **配置服务信息**
   - **Name**: `knowledge-base-backend`
   - **Region**: 选择离你最近的区域（如 `Singapore` 或 `Oregon`）
   - **Branch**: `main` 或 `master`（根据你的默认分支）
   - **Root Directory**: 留空（项目根目录）

4. **配置构建和启动**
   - **Environment**: 选择 `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && python3 api_server.py`

5. **选择计划**
   - **Plan**: 选择 `Free`（免费，有休眠限制）
   - 或选择 `Starter`（$7/月，无休眠限制）

6. **环境变量**
   在 "Environment Variables" 部分，添加以下变量：
   ```
   PORT=5000
   HOST=0.0.0.0
   HF_HUB_DOWNLOAD_TIMEOUT=300
   ```

7. **创建服务**
   - 点击 "Create Web Service"
   - Render 会开始构建和部署

### 第二步：等待部署完成

1. **构建过程**
   - 首次部署可能需要 5-10 分钟
   - 会看到构建日志：
     - 安装 Python 依赖
     - 下载 AI 模型（可能需要较长时间）
     - 启动服务

2. **获取服务 URL**
   - 部署完成后，Render 会提供一个 URL
   - 格式如：`https://knowledge-base-backend.onrender.com`
   - **重要**：记下这个 URL，后续需要配置到前端

3. **测试后端**
   - 访问：`https://your-backend-url.onrender.com/api/health`
   - 应该返回 `{"status": "healthy"}`

### 第三步：部署前端到 Cloudflare Pages

1. **构建前端**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **在 Cloudflare Pages 部署**
   - 访问 https://dash.cloudflare.com/
   - 进入 "Pages" → "Create a project"
   - 选择 "Connect to Git"
   - 连接你的 GitHub 仓库

3. **配置构建设置**
   - **Framework preset**: `Vite`
   - **Build command**: `cd frontend && npm install && npm run build`
   - **Build output directory**: `frontend/dist`
   - **Root directory**: `/`（项目根目录）

4. **配置环境变量**
   在 "Environment variables" 中添加：
   ```
   VITE_API_URL=https://your-backend-url.onrender.com/api
   ```
   ⚠️ 将 `your-backend-url` 替换为 Render 给你的实际 URL

5. **部署**
   - 点击 "Save and Deploy"
   - 等待构建完成

### 第四步：测试部署

1. **访问前端**
   - Cloudflare Pages 会提供一个 URL
   - 格式如：`https://your-project.pages.dev`

2. **测试功能**
   - 测试上传文件
   - 测试问答功能
   - 检查浏览器控制台是否有错误

## ⚠️ 注意事项

### 首次访问延迟
- Render 免费版有休眠限制
- 如果服务休眠，首次访问需要等待 30-60 秒启动
- 这是正常现象，服务启动后会正常响应

### 模型下载
- 首次部署时，需要下载 AI 模型（~100MB）
- 这可能需要较长时间（5-10 分钟）
- 请耐心等待构建完成

### CORS 配置
- 后端已配置允许所有来源的 CORS
- 如果需要限制，可以修改 `backend/api_server.py` 中的 `send_cors_headers` 方法

### 文件上传限制
- Render 免费版有存储限制
- 上传的文件会保存在服务实例中
- 服务重启后，上传的文件可能会丢失（除非使用持久化存储）

## 🔧 故障排查

### 构建失败
- 检查 `requirements.txt` 是否正确
- 查看 Render 构建日志
- 确保 Python 版本兼容

### 服务无法启动
- 检查环境变量是否正确设置
- 查看 Render 服务日志
- 确保 `PORT` 和 `HOST` 环境变量已设置

### 前端无法连接后端
- 检查 `VITE_API_URL` 环境变量是否正确
- 检查后端 URL 是否可访问
- 检查浏览器控制台的错误信息

### 模型加载失败
- 检查网络连接（需要访问 Hugging Face）
- 增加 `HF_HUB_DOWNLOAD_TIMEOUT` 的值
- 查看后端日志

## 📝 部署后配置

### 更新环境变量
如果需要更新环境变量：
1. 在 Render Dashboard 中进入服务设置
2. 点击 "Environment"
3. 添加或修改环境变量
4. 服务会自动重新部署

### 查看日志
- 在 Render Dashboard 中点击 "Logs"
- 可以查看实时日志
- 帮助排查问题

## ✅ 部署完成检查清单

- [ ] 后端服务已部署并可以访问
- [ ] 前端已部署并可以访问
- [ ] 前端可以成功连接后端 API
- [ ] 文件上传功能正常
- [ ] 问答功能正常
- [ ] 浏览器控制台无错误

## 🎉 完成！

部署完成后，你的应用就可以通过 Cloudflare Pages 的 URL 访问了！

