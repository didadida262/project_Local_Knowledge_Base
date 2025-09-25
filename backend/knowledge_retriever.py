#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识检索器
集成Ollama大语言模型进行智能问答
"""

import requests
import json
from typing import List, Dict, Any
from .vector_knowledge_base import VectorKnowledgeBase


class KnowledgeRetriever:
    """知识检索器类"""
    
    def __init__(self, knowledge_base: VectorKnowledgeBase, ollama_url: str = "http://localhost:11434", ollama_model: str = "gemma3:4b"):
        """
        初始化知识检索器
        
        Args:
            knowledge_base: 向量知识库实例
            ollama_url: Ollama服务地址
            ollama_model: Ollama模型名称
        """
        self.kb = knowledge_base
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model
    
    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        搜索相关文档
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            
        Returns:
            搜索结果列表
        """
        return self.kb.search(query, top_k)
    
    def ask_question(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        基于知识库进行问答
        
        Args:
            question: 用户问题
            top_k: 检索相关文档数量
            
        Returns:
            问答结果
        """
        # 1. 检索相关文档
        search_results = self.search(question, top_k)
        
        if not search_results:
            return {
                'question': question,
                'answer': '抱歉，我在知识库中没有找到相关信息。',
                'sources': [],
                'confidence': 0.0
            }
        
        # 2. 构建上下文
        context = self._build_context(search_results)
        
        # 3. 调用Ollama生成答案
        answer = self._generate_answer(question, context)
        
        # 4. 计算置信度
        confidence = self._calculate_confidence(search_results)
        
        return {
            'question': question,
            'answer': answer,
            'sources': search_results,
            'confidence': confidence
        }
    
    def _build_context(self, search_results: List[Dict[str, Any]]) -> str:
        """构建上下文"""
        context_parts = []
        
        for i, result in enumerate(search_results, 1):
            context_parts.append(f"文档 {i}: {result['file_name']}")
            context_parts.append(f"内容: {result['text']}")
            context_parts.append(f"相似度: {result['similarity']:.3f}")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def _generate_answer(self, question: str, context: str) -> str:
        """使用Ollama生成答案"""
        prompt = f"""基于以下文档内容回答问题。请根据提供的文档内容给出准确、详细的答案。如果文档中没有相关信息，请明确说明。

文档内容：
{context}

问题：{question}

请基于上述文档内容回答问题："""

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 1000
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '抱歉，无法生成答案。')
            else:
                return f"Ollama服务错误: {response.status_code} - {response.text}"
                
        except requests.exceptions.ConnectionError:
            return "无法连接到Ollama服务，请确保Ollama正在运行。"
        except requests.exceptions.Timeout:
            return "Ollama服务响应超时，请稍后重试。"
        except Exception as e:
            return f"生成答案时发生错误: {str(e)}"
    
    def _calculate_confidence(self, search_results: List[Dict[str, Any]]) -> float:
        """计算答案置信度"""
        if not search_results:
            return 0.0
        
        # 基于最高相似度计算置信度
        max_similarity = max(result['similarity'] for result in search_results)
        
        # 将相似度转换为置信度 (0-1)
        confidence = min(max_similarity, 1.0)
        
        return confidence
    
    def get_ollama_models(self) -> List[str]:
        """获取可用的Ollama模型列表"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            else:
                return []
        except:
            return []
    
    def check_ollama_connection(self) -> bool:
        """检查Ollama连接状态"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
