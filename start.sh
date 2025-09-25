#!/bin/bash

# 设置颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================"
echo -e "🚀 本地向量知识库启动器"
echo -e "========================================${NC}"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3未安装或未添加到PATH${NC}"
    echo "请先安装Python 3.8+"
    exit 1
fi

# 检查Node.js是否安装
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js未安装或未添加到PATH${NC}"
    echo "请先安装Node.js 16+"
    exit 1
fi

# 检查依赖是否安装
echo -e "${BLUE}🔍 检查Python依赖...${NC}"
python3 -c "import sentence_transformers, faiss, PyPDF2, docx, bs4, jieba" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Python依赖未安装，正在安装...${NC}"
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Python依赖安装失败${NC}"
        exit 1
    fi
fi

echo
echo -e "${CYAN}========================================"
echo -e "选择启动模式:"
echo -e "1. 全栈启动 (后端API + React前端 - 推荐)"
echo -e "2. 仅构建知识库"
echo -e "3. 仅启动API服务器"
echo -e "========================================${NC}"
echo

read -p "请选择 (1-3): " choice

case $choice in
    1)
        echo
        echo -e "${GREEN}🎨 启动全栈应用...${NC}"
        
        # 检查前端依赖
        if [ ! -d "frontend/node_modules" ]; then
            echo -e "${BLUE}📦 安装前端依赖...${NC}"
            cd frontend
            npm install
            if [ $? -ne 0 ]; then
                echo -e "${RED}❌ 前端依赖安装失败，使用简化模式${NC}"
                cd ..
                choice=3
            else
                cd ..
            fi
        fi
        
        if [ "$choice" = "1" ]; then
            echo -e "${BLUE}🚀 启动后端API服务器...${NC}"
            python3 backend/api_server.py &
            API_PID=$!
            sleep 3
            
            echo -e "${BLUE}🌐 启动前端开发服务器...${NC}"
            cd frontend && npm run dev &
            FRONTEND_PID=$!
            cd ..
            
            echo -e "${GREEN}✅ 全栈应用已启动${NC}"
            echo -e "${CYAN}📱 前端地址: http://localhost:3000${NC}"
            echo -e "${CYAN}🔧 后端API: http://127.0.0.1:5000${NC}"
            echo
            echo "按Ctrl+C停止所有服务..."
            
            # 等待用户中断
            trap "kill $API_PID $FRONTEND_PID 2>/dev/null; exit" INT
            wait
        fi
        ;;
    2)
        echo
        echo -e "${BLUE}🔨 构建知识库...${NC}"
        python3 -c "
from backend.vector_knowledge_base import VectorKnowledgeBase
from pathlib import Path
kb = VectorKnowledgeBase()
kb.clear_knowledge_base()
kb.add_directory('docs')
kb.save_knowledge_base()
print('✅ 知识库构建完成')
"
        echo
        echo "按任意键退出..."
        read -n 1
        ;;
    3)
        echo
        echo -e "${BLUE}🚀 启动API服务器...${NC}"
        python3 backend/api_server.py
        ;;
    *)
        echo
        echo -e "${RED}❌ 无效选择，默认启动全栈应用...${NC}"
        choice=1
        ;;
esac

echo
echo -e "${GREEN}🎉 启动完成！${NC}"
