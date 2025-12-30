#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档处理器
支持多种格式文档的解析和内容提取
"""

import os
import re
import jieba
from pathlib import Path
from typing import List, Dict, Any
import PyPDF2
from docx import Document
import markdown
from bs4 import BeautifulSoup


class DocumentProcessor:
    """文档处理器类"""
    
    def __init__(self):
        self.supported_formats = {
            '.txt': self._process_txt,
            '.md': self._process_markdown,
            '.pdf': self._process_pdf,
            '.docx': self._process_docx,
            '.html': self._process_html,
            '.htm': self._process_html
        }
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        处理单个文档
        
        Args:
            file_path: 文档路径
            
        Returns:
            包含文档信息的字典
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        file_ext = file_path.suffix.lower()
        if file_ext not in self.supported_formats:
            raise ValueError(f"不支持的文件格式: {file_ext}")
        
        try:
            # 提取文档内容
            content = self.supported_formats[file_ext](file_path)
            
            # 清理和预处理文本
            cleaned_content = self._clean_text(content)
            
            # 分块处理
            chunks = self._chunk_text(cleaned_content)
            
            return {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'file_size': file_path.stat().st_size,
                'content': cleaned_content,
                'chunks': chunks,
                'chunk_count': len(chunks),
                'word_count': len(cleaned_content.split())
            }
            
        except Exception as e:
            raise Exception(f"处理文档失败 {file_path}: {str(e)}")
    
    def _process_txt(self, file_path: Path) -> str:
        """处理TXT文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _process_markdown(self, file_path: Path) -> str:
        """处理Markdown文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 移除YAML front matter（如果存在，常见于Jekyll、Hugo等静态站点）
        if md_content.startswith('---'):
            parts = md_content.split('---', 2)
            if len(parts) >= 3:
                md_content = parts[2].strip()
        
        # 转换为HTML再提取文本
        # 尝试使用扩展支持代码块、表格等（如果可用）
        try:
            html = markdown.markdown(
                md_content,
                extensions=['fenced_code', 'tables']
            )
        except:
            # 如果扩展不可用，使用基本转换
            html = markdown.markdown(md_content)
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取文本内容
        # 保留代码块内容（代码块通常包含重要信息）
        for code in soup.find_all(['code', 'pre']):
            code_text = code.get_text()
            if code_text and len(code_text.strip()) > 0:
                # 在代码块前后添加标记，便于识别
                code.string = f" [代码块: {code_text.strip()}] "
        
        # 提取所有文本
        text = soup.get_text()
        
        # 清理多余的空白，但保留段落结构
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        return '\n'.join(lines)
    
    def _process_pdf(self, file_path: Path) -> str:
        """处理PDF文件"""
        content = ""
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                content += page.extract_text() + "\n"
        return content
    
    def _process_docx(self, file_path: Path) -> str:
        """处理Word文档"""
        doc = Document(file_path)
        content = ""
        for paragraph in doc.paragraphs:
            content += paragraph.text + "\n"
        return content
    
    def _process_html(self, file_path: Path) -> str:
        """处理HTML文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text()
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 移除多余的空白字符（保留换行用于分段）
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # 最多保留两个连续换行
        
        # 移除特殊字符，但保留中文、英文、数字和基本标点
        # 保留：中文、英文、数字、空格、换行、基本标点符号
        text = re.sub(r'[^\w\s\u4e00-\u9fff，。！？；：、""''（）【】《》\n]', ' ', text)
        
        # 清理每行的多余空格，但保留段落结构
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            cleaned_line = ' '.join(line.split())
            if cleaned_line:  # 保留非空行
                cleaned_lines.append(cleaned_line)
        
        text = '\n'.join(cleaned_lines)
        
        return text.strip()
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        将文本分块
        
        Args:
            text: 输入文本
            chunk_size: 每块大小
            overlap: 重叠大小
            
        Returns:
            文本块列表
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # 如果不是最后一块，尝试在句号处分割
            if end < len(text):
                # 寻找最近的句号
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
    
    def process_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """
        处理目录中的所有文档
        
        Args:
            directory_path: 目录路径
            
        Returns:
            文档信息列表
        """
        directory = Path(directory_path)
        if not directory.exists():
            raise FileNotFoundError(f"目录不存在: {directory_path}")
        
        documents = []
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                try:
                    doc_info = self.process_document(str(file_path))
                    documents.append(doc_info)
                    print(f"✅ 处理完成: {file_path.name}")
                except Exception as e:
                    print(f"❌ 处理失败: {file_path.name} - {str(e)}")
        
        return documents
