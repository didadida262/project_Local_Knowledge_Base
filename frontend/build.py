#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端构建脚本
构建React应用并集成到Flask后端
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def build_frontend():
    """构建前端应用"""
    print("🔨 构建前端应用...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ frontend目录不存在")
        return False
    
    try:
        # 安装依赖
        print("📦 安装依赖...")
        result = subprocess.run(
            ['npm', 'install'],
            cwd=frontend_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ 依赖安装失败: {result.stderr}")
            return False
        
        # 构建应用
        print("🏗️  构建应用...")
        result = subprocess.run(
            ['npm', 'run', 'build'],
            cwd=frontend_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ 构建失败: {result.stderr}")
            return False
        
        # 复制构建文件到Flask静态目录
        dist_dir = frontend_dir / "dist"
        static_dir = Path("static")
        templates_dir = Path("templates")
        
        # 创建目录
        static_dir.mkdir(exist_ok=True)
        templates_dir.mkdir(exist_ok=True)
        
        # 复制静态文件
        if dist_dir.exists():
            print("📁 复制静态文件...")
            for item in dist_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, static_dir / item.name)
                elif item.is_dir():
                    shutil.copytree(item, static_dir / item.name, dirs_exist_ok=True)
        
        print("✅ 前端构建完成")
        return True
        
    except Exception as e:
        print(f"❌ 构建失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 前端构建工具")
    print("=" * 40)
    
    if build_frontend():
        print("🎉 构建成功！")
        print("💡 现在可以运行: python web_interface.py")
    else:
        print("❌ 构建失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
