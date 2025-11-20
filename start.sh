#!/bin/bash

# 设置错误时退出
set -e

# 设置Python路径（macOS通常使用python3）
PYTHON_EXE="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_EXE="python"
fi

# 检查Python是否安装
if ! command -v $PYTHON_EXE &> /dev/null; then
    echo "错误: Python未安装或不在PATH中。请安装Python 3.8+。"
    exit 1
fi

echo "============================================================"
echo "🚀 启动本地向量知识库"
echo "============================================================"

# 检查是否存在docs目录
if [ ! -d "docs" ]; then
    echo "📁 创建docs目录..."
    mkdir -p docs
    echo "请将文档放入docs目录后重新运行此脚本。"
    exit 1
fi

# 检查docs目录是否为空
if [ -z "$(ls -A docs)" ]; then
    echo "📁 docs目录为空，请添加文档后重新运行。"
    exit 1
fi

# 检查是否安装了依赖
echo "🔍 检查Python依赖..."
if ! $PYTHON_EXE -c "import sentence_transformers, faiss, numpy" &> /dev/null; then
    echo "❌ 缺少必要的Python依赖，正在安装..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败，请手动运行: pip3 install -r requirements.txt"
        exit 1
    fi
fi

# 检查是否安装了前端依赖
if [ ! -d "frontend/node_modules" ]; then
    echo "🔍 检查前端依赖..."
    cd frontend
    echo "正在安装前端依赖..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ 前端依赖安装失败，请手动运行: cd frontend && npm install"
        exit 1
    fi
    cd ..
fi

# 检查AI模型
echo "🔍 检查AI模型..."
echo ""

# 检查 SentenceTransformer 模型
echo "📦 检查 SentenceTransformer 模型 (all-MiniLM-L6-v2)..."
MODEL_CHECK=$($PYTHON_EXE -c "
import sys
import os
try:
    from sentence_transformers import SentenceTransformer
    model_name = 'all-MiniLM-L6-v2'
    cache_dir = os.path.expanduser('~/.cache/huggingface/hub')
    
    # 检查模型缓存目录
    model_path = os.path.join(cache_dir, 'models--sentence-transformers--all-MiniLM-L6-v2')
    if os.path.exists(model_path):
        print('✅ SentenceTransformer 模型已下载')
        sys.exit(0)
    else:
        print('⚠️  SentenceTransformer 模型未找到')
        print('📝 首次运行时会自动下载模型，这可能需要几分钟时间')
        print(f'📝 模型将下载到: {cache_dir}')
        sys.exit(2)
except ImportError:
    print('❌ sentence_transformers 未安装')
    sys.exit(1)
except Exception as e:
    print(f'❌ 模型检查失败: {e}')
    sys.exit(1)
" 2>&1)

MODEL_STATUS=$?
echo "$MODEL_CHECK"

if [ $MODEL_STATUS -eq 1 ]; then
    echo ""
    echo "❌ SentenceTransformer 模型检查失败，请确保已安装依赖"
    exit 1
elif [ $MODEL_STATUS -eq 2 ]; then
    echo ""
    echo "⚠️  提示: 首次运行时会自动下载模型，请耐心等待"
fi

echo ""

# 检查 Ollama 服务
echo "🤖 检查 Ollama 服务..."
OLLAMA_CHECK=$($PYTHON_EXE -c "
import sys
import requests
try:
    response = requests.get('http://localhost:11434/api/tags', timeout=3)
    if response.status_code == 200:
        models = response.json().get('models', [])
        model_names = [m['name'] for m in models]
        if model_names:
            print('✅ Ollama 服务运行正常')
            models_str = ', '.join(model_names)
            print(f'📦 已安装的模型: {models_str}')
            # 检查是否有 gemma3:4b 模型
            if any('gemma' in name.lower() or '4b' in name.lower() for name in model_names):
                print('✅ 检测到可用的语言模型')
            else:
                print('⚠️  未检测到 gemma3:4b 模型，但可以使用其他已安装的模型')
        else:
            print('⚠️  Ollama 服务运行正常，但未安装任何模型')
        sys.exit(0)
    else:
        print('⚠️  Ollama 服务响应异常')
        sys.exit(1)
except requests.exceptions.ConnectionError:
    print('❌ 无法连接到 Ollama 服务')
    sys.exit(1)
except Exception as e:
    print(f'❌ Ollama 检查失败: {e}')
    sys.exit(1)
" 2>&1)

OLLAMA_STATUS=$?
echo "$OLLAMA_CHECK"

if [ $OLLAMA_STATUS -ne 0 ]; then
    echo ""
    echo "⚠️  ⚠️  ⚠️  重要提示 ⚠️  ⚠️  ⚠️"
    echo "============================================================"
    echo "Ollama 服务未运行或未安装！"
    echo ""
    echo "Ollama 是用于AI问答功能的大语言模型服务。"
    echo "如果没有安装 Ollama，问答功能将无法使用。"
    echo ""
    echo "📥 安装步骤："
    echo "   1. 访问 https://ollama.ai 下载并安装 Ollama"
    echo "   2. 安装后运行以下命令下载模型："
    echo "      ollama pull gemma2:2b"
    echo "      或"
    echo "      ollama pull gemma3:4b"
    echo "   3. 确保 Ollama 服务正在运行（安装后通常会自动启动）"
    echo ""
    echo "💡 注意: 即使没有 Ollama，搜索功能仍然可以正常使用。"
    echo "============================================================"
    echo ""
    # 检查是否在交互式终端中运行
    if [ -t 0 ]; then
        read -p "是否继续启动? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "已取消启动"
            exit 1
        fi
    else
        echo "⚠️  非交互模式: 自动继续启动（问答功能可能不可用）"
    fi
    echo ""
fi

echo "============================================================"
echo "✅ 模型检查完成，准备启动服务..."
echo "============================================================"
echo ""

# 清理可能存在的旧进程
echo "🧹 清理旧进程..."
pkill -f "python.*api_server.py" 2>/dev/null || true
pkill -f "node.*vite" 2>/dev/null || true
pkill -f "npm.*dev" 2>/dev/null || true

# 等待端口释放
echo "⏳ 等待端口释放..."
sleep 2

# 启动后端API服务器
echo "🚀 启动后端API服务器..."
echo "⏳ 正在初始化AI模型，这可能需要几分钟..."
echo "📝 请持续关注后端窗口中的加载进度"
echo ""

# 在后台启动后端服务器
cd backend
$PYTHON_EXE api_server.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# 等待后端启动完成
echo ""
echo "📝 等待AI模型完全初始化..."
echo "📝 自动检测后端状态中..."
while true; do
    sleep 3
    if $PYTHON_EXE -c "import requests; response = requests.get('http://127.0.0.1:5000/api/health'); print('健康检查:', response.json())" &> /dev/null; then
        break
    fi
    echo "📝 等待后端启动中，请稍候..."
done
echo "✅ 后端连接正常"

# 启动前端开发服务器
echo "🌐 启动前端开发服务器..."
echo "⏳ 正在启动React前端应用..."

# 在后台启动前端服务器
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# 等待前端启动
echo "⏳ 等待前端服务器启动..."
sleep 5

echo "============================================================"
echo "✅ 本地向量知识库已启动 (完整版)"
echo "============================================================"
echo "🌐 前端地址: http://localhost:3000"
echo "🔧 后端API:  http://127.0.0.1:5000"
echo ""
echo "📝 前端和后端都已启动，请在浏览器中打开前端地址"
echo "📝 按 Ctrl+C 停止所有服务"
echo ""

# 打开浏览器
echo "正在打开浏览器..."
sleep 2
open http://localhost:3000 2>/dev/null || xdg-open http://localhost:3000 2>/dev/null || echo "请手动在浏览器中打开: http://localhost:3000"

# 创建清理函数
cleanup() {
    echo ""
    echo "🛑 正在停止所有服务..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    pkill -f "python.*api_server.py" 2>/dev/null || true
    pkill -f "node.*vite" 2>/dev/null || true
    echo "所有服务已停止。"
    exit 0
}

# 捕获中断信号
trap cleanup SIGINT SIGTERM

# 等待用户中断
echo "按 Ctrl+C 停止所有服务..."
wait

