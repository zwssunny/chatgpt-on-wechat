# Claude 模型配置指南

## 概述

CowAgent 支持 Anthropic 公司的 Claude 系列大语言模型。Claude 是 Anthropic 开发的 AI 助手，以其强大的推理能力、长上下文处理和安全性而闻名。在 CowAgent 中，您可以使用 Claude 模型作为核心 AI 引擎，支持 Agent 模式下的复杂任务规划、工具调用和长期记忆功能。

> **Agent 模式推荐模型**：`claude-sonnet-4-5` 和 `claude-sonnet-4-0` 是专门为 Agent 任务优化的模型，具备优秀的任务规划能力和工具调用能力。

## 支持的 Claude 模型

CowAgent 支持以下 Claude 模型：

| 模型名称 | 标识符 | 描述 | 推荐用途 |
|---------|--------|------|---------|
| Claude Sonnet 4.5 | `claude-sonnet-4-5` | Claude Sonnet 4.5 最新版，Agent 推荐模型 | Agent 模式、复杂任务规划 |
| Claude Sonnet 4.0 | `claude-sonnet-4-0` | Claude Sonnet 4.0，Agent 推荐模型 | Agent 模式、一般任务 |
| Claude Opus 4.0 | `claude-opus-4-0` | Claude Opus 4.0，最强大的 Claude 模型 | 高复杂度推理任务 |
| Claude 3.5 Sonnet 最新版 | `claude-3-5-sonnet-latest` | Claude 3.5 Sonnet 最新版本 | 通用任务、代码生成 |
| Claude 3.5 Sonnet 2024-10-22 | `claude-3-5-sonnet-20241022` | 固定版本的 Claude 3.5 Sonnet | 版本稳定性要求高的场景 |
| Claude 3.5 Sonnet 2024-06-20 | `claude-3-5-sonnet-20240620` | 早期版本的 Claude 3.5 Sonnet | 兼容性测试 |
| Claude 3 Opus 最新版 | `claude-3-opus-latest` | Claude 3 Opus 最新版本 | 复杂推理和分析 |
| Claude 3 Opus 2024-02-29 | `claude-3-opus-20240229` | 固定版本的 Claude 3 Opus | 历史版本兼容 |
| Claude 3 Sonnet 2024-02-29 | `claude-3-sonnet-20240229` | Claude 3 Sonnet 固定版本 | 一般任务 |
| Claude 3 Haiku 2024-03-07 | `claude-3-haiku-20240307` | Claude 3 Haiku，轻量快速模型 | 简单查询、低成本场景 |

## 配置步骤

### 1. 获取 Claude API 密钥

1. 访问 [Anthropic 控制台](https://console.anthropic.com/)
2. 注册或登录您的账户
3. 在 API 密钥页面创建新的 API 密钥
4. 复制生成的密钥（以 `sk-ant-` 开头）

### 2. 配置 CowAgent

#### 方法一：通过配置文件配置

编辑项目根目录下的 `config.json` 文件，添加或修改以下配置项：

```json
{
  "model": "claude-sonnet-4-5",
  "claude_api_key": "sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "claude_api_base": "https://api.anthropic.com",
  "bot_type": "chatGPT",
  "agent": true,
  "agent_max_context_tokens": 40000,
  "agent_max_context_turns": 20,
  "agent_max_steps": 15
}
```

#### 方法二：通过环境变量配置

您也可以通过环境变量配置 Claude API：

```bash
export CLAUDE_API_KEY="sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export CLAUDE_API_BASE="https://api.anthropic.com"
export MODEL="claude-sonnet-4-5"
```

#### 方法三：使用 LinkAI 平台中转

如果直接访问 Anthropic API 有困难，可以使用 LinkAI 平台作为中转：

```json
{
  "model": "claude-sonnet-4-5",
  "claude_api_key": "您的LinkAI平台API密钥",
  "claude_api_base": "https://api.link-ai.tech/anthropic",
  "use_linkai": true,
  "linkai_api_key": "您的LinkAI平台API密钥"
}
```

### 3. 配置说明

| 配置项 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `model` | 是 | - | 要使用的 Claude 模型标识符 |
| `claude_api_key` | 是 | - | Claude API 密钥或 LinkAI 平台 API 密钥 |
| `claude_api_base` | 否 | `"https://api.anthropic.com"` | Claude API 基础地址 |
| `bot_type` | 是 | `"chatGPT"` | 机器人类型，使用 Claude 时也设置为 `"chatGPT"` |
| `agent` | 否 | `false` | 是否启用 Agent 模式 |
| `agent_max_context_tokens` | 否 | `40000` | Agent 模式最大上下文 token 数 |
| `agent_max_context_turns` | 否 | `20` | Agent 模式最大上下文轮次 |
| `agent_max_steps` | 否 | `15` | Agent 模式最大执行步骤 |

## 配置示例

### 示例 1：基础配置（Agent 模式）

```json
{
  "channel_type": "web",
  "model": "claude-sonnet-4-5",
  "claude_api_key": "sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "claude_api_base": "https://api.anthropic.com",
  "bot_type": "chatGPT",
  "agent": true,
  "agent_max_context_tokens": 40000,
  "agent_max_context_turns": 20,
  "agent_max_steps": 15
}
```

### 示例 2：使用 LinkAI 平台中转

```json
{
  "channel_type": "feishu",
  "model": "claude-sonnet-4-0",
  "claude_api_key": "lk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "claude_api_base": "https://api.link-ai.tech/anthropic",
  "bot_type": "chatGPT",
  "use_linkai": true,
  "linkai_api_key": "lk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "agent": true
}
```

### 示例 3：多模型备用配置

```json
{
  "channel_type": "dingtalk",
  "model": "claude-sonnet-4-5",
  "claude_api_key": "sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "open_ai_api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "bot_type": "chatGPT",
  "agent": true,
  "agent_fallback_models": ["claude-sonnet-4-0", "gpt-4o"]
}
```

## 使用说明

### 1. 启动 CowAgent

配置完成后，启动 CowAgent：

```bash
# 使用启动脚本
bash <(curl -sS https://cdn.link-ai.tech/code/cow/run.sh)

# 或手动启动
python app.py
```

### 2. 验证配置

启动后，检查日志确认 Claude 模型已正确加载：

```
[INFO] 加载模型: claude-sonnet-4-5
[INFO] Claude API 配置成功
[INFO] Agent 模式已启用，最大上下文: 40000 tokens
```

### 3. 测试对话

通过配置的渠道（Web、飞书、钉钉等）发送测试消息，验证 Claude 模型是否正常工作。

## 注意事项

### 1. 成本控制

Claude 模型的定价因版本而异，使用前请了解相关费用：
- **Claude Opus**：最高性能，价格最高
- **Claude Sonnet**：平衡性能与成本，适合大多数 Agent 任务
- **Claude Haiku**：轻量快速，成本最低

Agent 模式下 Token 消耗较高，建议：
- 合理设置 `agent_max_context_tokens`（默认 40000）
- 限制 `agent_max_steps` 避免无限循环
- 定期监控 API 使用情况

### 2. 速率限制

Anthropic API 有速率限制，具体限制因账户类型而异。如果遇到限流错误：
- 降低请求频率
- 实现重试机制
- 联系 Anthropic 升级账户限制

### 3. 上下文长度

不同 Claude 模型支持的最大上下文长度不同：
- Claude 3.5 Sonnet：200,000 tokens
- Claude 3 Opus：200,000 tokens
- Claude 3 Sonnet：200,000 tokens
- Claude 3 Haiku：200,000 tokens

在 CowAgent 中，可通过 `agent_max_context_tokens` 配置实际使用的上下文长度。

### 4. 模型版本

建议使用 `latest` 版本的模型以获取最新功能和改进。如果需要版本稳定性，可使用带具体日期的模型版本。

## 故障排除

### 常见问题

#### 1. API 密钥错误

**症状**：`Authentication error` 或 `Invalid API key`

**解决方案**：
- 检查 `claude_api_key` 是否正确
- 确认密钥是否有访问对应模型的权限
- 如果使用 LinkAI 中转，确保 LinkAI 平台账户有余额

#### 2. 连接超时

**症状**：`Connection timeout` 或 `Network error`

**解决方案**：
- 检查网络连接，确保可以访问 Anthropic API
- 尝试使用 LinkAI 平台中转
- 检查 `claude_api_base` 配置是否正确

#### 3. 模型不可用

**症状**：`Model not found` 或 `Invalid model`

**解决方案**：
- 确认模型标识符拼写正确
- 检查您的 API 密钥是否有权访问该模型
- 尝试其他 Claude 模型版本

#### 4. Token 超限

**症状**：`Context length exceeded`

**解决方案**：
- 降低 `agent_max_context_tokens` 值
- 减少 `agent_max_context_turns` 轮次
- 使用支持更长上下文的模型（如 Claude 3.5 Sonnet）

#### 5. Agent 模式问题

**症状**：Agent 无法正确规划或执行任务

**解决方案**：
- 确保使用 Agent 推荐模型（`claude-sonnet-4-5` 或 `claude-sonnet-4-0`）
- 增加 `agent_max_steps` 允许更多执行步骤
- 检查工具配置和权限设置

### 日志调试

启用详细日志以帮助诊断问题：

```bash
# 设置日志级别
export LOG_LEVEL=DEBUG

# 启动 CowAgent
python app.py
```

查看日志中的错误信息和 API 响应，定位问题根源。

## 高级配置

### 自定义请求参数

在 `config.json` 中可添加 Claude API 的高级参数：

```json
{
  "claude_request_params": {
    "max_tokens": 4096,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50
  }
}
```

### 多模型回退

配置多个模型作为备用，当主模型不可用时自动切换：

```json
{
  "model": "claude-sonnet-4-5",
  "fallback_models": ["claude-sonnet-4-0", "gpt-4o", "gemini-3-flash-preview"],
  "agent_fallback_models": ["claude-sonnet-4-0", "glm-4.7"]
}
```

### 代理配置

如果需要通过代理访问 Claude API：

```json
{
  "http_proxy": "http://proxy.example.com:8080",
  "https_proxy": "http://proxy.example.com:8080"
}
```

## 性能优化建议

1. **模型选择**：Agent 任务推荐使用 `claude-sonnet-4-5`，平衡性能与成本
2. **上下文管理**：根据实际需求设置合理的上下文长度，避免不必要的 Token 消耗
3. **工具优化**：确保工具实现高效，减少不必要的 API 调用
4. **缓存策略**：对频繁查询的结果实施缓存，降低 API 调用频率
5. **批量处理**：将相关任务合并处理，减少 API 调用次数

## 相关资源

- [Anthropic 官方文档](https://docs.anthropic.com/)
- [Claude API 定价](https://www.anthropic.com/pricing)
- [CowAgent 项目主页](https://github.com/zhayujie/chatgpt-on-wechat)
- [LinkAI 平台](https://link-ai.tech/)

---

**最后更新**：2026年2月8日
**适用版本**：CowAgent 2.0.0 及以上