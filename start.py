#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一启动脚本
自动构建知识库并启动Web界面
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path
from vector_knowledge_base import VectorKnowledgeBase
from knowledge_retriever import KnowledgeRetriever


class KnowledgeBaseManager:
    """知识库管理器"""
    
    def __init__(self):
        self.kb = None
        self.retriever = None
        self.docs_dir = Path("docs")
        self.knowledge_base_dir = Path("knowledge_base")
    
    def check_docs_directory(self):
        """检查docs目录"""
        if not self.docs_dir.exists():
            print("❌ docs目录不存在，正在创建...")
            self.docs_dir.mkdir(exist_ok=True)
            
            # 创建说明文件
            readme_content = """# 文档目录

请将您的文档放入此目录，系统支持以下格式：

- 纯文本文件 (.txt)
- Markdown文件 (.md)
- PDF文件 (.pdf)
- Word文档 (.docx)
- HTML文件 (.html, .htm)

## 使用方法

1. 将文档放入此目录
2. 系统会自动处理并建立向量索引
3. 开始使用知识库进行搜索和问答

## 注意事项

- 文档会自动分块处理
- 支持中文和英文文档
- 建议文档大小不超过100MB
"""
            readme_path = self.docs_dir / "README.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            print("✅ docs目录已创建")
            return False
        
        # 检查是否有文档
        supported_extensions = {'.txt', '.md', '.pdf', '.docx', '.html', '.htm'}
        docs = [f for f in self.docs_dir.iterdir() 
                if f.is_file() and f.suffix.lower() in supported_extensions]
        
        if not docs:
            print("⚠️  docs目录为空，请添加文档后再启动")
            return False
        
        print(f"✅ 发现 {len(docs)} 个文档")
        return True
    
    def build_knowledge_base(self, force_rebuild=False):
        """构建知识库"""
        print("=" * 60)
        print("🧠 构建本地向量知识库")
        print("=" * 60)
        
        # 每次启动都重新构建知识库，确保与docs目录同步
        print("🔄 正在同步知识库与docs目录...")
        
        print("🔄 正在构建知识库...")
        print("⏳ 首次运行可能需要几分钟，请耐心等待...")
        start_time = time.time()
        
        try:
            # 清空旧的知识库
            if self.knowledge_base_dir.exists():
                print("🗑️  清理旧知识库...")
                import shutil
                shutil.rmtree(self.knowledge_base_dir)
            
            # 初始化新的知识库
            print("📥 加载嵌入模型...")
            self.kb = VectorKnowledgeBase(storage_dir=str(self.knowledge_base_dir))
            
            print("📄 处理文档...")
            # 添加文档
            added_count = self.kb.add_directory(str(self.docs_dir), recursive=True)
            
            if added_count == 0:
                print("❌ 没有找到可处理的文档")
                return False
            
            print("💾 保存知识库...")
            # 保存知识库
            if self.kb.save_knowledge_base():
                elapsed_time = time.time() - start_time
                stats = self.kb.get_stats()
                
                print("✅ 知识库构建完成")
                print(f"📊 统计信息:")
                print(f"   - 总向量数: {stats['total_vectors']}")
                print(f"   - 总文档数: {stats['total_documents']}")
                print(f"   - 唯一文件数: {stats['unique_files']}")
                print(f"   - 构建时间: {elapsed_time:.2f}秒")
                
                # 初始化检索器
                self.retriever = KnowledgeRetriever(self.kb)
                return True
            else:
                print("❌ 保存知识库失败")
                return False
                
        except Exception as e:
            print(f"❌ 构建知识库失败: {e}")
            print("💡 提示: 如果模型下载失败，请检查网络连接")
            return False
    
    def start_web_interface(self):
        """启动Web界面"""
        print("\n" + "=" * 60)
        print("🌐 启动Web界面")
        print("=" * 60)
        
        try:
            # 导入并启动Web界面
            from web_interface import app, init_knowledge_base
            
            # 初始化知识库
            init_knowledge_base(str(self.knowledge_base_dir))
            
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
    
    def rebuild_after_upload(self, uploaded_files):
        """用户上传文件后重建知识库"""
        print("\n" + "=" * 60)
        print("📁 检测到新文档，正在重建知识库...")
        print("=" * 60)
        
        # 显示上传的文件
        print("📄 新上传的文件:")
        for file in uploaded_files:
            print(f"   - {file}")
        
        # 重建知识库
        if self.build_knowledge_base(force_rebuild=True):
            print("✅ 知识库重建完成，新文档已可用")
            return True
        else:
            print("❌ 知识库重建失败")
            return False


def main():
    """主函数"""
    print("🚀 本地向量知识库启动器")
    print("=" * 60)
    
    # 创建管理器
    manager = KnowledgeBaseManager()
    
    # 检查docs目录
    if not manager.check_docs_directory():
        print("\n💡 请将文档放入docs目录后重新运行")
        input("按回车键退出...")
        return
    
    # 构建知识库
    if not manager.build_knowledge_base():
        print("\n❌ 知识库构建失败")
        input("按回车键退出...")
        return
    
    # 启动Web界面
    manager.start_web_interface()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 程序已退出")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        input("按回车键退出...")
