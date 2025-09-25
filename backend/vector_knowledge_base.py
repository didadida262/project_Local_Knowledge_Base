#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量知识库
使用Sentence Transformers和FAISS实现向量化存储和检索
"""

import os
import json
import pickle
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
import faiss
from .document_processor import DocumentProcessor


class VectorKnowledgeBase:
    """向量知识库类"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", storage_dir: str = "./knowledge_base"):
        """
        初始化向量知识库
        
        Args:
            model_name: 句子转换模型名称
            storage_dir: 存储目录
        """
        self.model_name = model_name
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        # 初始化模型
        print(f"🔄 加载模型: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        # 初始化FAISS索引
        self.index = faiss.IndexFlatIP(self.dimension)  # 内积相似度
        self.documents = []
        self.chunks = []
        
        # 加载已存在的知识库
        self._load_knowledge_base()
    
    def add_document(self, file_path: str) -> Dict[str, Any]:
        """
        添加单个文档到知识库
        
        Args:
            file_path: 文档路径
            
        Returns:
            处理结果
        """
        try:
            processor = DocumentProcessor()
            doc_info = processor.process_document(file_path)
            
            # 生成向量
            embeddings = self.model.encode(doc_info['chunks'])
            
            # 添加到FAISS索引
            self.index.add(embeddings.astype('float32'))
            
            # 保存文档信息
            doc_id = len(self.documents)
            doc_info['doc_id'] = doc_id
            doc_info['chunk_start'] = len(self.chunks)
            doc_info['chunk_end'] = len(self.chunks) + len(doc_info['chunks'])
            
            self.documents.append(doc_info)
            
            # 保存文本块
            for i, chunk in enumerate(doc_info['chunks']):
                self.chunks.append({
                    'doc_id': doc_id,
                    'chunk_id': i,
                    'text': chunk,
                    'embedding': embeddings[i].tolist()
                })
            
            print(f"✅ 文档已添加: {doc_info['file_name']} ({doc_info['chunk_count']} 块)")
            return doc_info
            
        except Exception as e:
            print(f"❌ 添加文档失败: {file_path} - {str(e)}")
            raise
    
    def add_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """
        添加目录中的所有文档
        
        Args:
            directory_path: 目录路径
            
        Returns:
            处理结果列表
        """
        processor = DocumentProcessor()
        documents = processor.process_directory(directory_path)
        
        results = []
        for doc_info in documents:
            try:
                # 生成向量
                embeddings = self.model.encode(doc_info['chunks'])
                
                # 添加到FAISS索引
                self.index.add(embeddings.astype('float32'))
                
                # 保存文档信息
                doc_id = len(self.documents)
                doc_info['doc_id'] = doc_id
                doc_info['chunk_start'] = len(self.chunks)
                doc_info['chunk_end'] = len(self.chunks) + len(doc_info['chunks'])
                
                self.documents.append(doc_info)
                
                # 保存文本块
                for i, chunk in enumerate(doc_info['chunks']):
                    self.chunks.append({
                        'doc_id': doc_id,
                        'chunk_id': i,
                        'text': chunk,
                        'embedding': embeddings[i].tolist()
                    })
                
                results.append(doc_info)
                print(f"✅ 文档已添加: {doc_info['file_name']} ({doc_info['chunk_count']} 块)")
                
            except Exception as e:
                print(f"❌ 添加文档失败: {doc_info['file_name']} - {str(e)}")
        
        return results
    
    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        搜索相关文档
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            
        Returns:
            搜索结果列表
        """
        if len(self.chunks) == 0:
            return []
        
        # 生成查询向量
        query_embedding = self.model.encode([query])
        
        # 搜索相似向量
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            # 确保索引是Python int类型
            idx = int(idx)
            if idx < len(self.chunks):
                chunk = self.chunks[idx]
                doc = self.documents[chunk['doc_id']]
                
                results.append({
                    'chunk_id': int(idx),
                    'doc_id': int(chunk['doc_id']),
                    'file_path': str(doc['file_path']),
                    'file_name': str(doc['file_name']),
                    'text': str(chunk['text']),
                    'similarity': float(score),
                    'chunk_index': int(chunk['chunk_id'])
                })
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """获取知识库统计信息"""
        total_chunks = len(self.chunks)
        total_documents = len(self.documents)
        unique_files = len(set(doc['file_path'] for doc in self.documents))
        
        return {
            'total_vectors': int(total_chunks),
            'total_documents': int(total_documents),
            'unique_files': int(unique_files),
            'model_name': str(self.model_name),
            'dimension': int(self.dimension)
        }
    
    def get_documents(self) -> List[Dict[str, Any]]:
        """获取所有文档信息"""
        return [
            {
                'file_path': str(doc['file_path']),
                'file_name': str(doc['file_name']),
                'chunk_count': int(doc['chunk_count']),
                'word_count': int(doc['word_count']),
                'file_size': int(doc['file_size'])
            }
            for doc in self.documents
        ]
    
    def save_knowledge_base(self):
        """保存知识库到磁盘"""
        # 保存FAISS索引
        faiss.write_index(self.index, str(self.storage_dir / "faiss_index.bin"))
        
        # 保存文档信息
        with open(self.storage_dir / "documents.json", 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)
        
        # 保存文本块
        with open(self.storage_dir / "chunks.json", 'w', encoding='utf-8') as f:
            json.dump(self.chunks, f, ensure_ascii=False, indent=2)
        
        # 保存配置
        config = {
            'model_name': self.model_name,
            'dimension': self.dimension,
            'total_documents': len(self.documents),
            'total_chunks': len(self.chunks)
        }
        with open(self.storage_dir / "config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"💾 知识库已保存到: {self.storage_dir}")
    
    def _load_knowledge_base(self):
        """从磁盘加载知识库"""
        config_file = self.storage_dir / "config.json"
        if not config_file.exists():
            print("📝 创建新的知识库")
            return
        
        try:
            # 加载配置
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 加载FAISS索引
            index_file = self.storage_dir / "faiss_index.bin"
            if index_file.exists():
                self.index = faiss.read_index(str(index_file))
            
            # 加载文档信息
            docs_file = self.storage_dir / "documents.json"
            if docs_file.exists():
                with open(docs_file, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
            
            # 加载文本块
            chunks_file = self.storage_dir / "chunks.json"
            if chunks_file.exists():
                with open(chunks_file, 'r', encoding='utf-8') as f:
                    self.chunks = json.load(f)
            
            print(f"📚 知识库已加载: {config['total_documents']} 文档, {config['total_chunks']} 块")
            
        except Exception as e:
            print(f"⚠️ 加载知识库失败: {str(e)}")
            print("📝 将创建新的知识库")
    
    def clear_knowledge_base(self):
        """清空知识库"""
        self.index = faiss.IndexFlatIP(self.dimension)
        self.documents = []
        self.chunks = []
        
        # 删除存储文件
        for file in self.storage_dir.glob("*"):
            file.unlink()
        
        print("🗑️ 知识库已清空")
