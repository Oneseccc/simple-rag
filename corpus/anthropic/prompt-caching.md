# Prompt Caching

## Overview

Prompt caching allows you to cache frequently used context between API calls, reducing latency by up to 85% and costs by up to 90% for long prompts.

## How It Works

When you send a request with prompt caching enabled, Anthropic's infrastructure:
1. Checks if a prefix of your prompt is already cached
2. If cached, uses the cached version (cache hit) — much faster and cheaper
3. If not cached, processes the full prompt and caches the prefix for future use

## Cache Lifetime

Cached prompts have a minimum lifetime of 5 minutes. Each time a cached prompt is used, the lifetime is extended by 5 minutes. The cache is ephemeral and not guaranteed to persist.

## Minimum Cacheable Length

The minimum cacheable prompt prefix length varies by model:
- **Claude Opus**: 1,024 tokens
- **Claude Sonnet**: 1,024 tokens
- **Claude Haiku**: 2,048 tokens

## Using Cache Breakpoints

Add `cache_control` to mark where the cache should break:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "system": [
    {
      "type": "text",
      "text": "You are a helpful assistant with deep knowledge of...",
      "cache_control": {"type": "ephemeral"}
    }
  ],
  "messages": [
    {"role": "user", "content": "Tell me about..."}
  ]
}
```

## Pricing

| Model | Base Input | Cache Write | Cache Read |
|-------|-----------|-------------|------------|
| Claude Opus 4.7 | $15/MTok | $18.75/MTok | $1.50/MTok |
| Claude Sonnet 4.6 | $3/MTok | $3.75/MTok | $0.30/MTok |
| Claude Haiku 4.5 | $0.80/MTok | $1/MTok | $0.08/MTok |

## Best Practices

- Place static content (system prompts, examples, documentation) first
- Put dynamic content (user messages) after the cache breakpoint
- Use cache breakpoints strategically to maximize reuse
- Monitor cache hit rates in your usage dashboard