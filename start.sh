#!/bin/bash

echo "========================================"
echo "🚀 本地向量知识库启动器"
echo "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装"
    echo "请先安装Python 3.8+"
    exit 1
fi

# 检查依赖是否安装
echo "🔍 检查依赖..."
python3 -c "import flask, sentence_transformers, faiss" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  依赖未安装，正在安装..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
fi

# 启动应用
echo "🚀 启动知识库系统..."
python3 start.py
