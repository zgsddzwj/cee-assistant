# 前端交互层 Implementation Plan

> **For agentic workers:** Use superpowers:subagent-driven-development or superpowers:executing-plans.

**Goal:** 构建基于 React + TypeScript + Vite 的高考志愿填报前端应用

**Architecture:** SPA 单页应用，React Router 管理路由，Zustand 管理状态，Axios 调用后端 API

**Tech Stack:** React 18 + TypeScript + Vite + React Router + Zustand + Tailwind CSS + Axios

---

## Task 1: 项目初始化与基础配置

**Files:** package.json, tsconfig.json, vite.config.ts, tailwind.config.js, index.html

- [ ] Step 1: 创建 package.json（含 React, TS, Vite, Tailwind, Zustand, Axios 依赖）
- [ ] Step 2: 创建 tsconfig.json（含 path alias `@/*`）
- [ ] Step 3: 创建 vite.config.ts（配置 React 插件和 path alias）
- [ ] Step 4: 创建 tailwind.config.js（配置 CSS 变量主题系统）
- [ ] Step 5: 创建 index.html
- [ ] Step 6: 运行 `npm install` 安装依赖
- [ ] Step 7: Commit

## Task 2: 全局样式与入口文件

**Files:** src/index.css, src/lib/utils.ts, src/main.tsx, src/App.tsx, src/pages/HomePage.tsx

- [ ] Step 1: 创建 index.css（Tailwind directives + CSS 变量主题）
- [ ] Step 2: 创建 lib/utils.ts（cn 工具函数合并 clsx + tailwind-merge）
- [ ] Step 3: 创建 main.tsx（React 根渲染）
- [ ] Step 4: 创建 App.tsx（BrowserRouter + 首页路由）
- [ ] Step 5: 创建 HomePage.tsx（占位：显示标题）
- [ ] Step 6: 运行 `npm run dev` 验证开发服务器
- [ ] Step 7: Commit

## Task 3: 类型定义与 API 客户端

**Files:** src/types/*.ts, src/api/client.ts

- [ ] Step 1: 创建 types/user.ts（User, StudentProfile 接口）
- [ ] Step 2: 创建 types/chat.ts（Message, ChatSession 接口）
- [ ] Step 3: 创建 types/recommendation.ts（College, Recommendation 接口）
- [ ] Step 4: 创建 api/client.ts（Axios 实例，含 token interceptor）
- [ ] Step 5: Commit

## Task 4: Zustand 状态管理

**Files:** src/stores/userStore.ts, src/stores/chatStore.ts

- [ ] Step 1: 创建 userStore（user, profile, isLoggedIn, setUser, logout）
- [ ] Step 2: 创建 chatStore（messages, isLoading, addMessage, setLoading）
- [ ] Step 3: Commit

## Task 5: 布局组件与路由

**Files:** src/components/layout/NavHeader.tsx, src/components/layout/AppLayout.tsx, src/App.tsx, src/pages/LoginPage.tsx, src/pages/ChatPage.tsx, src/pages/RecommendationPage.tsx

- [ ] Step 1: 创建 NavHeader（Logo + 导航链接 + 登录状态）
- [ ] Step 2: 创建 AppLayout（NavHeader + main content wrapper）
- [ ] Step 3: 更新 App.tsx（添加 /login, /chat, /recommendations 路由）
- [ ] Step 4: 创建 LoginPage.tsx（占位）
- [ ] Step 5: 创建 ChatPage.tsx（占位）
- [ ] Step 6: 创建 RecommendationPage.tsx（占位）
- [ ] Step 7: 验证路由切换正常
- [ ] Step 8: Commit

## Task 6: 首页实现

**Files:** src/pages/HomePage.tsx

- [ ] Step 1: 实现 Hero 区域（标题 + 副标题 + CTA 按钮）
- [ ] Step 2: 实现功能卡片区域（智能咨询 / 志愿推荐 / 院校查询）
- [ ] Step 3: 实现数据统计区域（3000+ 院校 / 500+ 专业 / AI 驱动）
- [ ] Step 4: Commit

## Task 7: 登录页实现

**Files:** src/pages/LoginPage.tsx

- [ ] Step 1: 实现登录表单（邮箱 + 密码 + 提交按钮）
- [ ] Step 2: 连接 userStore（登录后更新全局状态）
- [ ] Step 3: Commit

## Task 8: 智能咨询页实现

**Files:** src/components/chat/ChatMessage.tsx, src/components/chat/ChatInput.tsx, src/pages/ChatPage.tsx

- [ ] Step 1: 创建 ChatMessage（用户/AI 消息气泡，含头像和时间戳）
- [ ] Step 2: 创建 ChatInput（输入框 + 发送按钮）
- [ ] Step 3: 实现 ChatPage（消息列表 + 输入框 + Mock AI 回复）
- [ ] Step 4: Commit

## Task 9: 志愿推荐页实现

**Files:** src/components/recommendation/RecommendationCard.tsx, src/components/recommendation/ProbabilityBadge.tsx, src/pages/RecommendationPage.tsx

- [ ] Step 1: 创建 ProbabilityBadge（录取概率进度条 + 标签）
- [ ] Step 2: 创建 RecommendationCard（院校信息卡片）
- [ ] Step 3: 实现 RecommendationPage（Tab 切换：冲刺/稳妥/保底 + 卡片列表）
- [ ] Step 4: Commit

## Task 10: 项目文档

**Files:** cee-frontend/README.md

- [ ] Step 1: 创建 README.md（项目介绍 + 技术栈 + 快速开始 + 脚本说明）
- [ ] Step 2: Commit

---

## Self-Review Checklist

- [x] Spec coverage: 所有设计文档中的页面都有对应任务
- [x] Placeholder scan: 无 TBD/TODO 占位符
- [x] Type consistency: 类型定义在所有任务中保持一致
