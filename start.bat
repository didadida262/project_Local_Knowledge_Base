@echo off
chcp 65001 >nul
title 本地向量知识库启动器

echo.
echo ========================================
echo 🧠 本地向量知识库启动器
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

REM 检查依赖是否安装
echo 🔍 检查依赖...
python -c "import flask, sentence_transformers, faiss" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  依赖未安装，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

REM 检查Node.js（用于React前端）
echo 🔍 检查Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Node.js未安装，将使用简化模式
    set NODE_AVAILABLE=0
) else (
    echo ✅ Node.js已安装
    set NODE_AVAILABLE=1
)

REM 检查Ollama服务
echo 🔍 检查Ollama服务...
ollama list >nul 2>&1
if errorlevel 1 (
    echo ❌ Ollama服务未启动
    echo 请先启动Ollama: ollama serve
    pause
    exit /b 1
) else (
    echo ✅ Ollama服务正常
)

REM 检查docs目录
echo 🔍 检查文档目录...
if not exist "docs" (
    echo 📁 创建docs目录...
    mkdir docs
    echo 📝 创建说明文件...
    echo # 文档目录 > docs\README.md
    echo. >> docs\README.md
    echo 请将您的文档放入此目录，支持以下格式： >> docs\README.md
    echo - .txt (纯文本) >> docs\README.md
    echo - .md (Markdown) >> docs\README.md
    echo - .pdf (PDF文档) >> docs\README.md
    echo - .docx (Word文档) >> docs\README.md
    echo - .html/.htm (网页) >> docs\README.md
    echo. >> docs\README.md
    echo 然后重新运行此脚本。 >> docs\README.md
    echo ✅ docs目录已创建
)

REM 检查是否有文档
set DOC_COUNT=0
for %%f in (docs\*.txt docs\*.md docs\*.pdf docs\*.docx docs\*.html docs\*.htm) do (
    set /a DOC_COUNT+=1
)

if %DOC_COUNT%==0 (
    echo ⚠️  docs目录为空
    echo 请将文档放入docs目录后重新运行
    pause
    exit /b 1
) else (
    echo ✅ 找到 %DOC_COUNT% 个文档
)

REM 启动应用
echo.
echo 🚀 启动知识库系统...
echo 选择启动方式:
echo 1. 全栈启动 (React前端 - 推荐)
echo 2. 仅构建知识库
echo 3. 仅启动API服务器
echo.

set /p choice=请选择 (1-3): 

if "%choice%"=="1" (
    echo.
    echo 🎨 全栈启动...
    if %NODE_AVAILABLE%==1 (
        echo 📦 安装前端依赖...
        cd frontend
        if not exist "node_modules" (
            npm install
            if errorlevel 1 (
                echo ❌ 前端依赖安装失败，使用简化模式
                cd ..
                goto :api_only
            )
        )
        cd ..
        echo 🚀 启动全栈应用...
        start "后端API" cmd /k "python backend/api_server.py"
        timeout /t 3 /nobreak >nul
        echo 🌐 启动前端开发服务器...
        start "前端界面" cmd /k "cd frontend && npm run dev"
        echo ✅ 全栈应用已启动
        echo 📱 前端地址: http://localhost:3000
        echo 🔧 后端API: http://127.0.0.1:5000
    ) else (
        echo ❌ Node.js未安装，无法启动前端
        goto :api_only
    )
) else if "%choice%"=="2" (
    echo.
    echo 🔨 仅构建知识库...
    python -c "from backend.vector_knowledge_base import VectorKnowledgeBase; kb = VectorKnowledgeBase(); kb.add_directory('docs'); kb.save_knowledge_base(); print('✅ 知识库构建完成')"
) else if "%choice%"=="3" (
    :api_only
    echo.
    echo 🔧 仅启动API服务器...
    echo 🚀 启动后端API...
    python backend/api_server.py
) else (
    echo.
    echo ❌ 无效选择，使用默认启动
    goto :api_only
)

echo.
echo 💡 提示: 按任意键退出
pause >nul