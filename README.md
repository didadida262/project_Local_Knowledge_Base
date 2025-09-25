# 本地知识库项目 - Ollama对话工具

这是一个用于与本地Ollama大模型对话的Python工具，支持与qwen3:8b等模型进行交互式对话。

## 功能特性

- 🤖 支持与本地Ollama模型对话
- 💬 交互式命令行界面
- 🔄 自动检测和拉取模型
- 📡 流式输出支持
- ⚡ 简单易用的API

## 环境要求

- Python 3.7+
- Ollama已安装并运行
- 网络连接（用于首次下载模型）

## 安装步骤

### 1. 安装Ollama

首先需要安装Ollama：

**Windows:**
```bash
# 下载并安装Ollama
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

### 2. 启动Ollama服务

```bash
ollama serve
```

### 3. 安装Python依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```bash
python ollama_chat.py
```

### 程序化使用

```python
from ollama_chat import OllamaChat

# 创建客户端
chat = OllamaChat(model="qwen3:8b")

# 发送消息
response = chat.chat("你好，请介绍一下自己")
print(response)
```

## 可用命令

在交互式对话中，你可以使用以下命令：

- `quit` 或 `exit` - 退出程序
- `clear` - 清屏
- 直接输入消息与模型对话

## 支持的模型

默认使用 `qwen3:8b` 模型，你也可以修改代码中的模型名称来使用其他模型：

- qwen3:8b
- qwen3:14b
- llama3:8b
- llama3:70b
- 其他Ollama支持的模型

## 配置选项

你可以在 `ollama_chat.py` 中修改以下配置：

```python
# 修改Ollama服务地址
chat = OllamaChat(base_url="http://localhost:11434")

# 修改模型名称
chat = OllamaChat(model="your-model-name")
```

## 故障排除

### 1. 连接错误

如果遇到连接错误，请确保：
- Ollama服务正在运行 (`ollama serve`)
- 端口11434没有被占用
- 防火墙没有阻止连接

### 2. 模型不存在

如果模型不存在，程序会自动尝试拉取模型。如果拉取失败：
- 检查网络连接
- 确认模型名称正确
- 手动拉取模型：`ollama pull qwen3:8b`

### 3. 内存不足

如果遇到内存不足的问题：
- 尝试使用更小的模型
- 关闭其他占用内存的程序
- 增加系统虚拟内存

## 开发说明

### 项目结构

```
project_Local_Knowledge_Base/
├── ollama_chat.py      # 主程序文件
├── requirements.txt    # Python依赖
└── README.md          # 说明文档
```

### 扩展功能

你可以基于现有代码扩展以下功能：
- 多轮对话历史管理
- 自定义系统提示词
- 对话记录保存
- Web界面
- API服务

## 许可证

MIT License