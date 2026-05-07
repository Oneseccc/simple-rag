# Extended Thinking

## Overview

Extended thinking allows Claude to think through complex problems step-by-step before providing a response. This significantly improves performance on tasks requiring deep reasoning, math, coding, and analysis.

## How It Works

When extended thinking is enabled, Claude generates internal "thinking" tokens that are used to reason through the problem. These thinking tokens are visible in the response but are clearly separated from the final answer.

## Enabling Extended Thinking

```json
{
  "model": "claude-opus-4-7",
  "max_tokens": 16000,
  "thinking": {
    "type": "enabled",
    "budget_tokens": 10000
  },
  "messages": [
    {"role": "user", "content": "Solve this complex math problem..."}
  ]
}
```

## Budget Tokens

The `budget_tokens` parameter controls how many tokens Claude can use for thinking:
- Minimum: 1,024 tokens
- Maximum: 128,000 tokens
- Higher budgets allow deeper reasoning but increase latency and cost

## Response Format

```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "Let me work through this step by step..."
    },
    {
      "type": "text",
      "text": "The answer is 42."
    }
  ]
}
```

## When to Use Extended Thinking

- Complex mathematical proofs
- Multi-step reasoning problems
- Code debugging and analysis
- Strategic planning
- Scientific analysis

## Limitations

- Only available on Claude Opus 4.7 and Claude Sonnet 4.6
- Thinking tokens count toward output token limits
- Cannot be combined with certain features (e.g., streaming in some configurations)
- Thinking content may not always be coherent or complete