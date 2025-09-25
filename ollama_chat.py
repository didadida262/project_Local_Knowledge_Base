#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama本地大模型对话脚本
支持与qwen3:8b模型进行对话
"""

import requests
import json
import sys
from typing import Optional, Dict, Any


class OllamaChat:
    """Ollama对话客户端"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen3:8b"):
        """
        初始化Ollama对话客户端
        
        Args:
            base_url: Ollama服务地址，默认为本地11434端口
            model: 模型名称，默认为qwen3:8b
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.session = requests.Session()
        
    def check_ollama_status(self) -> bool:
        """检查Ollama服务是否运行"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_available_models(self) -> list:
        """获取可用的模型列表"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except requests.exceptions.RequestException:
            return []
    
    def check_model_exists(self) -> bool:
        """检查指定模型是否存在"""
        available_models = self.get_available_models()
        return self.model in available_models
    
    def pull_model(self) -> bool:
        """拉取模型（如果不存在）"""
        print(f"正在拉取模型 {self.model}，请稍候...")
        print("注意：模型下载可能需要几分钟到几十分钟，请耐心等待...")
        print("如果下载卡住，可以按 Ctrl+C 中断，然后重试")
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/pull",
                json={"name": self.model},
                stream=True,
                timeout=300  # 5分钟超时
            )
            
            if response.status_code == 200:
                last_status = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if 'status' in data:
                                status = data['status']
                                if status != last_status:  # 只在状态改变时打印
                                    print(f"状态: {status}")
                                    last_status = status
                            if 'completed' in data and data['completed']:
                                print("✓ 模型下载完成")
                                return True
                        except json.JSONDecodeError:
                            continue
                return True
            return False
        except requests.exceptions.Timeout:
            print("下载超时，请检查网络连接后重试")
            return False
        except requests.exceptions.RequestException as e:
            print(f"拉取模型失败: {e}")
            return False
        except KeyboardInterrupt:
            print("\n下载被用户中断")
            return False
    
    def chat(self, message: str, stream: bool = True) -> str:
        """
        与模型对话
        
        Args:
            message: 用户输入的消息
            stream: 是否使用流式输出
            
        Returns:
            模型的回复
        """
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": message}],
            "stream": stream
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/chat",
                json=payload,
                stream=stream,
                timeout=30
            )
            
            if response.status_code != 200:
                return f"错误: HTTP {response.status_code}"
            
            if stream:
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
                data = response.json()
                return data.get('message', {}).get('content', '')
                
        except requests.exceptions.RequestException as e:
            return f"请求失败: {e}"
    
    def interactive_chat(self):
        """交互式对话模式"""
        print("=" * 50)
        print("Ollama 本地大模型对话")
        print(f"模型: {self.model}")
        print("输入 'quit' 或 'exit' 退出")
        print("输入 'clear' 清屏")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n用户: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("再见！")
                    break
                elif user_input.lower() == 'clear':
                    import os
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                elif not user_input:
                    continue
                
                print(f"\n{self.model}: ", end='', flush=True)
                response = self.chat(user_input)
                
            except KeyboardInterrupt:
                print("\n\n程序被中断，再见！")
                break
            except Exception as e:
                print(f"\n发生错误: {e}")


def main():
    """主函数"""
    # 创建Ollama客户端
    chat_client = OllamaChat()
    
    # 检查Ollama服务状态
    print("检查Ollama服务状态...")
    if not chat_client.check_ollama_status():
        print("错误: 无法连接到Ollama服务")
        print("请确保Ollama正在运行，并且可以通过 http://localhost:11434 访问")
        print("启动Ollama命令: ollama serve")
        sys.exit(1)
    
    print("✓ Ollama服务运行正常")
    
    # 显示可用模型
    available_models = chat_client.get_available_models()
    if available_models:
        print(f"\n可用模型: {', '.join(available_models)}")
    
    # 检查模型是否存在
    print(f"\n检查模型 {chat_client.model} 是否存在...")
    if not chat_client.check_model_exists():
        print(f"模型 {chat_client.model} 不存在")
        
        # 询问用户是否要下载或使用现有模型
        if available_models:
            print(f"\n发现已有模型: {available_models[0]}")
            choice = input(f"是否使用现有模型 {available_models[0]} 进行对话？(y/n): ").strip().lower()
            if choice in ['y', 'yes', '是']:
                chat_client.model = available_models[0]
                print(f"✓ 已切换到模型 {chat_client.model}")
            else:
                print(f"正在拉取模型 {chat_client.model}...")
                if not chat_client.pull_model():
                    print("模型拉取失败，请检查网络连接或模型名称")
                    print("提示：你可以手动拉取模型: ollama pull qwen3:8b")
                    sys.exit(1)
        else:
            print(f"正在拉取模型 {chat_client.model}...")
            if not chat_client.pull_model():
                print("模型拉取失败，请检查网络连接或模型名称")
                print("提示：你可以手动拉取模型: ollama pull qwen3:8b")
                sys.exit(1)
    else:
        print(f"✓ 模型 {chat_client.model} 已存在")
    
    # 开始交互式对话
    chat_client.interactive_chat()


if __name__ == "__main__":
    main()
