# Cloudflare Pages 前端配置指南

## ✅ 正确的配置

### Build settings

1. **Framework preset**
   - 选择：`Vite` 或 `None`（都可以）

2. **Build command**
   - ✅ `cd frontend && npm install && npm run build`
   - 这个配置是正确的

3. **Build output directory**
   - ✅ **可以使用**：`/frontend/dist` 或 `frontend/dist` 都可以
   - Cloudflare Pages 会自动处理开头的斜杠
   - 两种写法效果相同：都是从项目根目录开始的路径
   - 如果界面默认显示 `/frontend/dist`，保持这样即可

4. **Root directory (advanced)**
   - 可以留空（默认是项目根目录）
   - 或者设置为 `/`（项目根目录）

### Environment variables

**重要**：`VITE_API_URL` 的值需要包含 `/api` 路径！

- ❌ **错误**：`https://knowledge-base-backend-delicate-forest-9324.fly.dev`
- ✅ **正确**：`https://knowledge-base-backend-delicate-forest-9324.fly.dev/api`

**原因**：
- 前端代码中，API 请求会直接使用 `VITE_API_URL` 作为 baseURL
- 如果只设置域名，请求会发送到 `https://xxx.fly.dev/stats`（缺少 `/api` 前缀）
- 正确设置后，请求会发送到 `https://xxx.fly.dev/api/stats`

## 📋 完整配置清单

### Build settings
```
Framework preset: Vite（或 None）
Build command: cd frontend && npm install && npm run build
Build output directory: frontend/dist
Root directory: （留空或 /）
```

### Environment variables
```
Variable name: VITE_API_URL
Value: https://knowledge-base-backend-delicate-forest-9324.fly.dev/api
```

## ⚠️ 常见错误

1. **Build output directory 路径**
   - ✅ `/frontend/dist` 和 `frontend/dist` 都可以
   - Cloudflare Pages 会正确处理，两种写法效果相同

2. **API URL 缺少 /api 路径**
   - ❌ `https://xxx.fly.dev`
   - ✅ `https://xxx.fly.dev/api`

3. **Root directory 设置错误**
   - 如果设置了 Root directory，Build output directory 需要相应调整
   - 建议：Root directory 留空，使用默认值

## 🔍 验证配置

部署后，检查：
1. 打开浏览器开发者工具
2. 查看 Network 标签
3. 检查 API 请求的 URL 是否正确
4. 应该看到请求发送到：`https://xxx.fly.dev/api/xxx`

## 📝 配置示例

### 方案 A：使用 Root directory（推荐）

```
Root directory: frontend
Build command: npm install && npm run build
Build output directory: dist
```

### 方案 B：不使用 Root directory（当前配置）

```
Root directory: （留空）
Build command: cd frontend && npm install && npm run build
Build output directory: frontend/dist
```

两种方案都可以，选择一种即可。

