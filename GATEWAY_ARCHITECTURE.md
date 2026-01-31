# Gateway 架构说明（修正版）

> OpenClaw Python 的 Gateway 连接架构详解 - 准确反映实际实现

---

## 目录

1. [核心理解](#核心理解)
2. [Gateway 的三个职责](#gateway-的三个职责)
3. [完整架构图](#完整架构图)
4. [消息流程详解](#消息流程详解)
5. [代码实现](#代码实现)
6. [常见误解澄清](#常见误解澄清)

---

## 核心理解

### 关键事实

**Telegram Bot 不通过 WebSocket 连接 Gateway！**

正确的理解：
- Telegram Bot 是**服务器端插件**，在同一进程内运行
- Bot 通过 **HTTP Long Polling** 连接 Telegram API
- Bot 通过 **Python 函数调用** 访问 Agent Runtime
- Gateway **管理** Bot 的生命周期（启动/停止）
- Gateway 通过 **WebSocket** 服务外部客户端（UI/CLI/Mobile）

### 三种不同的连接方式

```
1. Bot ↔ Telegram API
   协议：HTTP Long Polling
   目的：接收和发送用户消息

2. Bot ↔ Agent Runtime
   协议：Python 函数调用（同一进程内）
   目的：处理消息，生成回复

3. Gateway ↔ 外部客户端
   协议：WebSocket
   目的：为 Control UI、CLI、移动应用提供 API
```

---

## Gateway 的三个职责

### 职责 1：Channel 生命周期管理

Gateway 负责启动、停止和监控 channel 插件。

#### TypeScript 参考实现

```typescript
// src/gateway/server-channels.ts
class ChannelManager {
  private channels = new Map<string, ChannelRuntime>();
  
  async startChannel(channelId: string, accountId: string) {
    const plugin = getChannelPlugin(channelId);
    
    // Gateway 调用插件的启动方法
    const runtime = await plugin.gateway.startAccount({
      cfg: this.config,
      accountId,
      runtime: this.runtime,
      abortSignal: this.abortSignal
    });
    
    this.channels.set(`${channelId}:${accountId}`, runtime);
  }
  
  async stopChannel(channelId: string, accountId: string) {
    const key = `${channelId}:${accountId}`;
    const runtime = this.channels.get(key);
    
    if (runtime?.stop) {
      await runtime.stop();
    }
    
    this.channels.delete(key);
  }
  
  getRuntimeSnapshot() {
    return Array.from(this.channels.entries()).map(([key, runtime]) => ({
      channel: key.split(':')[0],
      account: key.split(':')[1],
      status: runtime.status || 'running'
    }));
  }
}
```

#### Python 实现

```python
# examples/10_gateway_telegram_bridge.py
class IntegratedOpenClawServer:
    """Gateway 管理 channels 的生命周期"""
    
    def __init__(self, config):
        self.config = config
        self.channels = {}  # channel_id -> channel_instance
        self.gateway_server = GatewayServer(config)
        
    async def start_channel(self, channel_id: str, config: dict):
        """启动 channel（Gateway 调用）"""
        if channel_id == "telegram":
            channel = EnhancedTelegramChannel()
            
            # 设置消息处理器
            channel.set_message_handler(
                self.create_message_handler(channel_id)
            )
            
            # 启动 channel
            await channel.start(config)
            
            # 注册到 registry
            self.channels[channel_id] = channel
            
    async def stop_channel(self, channel_id: str):
        """停止 channel（Gateway 调用）"""
        if channel_id in self.channels:
            await self.channels[channel_id].stop()
            del self.channels[channel_id]
    
    def get_channel_status(self):
        """获取所有 channels 状态"""
        return {
            channel_id: {
                "running": channel.is_running(),
                "healthy": channel.is_healthy()
            }
            for channel_id, channel in self.channels.items()
        }
```

### 职责 2：WebSocket API 服务

Gateway 为外部客户端提供 WebSocket 接口。

#### 支持的方法

```python
# openclaw/gateway/handlers.py

@register_handler("agent")
async def handle_agent(connection, params):
    """
    外部客户端通过 Gateway 发送消息给 Agent
    
    请求示例：
    {
      "type": "req",
      "id": "1",
      "method": "agent",
      "params": {
        "message": "Hello",
        "sessionId": "session-1"
      }
    }
    """
    message = params["message"]
    session_id = params.get("sessionId", "main")
    
    # Gateway 调用 Agent
    session = session_manager.get_session(session_id)
    
    # 流式返回结果
    async for event in agent_runtime.run_turn(session, message):
        await connection.send_event("agent", {
            "sessionId": session_id,
            "type": event.type,
            "data": event.data
        })

@register_handler("channels.list")
async def handle_channels_list(connection, params):
    """
    列出所有 channels 及其状态
    
    响应示例：
    {
      "type": "res",
      "id": "1",
      "ok": true,
      "payload": [
        {
          "id": "telegram",
          "label": "Telegram",
          "running": true,
          "healthy": true
        }
      ]
    }
    """
    channels = []
    for channel_id, channel in server.channels.items():
        channels.append({
            "id": channel_id,
            "label": channel.label,
            "running": channel.is_running(),
            "healthy": channel.is_healthy()
        })
    return channels

@register_handler("send")
async def handle_send(connection, params):
    """
    通过指定 channel 发送消息
    
    请求示例：
    {
      "type": "req",
      "id": "2",
      "method": "send",
      "params": {
        "channel": "telegram",
        "to": "123456",
        "message": "Hello from Gateway!"
      }
    }
    """
    channel_id = params["channel"]
    to = params["to"]
    message = params["message"]
    
    # Gateway 调用 channel 的发送方法
    channel = server.channels.get(channel_id)
    if channel:
        await channel.send_text(to, message)
        return {"sent": True}
    else:
        raise ValueError(f"Channel {channel_id} not found")
```

### 职责 3：事件广播

Agent 处理消息时会发送事件，Gateway 广播给所有 WebSocket 客户端。

#### 事件流程

```python
# 1. Agent Runtime 发送事件
class AgentRuntime:
    async def run_turn(self, session, message):
        # 发送开始事件
        self._emit_event({
            "type": "agent.start",
            "sessionId": session.id,
            "message": message
        })
        
        # 处理消息
        async for chunk in llm.stream(message):
            # 发送文本事件
            self._emit_event({
                "type": "agent.text",
                "sessionId": session.id,
                "text": chunk
            })
        
        # 发送完成事件
        self._emit_event({
            "type": "agent.done",
            "sessionId": session.id
        })

# 2. Gateway 监听并广播事件
class GatewayServer:
    def __init__(self):
        self.connections = set()
        
        # 订阅 Agent 事件
        agent_event_bus.subscribe(self.on_agent_event)
    
    async def on_agent_event(self, event):
        """收到 Agent 事件，广播给所有客户端"""
        await self.broadcast_event(event["type"], event)
    
    async def broadcast_event(self, event_type, payload):
        """广播给所有连接的 WebSocket 客户端"""
        disconnected = set()
        
        for connection in self.connections:
            try:
                await connection.send_event(event_type, payload)
            except Exception as e:
                logger.error(f"Failed to send to client: {e}")
                disconnected.add(connection)
        
        # 清理断开的连接
        self.connections -= disconnected
```

#### 事件类型

```python
# 常见事件类型
AGENT_EVENTS = {
    "agent.start": "Agent 开始处理",
    "agent.text": "Agent 生成文本",
    "agent.tool_use": "Agent 调用工具",
    "agent.done": "Agent 完成处理",
    "agent.error": "Agent 发生错误",
}

CHANNEL_EVENTS = {
    "channel.message": "Channel 收到消息",
    "channel.started": "Channel 启动",
    "channel.stopped": "Channel 停止",
    "channel.error": "Channel 错误",
}

SYSTEM_EVENTS = {
    "system.startup": "系统启动",
    "system.shutdown": "系统关闭",
}
```

---

## 完整架构图

### 组件关系图

```
┌────────────────────────────────────────────────────────────────┐
│                OpenClaw Server (单个 Python 进程)               │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                  Gateway Server                          │ │
│  │                                                          │ │
│  │  职责1: 生命周期管理                                      │ │
│  │    • startChannel("telegram", config)                   │ │
│  │    • stopChannel("telegram")                            │ │
│  │    • getChannelStatus()                                 │ │
│  │                                                          │ │
│  │  职责2: WebSocket API (ws://localhost:8765)             │ │
│  │    • handle("agent", params)                            │ │
│  │    • handle("send", params)                             │ │
│  │    • handle("channels.list")                            │ │
│  │                                                          │ │
│  │  职责3: 事件广播                                          │ │
│  │    • broadcastEvent("agent.text", data)                │ │
│  │    • broadcastEvent("channel.message", data)           │ │
│  └────────┬─────────────────────────────────────────┬──────┘ │
│           │ manages                                 │ broadcasts
│           │ (start/stop/monitor)                    │          │
│           ↓                                         ↓          │
│  ┌─────────────────────┐               ┌─────────────────────┐│
│  │   Telegram Bot      │  函数调用     │   Agent Runtime     ││
│  │    (Channel)        │ ─────────────→│                     ││
│  │                     │ ←─────────────│  • Session Manager  ││
│  │ - Long Polling      │   返回值      │  • Tool Registry    ││
│  │ - Message Handler   │               │  • LLM Providers    ││
│  │ - Send Messages     │               │  • Event Emitter    ││
│  └──────────┬──────────┘               └─────────────────────┘│
│             │                                     │            │
└─────────────┼─────────────────────────────────────┼────────────┘
              │ HTTP                                │
              │ Long Polling/POST                   │ HTTPS
              ↓                                     ↓
   ┌──────────────────┐                  ┌──────────────────┐
   │  Telegram API    │                  │    LLM APIs      │
   │    服务器        │                  │ Claude/GPT/Gemini│
   └──────────────────┘                  └──────────────────┘
              ↑
              │
         Telegram 用户
```

### 数据流程图

```
用户发送消息 "Hello"
        │
        ↓ (Telegram 客户端)
   Telegram API
        │
        ↓ (HTTP Long Polling)
   Telegram Bot
        │
        ↓ (函数调用)
   handle_telegram_message(message)
        │
        ↓ (函数调用)
   session_manager.get_session(session_id)
        │
        ↓ (函数调用)
   agent_runtime.run_turn(session, "Hello")
        │
        ├──→ emit_event("agent.start")  ─→  Gateway ─→ 广播给 WebSocket 客户端
        │
        ↓ (HTTPS)
   LLM API (Claude/GPT)
        │
        ↓ (返回响应)
   Agent Runtime
        │
        ├──→ emit_event("agent.text")   ─→  Gateway ─→ 广播给 WebSocket 客户端
        │
        ↓ (函数返回)
   handle_telegram_message 收到响应
        │
        ↓ (函数调用)
   telegram_channel.send_text(chat_id, response)
        │
        ↓ (HTTP POST)
   Telegram API
        │
        ├──→ emit_event("agent.done")   ─→  Gateway ─→ 广播给 WebSocket 客户端
        │
        ↓ (推送)
   Telegram 客户端
        │
        ↓
   用户看到回复
```

---

## 消息流程详解

### Scenario 1: Telegram 用户发送消息

```python
# 步骤 1: Telegram Bot 轮询
while True:
    updates = await telegram_api.get_updates()  # HTTP GET
    for update in updates:
        await handle_update(update)

# 步骤 2: 处理消息（内部方法）
async def handle_update(update):
    message = update.message
    
    # 创建标准化消息
    inbound = InboundMessage(
        channel_id="telegram",
        text=message.text,
        sender_id=str(message.from_user.id),
        chat_id=str(message.chat.id)
    )
    
    # 调用用户设置的处理器（函数调用！）
    await message_handler(inbound)

# 步骤 3: 用户处理器（在 IntegratedOpenClawServer 中定义）
async def message_handler(message: InboundMessage):
    # 获取 session（函数调用）
    session = session_manager.get_session(f"telegram-{message.chat_id}")
    
    # 调用 Agent（函数调用）
    response = ""
    async for event in agent_runtime.run_turn(session, message.text):
        if event.type == "agent.text":
            response += event.data["text"]
        
        # Agent 发送事件
        # Gateway 自动广播给 WebSocket 客户端
    
    # 发送回复（HTTP POST）
    await telegram_channel.send_text(message.chat_id, response)
```

### Scenario 2: WebSocket 客户端通过 Gateway 发送消息

```python
# 步骤 1: 客户端连接
ws = websocket.connect("ws://localhost:8765")

# 步骤 2: 握手
ws.send({
    "type": "req",
    "id": "1",
    "method": "connect",
    "params": {
        "maxProtocol": 1,
        "client": {"name": "web-ui", "version": "1.0", "platform": "web"}
    }
})

# 步骤 3: 发送消息到 Agent
ws.send({
    "type": "req",
    "id": "2",
    "method": "agent",
    "params": {
        "message": "Hello from Web!",
        "sessionId": "web-session"
    }
})

# 步骤 4: Gateway 处理
async def handle_agent_request(connection, params):
    session = session_manager.get_session(params["sessionId"])
    
    # 调用 Agent（函数调用）
    async for event in agent_runtime.run_turn(session, params["message"]):
        # 流式发送事件给客户端
        await connection.send_event("agent", {
            "type": event.type,
            "data": event.data
        })

# 步骤 5: 客户端接收事件
ws.on_message(event => {
    // { type: "event", event: "agent", payload: {...} }
    console.log(event.payload);
});
```

---

## 代码实现

### 集成服务器实现

```python
# examples/10_gateway_telegram_bridge.py
class IntegratedOpenClawServer:
    """
    集成 Gateway + Channels + Agent 的完整服务器
    
    展示了：
    1. Gateway 如何管理 Channel 生命周期
    2. Channel 如何通过函数调用访问 Agent
    3. Gateway 如何广播事件给 WebSocket 客户端
    """
    
    def __init__(self, config: ClawdbotConfig):
        # 核心组件
        self.session_manager = SessionManager(workspace)
        self.agent_runtime = AgentRuntime(...)
        self.gateway_server = GatewayServer(config)
        self.channels = {}
        
    async def setup_telegram(self, bot_token: str):
        """
        Gateway 管理 Telegram 生命周期
        
        这个方法展示了 Gateway 的职责1：生命周期管理
        """
        # 创建 channel
        telegram = EnhancedTelegramChannel()
        
        # 设置消息处理器
        async def handle_message(message: InboundMessage):
            # 这里展示了函数调用（不是网络请求）
            session = self.session_manager.get_session(...)
            
            # 调用 Agent（函数调用）
            response = ""
            async for event in self.agent_runtime.run_turn(...):
                response += event.data.get("text", "")
            
            # 发送回复
            await telegram.send_text(message.chat_id, response)
            
            # 广播事件（Gateway 的职责3）
            await self.gateway_server.broadcast_event("chat", {
                "channel": "telegram",
                "message": message.text,
                "response": response
            })
        
        telegram.set_message_handler(handle_message)
        
        # 启动 channel
        await telegram.start({"bot_token": bot_token})
        
        # 注册
        self.channels["telegram"] = telegram
    
    async def start(self):
        """启动服务器"""
        # 启动 Telegram
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if bot_token:
            await self.setup_telegram(bot_token)
        
        # 启动 Gateway（并行运行）
        gateway_task = asyncio.create_task(
            self.gateway_server.start()
        )
        
        await gateway_task
```

### Gateway Server 实现

```python
# openclaw/gateway/server.py
class GatewayServer:
    """
    Gateway 服务器实现
    
    职责：
    1. 生命周期管理（通过 IntegratedOpenClawServer）
    2. WebSocket API 服务
    3. 事件广播
    """
    
    def __init__(self, config: ClawdbotConfig):
        self.config = config
        self.connections = set()
        self.running = False
        
    async def handle_connection(self, websocket):
        """处理新的 WebSocket 连接（职责2）"""
        connection = GatewayConnection(websocket, self.config)
        self.connections.add(connection)
        
        try:
            async for message in websocket:
                await connection.handle_message(message)
        finally:
            self.connections.discard(connection)
    
    async def broadcast_event(self, event: str, payload: Any):
        """广播事件给所有客户端（职责3）"""
        disconnected = set()
        
        for connection in self.connections:
            try:
                await connection.send_event(event, payload)
            except Exception as e:
                logger.error(f"Failed to broadcast: {e}")
                disconnected.add(connection)
        
        self.connections -= disconnected
    
    async def start(self):
        """启动 WebSocket 服务器"""
        host = "127.0.0.1"
        port = self.config.gateway.port
        
        logger.info(f"Starting Gateway on ws://{host}:{port}")
        self.running = True
        
        async with websockets.serve(self.handle_connection, host, port):
            while self.running:
                await asyncio.sleep(1)
```

---

## 常见误解澄清

### ❌ 误解 1：Telegram Bot 通过 WebSocket 连接 Gateway

**错误图示**：
```
Telegram Bot (客户端) ─WebSocket→ Gateway Server
```

**正确理解**：
```
Gateway (管理器) ─start/stop→ Telegram Bot (插件)
Telegram Bot ─函数调用→ Agent Runtime
Gateway ─WebSocket→ 外部客户端 (UI/CLI)
```

### ❌ 误解 2：消息必须通过 Gateway 路由

**错误流程**：
```
User → Telegram API → Gateway → Telegram Bot → Agent
```

**正确流程**：
```
User → Telegram API → Telegram Bot ─函数调用→ Agent
                                       ↓
                                   发送事件
                                       ↓
                                    Gateway ─广播→ WebSocket 客户端
```

### ❌ 误解 3：配对（Pairing）是设备连接

**错误理解**：认为配对是让设备通过 WebSocket 连接到 Gateway

**正确理解**：配对是用户授权机制
- 用途：控制哪些 Telegram 用户可以私聊 Bot
- 流程：用户 → 获取配对码 → 管理员批准 → 用户进入 allowlist
- 实现：存储在服务器端的 allowlist

### ✅ 正确理解总结

1. **Telegram Bot 是服务器端插件**
   - 在同一个 Python 进程中运行
   - 由 Gateway 管理生命周期
   - 通过函数调用访问 Agent

2. **Gateway 的三个职责**
   - 生命周期管理：start/stop channels
   - WebSocket API：服务外部客户端
   - 事件广播：分发 Agent 事件

3. **通信方式**
   - Bot ↔ Telegram API：HTTP
   - Bot ↔ Agent：函数调用
   - Gateway ↔ 客户端：WebSocket

---

## 参考文档

- [TELEGRAM_CONNECTION_EXPLAINED.md](TELEGRAM_CONNECTION_EXPLAINED.md) - Telegram 连接详解
- [examples/10_gateway_telegram_bridge.py](examples/10_gateway_telegram_bridge.py) - 完整实现示例
- [README.md](README.md) - 项目概述

---

**现在你应该完全理解 Gateway 在 OpenClaw 架构中的真实作用了！** 🎉
