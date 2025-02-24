import os
import httpx
from volcenginesdkarkruntime import Ark

class DeepSeekClient:
    def __init__(self):
        # 从环境变量获取认证信息
        self.client = Ark(
            ak=os.getenv('VOLC_ACCESSKEY'),
            sk=os.getenv('VOLC_SECRETKEY'),
            timeout=httpx.Timeout(timeout=1800)
        )
        self.model = "ep-20250220113205-g59k8"

    async def chat_stream(self, message):
        """流式对话方法"""
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": message}
            ],
            stream=True
        )
        
        response = ""
        reasoning = ""
        
        for chunk in stream:
            if not chunk.choices:
                continue
            if chunk.choices[0].delta.reasoning_content:
                reasoning += chunk.choices[0].delta.reasoning_content
            else:
                response += chunk.choices[0].delta.content
                
        return {
            "response": response,
            "reasoning": reasoning
        }

    async def chat(self, message):
        """标准对话方法"""
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        
        return {
            "response": completion.choices[0].message.content,
            "reasoning": completion.choices[0].message.reasoning_content
        }