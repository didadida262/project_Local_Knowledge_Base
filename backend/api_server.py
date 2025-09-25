#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API服务器
提供RESTful API接口供React前端调用
"""

import os
import sys
import json
import time
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .vector_knowledge_base import VectorKnowledgeBase
from .knowledge_retriever import KnowledgeRetriever


class APIHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # 初始化知识库和检索器
        self.kb = VectorKnowledgeBase()
        self.retriever = KnowledgeRetriever(self.kb)
        super().__init__(*args, **kwargs)
    
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
            stats = self.kb.get_stats()
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode())
        except Exception as e:
            self.send_error(500, f"Failed to get stats: {str(e)}")
    
    def handle_documents(self):
        """处理文档列表请求"""
        try:
            documents = self.kb.get_documents()
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"documents": documents}).encode())
        except Exception as e:
            self.send_error(500, f"Failed to get documents: {str(e)}")
    
    def handle_health(self):
        """处理健康检查请求"""
        try:
            ollama_status = self.retriever.check_ollama_connection()
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
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            question = data.get('question', '')
            top_k = data.get('top_k', 5)
            
            if not question:
                self.send_error(400, "Question parameter is required")
                return
            
            print(f"🤖 处理问答请求: {question[:50]}...")
            result = self.retriever.ask_question(question, top_k)
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
            doc_info = self.kb.add_document(file_path)
            
            # 保存知识库
            self.kb.save_knowledge_base()
            
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
            # 清空现有知识库
            self.kb.clear_knowledge_base()
            
            # 重新加载docs目录
            docs_dir = Path("../docs")
            if docs_dir.exists():
                results = self.kb.add_directory(str(docs_dir))
                
                # 保存知识库
                self.kb.save_knowledge_base()
                
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
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, APIHandler)
    
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
    print("⏳ 正在初始化模型，请稍候...")
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
