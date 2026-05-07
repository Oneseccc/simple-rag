# System Prompts

## Overview

System prompts allow you to set context, personality, and behavioral guidelines for Claude. They are processed before user messages and influence all subsequent responses.

## Basic Usage

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "system": "You are a helpful customer support agent for Acme Corp. Be friendly, concise, and always suggest contacting support@acme.com for complex issues.",
  "messages": [
    {"role": "user", "content": "I can't log into my account."}
  ]
}
```

## Multi-part System Prompts

For complex setups, use an array of content blocks:

```json
{
  "system": [
    {
      "type": "text",
      "text": "You are a coding assistant.",
      "cache_control": {"type": "ephemeral"}
    },
    {
      "type": "text",
      "text": "Here are the project guidelines: ..."
    }
  ]
}
```

## Effective System Prompt Patterns

### Role Definition
Define who Claude is in this context:
"You are a senior Python developer reviewing code for a fintech startup."

### Behavioral Constraints
Set clear boundaries:
"Never provide financial advice. Always recommend consulting a professional."

### Output Format
Specify response structure:
"Always respond in JSON format with keys: summary, details, next_steps."

### Knowledge Scope
Limit what Claude discusses:
"Only answer questions about our product. For unrelated questions, politely redirect."

## Best Practices

1. Be specific and explicit about desired behavior
2. Include examples of ideal responses
3. Define edge cases and how to handle them
4. Keep system prompts focused and organized
5. Test system prompts with adversarial inputs
6. Use cache_control for static system prompts to reduce costs