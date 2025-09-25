# 🧠 本地向量知识库

一个完整的本地向量知识库系统，支持文档向量化、智能检索和基于Ollama的问答功能。

## ✨ 功能特性

- 📄 **多格式文档支持**: PDF, Word, Markdown, HTML, TXT
- 🔍 **智能向量检索**: 基于语义相似度的文档搜索
- 🤖 **AI问答**: 集成Ollama大模型进行智能问答
- 🌐 **Web界面**: 现代化的Web界面，支持搜索和问答
- 💻 **命令行工具**: 灵活的命令行接口
- 🚀 **高性能**: 基于FAISS的快速向量检索
- 🔒 **完全本地**: 所有数据和处理都在本地进行
- 📁 **默认语料库**: 使用docs目录作为基础语料库
- ⬆️ **文档上传**: 支持用户上传本地文档到知识库
- 🔄 **自动同步**: 每次启动自动同步docs目录与知识库
- 🚀 **一键启动**: 统一的启动脚本，自动处理所有依赖

## 🛠️ 技术栈

- **向量化**: Sentence Transformers
- **向量存储**: FAISS
- **文档处理**: PyPDF2, python-docx, BeautifulSoup
- **AI模型**: Ollama (支持多种开源模型)
- **Web框架**: Flask
- **前端**: HTML5 + JavaScript

## 📋 环境要求

- Python 3.8+
- Ollama已安装并运行
- 至少4GB可用内存
- 网络连接（用于下载模型）

## 🚀 快速开始

### 1. 一键启动（推荐）

**Windows用户:**
```bash
# 双击运行（推荐）
start.bat

# 或命令行运行
python start.py
```

**Linux/Mac用户:**
```bash
# 运行启动脚本
./start.sh

# 或直接运行
python3 start.py
```

### 2. 快速启动（避免卡住）

如果启动时模型加载卡住，可以使用快速启动：

```bash
# 快速启动，跳过模型重新加载
python quick_start.py
```

### 3. 手动设置

```bash
# 克隆项目
git clone <repository-url>
cd project_Local_Knowledge_Base

# 运行快速设置脚本
python quick_setup.py
```

### 2. 手动安装

#### 安装Ollama

**Windows:**
```bash
# 访问 https://ollama.ai/download 下载Windows版本
```

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### 启动Ollama服务

```bash
ollama serve
```

#### 安装Python依赖

```bash
pip install -r requirements.txt
```

#### 构建知识库

```bash
# 构建知识库（处理docs目录下的文档）
python knowledge_base_main.py --mode build

# 或者指定文档目录
python knowledge_base_main.py --mode build --documents /path/to/documents
```

## 📖 使用方法

### 1. 统一启动（推荐）

```bash
# 一键启动，自动构建知识库并打开Web界面
python start.py
```

**功能特点:**
- 🔄 每次启动自动同步docs目录与知识库
- 🗑️ 自动清理旧知识库，确保数据一致性
- 🌐 自动打开Web界面
- ⚡ 智能检测，避免重复构建

### 2. 快速启动

```bash
# 快速启动，使用现有知识库
python quick_start.py
```

**适用场景:**
- 知识库已构建完成
- 避免模型加载卡住
- 快速启动Web界面

### 3. 命令行模式

#### 交互式问答
```bash
python knowledge_base_main.py --mode interactive
```

#### 单次查询
```bash
python knowledge_base_main.py --mode query --question "什么是机器学习？"
```

#### 构建知识库
```bash
python knowledge_base_main.py --mode build --documents ./docs
```

### 4. Web界面功能

启动后访问 http://127.0.0.1:5000

**主要功能:**
- 🔍 **搜索**: 基于语义相似度的文档搜索
- ❓ **问答**: 基于知识库内容的智能问答
- 📄 **文档管理**: 上传、查看、管理文档
- 📊 **统计信息**: 查看知识库统计

### 5. 程序化使用

```python
from vector_knowledge_base import VectorKnowledgeBase
from knowledge_retriever import KnowledgeRetriever

# 初始化知识库
kb = VectorKnowledgeBase()

# 添加文档
kb.add_document("document.pdf")
kb.add_directory("./documents", recursive=True)

# 保存知识库
kb.save_knowledge_base()

# 初始化检索器
retriever = KnowledgeRetriever(kb)

# 问答
result = retriever.ask_question("什么是Python？")
print(result['answer'])
```

## 📁 项目结构

```
project_Local_Knowledge_Base/
├── start.py                  # 统一启动脚本（推荐）
├── quick_start.py            # 快速启动脚本
├── start.bat                 # Windows启动脚本
├── start.sh                  # Linux/Mac启动脚本
├── vector_knowledge_base.py  # 向量知识库核心
├── knowledge_retriever.py    # 知识检索器
├── knowledge_base_main.py    # 主程序
├── web_interface.py          # Web界面
├── quick_setup.py            # 快速设置脚本
├── ollama_chat.py            # Ollama对话工具
├── memory_optimized_chat.py  # 内存优化版本
├── requirements.txt          # Python依赖
├── docs/                     # 文档目录（用户放置文档）
│   ├── README.md             # 文档说明
│   ├── 三国演义.txt          # 示例文档
│   ├── 水浒传.txt            # 示例文档
│   ├── 红楼梦.txt            # 示例文档
│   └── 西游记.txt            # 示例文档
├── knowledge_base/           # 知识库存储目录
│   ├── faiss_index.bin       # FAISS索引
│   ├── documents.json        # 文档信息
│   └── metadata.json         # 元数据
└── README.md                 # 说明文档
```

## 🚀 启动脚本说明

### start.py - 统一启动脚本

**功能特点:**
- 🔄 **自动同步**: 每次启动自动同步docs目录与知识库
- 🗑️ **智能清理**: 自动清理旧知识库，确保数据一致性
- 🌐 **自动打开**: 启动后自动打开浏览器
- ⚡ **进度提示**: 显示详细的构建进度
- 🛡️ **错误处理**: 完善的错误处理和用户提示

**适用场景:**
- 首次使用
- 文档有变化
- 需要重新构建知识库

### quick_start.py - 快速启动脚本

**功能特点:**
- ⚡ **快速启动**: 使用现有知识库，避免重新构建
- 🔍 **智能检测**: 自动检测docs目录和Ollama服务
- 🌐 **Web界面**: 直接启动Web界面

**适用场景:**
- 知识库已构建完成
- 避免模型加载卡住
- 快速启动Web界面

## 🔧 配置选项

### 向量化模型

```python
# 在 vector_knowledge_base.py 中修改
kb = VectorKnowledgeBase(
    model_name="all-MiniLM-L6-v2",  # 可选: all-mpnet-base-v2, paraphrase-multilingual-MiniLM-L12-v2
    dimension=384,  # 根据模型调整
    storage_dir="./knowledge_base"
)
```

### Ollama配置

```python
# 在 knowledge_retriever.py 中修改
retriever = KnowledgeRetriever(
    knowledge_base=kb,
    ollama_url="http://localhost:11434",
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

## 🎯 使用场景

- **个人知识管理**: 整理和检索个人文档
- **企业文档系统**: 构建内部知识库
- **学术研究**: 文献检索和分析
- **技术支持**: 基于文档的智能客服
- **教育培训**: 智能学习助手

## 📋 使用流程

### 首次使用

1. **准备环境**
   ```bash
   # 安装Ollama
   ollama serve
   
   # 安装Python依赖
   pip install -r requirements.txt
   ```

2. **准备文档**
   ```bash
   # 将文档放入docs目录
   cp your_documents/* docs/
   ```

3. **启动系统**
   ```bash
   # 一键启动
   python start.py
   ```

4. **开始使用**
   - 访问 http://127.0.0.1:5000
   - 进行搜索和问答

### 日常使用

1. **添加新文档**
   - 方法1: 放入docs目录，重新启动
   - 方法2: 通过Web界面上传

2. **删除文档**
   - 从docs目录删除，重新启动

3. **快速启动**
   ```bash
   # 如果知识库已构建
   python quick_start.py
   ```

### 故障排除

1. **启动卡住**: 使用 `python quick_start.py`
2. **模型下载失败**: 检查网络连接
3. **内存不足**: 关闭其他程序
4. **知识库不同步**: 删除knowledge_base目录，重新启动

## 🔍 高级功能

### 1. 文档摘要

```python
summary = retriever.get_document_summary("document.pdf")
print(summary['summary'])
```

### 2. 相似文档搜索

```python
results = retriever.search_similar_documents("机器学习", top_k=10)
for result in results:
    print(f"{result['file_path']} (相似度: {result['max_similarity']:.3f})")
```

### 3. 知识库统计

```python
stats = kb.get_stats()
print(f"总向量数: {stats['total_vectors']}")
print(f"唯一文件数: {stats['unique_files']}")
```

## 🚨 故障排除

### 1. 内存不足

```bash
# 使用内存优化版本
python memory_optimized_chat.py
```

### 2. 模型下载失败

```bash
# 手动拉取模型
ollama pull gemma3:4b
```

### 3. 依赖安装失败

```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 4. 文档处理失败

- 检查文档格式是否支持
- 确认文档没有损坏
- 查看错误日志

## 🔄 更新和维护

### 添加新文档

**方法1: 直接放入docs目录（推荐）**
```bash
# 将文档放入docs目录
cp your_document.pdf docs/

# 重新启动系统，自动同步
python start.py
```

**方法2: 通过Web界面上传**
1. 启动系统: `python start.py`
2. 访问 http://127.0.0.1:5000
3. 进入"文档"标签页
4. 选择文件上传

**方法3: 命令行添加**
```bash
# 添加单个文档
python knowledge_base_main.py --mode interactive
# 然后输入: add:/path/to/document.pdf
```

### 删除文档

```bash
# 从docs目录删除文档
rm docs/old_document.pdf

# 重新启动系统，自动同步
python start.py
```

### 清空知识库

```python
# 程序化清空
from vector_knowledge_base import VectorKnowledgeBase
kb = VectorKnowledgeBase()
kb.clear_knowledge_base()
```

### 强制重建知识库

```bash
# 删除知识库目录
rm -rf knowledge_base/

# 重新启动
python start.py
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [Sentence Transformers](https://www.sbert.net/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Ollama](https://ollama.ai/)
- [Flask](https://flask.palletsprojects.com/)