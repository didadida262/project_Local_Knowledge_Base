#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内存优化版本的Ollama对话脚本
解决内存不足的问题
"""

import requests
import json
import sys
import time
import gc


class MemoryOptimizedChat:
    """内存优化的Ollama对话客户端"""
    
    def __init__(self, base_url="http://localhost:11434", model="gemma3:4b"):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.session = requests.Session()
        # 设置较小的超时时间
        self.session.timeout = 10
        
    def check_ollama_status(self):
        """检查Ollama服务状态"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self):
        """获取可用模型"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except:
            return []
    
    def chat_with_retry(self, message, max_retries=3):
        """带重试机制的对话"""
        for attempt in range(max_retries):
            try:
                print(f"尝试 {attempt + 1}/{max_retries}...")
                
                # 清理内存
                gc.collect()
                
                payload = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": message}],
                    "stream": True,
                    "options": {
                        "num_ctx": 2048,  # 减少上下文长度
                        "num_predict": 100,  # 限制输出长度
                        "temperature": 0.7
                    }
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    stream=True,
                    timeout=30
                )
                
                if response.status_code == 200:
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            try:
                                data = json.loads(line.decode('utf-8'))
                                if 'message' in data and 'content' in data['message']:
                                    content = data['message']['content']
                                    print(content, end='', flush=True)
                                    full_response += content
                                if data.get('done', False):
                                    break
                            except json.JSONDecodeError:
                                continue
                    print()  # 换行
                    return full_response
                else:
                    print(f"HTTP错误: {response.status_code}")
                    if attempt < max_retries - 1:
                        print("等待5秒后重试...")
                        time.sleep(5)
                        
            except requests.exceptions.Timeout:
                print("请求超时")
                if attempt < max_retries - 1:
                    print("等待5秒后重试...")
                    time.sleep(5)
            except Exception as e:
                print(f"请求失败: {e}")
                if attempt < max_retries - 1:
                    print("等待5秒后重试...")
                    time.sleep(5)
        
        return "抱歉，模型暂时无法响应，请稍后重试。"
    
    def interactive_chat(self):
        """交互式对话"""
        print("=" * 50)
        print("内存优化版 Ollama 对话")
        print(f"模型: {self.model}")
        print("输入 'quit' 退出")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n用户: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("再见！")
                    break
                elif not user_input:
                    continue
                
                print(f"\n{self.model}: ", end='', flush=True)
                response = self.chat_with_retry(user_input)
                
            except KeyboardInterrupt:
                print("\n\n程序被中断，再见！")
                break
            except Exception as e:
                print(f"\n发生错误: {e}")


def main():
    """主函数"""
    print("内存优化版 Ollama 对话工具")
    print("=" * 50)
    
    # 检查Ollama服务
    chat = MemoryOptimizedChat()
    
    print("检查Ollama服务状态...")
    if not chat.check_ollama_status():
        print("错误: 无法连接到Ollama服务")
        print("请确保Ollama正在运行")
        sys.exit(1)
    
    print("✓ Ollama服务运行正常")
    
    # 获取可用模型
    models = chat.get_available_models()
    if not models:
        print("错误: 没有找到可用模型")
        sys.exit(1)
    
    print(f"可用模型: {', '.join(models)}")
    
    # 选择模型
    if len(models) == 1:
        selected_model = models[0]
        print(f"使用模型: {selected_model}")
        chat.model = selected_model
    else:
        print("\n请选择要使用的模型:")
        for i, model in enumerate(models, 1):
            print(f"{i}. {model}")
        
        while True:
            try:
                choice = int(input("请输入选择 (数字): ")) - 1
                if 0 <= choice < len(models):
                    selected_model = models[choice]
                    chat.model = selected_model
                    break
                else:
                    print("无效选择，请重试")
            except ValueError:
                print("请输入有效数字")
    
    print(f"\n已选择模型: {chat.model}")
    print("开始对话...")
    
    # 开始交互式对话
    chat.interactive_chat()


if __name__ == "__main__":
    main()
