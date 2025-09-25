#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库Web界面
提供基于Flask的Web界面
"""

from flask import Flask, render_template, request, jsonify
import os
import json
import logging
from pathlib import Path
from vector_knowledge_base import VectorKnowledgeBase
from knowledge_retriever import KnowledgeRetriever

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 全局变量
kb = None
retriever = None

# 错误处理
@app.errorhandler(400)
def bad_request(error):
    logger.warning(f"Bad request: {error}")
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(404)
def not_found(error):
    logger.warning(f"Not found: {error}")
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

def init_knowledge_base(storage_dir="./knowledge_base"):
    """初始化知识库"""
    global kb, retriever
    kb = VectorKnowledgeBase(storage_dir=storage_dir)
    retriever = KnowledgeRetriever(kb)

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    """获取知识库统计信息"""
    if not kb:
        return jsonify({'error': '知识库未初始化'})
    
    stats = kb.get_stats()
    return jsonify(stats)

@app.route('/api/search', methods=['POST'])
def search():
    """搜索文档"""
    if not retriever:
        return jsonify({'error': '检索器未初始化'})
    
    data = request.get_json()
    query = data.get('query', '')
    top_k = data.get('top_k', 5)
    
    if not query:
        return jsonify({'error': '查询不能为空'})
    
    try:
        results = retriever.search_similar_documents(query, top_k)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """问答接口"""
    if not retriever:
        return jsonify({'error': '检索器未初始化'})
    
    data = request.get_json()
    question = data.get('question', '')
    top_k = data.get('top_k', 5)
    
    if not question:
        return jsonify({'error': '问题不能为空'})
    
    try:
        result = retriever.ask_question(question, top_k)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/add_document', methods=['POST'])
def add_document():
    """添加文档"""
    if not kb:
        return jsonify({'error': '知识库未初始化'})
    
    data = request.get_json()
    file_path = data.get('file_path', '')
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': '文件不存在'})
    
    try:
        success = kb.add_document(file_path)
        if success:
            kb.save_knowledge_base()
            return jsonify({'success': True, 'message': '文档添加成功'})
        else:
            return jsonify({'error': '文档添加失败'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/upload_document', methods=['POST'])
def upload_document():
    """上传文档"""
    if not kb:
        return jsonify({'error': '知识库未初始化'})
    
    if 'file' not in request.files:
        return jsonify({'error': '没有选择文件'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'})
    
    # 检查文件类型
    allowed_extensions = {'.txt', '.md', '.pdf', '.docx', '.html', '.htm'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        return jsonify({'error': f'不支持的文件格式: {file_ext}'})
    
    try:
        # 保存上传的文件到docs目录
        upload_dir = Path('docs')
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / file.filename
        file.save(str(file_path))
        
        # 添加到知识库
        success = kb.add_document(str(file_path))
        if success:
            kb.save_knowledge_base()
            
            # 获取更新后的统计信息
            stats = kb.get_stats()
            
            return jsonify({
                'success': True, 
                'message': f'文档 {file.filename} 上传成功，知识库已更新',
                'stats': {
                    'total_vectors': stats['total_vectors'],
                    'total_documents': stats['total_documents'],
                    'unique_files': stats['unique_files']
                }
            })
        else:
            return jsonify({'error': '文档处理失败'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/documents')
def get_documents():
    """获取文档列表"""
    if not kb:
        return jsonify({'error': '知识库未初始化'})
    
    try:
        # 获取唯一文件列表
        unique_files = list(set(doc['file_path'] for doc in kb.documents))
        documents = []
        
        for file_path in unique_files:
            file_chunks = [doc for doc in kb.documents if doc['file_path'] == file_path]
            documents.append({
                'file_path': file_path,
                'chunk_count': len(file_chunks),
                'last_modified': file_chunks[0]['timestamp'] if file_chunks else None
            })
        
        return jsonify({'documents': documents})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # 创建模板目录
    template_dir = Path('templates')
    template_dir.mkdir(exist_ok=True)
    
    # 创建HTML模板
    html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>本地向量知识库</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        button {
            padding: 12px 24px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #0056b3;
        }
        .results {
            margin-top: 20px;
        }
        .result-item {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 10px;
        }
        .result-title {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        .result-content {
            color: #666;
            line-height: 1.5;
        }
        .similarity {
            color: #007bff;
            font-size: 14px;
        }
        .loading {
            text-align: center;
            color: #666;
            padding: 20px;
        }
        .error {
            color: #dc3545;
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
            padding: 10px;
            margin: 10px 0;
        }
        .stats {
            background: #e9ecef;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .tabs {
            display: flex;
            margin-bottom: 20px;
        }
        .tab {
            padding: 10px 20px;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            cursor: pointer;
            border-radius: 4px 4px 0 0;
        }
        .tab.active {
            background: white;
            border-bottom: 1px solid white;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 本地向量知识库</h1>
        
        <div class="stats" id="stats">
            <div class="loading">加载统计信息...</div>
        </div>
        
        <div class="tabs">
            <div class="tab active" onclick="switchTab('search')">🔍 搜索</div>
            <div class="tab" onclick="switchTab('ask')">❓ 问答</div>
            <div class="tab" onclick="switchTab('documents')">📄 文档</div>
        </div>
        
        <!-- 搜索标签页 -->
        <div id="search-tab" class="tab-content active">
            <div class="search-box">
                <input type="text" id="searchQuery" placeholder="输入关键词搜索相关文档...">
                <button onclick="searchDocuments()">搜索</button>
            </div>
            <div id="searchResults" class="results"></div>
        </div>
        
        <!-- 问答标签页 -->
        <div id="ask-tab" class="tab-content">
            <div class="search-box">
                <input type="text" id="askQuery" placeholder="输入问题，基于知识库内容回答...">
                <button onclick="askQuestion()">提问</button>
            </div>
            <div id="askResults" class="results"></div>
        </div>
        
        <!-- 文档标签页 -->
        <div id="documents-tab" class="tab-content">
            <div class="search-box">
                <input type="text" id="filePath" placeholder="输入文件路径...">
                <button onclick="addDocument()">添加文档</button>
            </div>
            <div style="margin: 20px 0; padding: 20px; border: 2px dashed #ddd; border-radius: 8px;">
                <h4>📁 上传本地文档</h4>
                <input type="file" id="fileUpload" accept=".txt,.md,.pdf,.docx,.html,.htm" multiple>
                <button onclick="uploadDocument()" style="margin-left: 10px;">上传到知识库</button>
                <p style="color: #666; font-size: 14px; margin-top: 10px;">
                    支持格式: TXT, MD, PDF, DOCX, HTML
                </p>
            </div>
            <div id="documentsList" class="results"></div>
        </div>
    </div>

    <script>
        // 切换标签页
        function switchTab(tabName) {
            // 隐藏所有标签页内容
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // 显示选中的标签页
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
            
            // 加载文档列表
            if (tabName === 'documents') {
                loadDocuments();
            }
        }
        
        // 加载统计信息
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                if (stats.error) {
                    document.getElementById('stats').innerHTML = 
                        `<div class="error">错误: ${stats.error}</div>`;
                    return;
                }
                
                document.getElementById('stats').innerHTML = `
                    <strong>知识库统计:</strong>
                    总向量数: ${stats.total_vectors} | 
                    总文档数: ${stats.total_documents} | 
                    唯一文件数: ${stats.unique_files}
                `;
            } catch (error) {
                document.getElementById('stats').innerHTML = 
                    `<div class="error">加载统计信息失败: ${error.message}</div>`;
            }
        }
        
        // 搜索文档
        async function searchDocuments() {
            const query = document.getElementById('searchQuery').value.trim();
            if (!query) return;
            
            const resultsDiv = document.getElementById('searchResults');
            resultsDiv.innerHTML = '<div class="loading">搜索中...</div>';
            
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query: query, top_k: 10})
                });
                const data = await response.json();
                
                if (data.error) {
                    resultsDiv.innerHTML = `<div class="error">错误: ${data.error}</div>`;
                    return;
                }
                
                if (data.results.length === 0) {
                    resultsDiv.innerHTML = '<div>没有找到相关文档</div>';
                    return;
                }
                
                let html = '<h3>搜索结果:</h3>';
                data.results.forEach((result, index) => {
                    html += `
                        <div class="result-item">
                            <div class="result-title">${result.file_path}</div>
                            <div class="similarity">相似度: ${result.max_similarity.toFixed(3)}</div>
                            <div class="result-content">${result.preview}</div>
                        </div>
                    `;
                });
                
                resultsDiv.innerHTML = html;
            } catch (error) {
                resultsDiv.innerHTML = `<div class="error">搜索失败: ${error.message}</div>`;
            }
        }
        
        // 问答
        async function askQuestion() {
            const question = document.getElementById('askQuery').value.trim();
            if (!question) return;
            
            const resultsDiv = document.getElementById('askResults');
            resultsDiv.innerHTML = '<div class="loading">思考中...</div>';
            
            try {
                const response = await fetch('/api/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({question: question, top_k: 5})
                });
                const data = await response.json();
                
                if (data.error) {
                    resultsDiv.innerHTML = `<div class="error">错误: ${data.error}</div>`;
                    return;
                }
                
                let html = `
                    <div class="result-item">
                        <div class="result-title">问题: ${data.question}</div>
                        <div class="result-content">${data.answer}</div>
                    </div>
                `;
                
                if (data.sources && data.sources.length > 0) {
                    html += '<h4>参考文档:</h4>';
                    data.sources.forEach((source, index) => {
                        html += `
                            <div class="result-item">
                                <div class="result-title">${source.file_path}</div>
                                <div class="similarity">相似度: ${source.similarity_score.toFixed(3)}</div>
                                <div class="result-content">${source.chunk_preview}</div>
                            </div>
                        `;
                    });
                }
                
                resultsDiv.innerHTML = html;
            } catch (error) {
                resultsDiv.innerHTML = `<div class="error">问答失败: ${error.message}</div>`;
            }
        }
        
        // 加载文档列表
        async function loadDocuments() {
            const resultsDiv = document.getElementById('documentsList');
            resultsDiv.innerHTML = '<div class="loading">加载文档列表...</div>';
            
            try {
                const response = await fetch('/api/documents');
                const data = await response.json();
                
                if (data.error) {
                    resultsDiv.innerHTML = `<div class="error">错误: ${data.error}</div>`;
                    return;
                }
                
                if (data.documents.length === 0) {
                    resultsDiv.innerHTML = '<div>知识库中没有文档</div>';
                    return;
                }
                
                let html = '<h3>文档列表:</h3>';
                data.documents.forEach((doc, index) => {
                    html += `
                        <div class="result-item">
                            <div class="result-title">${doc.file_path}</div>
                            <div class="result-content">
                                块数: ${doc.chunk_count} | 
                                最后修改: ${doc.last_modified || '未知'}
                            </div>
                        </div>
                    `;
                });
                
                resultsDiv.innerHTML = html;
            } catch (error) {
                resultsDiv.innerHTML = `<div class="error">加载文档列表失败: ${error.message}</div>`;
            }
        }
        
        // 添加文档
        async function addDocument() {
            const filePath = document.getElementById('filePath').value.trim();
            if (!filePath) return;
            
            const resultsDiv = document.getElementById('documentsList');
            resultsDiv.innerHTML = '<div class="loading">添加文档中...</div>';
            
            try {
                const response = await fetch('/api/add_document', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({file_path: filePath})
                });
                const data = await response.json();
                
                if (data.error) {
                    resultsDiv.innerHTML = `<div class="error">错误: ${data.error}</div>`;
                    return;
                }
                
                resultsDiv.innerHTML = `<div class="result-item">${data.message}</div>`;
                loadDocuments(); // 重新加载文档列表
                loadStats(); // 重新加载统计信息
            } catch (error) {
                resultsDiv.innerHTML = `<div class="error">添加文档失败: ${error.message}</div>`;
            }
        }
        
        // 上传文档
        async function uploadDocument() {
            const fileInput = document.getElementById('fileUpload');
            const files = fileInput.files;
            
            if (files.length === 0) {
                alert('请选择要上传的文件');
                return;
            }
            
            const resultsDiv = document.getElementById('documentsList');
            resultsDiv.innerHTML = '<div class="loading">上传文档中...</div>';
            
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const response = await fetch('/api/upload_document', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await response.json();
                    
                    if (data.error) {
                        resultsDiv.innerHTML += `<div class="error">上传 ${file.name} 失败: ${data.error}</div>`;
                    } else {
                        resultsDiv.innerHTML += `<div class="result-item">✅ ${data.message}</div>`;
                        
                        // 显示更新后的统计信息
                        if (data.stats) {
                            resultsDiv.innerHTML += `
                                <div class="result-item" style="background: #e8f5e8; border-color: #4caf50;">
                                    📊 知识库已更新: 总向量数 ${data.stats.total_vectors} | 总文档数 ${data.stats.total_documents} | 唯一文件数 ${data.stats.unique_files}
                                </div>
                            `;
                        }
                    }
                } catch (error) {
                    resultsDiv.innerHTML += `<div class="error">上传 ${file.name} 失败: ${error.message}</div>`;
                }
            }
            
            // 清空文件选择
            fileInput.value = '';
            
            // 重新加载文档列表和统计信息
            loadDocuments();
            loadStats();
        }
        
        // 回车键支持
        document.getElementById('searchQuery').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') searchDocuments();
        });
        
        document.getElementById('askQuery').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') askQuestion();
        });
        
        document.getElementById('filePath').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') addDocument();
        });
        
        // 页面加载时初始化
        window.onload = function() {
            loadStats();
        };
    </script>
</body>
</html>'''
    
    # 写入HTML模板
    with open(template_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    # 初始化知识库
    init_knowledge_base()
    
    print("启动Web界面...")
    print("访问地址: http://localhost:5000")
    app.run(debug=False, host='127.0.0.1', port=5000, threaded=True)
