# 前端构建阶段
FROM node:22-alpine as frontend-builder

WORKDIR /app/frontend

# 全局安装 pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# 首先复制整个前端目录
COPY src/frontend/ .

# 安装依赖
RUN pnpm install --frozen-lockfile

# 构建
RUN pnpm run build

# 后端构建阶段
FROM python:3.13-slim as backend-builder

WORKDIR /app/backend
COPY src/backend/ .

# 安装 PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# 安装依赖
RUN pdm install --prod

# 最终运行阶段
FROM python:3.13-slim

WORKDIR /app

# 复制后端文件
COPY --from=backend-builder /app/backend/ ./backend/
COPY --from=backend-builder /root/.local/share/pdm/venv/ ./venv/

# 复制前端构建文件
COPY --from=frontend-builder /app/frontend/dist/ ./backend/frontend/dist/

# 设置环境变量
ENV PATH="/app/venv/bin:$PATH"
ENV DEV_MODE=false
ENV PYTHONPATH=/app/backend

# 暴露端口
EXPOSE 8000

# 设置工作目录
WORKDIR /app/backend

# 启动命令
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 