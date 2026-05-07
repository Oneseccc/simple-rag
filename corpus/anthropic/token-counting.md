# Token Counting

## Overview

Tokens are the fundamental units that Claude uses to process text. Understanding token usage is essential for managing costs, staying within context limits, and optimizing API requests.

## What Are Tokens?

A token is a sequence of characters that the model processes as a single unit. In English, one token is roughly 3-4 characters or about 0.75 words. Other languages may have different token-to-character ratios.

Examples:
- "Hello" = 1 token
- "extraordinary" = 1 token
- "antidisestablishmentarianism" = 4 tokens
- A typical English paragraph (~100 words) = ~130 tokens

## Token Counting API

Use the token counting endpoint to determine the exact token count of a request before sending it:

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ],
    system="You are a helpful assistant."
)

print(response.input_tokens)  # e.g., 18
```

## Usage in Responses

Every Messages API response includes a `usage` object:

```json
{
  "usage": {
    "input_tokens": 25,
    "output_tokens": 142,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0
  }
}
```

## Context Window Limits

| Model | Context Window | Max Output Tokens |
|-------|---------------|-------------------|
| claude-opus-4-7 | 200,000 | 32,000 |
| claude-sonnet-4-6 | 200,000 | 16,000 |
| claude-haiku-4-5-20251001 | 200,000 | 8,192 |

## Estimating Costs

Multiply token counts by the per-token price for your model. Input and output tokens are priced differently:

```
Cost = (input_tokens * input_price) + (output_tokens * output_price)
```

## Best Practices

- Use the token counting API to validate requests before sending them.
- Monitor the `usage` field in responses to track consumption.
- Set `max_tokens` to a reasonable value to control output length and costs.
- Account for system prompts, tool definitions, and conversation history in your token budget.
