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

# 检查 SentenceTransformer 模型（快速检查，不实际加载模型）
echo "📦 检查 SentenceTransformer 模型 (all-MiniLM-L6-v2)..."
MODEL_CHECK=$($PYTHON_EXE -c "
import sys
import os
# 只检查模块是否可导入，不实际加载模型（避免卡住）
try:
    import sentence_transformers
    print('✅ sentence_transformers 已安装')
    # 检查缓存目录是否存在模型文件
    cache_dir = os.path.expanduser('~/.cache/huggingface/hub')
    if os.path.exists(cache_dir):
        try:
            items = os.listdir(cache_dir)
            if any('MiniLM' in item for item in items):
                print('✅ 模型文件已存在')
            else:
                print('⚠️  模型文件未找到，首次运行时会自动下载')
        except:
            print('⚠️  无法检查模型文件，启动时会自动处理')
    else:
        print('⚠️  模型缓存目录不存在，首次运行时会自动创建并下载模型')
    sys.exit(0)
except ImportError:
    print('❌ sentence_transformers 未安装')
    sys.exit(1)
except Exception as e:
    error_msg = str(e)
    if 'cached_download' in error_msg or 'huggingface_hub' in error_msg:
        print('⚠️  版本可能不兼容，建议运行: pip install --upgrade sentence-transformers')
        print('   但将继续启动，系统会尝试自动处理')
    else:
        print(f'⚠️  检查时出现警告: {error_msg[:80]}')
    sys.exit(0)
" 2>&1)

MODEL_STATUS=$?
echo "$MODEL_CHECK"

if [ $MODEL_STATUS -eq 1 ]; then
    echo ""
    echo "❌ sentence_transformers 未安装"
    echo "📝 请运行: pip3 install -r requirements.txt"
    exit 1
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
MAX_WAIT_TIME=300  # 最大等待5分钟
WAIT_COUNT=0
while [ $WAIT_COUNT -lt $MAX_WAIT_TIME ]; do
    sleep 3
    WAIT_COUNT=$((WAIT_COUNT + 3))
    # 检查后端健康状态，忽略警告信息
    if $PYTHON_EXE -c "
import sys
import warnings
warnings.filterwarnings('ignore')
try:
    import requests
    response = requests.get('http://127.0.0.1:5000/api/health', timeout=2)
    if response.status_code == 200:
        sys.exit(0)
    else:
        sys.exit(1)
except:
    sys.exit(1)
" 2>/dev/null; then
        echo "✅ 后端连接正常"
        break
    fi
    if [ $((WAIT_COUNT % 30)) -eq 0 ]; then
        echo "📝 已等待 ${WAIT_COUNT} 秒，继续等待后端启动中..."
    fi
    # 检查后端进程是否还在运行
    if ! ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo ""
        echo "❌ 后端进程已停止"
        echo "📝 查看错误日志:"
        tail -20 backend.log 2>/dev/null || echo "   无法读取日志文件"
        exit 1
    fi
done

if [ $WAIT_COUNT -ge $MAX_WAIT_TIME ]; then
    echo ""
    echo "⚠️  后端启动超时（已等待 ${MAX_WAIT_TIME} 秒）"
    echo "📝 查看后端日志: tail -f backend.log"
    echo "📝 但将继续启动前端，你可以稍后检查后端状态"
fi

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

