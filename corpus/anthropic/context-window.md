# Context Window and Token Limits

## Context Window Sizes

| Model | Context Window | Max Output |
|-------|---------------|------------|
| Claude Opus 4.7 | 200K tokens (1M with extended) | 32,768 tokens |
| Claude Sonnet 4.6 | 200K tokens | 16,384 tokens |
| Claude Haiku 4.5 | 200K tokens | 8,192 tokens |

## Extended Context (Opus 4.7)

Claude Opus 4.7 supports an extended context window of up to 1 million tokens. This is automatically available — no special configuration needed.

## Long Context Best Practices

1. **Place important information at the beginning and end** — Claude attends more to these positions
2. **Use XML tags or clear formatting** to structure long documents
3. **Ask specific questions** rather than open-ended ones for better retrieval from long contexts
4. **Use prompt caching** for repeated long contexts to reduce cost and latency

## Token Counting

You can count tokens before sending a request using the token counting API:

```json
POST /v1/messages/count_tokens

{
  "model": "claude-sonnet-4-6",
  "messages": [
    {"role": "user", "content": "Your message here"}
  ]
}
```

Response:
```json
{
  "input_tokens": 15
}
```

## Managing Context

- System prompt tokens count toward the context window
- Tool definitions count toward the context window
- Previous conversation turns count toward the context window
- Consider summarizing long conversations to stay within limits