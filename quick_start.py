#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动脚本 - 避免模型加载卡住
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path


def check_ollama():
    """检查Ollama服务"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama服务运行正常")
            return True
        else:
            print("⚠️  Ollama服务响应异常")
            return False
    except Exception as e:
        print(f"⚠️  无法连接到Ollama服务: {e}")
        print("💡 请确保Ollama正在运行: ollama serve")
        return False


def start_web_interface():
    """启动Web界面"""
    print("\n" + "=" * 60)
    print("🌐 启动Web界面")
    print("=" * 60)
    
    try:
        # 导入并启动Web界面
        from web_interface import app, init_knowledge_base
        
        # 初始化知识库
        print("🔄 正在初始化知识库...")
        init_knowledge_base("./knowledge_base")
        
        print("🚀 启动Web服务器...")
        print("📱 访问地址: http://127.0.0.1:5000")
        print("💡 提示: 按 Ctrl+C 停止服务器")
        print("=" * 60)
        
        # 自动打开浏览器
        try:
            webbrowser.open('http://127.0.0.1:5000')
            print("🌐 已自动打开浏览器")
        except:
            print("⚠️  无法自动打开浏览器，请手动访问 http://127.0.0.1:5000")
        
        # 启动Flask应用
        app.run(debug=False, host='127.0.0.1', port=5000, threaded=True)
        
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动Web界面失败: {e}")
        print("💡 请检查依赖是否安装: pip install -r requirements.txt")


def main():
    """主函数"""
    print("🚀 本地向量知识库 - 快速启动")
    print("=" * 60)
    
    # 检查docs目录
    docs_dir = Path("docs")
    if not docs_dir.exists():
        print("❌ docs目录不存在，正在创建...")
        docs_dir.mkdir(exist_ok=True)
        print("✅ docs目录已创建")
        print("💡 请将文档放入docs目录后重新运行")
        input("按回车键退出...")
        return
    
    # 检查是否有文档
    supported_extensions = {'.txt', '.md', '.pdf', '.docx', '.html', '.htm'}
    docs = [f for f in docs_dir.iterdir() 
            if f.is_file() and f.suffix.lower() in supported_extensions]
    
    if not docs:
        print("⚠️  docs目录为空")
        print("💡 请将文档放入docs目录，或通过Web界面上传文档")
        choice = input("是否继续启动？(y/n): ").strip().lower()
        if choice not in ['y', 'yes', '是']:
            return
    
    # 检查Ollama服务
    if not check_ollama():
        print("⚠️  Ollama服务未运行，问答功能可能不可用")
        print("💡 请运行: ollama serve")
        choice = input("是否继续启动？(y/n): ").strip().lower()
        if choice not in ['y', 'yes', '是']:
            return
    
    # 启动Web界面
    start_web_interface()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 程序已退出")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        input("按回车键退出...")
