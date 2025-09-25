#!/usr/bin/env python3
"""
简化的API服务器
用于调试API服务器启动问题
"""
import sys
import os
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class SimpleAPIHandler(BaseHTTPRequestHandler):
    """简化的API处理器"""
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            health_data = {
                "status": "healthy",
                "message": "简化API服务器正常运行",
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(health_data).encode())
        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            stats_data = {
                "total_vectors": 6336,
                "total_documents": 4,
                "unique_files": 4,
                "model_name": "all-MiniLM-L6-v2",
                "dimension": 384,
                "use_reranker": False,
                "reranker_model": None
            }
            self.wfile.write(json.dumps(stats_data).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def do_POST(self):
        """处理POST请求"""
        if self.path == '/api/search':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_data = {
                "results": [
                    {
                        "chunk_id": 1,
                        "doc_id": 1,
                        "file_path": "docs/test.txt",
                        "file_name": "test.txt",
                        "text": "这是一个测试文档",
                        "similarity": 0.95,
                        "chunk_index": 0
                    }
                ]
            }
            self.wfile.write(json.dumps(response_data).encode())
        elif self.path == '/api/ask':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_data = {
                "question": "测试问题",
                "answer": "这是一个测试回答",
                "sources": [],
                "confidence": 0.8
            }
            self.wfile.write(json.dumps(response_data).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"📝 {self.address_string()} - {format % args}")

def run_simple_api_server(port=5000):
    """运行简化API服务器"""
    try:
        print("🚀 启动简化API服务器...")
        server = HTTPServer(('127.0.0.1', port), SimpleAPIHandler)
        print(f"✅ 简化API服务器已启动，监听端口: {port}")
        print(f"🌐 健康检查地址: http://127.0.0.1:{port}/api/health")
        print(f"📊 统计信息地址: http://127.0.0.1:{port}/api/stats")
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
    run_simple_api_server()
