# Claude API Basics

## Authentication

All API requests require an API key passed in the `x-api-key` header. You can create API keys in the Anthropic Console.

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: YOUR_API_KEY" \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01"
```

## Messages API

The Messages API is the primary way to interact with Claude. It accepts a series of messages and returns a model-generated response.

### Request Format

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "messages": [
    {"role": "user", "content": "Hello, Claude!"}
  ]
}
```

### Response Format

```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello! How can I help you today?"
    }
  ],
  "model": "claude-sonnet-4-6",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 12,
    "output_tokens": 10
  }
}
```

### System Prompts

You can provide a system prompt to set context and behavior:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "system": "You are a helpful coding assistant.",
  "messages": [
    {"role": "user", "content": "Write a Python function to sort a list."}
  ]
}
```

## Rate Limits

Rate limits vary by model and plan:
- Free tier: 5 RPM, 25K tokens per minute
- Build tier: 50 RPM, 50K tokens per minute
- Scale tier: Custom limits

## Error Handling

Common error codes:
- `400`: Invalid request format
- `401`: Invalid API key
- `429`: Rate limit exceeded
- `500`: Internal server error
- `529`: API overloaded