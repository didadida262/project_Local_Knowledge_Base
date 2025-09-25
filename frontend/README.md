# 前端应用

基于React + TypeScript + Vite的现代化前端界面。

## 🚀 快速开始

### 开发模式

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 构建生产版本

```bash
# 构建应用
npm run build

# 预览构建结果
npm run preview
```

## 📁 项目结构

```
frontend/
├── src/
│   ├── components/          # React组件
│   │   ├── StatsCard.tsx   # 统计卡片
│   │   ├── SearchTab.tsx   # 搜索标签页
│   │   ├── QATab.tsx       # 问答标签页
│   │   └── DocumentsTab.tsx # 文档管理标签页
│   ├── services/           # API服务
│   │   └── api.ts          # API接口
│   ├── App.tsx             # 主应用组件
│   ├── main.tsx            # 应用入口
│   └── index.css           # 全局样式
├── public/                 # 静态资源
├── package.json           # 依赖配置
├── vite.config.ts         # Vite配置
├── tsconfig.json          # TypeScript配置
└── build.py               # 构建脚本
```

## 🛠️ 技术栈

- **React 18**: 用户界面库
- **TypeScript**: 类型安全
- **Vite**: 构建工具
- **Axios**: HTTP客户端
- **Lucide React**: 图标库
- **Tailwind CSS**: 样式框架

## 🎨 功能特性

- 📊 **统计面板**: 显示知识库统计信息
- 🔍 **智能搜索**: 基于语义相似度的文档搜索
- ❓ **智能问答**: 基于知识库内容的AI问答
- 📄 **文档管理**: 上传、查看、管理文档
- 📱 **响应式设计**: 支持各种屏幕尺寸
- ⚡ **快速加载**: 基于Vite的快速开发体验

## 🔧 开发指南

### 添加新组件

1. 在 `src/components/` 目录下创建新组件
2. 使用TypeScript定义Props接口
3. 导出组件并在App.tsx中使用

### 添加新API

1. 在 `src/services/api.ts` 中添加新的API函数
2. 使用TypeScript定义请求和响应类型
3. 在组件中调用API函数

### 样式指南

- 使用Tailwind CSS类名
- 保持组件样式的一致性
- 使用响应式设计原则

## 🚀 部署

### 开发环境

```bash
# 启动全栈应用
python start_fullstack.py
```

### 生产环境

```bash
# 构建前端
cd frontend
npm run build

# 启动后端
python web_interface.py
```

## 📝 注意事项

- 确保后端API服务运行在端口5000
- 前端开发服务器运行在端口3000
- 使用代理配置连接前后端
- 支持热重载开发体验
