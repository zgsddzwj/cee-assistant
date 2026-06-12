# 高考志愿填报助手 - 前端

基于 React + TypeScript + Vite 构建的高考志愿填报前端应用。

## 技术栈

- **React 18** - UI 框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **React Router** - 路由管理
- **Zustand** - 状态管理
- **Tailwind CSS** - 原子化样式
- **Axios** - HTTP 请求
- **Lucide React** - 图标库

## 快速开始

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 项目结构

```
src/
├── api/           # API 请求封装
├── components/    # 通用组件
│   ├── layout/    # 布局组件
│   ├── chat/      # 聊天组件
│   └── recommendation/  # 推荐组件
├── pages/         # 页面组件
├── stores/        # Zustand 状态管理
├── types/         # TypeScript 类型定义
├── lib/           # 工具函数
├── App.tsx        # 根组件
├── main.tsx       # 入口文件
└── index.css      # 全局样式
```

## 页面路由

| 路由 | 页面 | 说明 |
|------|------|------|
| `/` | 首页 | 产品介绍 + 功能入口 |
| `/login` | 登录页 | 用户登录 |
| `/chat` | 智能咨询 | AI 对话（核心页面） |
| `/recommendations` | 志愿推荐 | 推荐结果展示 |

## 开发计划

- [x] 项目初始化
- [x] 全局样式与路由
- [x] 类型定义与 API 客户端
- [x] 状态管理
- [x] 布局组件
- [x] 首页
- [x] 登录页
- [x] 智能咨询页
- [x] 志愿推荐页
- [ ] 院校详情页
- [ ] 数据可视化页
- [ ] 后端 API 对接
