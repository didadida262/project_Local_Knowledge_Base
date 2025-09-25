#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全栈启动脚本
同时启动后端API和前端React应用
"""

import os
import sys
import time
import subprocess
import webbrowser
import threading
from pathlib import Path


class FullStackManager:
    """全栈管理器"""
    
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.backend_port = 5000
        self.frontend_port = 3000
    
    def check_dependencies(self):
        """检查依赖"""
        print("🔍 检查依赖...")
        
        # 检查Python依赖
        try:
            import flask, sentence_transformers, faiss
            print("✅ Python依赖已安装")
        except ImportError as e:
            print(f"❌ Python依赖缺失: {e}")
            print("请运行: pip install -r requirements.txt")
            return False
        
        # 检查Node.js和npm
        try:
            subprocess.run(['node', '--version'], check=True, capture_output=True)
            subprocess.run(['npm', '--version'], check=True, capture_output=True)
            print("✅ Node.js和npm已安装")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Node.js或npm未安装")
            print("请安装Node.js: https://nodejs.org/")
            return False
        
        return True
    
    def install_frontend_dependencies(self):
        """安装前端依赖"""
        print("📦 安装前端依赖...")
        
        frontend_dir = Path("frontend")
        if not frontend_dir.exists():
            print("❌ frontend目录不存在")
            return False
        
        try:
            # 检查是否已安装依赖
            node_modules = frontend_dir / "node_modules"
            if node_modules.exists():
                print("✅ 前端依赖已安装")
                return True
            
            # 安装依赖
            result = subprocess.run(
                ['npm', 'install'],
                cwd=frontend_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ 前端依赖安装完成")
                return True
            else:
                print(f"❌ 前端依赖安装失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 安装前端依赖失败: {e}")
            return False
    
    def start_backend(self):
        """启动后端"""
        print("🚀 启动后端API...")
        
        try:
            # 启动API服务器
            self.backend_process = subprocess.Popen(
                [sys.executable, 'backend/api_server.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 等待后端启动
            time.sleep(3)
            
            # 检查后端是否启动成功
            if self.backend_process.poll() is None:
                print(f"✅ 后端API已启动 (端口: {self.backend_port})")
                return True
            else:
                print("❌ 后端启动失败")
                return False
                
        except Exception as e:
            print(f"❌ 启动后端失败: {e}")
            return False
    
    def start_frontend(self):
        """启动前端"""
        print("🚀 启动前端应用...")
        
        frontend_dir = Path("frontend")
        
        try:
            # 启动Vite开发服务器
            self.frontend_process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 等待前端启动
            time.sleep(5)
            
            # 检查前端是否启动成功
            if self.frontend_process.poll() is None:
                print(f"✅ 前端应用已启动 (端口: {self.frontend_port})")
                return True
            else:
                print("❌ 前端启动失败")
                return False
                
        except Exception as e:
            print(f"❌ 启动前端失败: {e}")
            return False
    
    def open_browser(self):
        """打开浏览器"""
        try:
            webbrowser.open(f'http://localhost:{self.frontend_port}')
            print("🌐 已自动打开浏览器")
        except:
            print(f"⚠️  无法自动打开浏览器，请手动访问 http://localhost:{self.frontend_port}")
    
    def start(self):
        """启动全栈应用"""
        print("=" * 60)
        print("🚀 本地向量知识库 - 全栈启动")
        print("=" * 60)
        
        # 检查依赖
        if not self.check_dependencies():
            return False
        
        # 安装前端依赖
        if not self.install_frontend_dependencies():
            return False
        
        # 启动后端
        if not self.start_backend():
            return False
        
        # 启动前端
        if not self.start_frontend():
            self.stop_backend()
            return False
        
        # 打开浏览器
        self.open_browser()
        
        print("\n" + "=" * 60)
        print("🎉 全栈应用启动成功！")
        print("=" * 60)
        print(f"📱 前端地址: http://localhost:{self.frontend_port}")
        print(f"🔧 后端API: http://localhost:{self.backend_port}")
        print("💡 按 Ctrl+C 停止所有服务")
        print("=" * 60)
        
        try:
            # 保持运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 正在停止服务...")
            self.stop_all()
    
    def stop_backend(self):
        """停止后端"""
        if self.backend_process:
            self.backend_process.terminate()
            self.backend_process.wait()
            print("✅ 后端已停止")
    
    def stop_frontend(self):
        """停止前端"""
        if self.frontend_process:
            self.frontend_process.terminate()
            self.frontend_process.wait()
            print("✅ 前端已停止")
    
    def stop_all(self):
        """停止所有服务"""
        self.stop_frontend()
        self.stop_backend()
        print("👋 所有服务已停止")


def main():
    """主函数"""
    try:
        manager = FullStackManager()
        manager.start()
    except KeyboardInterrupt:
        print("\n👋 程序已退出")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        input("按回车键退出...")


if __name__ == "__main__":
    main()
