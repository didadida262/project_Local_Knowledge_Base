#!/usr/bin/env python3
"""
渐进式启动服务器
先启动基础HTTP服务，再逐步初始化AI组件
"""
import sys
import os
import json
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ProgressiveAPIHandler(BaseHTTPRequestHandler):
    """渐进式API处理器"""
    
    def __init__(self, *args, **kwargs):
        self.kb = None
        self.retriever = None
        self.initialization_complete = False
        self.initialization_error = None
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if self.initialization_complete:
                health_data = {
                    "status": "healthy",
                    "message": "服务器完全初始化完成",
                    "timestamp": time.time()
                }
            elif self.initialization_error:
                health_data = {
                    "status": "error",
                    "message": f"初始化失败: {self.initialization_error}",
                    "timestamp": time.time()
                }
            else:
                health_data = {
                    "status": "initializing",
                    "message": "服务器正在初始化中，请稍候...",
                    "timestamp": time.time()
                }
            
            self.wfile.write(json.dumps(health_data).encode())
            
        elif self.path == '/api/stats':
            if not self.initialization_complete:
                self.send_response(503)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "服务器正在初始化中，请稍候..."
                }).encode())
                return
            
            try:
                stats = self.kb.get_stats()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(stats).encode())
            except Exception as e:
                self.send_error(500, f"Failed to get stats: {str(e)}")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def do_POST(self):
        """处理POST请求"""
        if not self.initialization_complete:
            self.send_response(503)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "服务器正在初始化中，请稍候..."
            }).encode())
            return
        
        if self.path == '/api/search':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())
                
                query = data.get('query', '')
                top_k = data.get('top_k', 10)
                
                if not query:
                    self.send_error(400, "Query parameter is required")
                    return
                
                results = self.retriever.search(query, top_k)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
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
                self.send_error(500, f"Search failed: {str(e)}")
        
        elif self.path == '/api/ask':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())
                
                question = data.get('question', '')
                top_k = data.get('top_k', 5)
                
                if not question:
                    self.send_error(400, "Question parameter is required")
                    return
                
                result = self.retriever.ask_question(question, top_k)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            except Exception as e:
                self.send_error(500, f"Ask failed: {str(e)}")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"📝 {self.address_string()} - {format % args}")

def initialize_ai_components(handler):
    """在后台线程中初始化AI组件"""
    try:
        print("🔄 开始初始化AI组件...")
        
        # 导入AI组件
        from backend.vector_knowledge_base import VectorKnowledgeBase
        from backend.knowledge_retriever import KnowledgeRetriever
        
        print("🔄 初始化知识库...")
        handler.kb = VectorKnowledgeBase(use_reranker=False)
        print("✅ 知识库初始化完成")
        
        print("🔄 初始化检索器...")
        handler.retriever = KnowledgeRetriever(knowledge_base=handler.kb)
        print("✅ 检索器初始化完成")
        
        handler.initialization_complete = True
        print("🎉 AI组件初始化完成！")
        
    except Exception as e:
        print(f"❌ AI组件初始化失败: {e}")
        handler.initialization_error = str(e)
        import traceback
        traceback.print_exc()

def run_progressive_server(port=5000):
    """运行渐进式服务器"""
    try:
        print("🚀 启动渐进式API服务器...")
        
        # 创建处理器实例
        handler_instance = ProgressiveAPIHandler
        
        # 启动HTTP服务器
        server = HTTPServer(('127.0.0.1', port), handler_instance)
        print(f"✅ HTTP服务器已启动，监听端口: {port}")
        print(f"🌐 健康检查地址: http://127.0.0.1:{port}/api/health")
        
        # 在后台线程中初始化AI组件
        init_thread = threading.Thread(
            target=initialize_ai_components, 
            args=(handler_instance,),
            daemon=True
        )
        init_thread.start()
        
        print("🔄 AI组件正在后台初始化中...")
        print("按 Ctrl+C 停止服务器")
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 收到停止信号，正在关闭服务器...")
        server.shutdown()
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_progressive_server()
