@echo off
chcp 65001 >nul
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
taskkill /f /im node.exe >nul 2>&1 >nul

:: 等待端口释放
echo ⏳ 等待端口释放...
ping -n 3 127.0.0.1 >nul

:: 启动后端API服务器
echo 🚀 启动后端API服务器...
echo ⏳ 正在初始化AI模型，这可能需要几分钟...
echo 📝 请持续关注后端窗口中的加载进度
echo.
start "后端API" cmd /k "cd backend && python api_server.py"

:: 等待后端启动完成
echo.
echo 📝 等待AI模型完全初始化...
echo 📝 自动检测后端状态中...
:wait_backend
ping -n 3 127.0.0.1 >nul
%PYTHON_EXE% -c "import requests; response = requests.get('http://127.0.0.1:5000/api/health'); print('健康检查:', response.json())" >nul 2>nul
if %errorlevel% neq 0 (
    echo 📝 等待后端启动中，请稍候...
    goto wait_backend
)
echo ✅ 后端连接正常

:: 启动前端开发服务器
echo 🌐 启动前端开发服务器...
echo ⏳ 正在启动React前端应用...
start "前端界面" cmd /k "echo 🚀 启动React开发服务器... && cd frontend && npm run dev"

:: 等待前端启动
echo ⏳ 等待前端服务器启动...
ping -n 5 127.0.0.1 >nul

echo ============================================================
echo ✅ 本地向量知识库已启动 (完整版)
echo ============================================================
echo 🌐 前端地址: http://localhost:3000
echo 🔧 后端API:  http://127.0.0.1:5000
echo.
echo 📝 前端和后端都已启动，请在浏览器中打开前端地址
echo 📝 关闭两个服务窗口即可停止系统
echo.
echo 按任意键激活浏览器并打开前端地址...
pause >nul
start http://localhost:3000

:: 停止所有进程
echo 🛑 正在停止所有服务...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1
echo 所有服务已停止。
endlocal