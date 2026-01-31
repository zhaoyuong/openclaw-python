# Gateway WebSocket API 方法列表

> 完整的 Gateway WebSocket 方法清单（85个核心方法 + channel 扩展方法）

---

## ⚠️ 重要区分

**Agent 的功能 vs Gateway 的方法**

- **Agent Runtime** 只有一个核心功能：`run_turn(session, message)` → 调用 LLM，返回响应
- **Gateway** 提供 85 个方法，其中：
  - **2 个方法**调用 Agent：`agent`, `chat.send`
  - **83 个方法**是系统管理：配置、channels、sessions、日志、健康检查等

详见：[AGENT_VS_GATEWAY_METHODS.md](AGENT_VS_GATEWAY_METHODS.md)

---

## 方法总览

Gateway 提供 **85 个核心方法**，按功能分类如下：

| 分类 | 方法数量 | 说明 |
|------|----------|------|
| Agent & Chat | 7 | 与 AI Agent 对话 |
| Channels | 2 | 管理通信渠道（Telegram、Discord 等） |
| Sessions | 6 | 会话管理 |
| Configuration | 5 | 系统配置 |
| Models & Agents | 2 | 模型和代理管理 |
| Skills | 4 | 技能/工具管理 |
| Nodes | 7 | 分布式节点管理 |
| Devices | 5 | 设备配对和令牌管理 |
| Cron | 6 | 定时任务 |
| Exec Approvals | 6 | 执行审批 |
| Logs | 1 | 日志查看 |
| Health & Status | 4 | 系统健康状态 |
| TTS | 6 | 文本转语音 |
| Voice Wake | 2 | 语音唤醒 |
| Wizard | 4 | 向导流程 |
| System | 5 | 系统管理 |
| Talk Mode | 1 | 对话模式 |
| Browser | 1 | 浏览器请求 |
| Usage | 2 | 使用情况统计 |
| Update | 1 | 系统更新 |
| Web | (channel 扩展) | Web 相关方法 |

---

## 详细方法列表

### 1. Agent & Chat 方法 (7个)

与 AI Agent 交互和对话的方法。

| 方法 | 说明 | 是否调用 Agent | 使用场景 |
|------|------|---------------|----------|
| `agent` | 调用 Agent 处理消息 | ✅ 是 | CLI、自定义客户端直接调用 |
| `chat.send` | 发送 WebChat 消息 | ✅ 是 | Control UI 对话功能 |
| `agent.wait` | 等待 Agent 任务完成 | ⚠️ 间接 | 同步等待 Agent 响应 |
| `chat.abort` | 中止 Agent 运行 | ⚠️ 控制 | 停止当前对话 |
| `agent.identity.get` | 获取 Agent 身份信息 | ❌ 否 | 获取 Agent 名称、头像等（只是读配置） |
| `chat.history` | 获取对话历史 | ❌ 否 | 读取会话文件（不调用 Agent） |
| `send` | 通过指定 channel 发送消息 | ❌ 否 | 远程发送（通过 Bot 发送，不直接调用 Agent） |

**关键理解**：
- 只有 `agent` 和 `chat.send` 真正调用 `agent_runtime.run_turn()`
- 其他方法是辅助功能：获取历史、中止、查询信息等

**示例**：

```javascript
// Control UI 发送消息
await client.request("chat.send", {
  sessionKey: "ui-session-1",
  message: "你好",
  deliver: false
})

// CLI 调用 Agent
await client.request("agent", {
  message: "分析这段代码",
  sessionKey: "cli-session"
})

// 通过 Telegram 发送消息
await client.request("send", {
  channel: "telegram",
  to: "123456",
  message: "通知：任务完成"
})
```

---

### 2. Channels 方法 (2个)

管理通信渠道（Telegram、Discord、Slack 等）。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `channels.status` | 获取所有 channels 状态 | Read |
| `channels.logout` | 登出 channel 账号 | Admin |

**示例**：

```javascript
// 查看 Telegram Bot 状态
const status = await client.request("channels.status")
// 返回：
// {
//   telegram: { running: true, connected: true },
//   discord: { running: false, lastError: "not configured" }
// }

// 登出 Telegram
await client.request("channels.logout", {
  channel: "telegram"
})
```

---

### 3. Sessions 方法 (6个)

会话和对话历史管理。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `sessions.list` | 列出所有会话 | Read |
| `sessions.preview` | 预览会话内容 | Read |
| `sessions.patch` | 修改会话属性 | Admin |
| `sessions.reset` | 重置会话 | Admin |
| `sessions.delete` | 删除会话 | Admin |
| `sessions.compact` | 压缩会话存储 | Admin |

**示例**：

```javascript
// 列出所有会话
const sessions = await client.request("sessions.list")

// 预览会话
const preview = await client.request("sessions.preview", {
  sessionKey: "telegram:123456:main",
  limit: 10
})

// 删除会话
await client.request("sessions.delete", {
  sessionKey: "old-session"
})
```

---

### 4. Configuration 方法 (5个)

系统配置管理。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `config.get` | 获取配置 | Admin |
| `config.set` | 设置配置 | Admin |
| `config.apply` | 应用配置更改 | Admin |
| `config.patch` | 部分更新配置 | Admin |
| `config.schema` | 获取配置架构 | Admin |

**示例**：

```javascript
// 获取当前配置
const config = await client.request("config.get")

// 更新配置
await client.request("config.patch", {
  agents: {
    main: {
      model: "anthropic/claude-opus-4"
    }
  }
})

// 应用配置（重启相关服务）
await client.request("config.apply")
```

---

### 5. Models & Agents 方法 (2个)

模型和 Agent 管理。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `models.list` | 列出可用模型 | Read |
| `agents.list` | 列出所有 Agents | Read |

**示例**：

```javascript
// 列出模型
const models = await client.request("models.list")
// 返回：
// [
//   { id: "anthropic/claude-opus-4", name: "Claude Opus 4" },
//   { id: "openai/gpt-4", name: "GPT-4" },
//   ...
// ]

// 列出 Agents
const agents = await client.request("agents.list")
```

---

### 6. Skills 方法 (4个)

技能/工具管理。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `skills.status` | 获取技能状态 | Read |
| `skills.bins` | 列出技能可执行文件 | Node Role |
| `skills.install` | 安装技能 | Admin |
| `skills.update` | 更新技能 | Admin |

**示例**：

```javascript
// 查看技能状态
const skills = await client.request("skills.status")

// 安装技能
await client.request("skills.install", {
  name: "weather",
  source: "github:openclaw/skill-weather"
})
```

---

### 7. Nodes 方法 (7个)

分布式节点管理（用于扩展 OpenClaw 到多台机器）。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `node.list` | 列出所有节点 | Read |
| `node.describe` | 获取节点详情 | Read |
| `node.invoke` | 调用远程节点 | Write |
| `node.invoke.result` | 节点调用结果 | Node Role |
| `node.event` | 节点事件 | Node Role |
| `node.rename` | 重命名节点 | Pairing |
| `node.pair.*` | 节点配对相关 | Pairing |

---

### 8. Devices 方法 (5个)

设备配对和令牌管理。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `device.pair.list` | 列出配对设备 | Pairing |
| `device.pair.approve` | 批准设备配对 | Pairing |
| `device.pair.reject` | 拒绝设备配对 | Pairing |
| `device.token.rotate` | 轮换设备令牌 | Pairing |
| `device.token.revoke` | 撤销设备令牌 | Pairing |

---

### 9. Cron 方法 (6个)

定时任务管理。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `cron.list` | 列出所有定时任务 | Read |
| `cron.status` | 获取 Cron 状态 | Read |
| `cron.runs` | 获取任务运行历史 | Read |
| `cron.add` | 添加定时任务 | Admin |
| `cron.update` | 更新定时任务 | Admin |
| `cron.remove` | 删除定时任务 | Admin |
| `cron.run` | 手动触发任务 | Admin |

**示例**：

```javascript
// 添加定时任务
await client.request("cron.add", {
  id: "daily-report",
  schedule: "0 9 * * *",  // 每天 9:00
  action: {
    type: "agent",
    message: "生成每日报告",
    channel: "telegram",
    to: "123456"
  }
})

// 列出任务
const jobs = await client.request("cron.list")

// 手动触发
await client.request("cron.run", { id: "daily-report" })
```

---

### 10. Exec Approvals 方法 (6个)

执行审批管理（用于控制敏感操作）。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `exec.approvals.get` | 获取审批配置 | Admin |
| `exec.approvals.set` | 设置审批配置 | Admin |
| `exec.approvals.node.get` | 获取节点审批配置 | Admin |
| `exec.approvals.node.set` | 设置节点审批配置 | Admin |
| `exec.approval.request` | 请求审批 | Approvals |
| `exec.approval.resolve` | 批准/拒绝审批 | Approvals |

---

### 11. Logs 方法 (1个)

日志查看。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `logs.tail` | 实时查看日志 | Read |

---

### 12. Health & Status 方法 (4个)

系统健康状态。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `health` | 获取健康状态 | Read |
| `status` | 获取系统状态 | Read |
| `system-presence` | 获取系统在线状态 | Read |
| `last-heartbeat` | 获取最后心跳时间 | Read |

---

### 13. TTS 方法 (6个)

文本转语音。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `tts.status` | 获取 TTS 状态 | Read |
| `tts.providers` | 列出 TTS 提供商 | Read |
| `tts.enable` | 启用 TTS | Write |
| `tts.disable` | 禁用 TTS | Write |
| `tts.convert` | 转换文本为语音 | Write |
| `tts.setProvider` | 设置 TTS 提供商 | Write |

---

### 14. Voice Wake 方法 (2个)

语音唤醒。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `voicewake.get` | 获取唤醒词 | Read |
| `voicewake.set` | 设置唤醒词 | Write |

---

### 15. Wizard 方法 (4个)

向导流程（初始化配置等）。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `wizard.start` | 开始向导 | Admin |
| `wizard.next` | 向导下一步 | Admin |
| `wizard.cancel` | 取消向导 | Admin |
| `wizard.status` | 获取向导状态 | Admin |

---

### 16. System 方法 (5个)

系统管理。

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `system-event` | 发送系统事件 | - |
| `wake` | 唤醒系统 | Write |
| `set-heartbeats` | 设置心跳 | - |
| `usage.status` | 获取使用统计 | Read |
| `usage.cost` | 获取费用统计 | Read |

---

### 17. 其他方法 (4个)

| 方法 | 说明 | 权限要求 |
|------|------|----------|
| `talk.mode` | 设置对话模式 | Write |
| `browser.request` | 浏览器请求 | Write |
| `update.run` | 运行系统更新 | Admin |

---

## Gateway 事件列表 (11个)

除了方法调用，Gateway 还会主动推送事件：

| 事件 | 说明 | 触发时机 |
|------|------|----------|
| `connect.challenge` | 连接挑战 | 设备配对时 |
| `agent` | Agent 事件 | Agent 处理消息时 |
| `chat` | Chat 事件 | WebChat 对话时 |
| `presence` | 在线状态 | 定期广播 |
| `tick` | 定时心跳 | 每隔一段时间 |
| `health` | 健康状态 | 状态变化时 |
| `heartbeat` | 心跳事件 | 心跳任务时 |
| `cron` | Cron 事件 | 定时任务执行 |
| `shutdown` | 关闭通知 | 服务器关闭前 |
| `talk.mode` | 对话模式变化 | 模式切换时 |
| `voicewake.changed` | 唤醒词变化 | 唤醒词更新时 |
| `exec.approval.*` | 审批事件 | 审批请求/解决时 |
| `device.pair.*` | 设备配对事件 | 设备配对操作时 |
| `node.pair.*` | 节点配对事件 | 节点配对操作时 |
| `node.invoke.request` | 节点调用请求 | 调用远程节点时 |

---

## 权限系统

Gateway 使用基于角色和作用域的权限系统：

### 角色 (Roles)

| 角色 | 说明 | 权限 |
|------|------|------|
| `operator` | 操作员 | 根据 scopes 决定 |
| `node` | 远程节点 | 只能调用特定方法 |

### 作用域 (Scopes)

| 作用域 | 说明 | 包含的方法 |
|--------|------|------------|
| `operator.admin` | 管理员 | 所有方法 |
| `operator.read` | 只读 | health, logs.tail, channels.status 等 |
| `operator.write` | 读写 | send, agent, chat.send 等 |
| `operator.approvals` | 审批 | exec.approval.* |
| `operator.pairing` | 配对 | device.pair.*, node.pair.* |

**Control UI 的权限**：

```typescript
// ui/src/ui/gateway.ts Line 135
const scopes = ["operator.admin", "operator.approvals", "operator.pairing"];
const role = "operator";
```

Control UI 拥有全部权限（admin scope）。

---

## Channel 扩展方法

除了核心的 85 个方法，各个 channel 插件还可以注册自己的方法：

```typescript
// src/gateway/server-methods-list.ts Line 88
const channelMethods = listChannelPlugins().flatMap((plugin) => plugin.gatewayMethods ?? []);
```

例如：
- Telegram 插件可能添加：`telegram.sendPhoto`, `telegram.sendDocument` 等
- Discord 插件可能添加：`discord.sendEmbed`, `discord.reactToMessage` 等

---

## 使用示例

### 完整的 Control UI 连接流程

```typescript
// 1. 创建客户端
const client = new GatewayBrowserClient({
  url: 'ws://localhost:8765',
  clientName: "openclaw-control-ui",
  mode: "webchat",
  onHello: (hello) => {
    console.log("连接成功", hello);
  },
  onEvent: (evt) => {
    console.log("收到事件", evt);
  }
});

// 2. 启动连接
client.start();

// 3. 发送消息
await client.request("chat.send", {
  sessionKey: "ui-session-1",
  message: "你好",
  deliver: false
});

// 4. 查看 channels 状态
const status = await client.request("channels.status");

// 5. 查看模型列表
const models = await client.request("models.list");

// 6. 获取配置
const config = await client.request("config.get");
```

### CLI 工具使用

```python
# Python CLI 示例
import asyncio
import websockets
import json

async def call_agent():
    async with websockets.connect('ws://localhost:8765') as ws:
        # 握手
        await ws.send(json.dumps({
            "type": "req",
            "id": "1",
            "method": "connect",
            "params": {
                "maxProtocol": 3,
                "client": {"id": "cli", "version": "1.0"},
                "role": "operator",
                "scopes": ["operator.write"]
            }
        }))
        
        # 接收握手响应
        hello = json.loads(await ws.recv())
        print("Connected:", hello)
        
        # 调用 Agent
        await ws.send(json.dumps({
            "type": "req",
            "id": "2",
            "method": "agent",
            "params": {
                "message": "Hello from CLI",
                "sessionKey": "cli-session"
            }
        }))
        
        # 接收响应
        response = json.loads(await ws.recv())
        print("Response:", response)

asyncio.run(call_agent())
```

---

## 总结

Gateway WebSocket API 提供了：

- ✅ **85+ 核心方法**：覆盖所有系统功能
- ✅ **11+ 事件类型**：实时推送系统状态
- ✅ **权限系统**：基于角色和作用域的访问控制
- ✅ **扩展性**：Channel 插件可添加自定义方法
- ✅ **多种客户端**：Control UI、CLI、iOS App、自定义应用

这就是为什么不是所有软件都需要自己的 bot — Gateway 提供了完整的 API，客户端可以直接通过 WebSocket 与系统交互！

---

## 相关文档

- [WEBSOCKET_VS_TELEGRAM.md](WEBSOCKET_VS_TELEGRAM.md) - WebSocket vs Telegram 对比
- [CONTROL_UI_EXPLAINED.md](CONTROL_UI_EXPLAINED.md) - Control UI 详解
- [GATEWAY_ARCHITECTURE.md](GATEWAY_ARCHITECTURE.md) - Gateway 架构说明

---

**源代码位置**：
- TypeScript: `openclaw/src/gateway/server-methods-list.ts`
- Python: `openclaw-python/openclaw/gateway/handlers.py`
