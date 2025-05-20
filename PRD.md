# FlowMaster - 产品需求文档 (PRD)

## 1. 产品概述

FlowMaster是一款专为提高工作效率设计的应用，帮助用户优先处理有意义的工作，高效管理任务，并通过采用灵活、直观的时间和任务管理方法来减少干扰。FlowMaster受避免僵化日程安排、结构化拖延和战略决策原则的启发，使用户能够专注于最重要的事务，同时保持对工作流程的控制。

### 1.1 目标

提供一个支持用户以下行为的工具：

- 避免僵化的日程安排，专注于高优先级或高兴趣的任务
- 使用简单的三列表系统（待办、关注、稍后）管理任务
- 使用数字化3x5卡片系统有效规划每日任务

### 1.2 目标用户

主要为个人项目，但也适合：

1. 寻求工作灵活性的专业人士、自由职业者和创意工作者
2. 面临过度日程安排或频繁中断困扰的个人
3. 对结构化拖延和战略性不完美等生产力技巧感兴趣的用户

## 2. 功能与需求

### 2.1 任务管理

#### 2.1.1 三列表系统

**描述**：用户可以将任务组织到三个列表中：

- **待办列表**：必须完成的具有截止日期或高优先级的任务
- **关注列表**：需要近期关注的后续跟进和提醒
- **稍后列表**：未来想法或低优先级任务

**需求**：

- 在每个列表中创建、编辑和删除任务
- 拖放功能，可在列表之间移动任务
- 待办和关注列表的可选截止日期和优先级标签
- 自动归档已完成任务或将其移至"保管库"部分
- 视觉指示器（如颜色编码）区分列表类型

#### 2.1.2 每日3x5卡片系统

**描述**：每晚，用户为第二天创建一张数字3x5卡片，上面有3-5个关键任务。卡片背面作为"反待办清单"，记录成就。

**需求**：

- 专用界面，用于创建限制为3-5个任务的每日3x5卡片
- 翻转动画，在正面（任务）和背面（成就）之间切换
- 手动添加成就或从已完成的待办任务自动填充的能力
- 任务标记完成时的内啡肽提升通知（如五彩纸屑动画）
- 保存每日卡片以供历史回顾

#### 2.1.3 决策框架

**描述**：引导用户做出与其优先事项一致的有意识承诺。

**需求**：

- 决策提示：在添加新的待办任务之前，用户回答"我的头脑和心灵都同意吗？"（是/否切换）
- 对没有完全承诺添加的任务发出警告，并可选择移至稍后列表
- 月度反思工具，评估在喜爱与不喜爱任务上花费的时间，并提供委派或消除不喜爱任务的建议

#### 2.1.4 AI驱动的任务优先级

**描述**：基于用户习惯和行为模式，智能推荐任务优先级和每日计划。

**需求**：

- 分析用户完成任务的历史模式和时间偏好
- 学习用户的工作习惯，提供个性化任务排序建议
- 识别用户高效率时段，推荐在这些时间安排重要任务
- 提供智能提醒，基于过去的完成模式和当前工作负载
- 用户可随时覆盖AI建议，保持控制权

## 3. 用户界面与体验

### 3.1 设计原则

- **极简主义**：清晰、无干扰的界面，减少认知负担
- **直观性**：易于理解和使用，无需复杂说明
- **视觉吸引力**：美观的设计元素和流畅的动画
- **响应式**：在所有设备上提供一致的体验

### 3.2 关键界面

#### 3.2.1 主页仪表板

- 显示待办、关注和稍后列表，包含任务计数和快速添加按钮
- 当日3x5卡片的突出显示和快速访问
- 任务完成进度的视觉指示器
- 个性化的AI建议区域

#### 3.2.2 每日卡片视图

- 3x5卡片界面，带有前/后切换和成就追踪器
- 卡片设计美观，模拟物理卡片的质感
- 简洁的任务输入和编辑功能
- 成就记录和庆祝动画

#### 3.2.3 任务详情视图

- 详细的任务信息和编辑选项
- 优先级和截止日期设置
- 标签和分类功能
- 任务历史和相关笔记

## 4. 技术需求

### 4.1 前端技术栈

- **框架**：Vue.js 3 (使用Composition API)
- **UI库**：Tailwind CSS 用于响应式设计
- **动画**：Vue Transition + GSAP用于流畅动画
- **状态管理**：Pinia用于应用状态
- **路由**：Vue Router用于页面导航

### 4.2 后端技术栈

- **API框架**：FastAPI (Python)
- **数据库**：MongoDB
- **认证**：JWT认证
- **AI组件**：使用scikit-learn和TensorFlow Lite进行用户行为分析

### 4.3 数据库设计

#### 4.3.1 集合结构

**用户集合**：
```json
{
  "_id": "ObjectId",
  "username": "String",
  "email": "String",
  "password": "String (hashed)",
  "preferences": {
    "theme": "String",
    "notifications": "Boolean"
  },
  "created_at": "Date",
  "last_login": "Date"
}
```

**任务集合**：
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId (ref: users)",
  "title": "String",
  "description": "String",
  "list_type": "String (todo, watch, later)",
  "priority": "Number (1-5, optional)",
  "due_date": "Date (optional)",
  "tags": "Array of Strings",
  "is_completed": "Boolean",
  "completed_at": "Date",
  "created_at": "Date",
  "updated_at": "Date"
}
```

**每日卡片集合**：
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId (ref: users)",
  "date": "Date",
  "tasks": [
    {
      "task_id": "ObjectId (ref: tasks)",
      "title": "String",
      "is_completed": "Boolean"
    }
  ],
  "accomplishments": [
    {
      "title": "String",
      "source": "String (manual, task)",
      "task_id": "ObjectId (optional, ref: tasks)"
    }
  ],
  "created_at": "Date",
  "updated_at": "Date"
}
```

**用户行为集合**：
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId (ref: users)",
  "task_completion_patterns": {
    "morning_completion_rate": "Number",
    "afternoon_completion_rate": "Number",
    "evening_completion_rate": "Number",
    "weekday_completion_rate": "Object",
    "priority_completion_rate": "Object"
  },
  "productive_hours": "Array of Objects",
  "task_preferences": "Object",
  "updated_at": "Date"
}
```

### 4.4 API端点

#### 4.4.1 用户API

- `POST /api/users/register` - 注册新用户
- `POST /api/users/login` - 用户登录
- `GET /api/users/profile` - 获取用户资料
- `PUT /api/users/profile` - 更新用户资料
- `PUT /api/users/preferences` - 更新用户偏好设置

#### 4.4.2 任务API

- `GET /api/tasks` - 获取所有任务（可按列表类型筛选）
- `POST /api/tasks` - 创建新任务
- `GET /api/tasks/{id}` - 获取特定任务
- `PUT /api/tasks/{id}` - 更新任务
- `DELETE /api/tasks/{id}` - 删除任务
- `PUT /api/tasks/{id}/complete` - 标记任务为完成
- `PUT /api/tasks/{id}/move` - 将任务移至不同列表

#### 4.4.3 每日卡片API

- `GET /api/daily-cards` - 获取所有每日卡片
- `GET /api/daily-cards/today` - 获取今天的卡片
- `POST /api/daily-cards` - 创建新的每日卡片
- `PUT /api/daily-cards/{id}` - 更新每日卡片
- `POST /api/daily-cards/{id}/accomplishments` - 添加成就

#### 4.4.4 AI分析API

- `GET /api/analytics/productivity` - 获取生产力分析
- `GET /api/analytics/recommendations` - 获取任务推荐
- `GET /api/analytics/insights` - 获取用户行为洞察

## 5. 实施计划

### 5.1 MVP功能

1. 基本的三列表任务管理系统
2. 简化版每日3x5卡片功能
3. 基本用户认证和数据存储
4. 简单的任务优先级排序
5. 响应式Web界面

### 5.2 未来迭代

1. 高级AI驱动的任务推荐
2. 详细的生产力分析和报告
3. 集成日历和提醒功能
4. 移动应用版本
5. 团队协作功能

## 6. 设计规范

### 6.1 色彩方案

- **主色**：#3B82F6（蓝色）- 代表专注和生产力
- **辅助色**：#10B981（绿色）- 代表完成和成就
- **强调色**：#F59E0B（橙色）- 代表优先级和注意
- **中性色**：#F3F4F6到#1F2937的灰度范围

### 6.2 排版

- **主要字体**：Inter，无衬线字体，清晰易读
- **标题大小**：24-32px
- **正文大小**：16px
- **小文本**：14px

### 6.3 组件样式

- **卡片**：轻微阴影，圆角边缘，简洁边框
- **按钮**：明确的悬停状态，适当的内边距，一致的圆角
- **输入框**：简洁的边框，清晰的焦点状态
- **列表项**：足够的间距，清晰的分隔，一致的内边距

---

本PRD文档旨在提供FlowMaster应用的全面概述，重点关注核心功能和技术实现。该应用的设计理念是帮助用户以更灵活、更有效的方式管理任务，同时利用AI技术提供个性化的任务优先级建议。
