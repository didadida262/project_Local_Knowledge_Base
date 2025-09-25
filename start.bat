@echo off
setlocal

:: 设置Python路径
set "PYTHON_EXE=python"

:: 检查Python是否安装
where %PYTHON_EXE% >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: Python未安装或不在PATH中。请安装Python 3.8+。
    pause
    exit /b 1
)

echo ============================================================
echo 🚀 启动本地向量知识库
echo ============================================================

:: 检查是否存在docs目录
if not exist "docs" (
    echo 📁 创建docs目录...
    mkdir docs
    echo 请将文档放入docs目录后重新运行此脚本。
    pause
    exit /b 1
)

:: 检查docs目录是否为空
dir docs /b >nul 2>nul
if %errorlevel% neq 0 (
    echo 📁 docs目录为空，请添加文档后重新运行。
    pause
    exit /b 1
)

:: 检查是否安装了依赖
echo 🔍 检查Python依赖...
%PYTHON_EXE% -c "import sentence_transformers, faiss, numpy" >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ 缺少必要的Python依赖，正在安装...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败，请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

:: 检查是否安装了前端依赖
if not exist "frontend\node_modules" (
    echo 🔍 检查前端依赖...
    cd frontend
    echo 正在安装前端依赖...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ 前端依赖安装失败，请手动运行: cd frontend && npm install
        pause
        exit /b 1
    )
    cd ..
)

:: 清理可能存在的旧进程
echo 🧹 清理旧进程...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1

:: 等待端口释放
echo ⏳ 等待端口释放...
timeout /t 3 /nobreak >nul

:: 启动后端API服务器
echo 🚀 启动后端API服务器...
echo ⏳ 正在加载AI模型，这可能需要几分钟...
start "后端API" cmd /k "python backend/api_server.py"
echo ⏳ 等待服务器完全启动...
timeout /t 10 /nobreak >nul

:: 启动前端开发服务器
echo 🌐 启动前端开发服务器...
start "前端界面" cmd /k "cd frontend && npm run dev"

echo ============================================================
echo ✅ 本地向量知识库已启动
echo ============================================================
echo 前端地址: http://localhost:3000
echo 后端API:  http://127.0.0.1:5000
echo.
echo 请在浏览器中打开前端地址。
echo.
echo 按任意键退出...
pause >nul

:: 停止所有进程
echo 🛑 正在停止所有服务...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1
echo 所有服务已停止。
endlocal