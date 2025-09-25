# 使用说明

## 📁 默认语料库

系统默认使用 `docs/` 目录作为基础语料库，该目录下的所有支持格式文档会自动被处理。

### 支持的文档格式
- 纯文本文件 (.txt)
- Markdown文件 (.md)
- PDF文件 (.pdf)
- Word文档 (.docx)
- HTML文件 (.html, .htm)

## 🚀 快速开始

### 1. 准备文档
将您的文档放入 `docs/` 目录：
```bash
# 示例：将文档复制到docs目录
cp your_document.pdf docs/
cp your_notes.md docs/
```

### 2. 构建知识库
```bash
# 构建知识库（处理docs目录下的所有文档）
python knowledge_base_main.py --mode build
```

### 3. 开始使用
```bash
# 交互式问答
python knowledge_base_main.py --mode interactive

# 或启动Web界面
python web_interface.py
# 访问 http://localhost:5000
```

## 💻 命令行使用

### 交互式模式
```bash
python knowledge_base_main.py --mode interactive
```

可用命令：
- 直接输入问题进行问答
- `search:关键词` - 搜索相关文档
- `summary:文件路径` - 获取文档摘要
- `stats` - 查看知识库统计
- `add:路径` - 添加新文档到知识库
- `upload:路径` - 上传本地文档
- `quit` - 退出

### 单次查询
```bash
python knowledge_base_main.py --mode query --question "你的问题"
```

### 构建知识库
```bash
# 使用默认docs目录
python knowledge_base_main.py --mode build

# 指定其他目录
python knowledge_base_main.py --mode build --documents /path/to/documents
```

## 🌐 Web界面使用

### 启动Web界面
```bash
python web_interface.py
```

### 功能说明
1. **搜索标签页**: 搜索相关文档
2. **问答标签页**: 基于知识库内容进行问答
3. **文档标签页**: 
   - 添加本地文档（输入文件路径）
   - 上传文档（选择文件上传）

### 上传文档
1. 进入"文档"标签页
2. 选择要上传的文件（支持多选）
3. 点击"上传到知识库"
4. 系统会自动处理并添加到知识库

## 📊 知识库管理

### 查看统计信息
```bash
# 命令行查看
python knowledge_base_main.py --mode interactive
# 然后输入: stats

# 或通过Web界面查看
```

### 添加新文档
1. **方法1**: 将文档放入 `docs/` 目录，然后重新构建知识库
2. **方法2**: 使用交互式模式添加
3. **方法3**: 通过Web界面上传

### 重新构建知识库
```bash
# 删除旧的知识库数据
rm -rf knowledge_base/

# 重新构建
python knowledge_base_main.py --mode build
```

## 🔧 高级功能

### 自定义配置
```python
# 修改向量化模型
kb = VectorKnowledgeBase(
    model_name="all-mpnet-base-v2",  # 更强大的模型
    dimension=768,
    storage_dir="./knowledge_base"
)

# 修改推理模型
retriever = KnowledgeRetriever(
    knowledge_base=kb,
    ollama_model="llama3:8b"  # 或其他模型
)
```

### 程序化使用
```python
from vector_knowledge_base import VectorKnowledgeBase
from knowledge_retriever import KnowledgeRetriever

# 初始化知识库
kb = VectorKnowledgeBase()

# 添加文档
kb.add_document("document.pdf")
kb.add_directory("./docs", recursive=True)

# 保存知识库
kb.save_knowledge_base()

# 初始化检索器
retriever = KnowledgeRetriever(kb)

# 问答
result = retriever.ask_question("你的问题")
print(result['answer'])
```

## 🚨 常见问题

### 1. 文档处理失败
- 检查文档格式是否支持
- 确认文档没有损坏
- 查看错误日志

### 2. 内存不足
```bash
# 使用内存优化版本
python memory_optimized_chat.py
```

### 3. 模型下载失败
```bash
# 手动拉取模型
ollama pull gemma3:4b
```

### 4. 知识库为空
- 确保 `docs/` 目录中有文档
- 运行构建命令：`python knowledge_base_main.py --mode build`
- 检查文档格式是否支持

## 📝 最佳实践

1. **文档组织**: 将相关文档放在 `docs/` 目录的子目录中
2. **文档质量**: 确保文档内容清晰，避免扫描质量差的PDF
3. **定期更新**: 添加新文档后重新构建知识库
4. **备份数据**: 定期备份 `knowledge_base/` 目录
5. **性能优化**: 对于大量文档，考虑分批处理
