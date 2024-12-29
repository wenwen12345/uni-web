# Vite + Vue + Shadcn + FastAPI 全栈应用

这是一个 uni-api 的 web 面板，采用Vue 3作为前端框架，FastAPI作为后端服务。

## 技术栈

### 前端
- Vue 3 - 渐进式JavaScript框架
- Vite - 下一代前端构建工具
- Shadcn/Vue - 高质量UI组件库
- TypeScript - 类型安全的JavaScript超集
- Tailwind CSS - 实用优先的CSS框架

### 后端
- FastAPI - 现代、快速的Python Web框架
- Pydantic - 数据验证和设置管理
- Uvicorn - 轻量级ASGI服务器
- Python 3.10+ - 编程语言

## 项目结构

```
.
├── src/
│   ├── frontend/           # Vue 前端项目
│   │   ├── src/           # 源代码
│   │   ├── public/        # 静态资源
│   │   └── package.json   # 前端依赖
│   └── backend/           # FastAPI 后端项目
│       ├── app/           # 应用代码
│       │   ├── main.py    # 主程序
│       │   ├── api/       # API 路由
│       │   └── core/      # 核心配置
│       └── pyproject.toml # 后端依赖配置
├── docker-compose.yml     # Docker编排配置
├── Dockerfile            # Docker构建文件
└── README.md            # 项目说明文档
```

## 环境要求

- Node.js 16+
- Python 3.10+
- PDM (Python依赖管理工具)
- pnpm (推荐的Node.js包管理器)
- Docker & Docker Compose (可选，用于容器化部署)

## 开发指南

### 后端开发

1. 安装PDM（如果未安装）:
```bash
pip install pdm
```

2. 安装后端依赖:
```bash
cd src/backend
pdm install
```

3. 启动开发服务器:
```bash
pdm run dev
```

后端服务将在 http://localhost:8000 启动

### 前端开发

1. 安装pnpm（如果未安装）:
```bash
npm install -g pnpm
```

2. 安装前端依赖:
```bash
cd src/frontend
pnpm install
```

3. 启动开发服务器:
```bash
pnpm dev
```

前端服务将在 http://localhost:5173 启动

## Docker部署

使用Docker Compose进行部署：

```bash
docker-compose up -d
```

## API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 开发工具推荐

- VS Code
- Vue.js Devtools
- Python Extension Pack
- Docker Extension

## 测试

### 后端测试
```bash
cd src/backend
pdm run test
```

### 前端测试
```bash
cd src/frontend
pnpm test
```

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情
