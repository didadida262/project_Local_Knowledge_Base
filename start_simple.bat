@echo off
chcp 65001 >nul
title 本地向量知识库启动器 (简化版)

echo.
echo ========================================
echo 🚀 本地向量知识库启动器 (简化版)
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查Node.js是否安装
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js未安装或未添加到PATH
    echo 请先安装Node.js 16+
    pause
    exit /b 1
)

echo 🔍 检查Python依赖...
python -c "import sentence_transformers, faiss, PyPDF2, docx, bs4, jieba" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Python依赖未安装，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Python依赖安装失败
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo 选择启动模式:
echo 1. 全栈启动 (后端API + React前端 - 推荐)
echo 2. 仅构建知识库
echo 3. 仅启动API服务器
echo ========================================
echo.

set /p choice=请选择 (1-3): 

if "%choice%"=="1" (
    echo.
    echo 🎨 启动全栈应用...
    
    REM 检查前端依赖
    if not exist "frontend\node_modules" (
        echo 📦 安装前端依赖...
        cd frontend
        npm install
        if errorlevel 1 (
            echo ❌ 前端依赖安装失败，使用简化模式
            cd ..
            goto :api_only
        )
        cd ..
    )
    
    echo 🚀 启动后端API服务器 (简化模式，无重排模型)...
    start "后端API" cmd /k "python -c \"import sys; sys.path.append('.'); from backend.vector_knowledge_base import VectorKnowledgeBase; from backend.api_server import run_server; kb = VectorKnowledgeBase(use_reranker=False); run_server()\""
    timeout /t 5 /nobreak >nul
    
    echo 🌐 启动前端开发服务器...
    start "前端界面" cmd /k "cd frontend && npm run dev"
    
    echo ✅ 全栈应用已启动
    echo 📱 前端地址: http://localhost:3000
    echo 🔧 后端API: http://127.0.0.1:5000
    echo.
    echo 按任意键退出...
    pause >nul
    
) else if "%choice%"=="2" (
    echo.
    echo 🔨 构建知识库...
    python -c "import sys; sys.path.append('.'); from backend.vector_knowledge_base import VectorKnowledgeBase; kb = VectorKnowledgeBase(use_reranker=False); kb.clear_knowledge_base(); kb.add_directory('docs'); kb.save_knowledge_base(); print('✅ 知识库构建完成')"
    echo.
    echo 按任意键退出...
    pause >nul
    
) else if "%choice%"=="3" (
    :api_only
    echo.
    echo 🚀 启动API服务器 (简化模式)...
    python -c "import sys; sys.path.append('.'); from backend.vector_knowledge_base import VectorKnowledgeBase; from backend.api_server import run_server; kb = VectorKnowledgeBase(use_reranker=False); run_server()"
    
) else (
    echo.
    echo ❌ 无效选择，默认启动全栈应用...
    goto :start_fullstack
)

echo.
echo 🎉 启动完成！
