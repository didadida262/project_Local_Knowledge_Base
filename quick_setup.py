#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速设置脚本
自动安装依赖并构建知识库
"""

import subprocess
import sys
import os
from pathlib import Path


def install_dependencies():
    """安装依赖"""
    print("正在安装Python依赖...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 依赖安装失败: {e}")
        return False


def check_ollama():
    """检查Ollama服务"""
    print("检查Ollama服务...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✓ Ollama服务运行正常")
            return True
        else:
            print("✗ Ollama服务响应异常")
            return False
    except Exception as e:
        print(f"✗ 无法连接到Ollama服务: {e}")
        print("请确保Ollama正在运行: ollama serve")
        return False


def create_docs_directory():
    """创建docs目录"""
    print("创建docs目录...")
    
    # 创建docs目录
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # 创建README文件说明
    readme_content = """# 文档目录

请将您的文档放入此目录，系统支持以下格式：

- 纯文本文件 (.txt)
- Markdown文件 (.md)
- PDF文件 (.pdf)
- Word文档 (.docx)
- HTML文件 (.html, .htm)

## 使用方法

1. 将文档放入此目录
2. 运行构建命令：`python knowledge_base_main.py --mode build`
3. 开始使用知识库进行搜索和问答

## 注意事项

- 文档会自动分块处理
- 支持中文和英文文档
- 建议文档大小不超过100MB
"""
    
    readme_path = docs_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✓ 创建了docs目录")
    return docs_dir


def main():
    """主函数"""
    print("=" * 60)
    print("本地向量知识库 - 快速设置")
    print("=" * 60)
    
    # 1. 安装依赖
    if not install_dependencies():
        print("设置失败：依赖安装失败")
        return False
    
    # 2. 检查Ollama
    if not check_ollama():
        print("警告：Ollama服务未运行，问答功能可能不可用")
        print("请运行：ollama serve")
    
    # 3. 创建docs目录
    docs_dir = create_docs_directory()
    
    # 4. 构建知识库
    print("\n构建知识库...")
    try:
        from knowledge_base_main import KnowledgeBaseManager
        
        manager = KnowledgeBaseManager()
        success = manager.build_knowledge_base(str(docs_dir), recursive=True)
        
        if success:
            print("✓ 知识库构建完成")
        else:
            print("✗ 知识库构建失败")
            return False
            
    except Exception as e:
        print(f"✗ 知识库构建失败: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("设置完成！")
    print("=" * 60)
    print("使用方法：")
    print("1. 命令行模式：python knowledge_base_main.py")
    print("2. Web界面：python web_interface.py")
    print("3. 交互式模式：python knowledge_base_main.py --mode interactive")
    print("\n示例查询：")
    print("- 什么是Python？")
    print("- 机器学习有哪些类型？")
    print("- 如何开发Web应用？")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
