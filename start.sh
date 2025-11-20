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

