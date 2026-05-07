# Streaming

## Overview

Streaming allows you to receive Claude's response in real-time as it's being generated, rather than waiting for the complete response. This provides a better user experience for interactive applications.

## Server-Sent Events (SSE)

Claude uses Server-Sent Events for streaming. The stream sends events as the response is generated.

## Enabling Streaming

Set `stream: true` in your request:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "stream": true,
  "messages": [
    {"role": "user", "content": "Tell me a story."}
  ]
}
```

## Event Types

### message_start
Sent at the beginning of a response:
```
event: message_start
data: {"type": "message_start", "message": {"id": "msg_...", "type": "message", "role": "assistant"}}
```

### content_block_delta
Sent for each chunk of generated text:
```
event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Once upon"}}
```

### message_stop
Sent when the response is complete:
```
event: message_stop
data: {"type": "message_stop"}
```

## Python SDK Example

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a story."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## Best Practices

- Use streaming for interactive applications
- Handle partial responses gracefully
- Implement reconnection logic for dropped connections
- Buffer output for UI rendering to avoid flicker