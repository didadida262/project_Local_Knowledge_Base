#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API服务器
提供RESTful API接口供React前端调用
"""

# 设置控制台编码支持
import locale
import sys
import os
import json
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except:
    pass
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import re

# 添加backend目录到Python路径
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from vector_knowledge_base import VectorKnowledgeBase
from knowledge_retriever import KnowledgeRetriever


class APIHandler(BaseHTTPRequestHandler):
    # 类级静态变量，确保单例模式
    _kb = None
    _retriever = None
    _initialized = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @property
    def kb(self):
        return APIHandler._kb
    
    @property
    def retriever(self):
        return APIHandler._retriever
    
    def do_OPTIONS(self):
        """处理CORS预检请求"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            if path == '/api/stats':
                self.handle_stats()
            elif path == '/api/documents':
                self.handle_documents()
            elif path == '/api/health':
                self.handle_health()
            else:
                self.send_error(404, "Not Found")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def do_POST(self):
        """处理POST请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            if path == '/api/search':
                self.handle_search()
            elif path == '/api/ask':
                self.handle_ask()
            elif path == '/api/upload_document':
                self.handle_upload()
            elif path == '/api/add_document':
                self.handle_add_document()
            elif path == '/api/rebuild':
                self.handle_rebuild()
            else:
                self.send_error(404, "Not Found")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def send_cors_headers(self):
        """发送CORS头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
    
    def handle_stats(self):
        """处理统计信息请求"""
        try:
            if APIHandler._kb is None:
                self.send_error(500, "Failed to get stats: knowledge base not initialized")
                return
            stats = APIHandler._kb.get_stats()
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode())
        except Exception as e:
            self.send_error(500, f"Failed to get stats: {str(e)}")
    
    def handle_documents(self):
        """处理文档列表请求"""
        try:
            if APIHandler._kb is None:
                self.send_error(500, "Failed to get documents: knowledge base not initialized")
                return
            documents = APIHandler._kb.get_documents()
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"documents": documents}).encode())
        except Exception as e:
            self.send_error(500, f"Failed to get documents: {str(e)}")
    
    def handle_health(self):
        """处理健康检查请求"""
        try:
            if APIHandler._retriever is None:
                self.send_error(500, "Health check failed: retriever not initialized")
                return
                
            ollama_status = APIHandler._retriever.check_ollama_connection()
            health_data = {
                "status": "healthy", 
                "ollama_connected": ollama_status,
                "timestamp": time.time()
            }
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(health_data).encode())
        except Exception as e:
            self.send_error(500, f"Health check failed: {str(e)}")
    
    def handle_search(self):
        """处理搜索请求"""
        try:
            if APIHandler._retriever is None:
                self.send_error(500, "Search failed: retriever not initialized")
                return
                
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            query = data.get('query', '')
            top_k = data.get('top_k', 10)
            
            if not query:
                self.send_error(400, "Query parameter is required")
                return
            
            results = APIHandler._retriever.search(query, top_k)
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            # 确保所有数据都是JSON可序列化的
            serializable_results = []
            for result in results:
                serializable_result = {
                    'chunk_id': int(result['chunk_id']),
                    'doc_id': int(result['doc_id']),
                    'file_path': str(result['file_path']),
                    'file_name': str(result['file_name']),
                    'text': str(result['text']),
                    'similarity': float(result['similarity']),
                    'chunk_index': int(result['chunk_index'])
                }
                serializable_results.append(serializable_result)
            self.wfile.write(json.dumps({"results": serializable_results}).encode())
        except Exception as e:
            import traceback
            error_msg = f"Search failed: {str(e)}\n{traceback.format_exc()}"
            self.send_error(500, error_msg)
    
    def handle_ask(self):
        """处理问答请求"""
        try:
            if APIHandler._retriever is None:
                self.send_error(500, "Ask question failed: retriever not initialized")
                return
                
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            question = data.get('question', '')
            top_k = data.get('top_k', 5)
            
            if not question:
                self.send_error(400, "Question parameter is required")
                return
            
            print(f"🤖 处理问答请求: {question[:50]}...")
            result = APIHandler._retriever.ask_question(question, top_k)
            print(f"✅ 问答处理完成")
            
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            import traceback
            error_msg = f"Ask failed: {str(e)}\n{traceback.format_exc()}"
            print(f"❌ 问答处理失败: {error_msg}")
            self.send_error(500, error_msg)
    
    def handle_upload(self):
        """处理文件上传请求（支持文件夹上传）"""
        try:
            if APIHandler._kb is None:
                self.send_error(500, "Upload failed: knowledge base not initialized")
                return
            
            # 解析multipart/form-data
            content_type = self.headers.get('Content-Type', '')
            if not content_type.startswith('multipart/form-data'):
                self.send_error(400, "Content-Type must be multipart/form-data")
                return
            
            # 解析boundary
            boundary_match = re.search(r'boundary=([^;]+)', content_type)
            if not boundary_match:
                self.send_error(400, "Boundary not found in Content-Type")
                return
            
            boundary = boundary_match.group(1).strip('"')
            boundary_bytes = ('--' + boundary).encode('utf-8')
            
            # 读取请求体
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # 分割multipart数据
            parts = post_data.split(boundary_bytes)
            
            # 创建临时上传目录
            project_root = Path(__file__).parent.parent
            upload_dir = project_root / "uploads"
            upload_dir.mkdir(exist_ok=True)
            
            uploaded_files = []
            supported_extensions = {'.txt', '.md', '.pdf', '.docx', '.html', '.htm'}
            
            # 处理所有上传的文件
            for part in parts:
                if not part.strip() or part.strip() == b'--':
                    continue
                
                # 查找Content-Disposition头
                header_end = part.find(b'\r\n\r\n')
                if header_end == -1:
                    continue
                
                header = part[:header_end].decode('utf-8', errors='ignore')
                file_data = part[header_end + 4:]
                
                # 提取文件名（可能包含路径，因为文件夹上传）
                # 检查是否有name="files"（多个文件）或name="file"（单个文件）
                name_match = re.search(r'name="([^"]+)"', header)
                filename_match = re.search(r'filename="([^"]+)"', header)
                
                if filename_match:
                    filename = filename_match.group(1)
                    
                    # 移除末尾的\r\n
                    file_data = file_data.rstrip(b'\r\n')
                    
                    if filename and file_data:
                        # 检查文件扩展名
                        file_ext = Path(filename).suffix.lower()
                        if file_ext not in supported_extensions:
                            continue  # 跳过不支持的文件格式
                        
                        # 保持文件夹结构（如果上传的是文件夹）
                        # 移除可能的路径分隔符，只保留文件名
                        safe_filename = filename.replace('\\', '/').split('/')[-1]
                        
                        # 保存文件
                        file_path = upload_dir / safe_filename
                        with open(file_path, 'wb') as f:
                            f.write(file_data)
                        
                        uploaded_files.append(str(file_path))
            
            if not uploaded_files:
                self.send_error(400, "No supported files found in upload")
                return
            
            # 批量添加文档到知识库
            results = []
            errors = []
            
            for file_path in uploaded_files:
                try:
                    doc_info = APIHandler._kb.add_document(file_path)
                    results.append(doc_info)
                except Exception as e:
                    errors.append(f"{Path(file_path).name}: {str(e)}")
            
            # 保存知识库
            APIHandler._kb.save_knowledge_base()
            
            # 构建响应消息
            if errors:
                message = f"成功处理 {len(results)} 个文件，失败 {len(errors)} 个"
            else:
                message = f"成功处理 {len(results)} 个文件"
            
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": message,
                "processed_count": len(results),
                "error_count": len(errors),
                "documents": results,
                "errors": errors if errors else None
            }).encode())
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.send_error(500, f"Upload failed: {str(e)}")
    
    def handle_add_document(self):
        """处理添加文档请求"""
        try:
            if APIHandler._kb is None:
                self.send_error(500, "Add document failed: knowledge base not initialized")
                return
                
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            file_path = data.get('file_path', '')
            if not file_path:
                self.send_error(400, "file_path parameter is required")
                return
            
            if not os.path.exists(file_path):
                self.send_error(404, f"File not found: {file_path}")
                return
            
            # 添加文档到知识库
            doc_info = APIHandler._kb.add_document(file_path)
            
            # 保存知识库
            APIHandler._kb.save_knowledge_base()
            
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": f"文档 {doc_info['file_name']} 添加成功",
                "document": doc_info
            }).encode())
        except Exception as e:
            self.send_error(500, f"Add document failed: {str(e)}")
    
    def handle_rebuild(self):
        """处理重建知识库请求"""
        try:
            if APIHandler._kb is None:
                self.send_error(500, "Rebuild failed: knowledge base not initialized")
                return
                
            # 清空现有知识库
            APIHandler._kb.clear_knowledge_base()
            
            # 保存清空后的知识库
            APIHandler._kb.save_knowledge_base()
            
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": "知识库已清空，请通过上传文件重新构建"
            }).encode())
        except Exception as e:
            self.send_error(500, f"Rebuild failed: {str(e)}")
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")


def run_server(port=5000):
    """启动服务器"""
    print("=" * 60)
    print("🚀 本地向量知识库 API服务器")
    print("=" * 60)
    print(f"📡 服务地址: http://127.0.0.1:{port}")
    print("📋 可用API端点:")
    print("   GET  /api/stats - 获取统计信息")
    print("   GET  /api/documents - 获取文档列表")
    print("   GET  /api/health - 健康检查")
    print("   POST /api/search - 搜索文档")
    print("   POST /api/ask - AI问答")
    print("   POST /api/upload_document - 上传文档")
    print("   POST /api/add_document - 添加文档")
    print("   POST /api/rebuild - 重建知识库")
    print("=" * 60)
    print("⏳ 正在初始化所有AI模型，请稍候...")
    
    # 在启动HTTP服务器之前完全初始化所有模型
    try:
        print("🔄 正在加载向量模型...")
        kb = VectorKnowledgeBase()
        
        # 获取知识库初始状态
        kb_stats_before = kb.get_stats()
        total_docs = kb_stats_before.get('total_documents', 0)
        total_vectors = kb_stats_before.get('total_vectors', 0)
        
        if total_docs == 0:
            print("✅ 向量模型加载完成，知识库为空，等待用户上传文件")
        else:
            print(f"✅ 向量模型加载完成，知识库已包含 {total_docs} 文档, {total_vectors} 向量")
        
        print("🔄 正在初始化检索器...")
        retriever = KnowledgeRetriever(kb)
        print("✅ 检索器初始化完成")
        
        # 验证初始化状态
        print("🔄 正在验证系统初始化状态...")
        
        # 测试知识库功能
        if kb is None:
            raise Exception("知识库对象为空")
        kb_stats = kb.get_stats()
        print(f"📊 知识库状态: {kb_stats.get('total_documents', 0)} 文档, {kb_stats.get('total_vectors', 0)} 向量")
        
        # 测试检索器功能
        if retriever is None:
            raise Exception("检索器对象为空")
        
        # 检查Ollama连接和模型
        print("🔍 检查Ollama服务和模型...")
        ollama_status = retriever.check_ollama_connection()
        if not ollama_status:
            print("=" * 60)
            print("❌ 错误: 无法连接到Ollama服务")
            print("=" * 60)
            print("请确保Ollama服务正在运行:")
            print("  1. 检查Ollama是否安装: ollama --version")
            print("  2. 启动Ollama服务: ollama serve")
            print("  3. 或访问 https://ollama.ai 下载安装Ollama")
            print("=" * 60)
            print("⚠️  注意: 即使没有Ollama，搜索功能仍然可以正常使用")
            print("⚠️  但AI问答功能将不可用")
            print("=" * 60)
        else:
            # 检查模型是否存在
            available_models = retriever.get_ollama_models()
            required_model = "gemma2:2b"
            
            if not available_models:
                print("=" * 60)
                print("❌ 错误: Ollama服务运行正常，但未安装任何模型")
                print("=" * 60)
                print(f"请安装所需的模型: {required_model}")
                print(f"运行命令: ollama pull {required_model}")
                print("=" * 60)
                raise Exception(f"Ollama模型 {required_model} 未安装")
            
            # 检查是否有所需模型（支持完整匹配或部分匹配）
            model_found = False
            matching_models = []
            for model in available_models:
                if required_model.lower() in model.lower() or "gemma2" in model.lower():
                    model_found = True
                    matching_models.append(model)
            
            if not model_found:
                print("=" * 60)
                print(f"❌ 错误: 未找到所需的Ollama模型: {required_model}")
                print("=" * 60)
                print(f"已安装的模型: {', '.join(available_models) if available_models else '无'}")
                print("")
                print("解决方案:")
                print(f"  1. 安装模型: ollama pull {required_model}")
                print("  2. 或使用其他已安装的模型（需要修改代码）")
                print("=" * 60)
                raise Exception(f"Ollama模型 {required_model} 未安装，已安装的模型: {', '.join(available_models)}")
            else:
                print(f"✅ 找到模型: {', '.join(matching_models)}")
        
        print(f"🔗 Ollama连接状态: {'连接正常' if ollama_status else '连接失败'}")
        
        # 将初始化的实例设置为APIHandler的类属性
        APIHandler._kb = kb
        APIHandler._retriever = retriever
        APIHandler._initialized = True
        
        # 验证API预备性
        print("🔍 验证API预备性...")
        if APIHandler._kb is None:
            raise Exception("知识库对象未正确设置")
        if APIHandler._retriever is None:
            raise Exception("检索器对象未正确设置")
        
        print("🎉 所有AI模型初始化完成并验证通过！")
        print("✅ 系统已完全就绪，开始接受请求")
        
    except Exception as e:
        print(f"❌ AI模型初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("🚀 正在启动HTTP服务器...")
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, APIHandler)
    
    print("=" * 60)
    print("✅ 服务器已就绪，可以接受连接")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()
