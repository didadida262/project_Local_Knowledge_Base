#!/usr/bin/env python3
"""
简单的测试服务器
用于调试HTTP服务器启动问题
"""
import sys
import os
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestHandler(BaseHTTPRequestHandler):
    """测试HTTP处理器"""
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            health_data = {
                "status": "healthy",
                "message": "测试服务器正常运行",
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(health_data).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def do_POST(self):
        """处理POST请求"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response_data = {
            "status": "success",
            "message": "POST请求处理成功"
        }
        self.wfile.write(json.dumps(response_data).encode())
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"📝 {self.address_string()} - {format % args}")

def run_test_server(port=5000):
    """运行测试服务器"""
    try:
        print("🚀 启动测试HTTP服务器...")
        server = HTTPServer(('127.0.0.1', port), TestHandler)
        print(f"✅ 测试服务器已启动，监听端口: {port}")
        print(f"🌐 健康检查地址: http://127.0.0.1:{port}/api/health")
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
    run_test_server()
