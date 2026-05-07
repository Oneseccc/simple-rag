# Multi-Turn Conversations

## Overview

The Messages API supports multi-turn conversations by passing an array of messages with alternating `user` and `assistant` roles. Claude uses the full conversation history as context for generating its response.

## Message Roles

Each message must have a `role` field set to either `user` or `assistant`. Messages must alternate between user and assistant roles, starting with a user message.

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "system": "You are a helpful math tutor.",
  "messages": [
    {"role": "user", "content": "What is the derivative of x^2?"},
    {"role": "assistant", "content": "The derivative of x^2 is 2x."},
    {"role": "user", "content": "What about x^3?"}
  ]
}
```

## Conversation Structure

The API is stateless. You must send the entire conversation history with each request. The server does not retain previous messages between requests.

### Prefilling the Assistant Response

You can include a partial assistant message at the end of the messages array to steer Claude's response:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 256,
  "messages": [
    {"role": "user", "content": "List three fruits."},
    {"role": "assistant", "content": "1."}
  ]
}
```

Claude will continue from the prefilled text, responding with something like `" Apple\n2. Banana\n3. Cherry"`.

## Managing Context Length

As conversations grow, the total token count increases. When the conversation approaches the model's context window limit, consider:

- Summarizing earlier parts of the conversation
- Dropping the oldest messages while keeping the system prompt
- Using prompt caching to reduce costs on repeated prefixes

## Token Costs

All messages in the conversation count toward input tokens. For long conversations, this means input token costs grow with each turn. Use prompt caching with a static system prompt and earlier messages to reduce repeated charges.

## Best Practices

- Always maintain strict alternation between user and assistant roles.
- Keep the system prompt consistent across turns for coherent behavior.
- Trim or summarize older messages to stay within context limits.
- Use prefilling sparingly and only to guide output format.
