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
        """处理文件上传请求"""
        try:
            # 简化的上传处理 - 实际项目中需要处理multipart/form-data
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": "文件上传功能暂未实现，请使用添加文档功能"
            }).encode())
        except Exception as e:
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
            
            # 重新加载docs目录
            docs_dir = Path("../docs")
            if docs_dir.exists():
                results = APIHandler._kb.add_directory(str(docs_dir))
                
                # 保存知识库
                APIHandler._kb.save_knowledge_base()
                
                self.send_response(200)
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "message": f"知识库重建完成，处理了 {len(results)} 个文档",
                    "documents": results
                }).encode())
            else:
                self.send_error(404, "docs directory not found")
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
        print("🔄 正在初始化知识库...")
        kb = VectorKnowledgeBase()
        print("✅ 知识库初始化完成")
        
        # 检查是否需要自动加载docs目录
        print("🔍 检查默认语料库...")
        kb_stats_before = kb.get_stats()
        print(f"📊 当前知识库统计: {kb_stats_before.get('total_documents', 0)} 文档, {kb_stats_before.get('total_vectors', 0)} 向量")
        
        # 如果知识库是空的，尝试加载docs目录
        if kb_stats_before.get('total_documents', 0) == 0:
            docs_dir = Path("../docs")  # 从backend目录向上，然后进入docs
            print(f"📝 知识库为空，检查并加载docs目录: {docs_dir.absolute()}")
            
            if docs_dir.exists():
                print("📂 发现docs目录，正在加载默认语料库...")
                results = kb.add_directory(str(docs_dir))
                kb.save_knowledge_base()
                print(f"✅ 加载完成：添加了 {len(results)} 个文档到知识库")
            else:
                print("⚠️ docs目录不存在，跳过默认语料库加载")
        else:
            print("✅ 知识库不为空，跳过默认语料库加载")
        
        print("🔄 正在初始化检索器...")
        retriever = KnowledgeRetriever(kb)
        print("✅ 检索器初始化完成")
        
        # 验证初始化状态
        print("🔄 正在验证系统初始化状态...")
        
        # 测试知识库功能
        if kb is None:
            raise Exception("知识库对象为空")
        kb_stats = kb.get_stats()
        print(f"📊 知识库统计: {kb_stats.get('total_documents', 0)} 文档, {kb_stats.get('total_vectors', 0)} 向量")
        
        # 测试检索器功能
        if retriever is None:
            raise Exception("检索器对象为空")
        ollama_status = retriever.check_ollama_connection()
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
