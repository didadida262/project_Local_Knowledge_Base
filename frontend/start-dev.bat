@echo off
echo 🚀 启动前端开发服务器...
echo.

REM 检查Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js未安装
    echo 请安装Node.js: https://nodejs.org/
    pause
    exit /b 1
)

REM 安装依赖
if not exist "node_modules" (
    echo 📦 安装依赖...
    npm install
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

REM 启动开发服务器
echo 🌐 启动开发服务器...
npm run dev
