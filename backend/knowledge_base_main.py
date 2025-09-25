#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地向量知识库主程序
集成文档处理、向量化、检索和问答功能
"""

import os
import sys
import argparse
from pathlib import Path
from vector_knowledge_base import VectorKnowledgeBase
from knowledge_retriever import KnowledgeRetriever


class KnowledgeBaseManager:
    """知识库管理器"""
    
    def __init__(self, storage_dir: str = "./knowledge_base"):
        self.storage_dir = storage_dir
        self.kb = VectorKnowledgeBase(storage_dir=storage_dir)
        self.retriever = KnowledgeRetriever(self.kb)
    
    def add_documents(self, path: str, recursive: bool = True) -> int:
        """添加文档到知识库"""
        path = Path(path)
        
        if path.is_file():
            print(f"添加单个文件: {path}")
            success = self.kb.add_document(str(path))
            return 1 if success else 0
        elif path.is_dir():
            print(f"添加目录: {path} (递归: {recursive})")
            return self.kb.add_directory(str(path), recursive)
        else:
            print(f"路径不存在: {path}")
            return 0
    
    def build_knowledge_base(self, documents_dir: str = "docs", recursive: bool = True):
        """构建知识库"""
        print("=" * 60)
        print("构建本地向量知识库")
        print("=" * 60)
        print(f"默认语料库目录: {documents_dir}")
        print("支持用户上传本地文档")
        print("=" * 60)
        
        # 添加文档
        added_count = self.add_documents(documents_dir, recursive)
        
        if added_count == 0:
            print("没有找到可处理的文档")
            return False
        
        print(f"成功添加 {added_count} 个文档")
        
        # 保存知识库
        if self.kb.save_knowledge_base():
            print("知识库构建完成并已保存")
            
            # 显示统计信息
            stats = self.kb.get_stats()
            print(f"\n知识库统计:")
            print(f"- 总向量数: {stats['total_vectors']}")
            print(f"- 总文档数: {stats['total_documents']}")
            print(f"- 唯一文件数: {stats['unique_files']}")
            
            return True
        else:
            print("保存知识库失败")
            return False
    
    def interactive_mode(self):
        """交互式模式"""
        print("=" * 60)
        print("本地向量知识库 - 交互式模式")
        print("=" * 60)
        
        # 检查知识库状态
        stats = self.kb.get_stats()
        if stats['total_vectors'] == 0:
            print("知识库为空，请先添加文档")
            return
        
        print(f"知识库状态: {stats['total_vectors']} 个向量, {stats['unique_files']} 个文件")
        print("\n可用命令:")
        print("- 直接输入问题进行问答")
        print("- 'search:关键词' - 搜索相关文档")
        print("- 'summary:文件路径' - 获取文档摘要")
        print("- 'stats' - 查看知识库统计")
        print("- 'add:路径' - 添加新文档到知识库")
        print("- 'upload:路径' - 上传本地文档")
        print("- 'quit' - 退出")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n请输入: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("再见！")
                    break
                elif not user_input:
                    continue
                elif user_input.lower() == 'stats':
                    stats = self.kb.get_stats()
                    print(f"\n知识库统计:")
                    print(f"- 总向量数: {stats['total_vectors']}")
                    print(f"- 总文档数: {stats['total_documents']}")
                    print(f"- 唯一文件数: {stats['unique_files']}")
                    print(f"- 存储目录: {stats['storage_dir']}")
                    continue
                elif user_input.startswith('add:'):
                    path = user_input[4:].strip()
                    print(f"\n添加用户文档: {path}")
                    count = self.add_documents(path)
                    if count > 0:
                        self.kb.save_knowledge_base()
                        print(f"成功添加 {count} 个用户文档")
                    else:
                        print("添加失败或没有找到文档")
                    continue
                elif user_input.startswith('upload:'):
                    # 支持用户上传本地文档
                    path = user_input[7:].strip()
                    print(f"\n上传本地文档: {path}")
                    if os.path.exists(path):
                        count = self.add_documents(path)
                        if count > 0:
                            self.kb.save_knowledge_base()
                            print(f"成功上传 {count} 个文档")
                        else:
                            print("上传失败或没有找到文档")
                    else:
                        print("文件或目录不存在")
                    continue
                elif user_input.startswith('search:'):
                    query = user_input[7:].strip()
                    print(f"\n搜索: {query}")
                    results = self.retriever.search_similar_documents(query)
                    for i, result in enumerate(results[:5], 1):
                        print(f"{i}. {result['file_path']} (相似度: {result['max_similarity']:.3f})")
                        print(f"   预览: {result['preview']}...")
                        print()
                    continue
                elif user_input.startswith('summary:'):
                    file_path = user_input[8:].strip()
                    print(f"\n获取文档摘要: {file_path}")
                    summary = self.retriever.get_document_summary(file_path)
                    if 'error' in summary:
                        print(f"错误: {summary['error']}")
                    else:
                        print(f"文档: {summary['file_path']}")
                        print(f"块数: {summary['chunk_count']}")
                        print(f"摘要: {summary['summary']}")
                    continue
                
                # 普通问答
                print(f"\n问题: {user_input}")
                result = self.retriever.ask_question(user_input)
                
                print(f"\n回答: {result['answer']}")
                
                if result['sources']:
                    print(f"\n参考文档:")
                    for i, source in enumerate(result['sources'][:3], 1):
                        print(f"{i}. {source['file_path']} (相似度: {source['similarity_score']:.3f})")
                        print(f"   预览: {source['chunk_preview']}")
                        print()
                
            except KeyboardInterrupt:
                print("\n\n程序被中断，再见！")
                break
            except Exception as e:
                print(f"\n发生错误: {e}")
    
    def query_mode(self, question: str):
        """查询模式"""
        result = self.retriever.ask_question(question)
        
        print(f"问题: {result['question']}")
        print(f"回答: {result['answer']}")
        
        if result['sources']:
            print(f"\n参考文档:")
            for i, source in enumerate(result['sources'], 1):
                print(f"{i}. {source['file_path']} (相似度: {source['similarity_score']:.3f})")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="本地向量知识库")
    parser.add_argument("--mode", choices=["build", "interactive", "query"], 
                       default="interactive", help="运行模式")
    parser.add_argument("--documents", default="docs", 
                       help="文档目录路径 (默认: docs目录)")
    parser.add_argument("--recursive", action="store_true", 
                       help="递归处理子目录")
    parser.add_argument("--question", help="查询问题 (query模式)")
    parser.add_argument("--storage", default="./knowledge_base", 
                       help="知识库存储目录")
    
    args = parser.parse_args()
    
    # 初始化管理器
    manager = KnowledgeBaseManager(storage_dir=args.storage)
    
    if args.mode == "build":
        # 构建模式
        success = manager.build_knowledge_base(args.documents, args.recursive)
        if not success:
            sys.exit(1)
    
    elif args.mode == "query":
        # 查询模式
        if not args.question:
            print("错误: 查询模式需要提供 --question 参数")
            sys.exit(1)
        
        # 检查知识库
        stats = manager.kb.get_stats()
        if stats['total_vectors'] == 0:
            print("错误: 知识库为空，请先构建知识库")
            sys.exit(1)
        
        manager.query_mode(args.question)
    
    else:
        # 交互模式
        manager.interactive_mode()


if __name__ == "__main__":
    main()
