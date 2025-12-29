#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识检索器
集成Ollama大语言模型进行智能问答
"""

import requests
import json
import time
from typing import List, Dict, Any
from vector_knowledge_base import VectorKnowledgeBase


class KnowledgeRetriever:
    """知识检索器类"""
    
    def __init__(self, knowledge_base: VectorKnowledgeBase, ollama_url: str = "http://localhost:11434", ollama_model: str = "gemma2:2b"):
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

        # 添加重试机制
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 尝试调用Ollama (第{attempt + 1}次)...")
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
                    timeout=60  # 增加超时时间
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Ollama调用成功")
                    return result.get('response', '抱歉，无法生成答案。')
                else:
                    error_text = response.text
                    print(f"⚠️ Ollama返回错误: {response.status_code}")
                    
                    # 检查是否是模型不存在的错误
                    if "model" in error_text.lower() and ("not found" in error_text.lower() or "does not exist" in error_text.lower()):
                        error_msg = f"""
❌ 错误: Ollama模型 '{self.ollama_model}' 未找到或未下载

解决方案:
1. 检查模型是否已安装: ollama list
2. 如果未安装，运行: ollama pull {self.ollama_model}
3. 安装完成后重新启动服务

当前请求的模型: {self.ollama_model}
"""
                        print(error_msg)
                        return f"错误: 模型 {self.ollama_model} 未安装，请运行 'ollama pull {self.ollama_model}' 安装模型"
                    
                    if attempt < max_retries - 1:
                        print(f"🔄 等待2秒后重试...")
                        time.sleep(2)
                        continue
                    return f"Ollama服务错误: {response.status_code} - {error_text}"
                    
            except requests.exceptions.ConnectionError as e:
                print(f"❌ 连接错误: {e}")
                if attempt < max_retries - 1:
                    print(f"🔄 等待3秒后重试...")
                    time.sleep(3)
                    continue
                error_msg = """
❌ 错误: 无法连接到Ollama服务

解决方案:
1. 检查Ollama服务是否运行: ollama list
2. 如果未运行，启动Ollama: ollama serve
3. 确保Ollama服务地址正确: http://localhost:11434
4. 如果未安装Ollama，访问 https://ollama.ai 下载安装

注意: 即使没有Ollama，搜索功能仍然可以正常使用
"""
                print(error_msg)
                return "无法连接到Ollama服务，请确保Ollama正在运行。"
            except requests.exceptions.Timeout as e:
                print(f"⏰ 超时错误: {e}")
                if attempt < max_retries - 1:
                    print(f"🔄 等待2秒后重试...")
                    time.sleep(2)
                    continue
                return "Ollama服务响应超时，请稍后重试。"
            except Exception as e:
                print(f"❌ 未知错误: {e}")
                if attempt < max_retries - 1:
                    print(f"🔄 等待2秒后重试...")
                    time.sleep(2)
                    continue
                return f"生成答案时发生错误: {str(e)}"
        
        return "多次重试失败，请检查Ollama服务状态。"
    
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
