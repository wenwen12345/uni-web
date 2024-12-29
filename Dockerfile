# 前端构建阶段
FROM node:22-alpine as frontend-builder

WORKDIR /app/frontend

# 全局安装 pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# 复制源代码
COPY src/frontend/ .
RUN ls -la
# 安装依赖
RUN pnpm install

# 构建
RUN pnpm run build

# 最终运行阶段
FROM python:3.13-slim

WORKDIR /app

# 安装PDM
RUN pip install -U pip setuptools wheel && \
    pip install pdm

# 复制后端代码
COPY src/backend/ ./backend/

# 设置PDM配置并安装依赖
WORKDIR /app/backend
ENV PDM_USE_VENV=false
RUN pdm config python.use_venv false && \
    pdm install --prod --no-lock --no-editable

# 复制前端构建文件
COPY --from=frontend-builder /app/frontend/dist/ ./frontend/dist/

# 设置环境变量
ENV PYTHONPATH=/app/backend/__pypackages__/3.13/lib
ENV DEV_MODE=false

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 