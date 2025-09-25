@echo off
chcp 65001 >nul
title 本地向量知识库启动器

echo.
echo ========================================
echo 🚀 本地向量知识库启动器
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

REM 启动应用
echo 🚀 启动知识库系统...
echo 💡 如果启动卡住，请使用: python quick_start.py
python quick_start.py

pause
