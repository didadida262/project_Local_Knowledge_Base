# 本地向量知识库系统

基于Ollama大语言模型的智能文档检索与问答系统，支持多格式文档的向量化存储和语义搜索。

## ✨ 核心特性

- **🤖 AI驱动**: 基于本地Ollama大语言模型
- **📚 多格式支持**: PDF、Word、Markdown、HTML、TXT等
- **🔍 智能搜索**: 语义搜索和关键词搜索
- **💬 AI问答**: 基于文档内容的智能问答
- **🎨 现代界面**: React + TypeScript + Aceternity UI
- **🔒 完全本地**: 数据不上传云端，保护隐私
- **🚀 自动启动**: 一键启动脚本，自动初始化知识库
- **📖 默认语料**: 自动加载docs目录作为默认语料库

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- Node.js 16+
- Ollama (本地部署)

### 2. 安装Ollama并拉取模型

```bash
# 下载并安装Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 拉取推理模型
ollama pull gemma3:4b
```

### 3. 一键启动

```bash
# Windows
start.bat
```

脚本将自动完成：
- ✅ 检查Python和Node.js环境
- 📦 安装后端Python依赖
- 🌐 安装前端Node.js依赖
- 🤖 加载AI模型并初始化知识库
- 📂 自动扫描docs目录作为默认语料库
- 🚀 启动后端API服务器
- 💫 启动前端开发服务器
- 🌐 自动打开浏览器

### 4. 访问应用

- **前端界面**: http://localhost:3000
- **后端API**: http://127.0.0.1:5000

## 📁 项目结构

```
project_Local_Knowledge_Base/
├── backend/                 # 后端代码
│   ├── document_processor.py    # 文档处理器
│   ├── vector_knowledge_base.py # 向量知识库
│   ├── knowledge_retriever.py  # 知识检索器
│   ├── api_server.py           # API服务器
│   └── knowledge_base/          # 向量存储目录
│       ├── config.json         # 配置文件
│       ├── documents.json      # 文档索引
│       ├── chunks.json         # 文本块
│       └── faiss_index.bin     # FAISS索引
├── frontend/                # 前端代码
│   ├── src/
│   │   ├── components/         # React组件
│   │   │   ├── StatsCard.tsx   # 统计卡片
│   │   │   ├── SearchTab.tsx    # 搜索界面
│   │   │   ├── QATab.tsx        # 问答界面
│   │   │   ├── DocumentsTab.tsx # 文档管理
│   │   │   └── LoadingScreen.tsx # 加载界面
│   │   ├── services/           # API服务
│   │   └── App.tsx             # 主应用
│   └── package.json
├── docs/                    # 默认文档目录
│   ├── 三国演义.txt
│   ├── 水浒传.txt  
│   ├── 红楼梦.txt
│   └── 西游记.txt
├── start.bat               # 启动脚本
├── requirements.txt        # Python依赖
└── README.md              # 项目说明
```

## 🛠️ 技术栈

### 后端
- **Python 3.8+**: 核心语言
- **Sentence Transformers**: 文本向量化  
- **FAISS**: 向量索引存储
- **HTTP Server**: Python内置HTTP服务器
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

### 模型工作流程
```
文档输入 → 嵌入模型 → FAISS向量索引 → 语义搜索 → 推理模型 → AI回答
```

## 📖 使用指南

### 1. 准备文档

将文档放入 `docs/` 目录，系统启动时会自动扫描并加载这些文档：

支持格式：
- **TXT文本文件**: 纯文本文档
- **Markdown文档**: .md文件
- **PDF文档**: .pdf文件
- **Word文档**: .docx文件
- **HTML网页**: .html文件

### 2. 启动系统

运行启动脚本：
```bash
start.bat
```

系统将自动：
1. 📦 检查和安装依赖
2. 🤖 加载AI模型  
3. 📚 初始化知识库
4. 📂 扫描并加载docs目录作为默认语料库
5. 🚀 启动前后端服务
6. 🌐 打开浏览器访问界面

### 3. 智能搜索

在搜索页面输入关键词，系统会基于语义相似度返回相关文档片段，并显示相似度分数。

### 4. AI问答

在问答页面提问，AI会基于知识库内容生成答案，并提供参考文档来源。

### 5. 文档管理

查看已加载的文档列表，支持重新构建知识库。

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

### 重建知识库
```http
POST /api/rebuild
Content-Type: application/json

{
  "docs_dir": "./docs"
}
```

## 🎨 界面特性

- **暗黑主题**: Aceternity UI酷炫暗黑风格
- **动态背景**: 渐变光效和网格背景  
- **流畅动画**: Framer Motion动画效果
- **响应式设计**: 适配各种屏幕尺寸
- **实时统计**: 知识库数据实时显示
- **加载动画**: 模型初始化进度提示

## 🔒 隐私安全

- **完全本地**: 所有数据存储在本地
- **无网络传输**: 除模型下载外无网络传输
- **数据加密**: 向量数据本地加密存储
- **访问控制**: 仅本地网络访问

## 🚀 性能优化

- **向量索引**: FAISS高效向量搜索
- **文档分块**: 智能文本分块处理  
- **缓存机制**: 向量和索引缓存
- **并发支持**: 支持多用户同时使用
- **启动优化**: 模型预热和并行加载

## 问题解决

**如果遇到 `ECONNREFUSED` 错误：**
1. 检查端口5000是否被占用：`netstat -ano | findstr :5000`
2. 重启所有服务：`taskkill /f /im python.exe`
3. 等待AI模型加载完成（首次启动可能需要几分钟）

**如果知识库统计显示0：**
1. 确保docs目录中有文档文件
2. 重启系统让系统重新扫描docs目录
3. 检查文件格式是否支持

## 📝 更新日志

### v1.0.0 (2025-10)
- 🎯 自动加载默认语料库（docs目录）
- 🔧 完善的后端初始化和错误处理
- 🚀 一键启动脚本优化
- 📊 实时知识库统计显示
- ✨ 改进用户体验




## 📄 许可证

MIT License

---

**本地向量知识库系统** - 让AI更智能，让知识更易获取 🚀