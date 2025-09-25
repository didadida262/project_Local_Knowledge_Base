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
echo 🚀 启动本地向量知识库 (最终稳定版)
echo ============================================================

:: 清理可能存在的旧进程
echo 🧹 清理旧进程...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1

:: 等待端口释放
echo ⏳ 等待端口释放...
timeout /t 3 /nobreak >nul

:: 启动渐进式服务器
echo 🚀 启动渐进式API服务器...
echo ⏳ 服务器将先启动HTTP服务，再在后台初始化AI组件...
start "渐进式API" cmd /k "python backend/progressive_server.py"

:: 等待HTTP服务器启动
echo ⏳ 等待HTTP服务器启动...
:wait_http
timeout /t 2 /nobreak >nul
netstat -ano | findstr :5000 >nul
if %errorlevel% neq 0 (
    echo 等待HTTP服务器启动中...
    goto wait_http
)
echo ✅ HTTP服务器已启动

:: 测试基础连接
echo 🔍 测试基础连接...
python -c "import requests; response = requests.get('http://127.0.0.1:5000/api/health'); print('服务器状态:', response.json())" 2>nul
if %errorlevel% neq 0 (
    echo ❌ 基础连接测试失败，等待重试...
    timeout /t 5 /nobreak >nul
    goto wait_http
)
echo ✅ 基础连接正常

:: 启动前端开发服务器
echo 🌐 启动前端开发服务器...
cd frontend
start "前端界面" cmd /k "npm run dev"
cd ..

echo ============================================================
echo ✅ 本地向量知识库已启动 (最终稳定版)
echo ============================================================
echo 前端地址: http://localhost:3000
echo 后端API:  http://127.0.0.1:5000
echo.
echo 🎯 特性:
echo - 渐进式启动，HTTP服务立即可用
echo - AI组件在后台初始化，不阻塞启动
echo - 前端会显示初始化状态
echo - 初始化完成后所有功能正常
echo.
echo 📝 说明:
echo - 首次启动可能需要几分钟来初始化AI组件
echo - 前端会显示"正在初始化中"状态
echo - 初始化完成后会自动显示完整功能
echo.
echo 按任意键退出...
pause >nul

:: 停止所有进程
echo 🛑 正在停止所有服务...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1
echo 所有服务已停止。
endlocal
