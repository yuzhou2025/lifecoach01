import os
import httpx
from volcenginesdkarkruntime import Ark

class DeepSeekClient:
    def __init__(self):
        # 从环境变量获取认证信息
        ak = os.getenv('VOLC_ACCESSKEY')
        sk = os.getenv('VOLC_SECRETKEY')
        
        # 验证必要的认证信息
        if not ak or not sk:
            missing_vars = []
            if not ak:
                missing_vars.append('VOLC_ACCESSKEY')
            if not sk:
                missing_vars.append('VOLC_SECRETKEY')
            raise ValueError(
                f"缺少必要的环境变量: {', '.join(missing_vars)}\n"
                "请在Vercel的环境变量设置中配置这些变量：\n"
                "1. 登录Vercel管理控制台\n"
                "2. 进入您的项目设置\n"
                "3. 点击'Environment Variables'\n"
                "4. 添加以下环境变量：\n"
                "   - VOLC_ACCESSKEY: 您的火山引擎访问密钥\n"
                "   - VOLC_SECRETKEY: 您的火山引擎访问密钥密文\n"
                "注意：确保这些环境变量与vercel.json中的配置保持一致"
            )
            
        self.client = Ark(
            ak=ak,
            sk=sk,
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