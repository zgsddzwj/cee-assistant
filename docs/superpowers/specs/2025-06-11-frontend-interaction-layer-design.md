# 前端交互层设计方案

## 概述

基于 React + TypeScript + Vite 构建的高考志愿填报前端应用，为考生提供智能咨询、志愿推荐、数据可视化等全流程交互体验。

## 一、技术栈

| 技术 | 用途 |
|------|------|
| React 18 | UI 框架 |
| TypeScript | 类型安全 |
| Vite | 构建工具 |
| React Router | 路由管理 |
| Zustand | 状态管理 |
| Tailwind CSS | 原子化样式 |
| shadcn/ui | UI 组件库 |
| Axios | HTTP 请求 |
| Recharts | 数据可视化 |

## 二、整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    前端 (React + Vite + TS)                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   路由层    │  │   状态层    │  │      API 层         │ │
│  │React Router │  │   Zustand   │  │    Axios Client     │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
│         │                │                    │            │
│  ┌──────▼────────────────▼────────────────────▼──────────┐ │
│  │                    页面组件层                           │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐ │ │
│  │  │ 首页/   │ │ 咨询页  │ │ 推荐页  │ │  院校详情   │ │ │
│  │  │登录注册 │ │ (Chat)  │ │(Result) │ │   (Detail)  │ │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────────┘ │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────────────────────┐ │ │
│  │  │信息填写 │ │数据可视 │ │      通用组件            │ │ │
│  │  │(Profile)│ │(Charts) │ │  Header/Footer/Modal   │ │ │
│  │  └─────────┘ └─────────┘ └─────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              后端 API (FastAPI 微服务)                       │
│         ┌─────────────┐  ┌─────────────┐                   │
│         │ 推荐引擎服务 │  │ Agent 服务   │                   │
│         │  :8001      │  │  :8002      │                   │
│         └─────────────┘  └─────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

## 三、页面设计

### 3.1 首页 (Landing Page)
- 顶部导航栏（Logo、登录/注册按钮）
- 核心功能入口卡片（智能咨询、志愿推荐、数据查询）
- 简洁的 Hero 区域，突出产品价值
- 底部 Footer

### 3.2 登录/注册页
- 表单：手机号/邮箱 + 密码
- 支持短信验证码登录
- 注册后自动创建考生档案

### 3.3 考生信息填写页 (Onboarding)
- 分步骤表单（Stepper）：
  - Step 1: 基本信息（省份、科类/选科）
  - Step 2: 成绩信息（分数、位次）
  - Step 3: 兴趣偏好（专业方向、地域偏好）
- 进度条显示完成度
- 信息保存到后端考生档案

### 3.4 智能咨询页 (Chat) - 核心页面
- 左侧：对话历史列表（可切换不同会话）
- 右侧：对话区域
  - 顶部：当前会话标题
  - 中部：消息气泡流（用户右对齐、AI 左对齐）
  - 底部：输入框 + 发送按钮
- AI 消息支持：
  - 纯文本回复
  - 推荐卡片（院校信息卡片，可点击查看详情）
  - 快捷操作按钮（"查看详情"、"加入志愿表"）

### 3.5 志愿推荐结果页 (Recommendation)
- 顶部：考生信息摘要（分数、位次、省份）
- 三栏布局：
  - **冲刺** (20%): 录取概率 30-50% 的院校
  - **稳妥** (50%): 录取概率 50-80% 的院校
  - **保底** (30%): 录取概率 80%+ 的院校
- 每所院校卡片包含：
  - 校徽、校名、所在地
  - 推荐专业、录取概率（进度条）
  - 历年分数线趋势（迷你图表）
  - 操作按钮（"查看详情"、"加入志愿表"）

### 3.6 院校/专业详情页 (Detail)
- 院校基本信息（简介、标签、官网链接）
- 历年录取数据表格
- 专业列表及详细介绍
- 就业前景分析
- 相似院校对比

### 3.7 数据可视化页 (Analytics)
- 个人成绩分析雷达图
- 志愿方案风险评估
- 历年分数线趋势图
- 专业热度排行榜

## 四、组件设计

### 4.1 通用组件
- `AppLayout` - 整体布局（Header + Sidebar + Content + Footer）
- `NavHeader` - 顶部导航
- `ChatMessage` - 聊天消息气泡
- `RecommendationCard` - 推荐院校卡片
- `ProbabilityBadge` - 录取概率标签（绿/黄/红）
- `LoadingSkeleton` - 加载骨架屏

### 4.2 页面级组件
- `ChatPage` - 咨询对话主页面
- `RecommendationPage` - 推荐结果展示
- `CollegeDetailPage` - 院校详情
- `ProfileForm` - 考生信息表单
- `AnalyticsDashboard` - 数据可视化面板

## 五、状态管理 (Zustand)

```typescript
// stores/userStore.ts - 用户状态
interface UserState {
  user: User | null;
  isLoggedIn: boolean;
  login: (credentials) => Promise<void>;
  logout: () => void;
}

// stores/chatStore.ts - 对话状态
interface ChatState {
  sessions: ChatSession[];
  currentSessionId: string;
  messages: Message[];
  sendMessage: (text: string) => Promise<void>;
  createSession: () => void;
}

// stores/recommendationStore.ts - 推荐状态
interface RecommendationState {
  studentProfile: StudentProfile | null;
  recommendations: Recommendation[];
  isLoading: boolean;
  fetchRecommendations: () => Promise<void>;
}
```

## 六、API 接口设计

```typescript
// api/client.ts
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000,
});

// api/chat.ts
export const chatApi = {
  sendMessage: (sessionId: string, message: string) => 
    apiClient.post('/agent/chat', { sessionId, message }),
  getHistory: (sessionId: string) => 
    apiClient.get(`/agent/history/${sessionId}`),
};

// api/recommendation.ts
export const recommendationApi = {
  getRecommendations: (profile: StudentProfile) => 
    apiClient.post('/recommend', profile),
  getCollegeDetail: (collegeId: string) => 
    apiClient.get(`/colleges/${collegeId}`),
};
```

## 七、路由设计

| 路由 | 页面 | 说明 |
|------|------|------|
| `/` | 首页 | 产品介绍 + 功能入口 |
| `/login` | 登录页 | 用户登录 |
| `/register` | 注册页 | 用户注册 |
| `/onboarding` | 信息填写 | 考生信息录入（需登录） |
| `/chat` | 智能咨询 | AI 对话（核心页面） |
| `/chat/:sessionId` | 具体会话 | 指定会话的对话 |
| `/recommendations` | 志愿推荐 | 推荐结果展示 |
| `/colleges/:id` | 院校详情 | 具体院校信息 |
| `/analytics` | 数据分析 | 可视化图表 |

## 八、项目结构

```
cee-frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── api/              # API 请求封装
│   │   ├── client.ts
│   │   ├── chat.ts
│   │   ├── recommendation.ts
│   │   └── user.ts
│   ├── components/       # 通用组件
│   │   ├── ui/           # shadcn/ui 组件
│   │   ├── layout/
│   │   │   ├── AppLayout.tsx
│   │   │   ├── NavHeader.tsx
│   │   │   └── Sidebar.tsx
│   │   ├── chat/
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── ChatSidebar.tsx
│   │   └── recommendation/
│   │       ├── RecommendationCard.tsx
│   │       ├── ProbabilityBadge.tsx
│   │       └── CollegeMiniChart.tsx
│   ├── pages/            # 页面组件
│   │   ├── HomePage.tsx
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   ├── OnboardingPage.tsx
│   │   ├── ChatPage.tsx
│   │   ├── RecommendationPage.tsx
│   │   ├── CollegeDetailPage.tsx
│   │   └── AnalyticsPage.tsx
│   ├── stores/           # Zustand 状态管理
│   │   ├── userStore.ts
│   │   ├── chatStore.ts
│   │   └── recommendationStore.ts
│   ├── types/            # TypeScript 类型定义
│   │   ├── user.ts
│   │   ├── chat.ts
│   │   ├── recommendation.ts
│   │   └── college.ts
│   ├── hooks/            # 自定义 Hooks
│   │   ├── useAuth.ts
│   │   ├── useChat.ts
│   │   └── useRecommendation.ts
│   ├── lib/              # 工具函数
│   │   └── utils.ts
│   ├── App.tsx           # 根组件
│   ├── main.tsx          # 入口文件
│   └── index.css         # 全局样式
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
└── README.md
```

## 九、错误处理

| 场景 | 处理策略 |
|------|----------|
| API 请求失败 | 显示 Toast 错误提示，提供重试按钮 |
| 登录过期 | 自动跳转登录页，保留当前路由 |
| 数据加载中 | 显示 Skeleton 骨架屏 |
| 空状态 | 显示友好提示，引导用户操作 |

## 十、响应式设计

- **桌面端** (>1024px): 完整布局，侧边栏展开
- **平板端** (768-1024px): 侧边栏收起为图标
- **移动端** (<768px): 底部导航栏，单列布局

---

END OF DESIGN SPEC
