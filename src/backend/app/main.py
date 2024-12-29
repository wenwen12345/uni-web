from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import httpx

# 判断是否为开发环境
DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"
VUE_DEV_SERVER = "http://localhost:5173"

async def proxy_request(request: Request, path: str = ""):
    client = httpx.AsyncClient()
    url = f"{VUE_DEV_SERVER}/{path}"
    
    # 转发原始请求的方法和头部
    headers = dict(request.headers)
    headers.pop("host", None)  # 移除 host 头，让 httpx 自动设置
    
    try:
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=await request.body(),
            follow_redirects=True
        )
        
        return StreamingResponse(
            response.iter_bytes(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    finally:
        await client.aclose()

class YamlData(BaseModel):
    content: str

app = FastAPI(
    title="FastAPI Backend",
    description="Backend API for Vue Frontend",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vue开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 只在生产环境下挂载静态文件
if not DEV_MODE:
    frontend_dist = "../frontend/dist"
    frontend_assets = os.path.join(frontend_dist, "assets")
    
    if not os.path.exists(frontend_dist):
        print(f"警告: 前端构建目录不存在: {frontend_dist}")
        print("请确保前端项目已经构建 (npm run build)")
    else:
        if os.path.exists(frontend_assets):
            app.mount("/assets", StaticFiles(directory=frontend_assets), name="static")
        
        

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI!"}

@app.post("/api/yaml")
async def save_yaml(data: YamlData):
    try:
        # 直接保存原始内容
        with open("app.yaml", "w", encoding="utf-8") as f:
            f.write(data.content)
        
        return {"message": "YAML 文件保存成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存文件失败: {str(e)}")

@app.get("/app.yaml")
async def get_yaml():
    if not os.path.exists("app.yaml"):
        raise HTTPException(status_code=404, detail="YAML 文件不存在")
    return FileResponse("app.yaml")

@app.get("/{path:path}")
async def serve_static(request: Request, path: str):
    # 开发环境下反向代理到 Vue 开发服务器
    if DEV_MODE:
        client = httpx.AsyncClient(base_url="http://localhost:5173")
        try:
            response = await client.get(f"/{path}", headers=dict(request.headers))
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Vue 开发服务器未启动")
        finally:
            await client.aclose()
    
    # 生产环境下返回静态文件
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    file_path = os.path.join(frontend_dist, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(frontend_dist, "index.html"))