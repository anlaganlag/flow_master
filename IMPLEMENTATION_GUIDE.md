# FlowMaster - 实施指南

本文档补充了PRD和SPEC中未详细说明的实施细节，为开发团队提供更具体的指导。

## 1. 项目结构

### 1.1 目录结构

```
flow_master/
├── frontend/                  # 前端Vue.js应用
│   ├── public/                # 静态资源
│   ├── src/                   # 源代码
│   │   ├── assets/            # 图片、字体等资源
│   │   ├── components/        # Vue组件
│   │   │   ├── common/        # 通用组件
│   │   │   ├── tasks/         # 任务相关组件
│   │   │   └── cards/         # 每日卡片组件
│   │   ├── views/             # 页面视图
│   │   ├── router/            # Vue Router配置
│   │   ├── store/             # Pinia状态管理
│   │   ├── services/          # API服务
│   │   ├── utils/             # 工具函数
│   │   ├── App.vue            # 根组件
│   │   └── main.js            # 入口文件
│   ├── .eslintrc.js           # ESLint配置
│   ├── tailwind.config.js     # Tailwind CSS配置
│   ├── vite.config.js         # Vite配置
│   └── package.json           # 依赖管理
│
├── backend/                   # 后端FastAPI应用
│   ├── app/                   # 应用代码
│   │   ├── api/               # API路由
│   │   │   ├── auth.py        # 认证相关API
│   │   │   ├── tasks.py       # 任务相关API
│   │   │   └── daily_cards.py # 每日卡片API
│   │   ├── core/              # 核心功能
│   │   │   ├── config.py      # 配置
│   │   │   ├── security.py    # 安全相关
│   │   │   └── db.py          # 数据库连接
│   │   ├── models/            # 数据模型
│   │   ├── schemas/           # Pydantic模式
│   │   └── main.py            # 应用入口
│   ├── tests/                 # 测试
│   ├── requirements.txt       # Python依赖
│   └── Dockerfile             # Docker配置
│
├── docker-compose.yml         # Docker Compose配置
├── .gitignore                 # Git忽略文件
├── README.md                  # 项目说明
├── PRD.md                     # 产品需求文档
└── SPEC.md                    # 技术规格文档
```

## 2. 开发环境设置

### 2.1 前端开发环境

1. **安装Node.js和npm**
   ```bash
   # 推荐使用Node.js 16+
   node -v  # 确认版本
   npm -v   # 确认npm版本
   ```

2. **设置前端项目**
   ```bash
   # 创建Vue项目
   npm create vite@latest frontend -- --template vue
   cd frontend
   
   # 安装依赖
   npm install
   npm install vue-router@4 pinia axios tailwindcss postcss autoprefixer
   
   # 初始化Tailwind CSS
   npx tailwindcss init -p
   
   # 启动开发服务器
   npm run dev
   ```

### 2.2 后端开发环境

1. **安装Python**
   ```bash
   # 推荐使用Python 3.9+
   python --version  # 确认版本
   ```

2. **设置虚拟环境**
   ```bash
   # 创建虚拟环境
   python -m venv venv
   
   # 激活虚拟环境
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install fastapi uvicorn motor pyjwt python-multipart bcrypt
   pip install pytest pytest-asyncio httpx  # 测试依赖
   ```

4. **启动后端服务**
   ```bash
   uvicorn app.main:app --reload
   ```

### 2.3 数据库设置

1. **安装MongoDB**
   - 使用Docker:
     ```bash
     docker run --name mongodb -p 27017:27017 -d mongo
     ```
   - 或下载安装MongoDB Community Edition

2. **创建数据库**
   ```bash
   # 连接MongoDB
   mongosh
   
   # 创建数据库
   use flowmaster
   
   # 创建集合
   db.createCollection("users")
   db.createCollection("tasks")
   db.createCollection("daily_cards")
   ```

### 2.4 使用Docker Compose

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 3. UI/UX设计规范

### 3.1 组件设计

#### 3.1.1 任务卡片组件

```vue
<!-- TaskCard.vue -->
<template>
  <div class="task-card" :class="priorityClass">
    <div class="task-header">
      <h3>{{ task.title }}</h3>
      <div class="task-actions">
        <!-- 操作按钮 -->
      </div>
    </div>
    <p v-if="task.description">{{ task.description }}</p>
    <div class="task-footer">
      <span v-if="task.due_date">{{ formatDate(task.due_date) }}</span>
      <span class="priority-badge">{{ priorityText }}</span>
    </div>
  </div>
</template>
```

#### 3.1.2 每日卡片组件

```vue
<!-- DailyCard.vue -->
<template>
  <div class="daily-card" :class="{ 'flipped': isFlipped }">
    <div class="card-front">
      <!-- 任务列表 -->
    </div>
    <div class="card-back">
      <!-- 成就列表 -->
    </div>
  </div>
</template>
```

### 3.2 颜色系统

| 用途 | 颜色 | 十六进制 |
|------|------|----------|
| 主色 | 蓝色 | #3B82F6 |
| 辅助色 | 绿色 | #10B981 |
| 强调色 | 橙色 | #F59E0B |
| 背景色 | 浅灰 | #F3F4F6 |
| 文本色 | 深灰 | #1F2937 |
| 边框色 | 中灰 | #D1D5DB |
| 成功色 | 绿色 | #10B981 |
| 错误色 | 红色 | #EF4444 |
| 警告色 | 黄色 | #F59E0B |

### 3.3 响应式断点

| 断点名称 | 宽度 |
|----------|------|
| sm | 640px |
| md | 768px |
| lg | 1024px |
| xl | 1280px |
| 2xl | 1536px |

## 4. API接口详细文档

### 4.1 认证API

#### 4.1.1 用户注册

**请求**:
```
POST /api/auth/register
Content-Type: application/json

{
  "username": "user123",
  "email": "user@example.com",
  "password": "securepassword"
}
```

**响应**:
```json
{
  "id": "60d21b4667d0d8992e610c85",
  "username": "user123",
  "email": "user@example.com",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 4.1.2 用户登录

**请求**:
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**响应**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 4.2 任务API

#### 4.2.1 创建任务

**请求**:
```
POST /api/tasks
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "完成项目规划",
  "description": "制定详细的项目计划和时间表",
  "list_type": "todo",
  "priority": 4,
  "due_date": "2023-06-30T00:00:00Z"
}
```

**响应**:
```json
{
  "id": "60d21b4667d0d8992e610c86",
  "title": "完成项目规划",
  "description": "制定详细的项目计划和时间表",
  "list_type": "todo",
  "priority": 4,
  "due_date": "2023-06-30T00:00:00Z",
  "is_completed": false,
  "created_at": "2023-06-15T10:30:00Z",
  "updated_at": "2023-06-15T10:30:00Z"
}
```

## 5. 数据流程图

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  用户界面   │      │   API层     │      │  数据库层   │
└──────┬──────┘      └──────┬──────┘      └──────┬──────┘
       │                    │                    │
       │  发送API请求       │                    │
       │ ─────────────────> │                    │
       │                    │  查询/更新数据     │
       │                    │ ─────────────────> │
       │                    │                    │
       │                    │  返回数据          │
       │                    │ <───────────────── │
       │  返回API响应       │                    │
       │ <───────────────── │                    │
       │                    │                    │
```

## 6. 测试计划

### 6.1 单元测试

#### 前端单元测试

```javascript
// TaskCard.spec.js
import { mount } from '@vue/test-utils'
import TaskCard from '@/components/tasks/TaskCard.vue'

describe('TaskCard.vue', () => {
  it('renders task title correctly', () => {
    const task = { title: '测试任务', priority: 3 }
    const wrapper = mount(TaskCard, {
      props: { task }
    })
    expect(wrapper.text()).toContain('测试任务')
  })
  
  it('applies correct priority class', () => {
    const task = { title: '高优先级任务', priority: 5 }
    const wrapper = mount(TaskCard, {
      props: { task }
    })
    expect(wrapper.classes()).toContain('priority-high')
  })
})
```

#### 后端单元测试

```python
# test_tasks.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/tasks",
            json={
                "title": "测试任务",
                "description": "这是一个测试任务",
                "list_type": "todo",
                "priority": 3
            },
            headers={"Authorization": f"Bearer {test_token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "测试任务"
        assert data["list_type"] == "todo"
```

## 7. 部署文档

### 7.1 前端部署 (Netlify)

1. 构建前端项目
   ```bash
   cd frontend
   npm run build
   ```

2. 部署到Netlify
   - 创建netlify.toml文件:
     ```toml
     [build]
       publish = "dist"
       command = "npm run build"
     
     [[redirects]]
       from = "/*"
       to = "/index.html"
       status = 200
     ```

### 7.2 后端部署 (Heroku)

1. 创建Procfile
   ```
   web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}
   ```

2. 部署到Heroku
   ```bash
   heroku create flowmaster-api
   git push heroku main
   ```

3. 设置环境变量
   ```bash
   heroku config:set MONGODB_URL=mongodb+srv://...
   heroku config:set SECRET_KEY=your-secret-key
   ```

### 7.3 数据库部署 (MongoDB Atlas)

1. 创建MongoDB Atlas账户
2. 创建新集群
3. 设置数据库用户和网络访问
4. 获取连接字符串并配置到后端环境变量

## 8. 实施任务清单

请参考 TASKS.md 文件获取详细的实施任务清单。
