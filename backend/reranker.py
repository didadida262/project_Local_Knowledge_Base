#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重排模型
使用BAAI/bge-reranker-large对搜索结果进行重新排序
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import List, Dict, Any
import numpy as np


class Reranker:
    """重排模型类"""
    
    def __init__(self, model_name: str = "BAAI/bge-reranker-large"):
        """
        初始化重排模型
        
        Args:
            model_name: 重排模型名称
        """
        self.model_name = model_name
        print(f"🔄 加载重排模型: {model_name}")
        
        # 加载tokenizer和模型
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        # 设置设备
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        
        print(f"✅ 重排模型加载完成，使用设备: {self.device}")
    
    def rerank(self, query: str, documents: List[Dict[str, Any]], top_k: int = None) -> List[Dict[str, Any]]:
        """
        对搜索结果进行重新排序
        
        Args:
            query: 查询文本
            documents: 文档列表
            top_k: 返回结果数量
            
        Returns:
            重新排序后的文档列表
        """
        if not documents:
            return []
        
        # 准备输入数据
        pairs = []
        for doc in documents:
            pairs.append([query, doc['text']])
        
        # 批量计算相关性分数
        scores = self._compute_scores(pairs)
        
        # 添加重排分数到文档
        for i, doc in enumerate(documents):
            doc['rerank_score'] = float(scores[i])
        
        # 按重排分数排序
        reranked_docs = sorted(documents, key=lambda x: x['rerank_score'], reverse=True)
        
        # 返回top_k结果
        if top_k is not None:
            return reranked_docs[:top_k]
        
        return reranked_docs
    
    def _compute_scores(self, pairs: List[List[str]]) -> np.ndarray:
        """
        计算查询-文档对的相关性分数
        
        Args:
            pairs: 查询-文档对列表
            
        Returns:
            相关性分数数组
        """
        # 批量编码
        inputs = self.tokenizer(
            pairs,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors='pt'
        )
        
        # 移动到设备
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # 计算分数
        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = torch.sigmoid(outputs.logits).squeeze().cpu().numpy()
        
        return scores
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            'model_name': self.model_name,
            'device': str(self.device),
            'max_length': 512
        }
