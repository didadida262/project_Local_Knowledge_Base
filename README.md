# 本地向量知识库系统

基于Ollama大语言模型的智能文档检索与问答系统，支持多格式文档的向量化存储和语义搜索。

## ✨ 核心特性

- **🤖 AI驱动**: 基于本地Ollama大语言模型
- **📚 多格式支持**: PDF、Word、Markdown、HTML、TXT等
- **🔍 智能搜索**: 语义搜索和关键词搜索
- **💬 AI问答**: 基于文档内容的智能问答
- **🎨 现代界面**: React + TypeScript + Aceternity UI
- **🔒 完全本地**: 数据不上传云端，保护隐私

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- Node.js 16+
- Ollama (本地部署)

### 2. 安装Ollama

```bash
# 下载并安装Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 拉取模型
ollama pull qwen2.5:7b
```

### 3. 一键启动

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
./start.sh
```

### 4. 访问应用

- 前端界面: http://localhost:3000
- 后端API: http://127.0.0.1:5000

## 📁 项目结构

```
project_Local_Knowledge_Base/
├── backend/                 # 后端代码
│   ├── document_processor.py    # 文档处理器
│   ├── vector_knowledge_base.py # 向量知识库
│   ├── knowledge_retriever.py  # 知识检索器
│   ├── reranker.py             # 重排模型
│   └── api_server.py           # API服务器
├── frontend/                # 前端代码
│   ├── src/
│   │   ├── components/         # React组件
│   │   ├── services/           # API服务
│   │   └── App.tsx             # 主应用
│   └── package.json
├── docs/                    # 默认文档目录
├── start.bat               # Windows启动脚本
├── start.sh                # Linux/Mac启动脚本
└── requirements.txt        # Python依赖
```

## 🛠️ 技术栈

### 后端
- **Python 3.8+**: 核心语言
- **Sentence Transformers**: 文本向量化
- **FAISS**: 向量索引存储
- **Transformers**: 重排模型支持
- **PyTorch**: 深度学习框架
- **PyPDF2**: PDF文档处理
- **python-docx**: Word文档处理
- **BeautifulSoup4**: HTML解析
- **jieba**: 中文分词

### 前端
- **React 18**: UI框架
- **TypeScript**: 类型安全
- **Vite**: 构建工具
- **Aceternity UI**: 暗黑主题UI库
- **Tailwind CSS**: 样式框架
- **Framer Motion**: 动画库
- **Axios**: HTTP客户端

### AI模型
- **嵌入模型**: all-MiniLM-L6-v2 (384维向量)
- **推理模型**: gemma3:4b (Ollama本地部署)
- **重排模型**: BAAI/bge-reranker-large (搜索结果优化)
- **Ollama**: 本地大语言模型服务

## 🤖 模型配置

### 嵌入模型 (Embedding Model)
- **模型名称**: `all-MiniLM-L6-v2`
- **类型**: Sentence Transformers
- **向量维度**: 384维
- **用途**: 将文档文本转换为向量表示，用于语义搜索
- **特点**: 轻量级、高效、支持多语言

### 推理模型 (Inference Model)
- **模型名称**: `gemma3:4b`
- **类型**: Ollama本地大语言模型
- **用途**: 基于检索到的文档内容生成AI回答
- **服务地址**: http://localhost:11434
- **特点**: 本地部署、隐私安全、支持中文

### 重排模型 (Rerank Model)
- **模型名称**: `BAAI/bge-reranker-large`
- **类型**: Transformers重排模型
- **用途**: 对FAISS初步检索结果进行重新排序，提升相关性
- **特点**: 高精度、支持长文本、免费开源

### 模型工作流程
```
文档输入 → 嵌入模型 → FAISS向量索引 → 语义搜索 → 重排模型 → 优化排序 → 推理模型 → AI回答
```

## 📖 使用指南

### 1. 添加文档

将文档放入 `docs/` 目录，支持格式：
- TXT文本文件
- Markdown文档
- PDF文档
- Word文档
- HTML网页

### 2. 智能搜索

在搜索页面输入关键词，系统会基于语义相似度返回相关文档片段。

### 3. AI问答

在问答页面提问，AI会基于知识库内容生成答案，并提供参考文档。

### 4. 文档管理

查看已添加的文档列表，支持重新构建知识库。

## 🔧 开发模式

### 后端开发
```bash
cd backend
python api_server.py
```

### 前端开发
```bash
cd frontend
npm install
npm run dev
```

## 📊 API接口

### 获取统计信息
```http
GET /api/stats
```

### 搜索文档
```http
POST /api/search
Content-Type: application/json

{
  "query": "搜索关键词",
  "top_k": 10
}
```

### AI问答
```http
POST /api/ask
Content-Type: application/json

{
  "question": "用户问题",
  "top_k": 5
}
```

### 获取文档列表
```http
GET /api/documents
```

## 🎨 界面预览

- **暗黑主题**: Aceternity UI风格
- **动态背景**: 渐变光效和网格背景
- **流畅动画**: Framer Motion动画效果
- **响应式设计**: 适配各种屏幕尺寸

## 🔒 隐私安全

- **完全本地**: 所有数据存储在本地
- **无网络传输**: 除模型下载外无网络传输
- **数据加密**: 敏感数据本地加密存储
- **访问控制**: 仅本地网络访问

## 🚀 性能优化

- **向量索引**: FAISS高效向量搜索
- **文档分块**: 智能文本分块处理
- **缓存机制**: 向量和索引缓存
- **并发支持**: 支持多用户同时使用

## 🚀 启动模式

### 推荐启动方式

| 启动脚本 | 特点 | 适用场景 |
|---------|------|----------|
| `start_final.bat` | 🎯 渐进式启动 + 最佳体验 | **推荐使用**，解决所有启动问题 |
| `start_ultimate.bat` | 🛡️ 守护进程 + 自动重启 | 生产环境，要求高稳定性 |
| `start_stable.bat` | 🚀 简化模式 + 健康检查 | 开发环境，避免重排模型问题 |
| `start.bat` | 🎯 完整功能 + 重排模型 | 需要最佳搜索效果 |
| `start_simple.bat` | ⚡ 快速启动 + 基础功能 | 快速测试和演示 |

### 问题解决

**如果遇到 `ECONNREFUSED` 错误：**
1. **推荐使用 `start_final.bat`** - 渐进式启动，彻底解决启动问题
2. 使用 `start_ultimate.bat` - 自动重启机制
3. 使用 `start_stable.bat` - 避免重排模型问题
4. 检查端口5000是否被占用：`netstat -ano | findstr :5000`
5. 重启所有服务：`taskkill /f /im python.exe`

**渐进式启动的优势：**
- ✅ HTTP服务立即可用，不等待AI组件初始化
- ✅ 前端显示初始化状态，用户体验更好
- ✅ 避免启动过程中的卡死问题
- ✅ 支持所有功能，包括重排模型

## 📝 更新日志

### v1.1.0 (2024-09)
- 🛡️ 添加守护进程和自动重启机制
- 🔧 修复ECONNREFUSED连接问题
- ⚡ 优化启动流程和错误处理
- 🎯 提供多种启动模式选择

### v1.0.0 (2024-09)
- ✨ 初始版本发布
- 🎨 Aceternity UI暗黑主题
- 🤖 Ollama集成
- 📚 多格式文档支持
- 🔍 智能搜索功能
- 💬 AI问答功能

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License

---

**本地向量知识库系统** - 让AI更智能，让知识更易获取 🚀
