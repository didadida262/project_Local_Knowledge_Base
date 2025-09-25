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
echo 🚀 启动本地向量知识库 (稳定模式)
echo ============================================================

:: 清理可能存在的旧进程
echo 🧹 清理旧进程...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1

:: 等待端口释放
echo ⏳ 等待端口释放...
timeout /t 3 /nobreak >nul

:: 启动后端API服务器 (使用简化模式，避免重排模型)
echo 🚀 启动后端API服务器...
echo ⏳ 使用简化模式，避免重排模型加载问题...
start "后端API" cmd /k "python -c \"from backend.vector_knowledge_base import VectorKnowledgeBase; from backend.knowledge_retriever import KnowledgeRetriever; from backend.api_server import run_server; kb = VectorKnowledgeBase(use_reranker=False); retriever = KnowledgeRetriever(knowledge_base=kb); run_server()\""

:: 等待后端完全启动
echo ⏳ 等待后端服务器启动...
:wait_backend
timeout /t 2 /nobreak >nul
netstat -ano | findstr :5000 >nul
if %errorlevel% neq 0 (
    echo 等待后端启动中...
    goto wait_backend
)
echo ✅ 后端服务器已启动

:: 测试后端连接
echo 🔍 测试后端连接...
python -c "import requests; response = requests.get('http://127.0.0.1:5000/api/health'); print('健康检查:', response.json())" 2>nul
if %errorlevel% neq 0 (
    echo ❌ 后端连接测试失败，等待重试...
    timeout /t 5 /nobreak >nul
    goto wait_backend
)
echo ✅ 后端连接正常

:: 启动前端开发服务器
echo 🌐 启动前端开发服务器...
cd frontend
start "前端界面" cmd /k "npm run dev"
cd ..

echo ============================================================
echo ✅ 本地向量知识库已启动 (稳定模式)
echo ============================================================
echo 前端地址: http://localhost:3000
echo 后端API:  http://127.0.0.1:5000
echo.
echo 📝 说明:
echo - 使用简化模式，避免重排模型加载问题
echo - 后端服务器已通过健康检查
echo - 前端会自动重试连接
echo.
echo 按任意键退出...
pause >nul

:: 停止所有进程
echo 🛑 正在停止所有服务...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1
echo 所有服务已停止。
endlocal
