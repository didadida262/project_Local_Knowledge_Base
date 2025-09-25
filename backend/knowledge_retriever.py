#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识检索器
提供智能查询和检索功能
"""

import requests
import json
from typing import List, Dict, Optional
from vector_knowledge_base import VectorKnowledgeBase


class KnowledgeRetriever:
    """知识检索器"""
    
    def __init__(self, 
                 knowledge_base: VectorKnowledgeBase,
                 ollama_url: str = "http://localhost:11434",
                 ollama_model: str = "gemma3:4b"):
        """
        初始化知识检索器
        
        Args:
            knowledge_base: 向量知识库实例
            ollama_url: Ollama服务地址
            ollama_model: Ollama模型名称
        """
        self.kb = knowledge_base
        self.ollama_url = ollama_url.rstrip('/')
        self.ollama_model = ollama_model
        self.session = requests.Session()
    
    def retrieve_relevant_docs(self, query: str, top_k: int = 5) -> List[Dict]:
        """检索相关文档"""
        return self.kb.search(query, top_k)
    
    def format_context(self, docs: List[Dict], max_length: int = 2000) -> str:
        """格式化检索到的文档为上下文"""
        if not docs:
            return "没有找到相关信息。"
        
        context_parts = []
        current_length = 0
        
        for i, doc in enumerate(docs, 1):
            # 构建文档片段
            chunk_text = doc.get('chunk_text', '')
            file_path = doc.get('file_path', '未知文件')
            similarity = doc.get('similarity_score', 0)
            
            # 限制每个片段长度
            if len(chunk_text) > 300:
                chunk_text = chunk_text[:300] + "..."
            
            doc_part = f"[文档{i}] (来源: {file_path}, 相似度: {similarity:.3f})\n{chunk_text}\n"
            
            if current_length + len(doc_part) > max_length:
                break
            
            context_parts.append(doc_part)
            current_length += len(doc_part)
        
        return "\n".join(context_parts)
    
    def query_ollama(self, prompt: str, context: str = "") -> str:
        """查询Ollama模型"""
        try:
            # 构建完整的提示词
            if context:
                full_prompt = f"""基于以下上下文信息回答问题：

上下文信息：
{context}

问题：{prompt}

请基于提供的上下文信息回答问题。如果上下文中包含相关信息，请详细回答。如果上下文中没有直接相关信息，请基于你的知识回答，并说明这是基于你的通用知识。"""
            else:
                full_prompt = prompt
            
            payload = {
                "model": self.ollama_model,
                "messages": [{"role": "user", "content": full_prompt}],
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_ctx": 4096
                }
            }
            
            response = self.session.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('message', {}).get('content', '')
            else:
                return f"请求失败: HTTP {response.status_code}"
                
        except Exception as e:
            return f"查询失败: {e}"
    
    def ask_question(self, question: str, top_k: int = 5) -> Dict:
        """智能问答"""
        print(f"问题: {question}")
        print("正在检索相关文档...")
        
        # 检索相关文档
        relevant_docs = self.retrieve_relevant_docs(question, top_k)
        
        if not relevant_docs:
            return {
                'question': question,
                'answer': '抱歉，在知识库中没有找到相关信息。',
                'sources': [],
                'context': ''
            }
        
        print(f"找到 {len(relevant_docs)} 个相关文档片段")
        
        # 格式化上下文
        context = self.format_context(relevant_docs)
        
        print("正在生成回答...")
        
        # 查询模型
        answer = self.query_ollama(question, context)
        
        # 准备源文档信息
        sources = []
        for doc in relevant_docs:
            sources.append({
                'file_path': doc.get('file_path', ''),
                'similarity_score': doc.get('similarity_score', 0),
                'chunk_preview': doc.get('chunk_text', '')[:100] + '...' if len(doc.get('chunk_text', '')) > 100 else doc.get('chunk_text', '')
            })
        
        return {
            'question': question,
            'answer': answer,
            'sources': sources,
            'context': context
        }
    
    def get_document_summary(self, file_path: str) -> Dict:
        """获取文档摘要"""
        # 查找该文件的所有块
        file_chunks = [doc for doc in self.kb.documents if doc.get('file_path') == file_path]
        
        if not file_chunks:
            return {'error': '文档未找到'}
        
        # 合并所有块
        full_text = '\n'.join([chunk['chunk_text'] for chunk in file_chunks])
        
        # 生成摘要
        summary_prompt = f"请为以下文档生成一个简洁的摘要：\n\n{full_text[:1000]}..."
        summary = self.query_ollama(summary_prompt)
        
        return {
            'file_path': file_path,
            'chunk_count': len(file_chunks),
            'summary': summary,
            'full_text_preview': full_text[:500] + '...' if len(full_text) > 500 else full_text
        }
    
    def search_similar_documents(self, query: str, top_k: int = 10) -> List[Dict]:
        """搜索相似文档"""
        docs = self.retrieve_relevant_docs(query, top_k)
        
        # 按文件路径分组
        file_groups = {}
        for doc in docs:
            file_path = doc.get('file_path', '')
            if file_path not in file_groups:
                file_groups[file_path] = {
                    'file_path': file_path,
                    'max_similarity': doc.get('similarity_score', 0),
                    'chunk_count': 1,
                    'preview': doc.get('chunk_text', '')[:200]
                }
            else:
                file_groups[file_path]['chunk_count'] += 1
                file_groups[file_path]['max_similarity'] = max(
                    file_groups[file_path]['max_similarity'],
                    doc.get('similarity_score', 0)
                )
        
        # 按相似度排序
        return sorted(file_groups.values(), key=lambda x: x['max_similarity'], reverse=True)
    
    def interactive_search(self):
        """交互式搜索"""
        print("=" * 60)
        print("知识库交互式搜索")
        print("=" * 60)
        print("可用命令:")
        print("- 直接输入问题进行问答")
        print("- 输入 'search:关键词' 进行文档搜索")
        print("- 输入 'summary:文件路径' 获取文档摘要")
        print("- 输入 'stats' 查看知识库统计")
        print("- 输入 'quit' 退出")
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
                elif user_input.startswith('search:'):
                    query = user_input[7:].strip()
                    print(f"\n搜索: {query}")
                    results = self.search_similar_documents(query)
                    for i, result in enumerate(results[:5], 1):
                        print(f"{i}. {result['file_path']} (相似度: {result['max_similarity']:.3f})")
                        print(f"   预览: {result['preview']}...")
                        print()
                    continue
                elif user_input.startswith('summary:'):
                    file_path = user_input[8:].strip()
                    print(f"\n获取文档摘要: {file_path}")
                    summary = self.get_document_summary(file_path)
                    if 'error' in summary:
                        print(f"错误: {summary['error']}")
                    else:
                        print(f"文档: {summary['file_path']}")
                        print(f"块数: {summary['chunk_count']}")
                        print(f"摘要: {summary['summary']}")
                    continue
                
                # 普通问答
                result = self.ask_question(user_input)
                
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


if __name__ == "__main__":
    # 示例用法
    from vector_knowledge_base import VectorKnowledgeBase
    
    # 初始化知识库
    kb = VectorKnowledgeBase()
    
    # 初始化检索器
    retriever = KnowledgeRetriever(kb)
    
    # 开始交互式搜索
    retriever.interactive_search()
