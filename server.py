import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.deepseek_client import DeepSeekClient
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置静态文件服务
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# 获取当前文件所在目录的绝对路径
BASE_DIR = Path(__file__).resolve().parent

# 挂载静态文件
app.mount("/scripts", StaticFiles(directory=str(BASE_DIR / "scripts")), name="scripts")
app.mount("/styles", StaticFiles(directory=str(BASE_DIR / "styles")), name="styles")

# 添加根路由
from fastapi.responses import FileResponse

@app.get("/")
async def read_root():
    return FileResponse(str(BASE_DIR / "index.html"))

@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse(str(BASE_DIR / "favicon.ico"))

# 创建DeepSeek客户端实例
deepseek_client = DeepSeekClient()

# 请求模型
class MessageRequest(BaseModel):
    message: str

@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "请求的API端点不存在", "path": request.url.path}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

@app.post("/api/chat")
async def chat(request: MessageRequest):
    try:
        # 调用DeepSeek API获取回复
        result = await deepseek_client.chat(request.message)
        
        # 提取建议
        suggestions = extract_suggestions(result["response"])
        
        return {
            "success": True,
            "message": result["response"],
            "reasoning": result.get("reasoning", ""),
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/stream")
async def chat_stream(request: MessageRequest):
    try:
        # 调用DeepSeek API获取流式回复
        result = await deepseek_client.chat_stream(request.message)
        
        # 提取建议
        suggestions = extract_suggestions(result["response"])
        
        return {
            "success": True,
            "message": result["response"],
            "reasoning": result.get("reasoning", ""),
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_suggestions(text):
    """从AI响应中提取建议"""
    suggestions = []
    sentences = text.split('。')
    
    for sentence in sentences:
        if any(keyword in sentence for keyword in ['建议', '推荐', '可以', '不妨']):
            suggestions.append(sentence.strip())
    
    return suggestions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)