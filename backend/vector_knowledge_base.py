#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地向量知识库实现
支持文档向量化、存储和检索
"""

import os
import json
import pickle
import numpy as np
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import hashlib
import time
from datetime import datetime

# 文档处理
import PyPDF2
import docx
import markdown
from bs4 import BeautifulSoup

# 向量化
from sentence_transformers import SentenceTransformer
import faiss

# 文本处理
import re
import jieba
from collections import Counter


class DocumentProcessor:
    """文档处理器"""
    
    def __init__(self):
        self.supported_extensions = {'.txt', '.md', '.pdf', '.docx', '.html', '.htm'}
        
    def extract_text_from_file(self, file_path: str) -> str:
        """从文件中提取文本"""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        extension = file_path.suffix.lower()
        
        try:
            if extension == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif extension == '.md':
                with open(file_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                    html = markdown.markdown(md_content)
                    soup = BeautifulSoup(html, 'html.parser')
                    return soup.get_text()
            
            elif extension == '.pdf':
                text = ""
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                return text
            
            elif extension == '.docx':
                doc = docx.Document(file_path)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text
            
            elif extension in ['.html', '.htm']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    return soup.get_text()
            
            else:
                raise ValueError(f"不支持的文件格式: {extension}")
                
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
            return ""
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """将文本分块"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # 尝试在句号、问号、感叹号处分割
            if end < len(text):
                for i in range(end, max(start + chunk_size // 2, end - 100), -1):
                    if text[i] in '。！？\n':
                        end = i + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def preprocess_text(self, text: str) -> str:
        """预处理文本"""
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符但保留中文、英文、数字和基本标点
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:()（）]', '', text)
        return text.strip()


class VectorKnowledgeBase:
    """向量知识库"""
    
    def __init__(self, 
                 model_name: str = "all-MiniLM-L6-v2",
                 dimension: int = 384,
                 storage_dir: str = "./knowledge_base"):
        """
        初始化向量知识库
        
        Args:
            model_name: 句子嵌入模型名称
            dimension: 向量维度
            storage_dir: 存储目录
        """
        self.dimension = dimension
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        # 初始化模型
        print(f"加载嵌入模型: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        
        # 初始化FAISS索引
        self.index = faiss.IndexFlatIP(dimension)  # 使用内积相似度
        self.documents = []  # 存储文档信息
        self.metadata = []   # 存储元数据
        
        # 文档处理器
        self.doc_processor = DocumentProcessor()
        
        # 加载现有数据
        self.load_knowledge_base()
    
    def add_document(self, file_path: str, metadata: Optional[Dict] = None) -> bool:
        """添加文档到知识库"""
        try:
            print(f"处理文档: {file_path}")
            
            # 提取文本
            text = self.doc_processor.extract_text_from_file(file_path)
            if not text:
                print(f"无法从文件中提取文本: {file_path}")
                return False
            
            # 预处理文本
            text = self.doc_processor.preprocess_text(text)
            
            # 分块
            chunks = self.doc_processor.chunk_text(text)
            
            # 为每个块生成嵌入
            embeddings = self.embedding_model.encode(chunks)
            
            # 添加到索引
            self.index.add(embeddings.astype('float32'))
            
            # 存储文档信息
            file_hash = hashlib.md5(str(file_path).encode()).hexdigest()
            for i, chunk in enumerate(chunks):
                doc_info = {
                    'file_path': str(file_path),
                    'file_hash': file_hash,
                    'chunk_index': i,
                    'chunk_text': chunk,
                    'timestamp': datetime.now().isoformat(),
                    'metadata': metadata or {}
                }
                self.documents.append(doc_info)
                self.metadata.append(doc_info)
            
            print(f"成功添加文档: {file_path} ({len(chunks)} 个块)")
            return True
            
        except Exception as e:
            print(f"添加文档失败 {file_path}: {e}")
            return False
    
    def add_directory(self, directory_path: str, recursive: bool = True) -> int:
        """添加目录中的所有文档"""
        directory_path = Path(directory_path)
        if not directory_path.exists():
            print(f"目录不存在: {directory_path}")
            return 0
        
        added_count = 0
        pattern = "**/*" if recursive else "*"
        
        for file_path in directory_path.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in self.doc_processor.supported_extensions:
                if self.add_document(str(file_path)):
                    added_count += 1
        
        print(f"总共添加了 {added_count} 个文档")
        return added_count
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """搜索相关文档"""
        if self.index.ntotal == 0:
            return []
        
        # 生成查询向量
        query_embedding = self.embedding_model.encode([query])
        
        # 搜索
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.documents):
                result = self.documents[idx].copy()
                result['similarity_score'] = float(score)
                results.append(result)
        
        return results
    
    def save_knowledge_base(self):
        """保存知识库"""
        try:
            # 保存FAISS索引
            faiss.write_index(self.index, str(self.storage_dir / "faiss_index.bin"))
            
            # 保存文档信息
            with open(self.storage_dir / "documents.json", 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
            
            # 保存元数据
            with open(self.storage_dir / "metadata.json", 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            
            print(f"知识库已保存到: {self.storage_dir}")
            return True
            
        except Exception as e:
            print(f"保存知识库失败: {e}")
            return False
    
    def load_knowledge_base(self):
        """加载知识库"""
        try:
            # 加载FAISS索引
            index_path = self.storage_dir / "faiss_index.bin"
            if index_path.exists():
                self.index = faiss.read_index(str(index_path))
                print(f"加载FAISS索引: {self.index.ntotal} 个向量")
            
            # 加载文档信息
            docs_path = self.storage_dir / "documents.json"
            if docs_path.exists():
                with open(docs_path, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
                print(f"加载文档信息: {len(self.documents)} 个文档块")
            
            # 加载元数据
            meta_path = self.storage_dir / "metadata.json"
            if meta_path.exists():
                with open(meta_path, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
                print(f"加载元数据: {len(self.metadata)} 条记录")
            
            return True
            
        except Exception as e:
            print(f"加载知识库失败: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """获取知识库统计信息"""
        return {
            'total_vectors': self.index.ntotal if hasattr(self.index, 'ntotal') else 0,
            'total_documents': len(self.documents),
            'unique_files': len(set(doc['file_path'] for doc in self.documents)),
            'storage_dir': str(self.storage_dir),
            'dimension': self.dimension
        }
    
    def clear_knowledge_base(self):
        """清空知识库"""
        self.index = faiss.IndexFlatIP(self.dimension)
        self.documents = []
        self.metadata = []
        print("知识库已清空")
