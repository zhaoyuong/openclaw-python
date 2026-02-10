# Control UI 设置指南

## 概述

Control UI 是 OpenClaw 的 Web 管理界面，使用 Lit (Web Components) 构建。

**技术栈**:
- **框架**: Lit 3.3.2 (Web Components)
- **构建**: Vite 7.3.1
- **加密**: @noble/ed25519 (设备认证)
- **Markdown**: marked 17.0.1
- **安全**: dompurify 3.3.1

**通信**:
- WebSocket 协议版本 3
- RPC 方法调用
- 实时事件推送

---

## 快速启动

### 1. 安装依赖

```bash
cd control-ui
npm install
```

### 2. 构建生产版本

```bash
npm run build
```

构建输出到 `openclaw/static/control-ui/`

### 3. 启动 Gateway

```bash
cd ..
openclaw gateway run
```

### 4. 访问 UI

打开浏览器访问: http://localhost:18789/

---

## 开发模式

### 启动开发服务器

```bash
# Terminal 1: Python Gateway
cd openclaw-python
openclaw gateway run

# Terminal 2: Vite dev server
cd control-ui
npm run dev
```

访问: http://localhost:5173/

**优势**:
- 热重载 (Hot Module Replacement)
- 快速刷新
- 源码映射 (Source Maps)

---

## 架构

### UI 结构

```
control-ui/
├── index.html              # HTML 入口
├── package.json            # 依赖配置
├── vite.config.ts          # Vite 构建配置
├── .env                    # 环境变量
└── src/
    ├── main.ts             # 应用入口
    ├── styles.css          # 全局样式
    └── ui/
        ├── app.ts          # 主应用组件 (OpenClawApp)
        ├── gateway.ts      # WebSocket 客户端
        ├── controllers/    # 业务逻辑层
        │   ├── chat.ts
        │   ├── config.ts
        │   ├── channels.ts
        │   └── ...
        └── views/          # 视图组件层
            ├── chat.ts
            ├── config.ts
            ├── channels.ts
            └── ...
```

### 通信架构

```
Browser (Lit UI)
    ↕ WebSocket (Protocol v3)
Python Gateway
    ↕ Agent Runtime
```

**RPC 方法示例**:
- `chat.send` - 发送消息
- `chat.history` - 获取历史
- `config.get` - 获取配置
- `config.set` - 设置配置
- `channels.list` - 列出频道
- `sessions.list` - 列出会话

**事件示例**:
- `agent` - Agent 事件
- `chat` - 聊天事件 (delta/final/error)
- `presence` - 在线状态
- `cron` - 定时任务

---

## 配置

### 环境变量 (.env)

```env
# Gateway WebSocket URL (development)
VITE_GATEWAY_WS_URL=ws://localhost:18789/ws

# Production uses relative path
# VITE_GATEWAY_WS_URL=/ws
```

### Vite 配置

关键配置项:
- `base`: 部署基础路径 (默认 `./`)
- `build.outDir`: 构建输出目录
- `server.port`: 开发服务器端口 (5173)
- `server.proxy`: API 代理配置 (开发模式)

---

## 视图功能

### Chat 视图
- 实时对话
- Streaming 响应
- 工具调用展示
- 历史记录

### Config 视图
- 配置编辑
- 实时验证
- 应用配置

### Channels 视图
- 频道管理
- 账号配置
- 状态监控

### Sessions 视图
- 会话列表
- 会话切换
- 会话历史

### Cron 视图
- 定时任务管理
- 任务调度
- 运行日志

### Skills 视图
- Skills 浏览
- 远程 Skills
- Skills 配置

---

## 常见问题

### Q: UI 不显示？

**检查**:
1. 是否运行了 `npm run build`?
2. `openclaw/static/control-ui/` 目录是否存在?
3. Gateway 是否正常启动?

### Q: WebSocket 连接失败？

**检查**:
1. Gateway 端口是否为 18789?
2. 防火墙是否阻止?
3. 查看浏览器控制台错误

### Q: 如何自定义 UI？

**步骤**:
1. 修改 `control-ui/src/` 中的源码
2. 开发模式测试: `npm run dev`
3. 构建: `npm run build`
4. 重启 Gateway

---

## 性能优化

### 生产构建

```bash
npm run build
```

**优化**:
- 代码分割 (Code splitting)
- Tree shaking
- 压缩和混淆
- Source maps

### 缓存策略

静态资源使用长期缓存:
- `assets/*.js` - 内容哈希命名
- `index.html` - 不缓存

---

## 故障排除

### 构建失败

```bash
# 清除缓存
rm -rf node_modules package-lock.json
npm install

# 重新构建
npm run build
```

### 开发服务器端口冲突

修改 `vite.config.ts`:
```typescript
server: {
  port: 5174,  // 改为其他端口
}
```

---

## 更新 UI

### 从 TypeScript 版本同步

```bash
cd /path/to/openclaw
git pull

cd /path/to/openclaw-python
cp -r ../openclaw/ui/ ./control-ui/

# 重新构建
cd control-ui
npm install
npm run build
```

---

## 技术细节

### Lit Web Components

主组件 `OpenClawApp`:
```typescript
@customElement('openclaw-app')
export class OpenClawApp extends LitElement {
  @state() private view = 'chat';
  @state() private connected = false;
  
  render() {
    return html`...`;
  }
}
```

### WebSocket 客户端

```typescript
class GatewayBrowserClient {
  async connect() {...}
  async request(method: string, params: any) {...}
  onEvent(handler: (event) => void) {...}
}
```

### 状态管理

使用 Lit 的响应式属性:
- `@state()` - 内部状态
- `@property()` - 外部属性
- `@query()` - DOM 查询

---

## 资源

- **Lit 文档**: https://lit.dev/
- **Vite 文档**: https://vitejs.dev/
- **OpenClaw 文档**: ../README.md

---

**Control UI v1.0.0**  
**完全对齐 TypeScript 版本** ✅
