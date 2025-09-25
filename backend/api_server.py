#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API服务器
提供RESTful API接口供React前端调用
"""

import os
import sys
import json
import time
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vector_knowledge_base import VectorKnowledgeBase
from knowledge_retriever import KnowledgeRetriever

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 全局变量
knowledge_base = None
retriever = None

def init_knowledge_base(kb_dir: str = "./knowledge_base"):
    """初始化知识库"""
    global knowledge_base, retriever
    
    try:
        print("🔄 正在初始化知识库...")
        knowledge_base = VectorKnowledgeBase(storage_dir=kb_dir)
        retriever = KnowledgeRetriever(knowledge_base)
        print("✅ 知识库初始化完成")
        return True
    except Exception as e:
        print(f"❌ 知识库初始化失败: {e}")
        return False

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取知识库统计信息"""
    try:
        if not knowledge_base:
            return jsonify({'error': '知识库未初始化'}), 500
        
        stats = knowledge_base.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_documents():
    """搜索文档"""
    try:
        if not knowledge_base:
            return jsonify({'error': '知识库未初始化'}), 500
        
        data = request.get_json()
        query = data.get('query', '')
        top_k = data.get('top_k', 10)
        
        if not query:
            return jsonify({'error': '查询内容不能为空'}), 400
        
        results = knowledge_base.search(query, top_k)
        
        # 格式化结果
        formatted_results = []
        for result in results:
            formatted_results.append({
                'file_path': result['file_path'],
                'max_similarity': result['similarity_score'],
                'preview': result['chunk_text'][:200] + '...' if len(result['chunk_text']) > 200 else result['chunk_text']
            })
        
        return jsonify({'results': formatted_results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """智能问答"""
    try:
        if not retriever:
            return jsonify({'error': '检索器未初始化'}), 500
        
        data = request.get_json()
        question = data.get('question', '')
        top_k = data.get('top_k', 5)
        
        if not question:
            return jsonify({'error': '问题不能为空'}), 400
        
        result = retriever.ask_question(question, top_k)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/documents', methods=['GET'])
def get_documents():
    """获取文档列表"""
    try:
        if not knowledge_base:
            return jsonify({'error': '知识库未初始化'}), 500
        
        # 从知识库获取文档信息
        documents = []
        for doc in knowledge_base.documents:
            file_path = doc['file_path']
            if not any(d['file_path'] == file_path for d in documents):
                documents.append({
                    'file_path': file_path,
                    'chunk_count': len([d for d in knowledge_base.documents if d['file_path'] == file_path]),
                    'last_modified': doc.get('timestamp', None)
                })
        
        return jsonify({'documents': documents})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload_document', methods=['POST'])
def upload_document():
    """上传文档"""
    try:
        if not knowledge_base:
            return jsonify({'error': '知识库未初始化'}), 500
        
        if 'file' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        # 保存文件到docs目录
        docs_dir = Path('docs')
        docs_dir.mkdir(exist_ok=True)
        
        file_path = docs_dir / file.filename
        file.save(file_path)
        
        # 添加到知识库
        success = knowledge_base.add_document(str(file_path))
        if success:
            knowledge_base.save_knowledge_base()
            return jsonify({
                'success': True,
                'message': f'文档 {file.filename} 上传成功'
            })
        else:
            return jsonify({'error': '文档处理失败'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add_document', methods=['POST'])
def add_document():
    """添加本地文档"""
    try:
        if not knowledge_base:
            return jsonify({'error': '知识库未初始化'}), 500
        
        data = request.get_json()
        file_path = data.get('file_path', '')
        
        if not file_path:
            return jsonify({'error': '文件路径不能为空'}), 400
        
        file_path = Path(file_path)
        if not file_path.exists():
            return jsonify({'error': '文件不存在'}), 400
        
        # 添加到知识库
        success = knowledge_base.add_document(str(file_path))
        if success:
            knowledge_base.save_knowledge_base()
            return jsonify({
                'success': True,
                'message': f'文档 {file_path.name} 添加成功'
            })
        else:
            return jsonify({'error': '文档处理失败'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'ok', 'message': 'API服务器运行正常'})

if __name__ == '__main__':
    print("🚀 启动API服务器...")
    
    # 初始化知识库
    if not init_knowledge_base():
        print("❌ 知识库初始化失败，服务器启动失败")
        sys.exit(1)
    
    print("✅ API服务器启动成功")
    print("📱 API地址: http://127.0.0.1:5000")
    print("💡 提示: 按 Ctrl+C 停止服务器")
    
    # 启动Flask应用
    app.run(debug=False, host='127.0.0.1', port=5000, threaded=True)
