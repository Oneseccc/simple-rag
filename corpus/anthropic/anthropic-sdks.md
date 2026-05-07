# Anthropic SDKs

## Python SDK

### Installation

```bash
pip install anthropic
```

### Basic Usage

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)
print(message.content[0].text)
```

### With System Prompt

```python
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="You are a helpful coding assistant.",
    messages=[
        {"role": "user", "content": "Write a quicksort in Python."}
    ]
)
```

### Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a story."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## TypeScript SDK

### Installation

```bash
npm install @anthropic-ai/sdk
```

### Basic Usage

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const message = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages: [
        { role: "user", content: "Hello, Claude!" }
    ],
});
console.log(message.content[0].text);
```

## Authentication

Both SDKs read the `ANTHROPIC_API_KEY` environment variable by default. You can also pass it explicitly:

```python
client = anthropic.Anthropic(api_key="your-api-key")
```

## Error Handling

```python
try:
    message = client.messages.create(...)
except anthropic.APIError as e:
    print(f"API error: {e.status_code}")
except anthropic.APIConnectionError:
    print("Connection failed")
except anthropic.RateLimitError:
    print("Rate limited - retry after backoff")
```