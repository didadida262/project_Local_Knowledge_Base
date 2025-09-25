# 🧠 本地向量知识库

一个完整的本地向量知识库系统，支持文档向量化、智能检索和基于Ollama的问答功能。

## ✨ 功能特性

- 📄 **多格式文档支持**: PDF, Word, Markdown, HTML, TXT
- 🔍 **智能向量检索**: 基于语义相似度的文档搜索
- 🤖 **AI问答**: 集成Ollama大模型进行智能问答
- 🌐 **现代化界面**: 炫酷React暗黑系界面
- 🚀 **一键启动**: 多种启动方式，自动处理依赖
- 🔒 **完全本地**: 所有数据和处理都在本地进行

## 🛠️ 技术栈

### 后端
- **Python 3.8+** + **Flask** + **Sentence Transformers** + **FAISS** + **Ollama**

### 前端
- **React 18** + **TypeScript** + **Vite** + **Tailwind CSS** + **Framer Motion**
- **Aceternity UI** 暗黑系设计

## 🚀 快速开始

### 一键启动

**Windows用户:**
```bash
# 双击运行（推荐）
start.bat
```

**Linux/Mac用户:**
```bash
# 直接启动API服务器
python backend/api_server.py

# 启动前端（需要Node.js）
cd frontend && npm install && npm run dev
```

### 启动模式

- **模式1**: 全栈启动 (React前端 - 推荐)
- **模式2**: 仅构建知识库
- **模式3**: 仅启动API服务器

## 📁 项目结构

```
project_Local_Knowledge_Base/
├── start.bat                 # 一键启动脚本
├── backend/                  # 后端代码
│   ├── api_server.py         # API服务器
│   ├── vector_knowledge_base.py
│   ├── knowledge_retriever.py
│   └── knowledge_base_main.py
├── frontend/                 # React前端
│   ├── src/components/       # 暗黑系组件
│   ├── package.json
│   └── tailwind.config.js
├── docs/                     # 文档目录
├── knowledge_base/           # 知识库存储
└── requirements.txt
```

## 🎨 界面预览

### React暗黑系界面
- 炫酷的暗黑主题
- 渐变背景 + 玻璃效果
- 流畅的动画过渡
- 现代化的用户体验
- 支持搜索、问答、文档管理

## 📖 使用方法

### 1. 准备文档
将文档放入 `docs/` 目录

### 2. 启动系统
```bash
# Windows用户
start.bat

# Linux/Mac用户
python backend/api_server.py
```

### 3. 开始使用
- 访问React界面进行搜索和问答
- 支持文档上传和管理
- 基于语义相似度的智能检索

## 🔧 配置选项

### 向量化模型
```python
# 在 backend/vector_knowledge_base.py 中修改
kb = VectorKnowledgeBase(
    model_name="all-MiniLM-L6-v2",  # 可选其他模型
    dimension=384
)
```

### Ollama模型
```python
# 在 backend/knowledge_retriever.py 中修改
retriever = KnowledgeRetriever(
    ollama_model="gemma3:4b"  # 或其他模型
)
```

## 📊 支持的文档格式

| 格式 | 扩展名 | 支持状态 |
|------|--------|----------|
| 纯文本 | .txt | ✅ |
| Markdown | .md | ✅ |
| PDF | .pdf | ✅ |
| Word | .docx | ✅ |
| HTML | .html, .htm | ✅ |

## 🚨 故障排除

### 常见问题
1. **启动卡住**: 使用 `python quick_start.py`
2. **内存不足**: 关闭其他程序或使用内存优化版本
3. **模型下载失败**: 检查网络连接
4. **前端依赖问题**: 使用 `python start_simple.py`

### 环境要求
- Python 3.8+
- Ollama已安装并运行
- 至少4GB可用内存
- 网络连接（用于下载模型）

## 🎯 使用场景

- **个人知识管理**: 整理和检索个人文档
- **企业文档系统**: 构建内部知识库
- **学术研究**: 文献检索和分析
- **技术支持**: 基于文档的智能客服

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [Sentence Transformers](https://www.sbert.net/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Ollama](https://ollama.ai/)
- [React](https://react.dev/)
- [Aceternity UI](https://ui.aceternity.com/)