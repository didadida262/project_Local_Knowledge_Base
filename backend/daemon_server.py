#!/usr/bin/env python3
"""
守护进程服务器
自动重启崩溃的后端服务
"""
import subprocess
import time
import sys
import os
import signal
import threading
from typing import Optional

class ServerDaemon:
    """服务器守护进程"""
    
    def __init__(self):
        self.server_process: Optional[subprocess.Popen] = None
        self.running = True
        self.restart_count = 0
        self.max_restarts = 10
        
    def start_server(self):
        """启动后端服务器"""
        try:
            print("🚀 启动后端API服务器...")
            self.server_process = subprocess.Popen([
                sys.executable, "-c", 
                "from backend.vector_knowledge_base import VectorKnowledgeBase; "
                "from backend.knowledge_retriever import KnowledgeRetriever; "
                "from backend.api_server import run_server; "
                "kb = VectorKnowledgeBase(use_reranker=False); "
                "retriever = KnowledgeRetriever(knowledge_base=kb); "
                "run_server()"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            print(f"✅ 后端服务器已启动 (PID: {self.server_process.pid})")
            return True
            
        except Exception as e:
            print(f"❌ 启动服务器失败: {e}")
            return False
    
    def check_server_health(self) -> bool:
        """检查服务器健康状态"""
        try:
            import requests
            response = requests.get('http://127.0.0.1:5000/api/health', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def restart_server(self):
        """重启服务器"""
        if self.server_process:
            print("🔄 停止旧服务器...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("⚠️ 强制终止服务器...")
                self.server_process.kill()
                self.server_process.wait()
        
        self.restart_count += 1
        print(f"🔄 重启服务器 (第{self.restart_count}次)...")
        
        if self.restart_count > self.max_restarts:
            print(f"❌ 超过最大重启次数({self.max_restarts})，停止守护进程")
            self.running = False
            return
        
        time.sleep(2)  # 等待端口释放
        self.start_server()
    
    def monitor_server(self):
        """监控服务器状态"""
        while self.running:
            try:
                if not self.server_process or self.server_process.poll() is not None:
                    print("⚠️ 检测到服务器进程已退出")
                    self.restart_server()
                    continue
                
                # 检查服务器健康状态
                if not self.check_server_health():
                    print("⚠️ 服务器健康检查失败")
                    self.restart_server()
                    continue
                
                time.sleep(10)  # 每10秒检查一次
                
            except KeyboardInterrupt:
                print("\n🛑 收到停止信号...")
                self.running = False
                break
            except Exception as e:
                print(f"❌ 监控过程中出错: {e}")
                time.sleep(5)
    
    def stop(self):
        """停止守护进程"""
        self.running = False
        if self.server_process:
            print("🛑 停止后端服务器...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
                self.server_process.wait()

def main():
    """主函数"""
    print("=" * 60)
    print("🛡️  后端服务器守护进程启动")
    print("=" * 60)
    
    daemon = ServerDaemon()
    
    # 设置信号处理
    def signal_handler(signum, frame):
        print(f"\n收到信号 {signum}，正在停止...")
        daemon.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # 启动服务器
        if not daemon.start_server():
            print("❌ 无法启动服务器，退出")
            sys.exit(1)
        
        # 等待服务器启动
        print("⏳ 等待服务器完全启动...")
        time.sleep(5)
        
        # 开始监控
        print("👁️ 开始监控服务器状态...")
        daemon.monitor_server()
        
    except KeyboardInterrupt:
        print("\n🛑 用户中断，正在停止...")
    except Exception as e:
        print(f"❌ 守护进程出错: {e}")
    finally:
        daemon.stop()
        print("✅ 守护进程已停止")

if __name__ == "__main__":
    main()
