"""Download Anthropic Claude documentation for the RAG corpus.

Fetches markdown content from the Anthropic docs site and cookbook repository.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

CORPUS_DIR = Path(__file__).parent.parent / "corpus" / "anthropic"

COOKBOOK_FILES = [
    ("misc/prompt_caching.ipynb", "prompt-caching.md"),
    ("misc/prompt_engineering_interactive_tutorial/Anthropic 1P/01_Basic_Prompt_Structure.ipynb", "prompt-engineering-basics.md"),
    ("misc/prompt_engineering_interactive_tutorial/Anthropic 1P/02_Being_Clear_and_Direct.ipynb", "prompt-engineering-clear-direct.md"),
    ("misc/prompt_engineering_interactive_tutorial/Anthropic 1P/03_Assigning_Roles.ipynb", "prompt-engineering-roles.md"),
    ("misc/prompt_engineering_interactive_tutorial/Anthropic 1P/04_Separating_Data_from_Instructions.ipynb", "prompt-engineering-data-separation.md"),
    ("misc/prompt_engineering_interactive_tutorial/Anthropic 1P/05_Formatting_Output_and_Speaking_for_Claude.ipynb", "prompt-engineering-formatting.md"),
    ("misc/prompt_engineering_interactive_tutorial/Anthropic 1P/06_Thinking_Step_by_Step.ipynb", "prompt-engineering-chain-of-thought.md"),
    ("misc/prompt_engineering_interactive_tutorial/Anthropic 1P/07_Using_Examples.ipynb", "prompt-engineering-examples.md"),
    ("misc/prompt_engineering_interactive_tutorial/Anthropic 1P/08_Avoiding_Hallucinations.ipynb", "prompt-engineering-hallucinations.md"),
    ("misc/prompt_engineering_interactive_tutorial/Anthropic 1P/09_Complex_Prompts_for_Financial_Analysis.ipynb", "prompt-engineering-complex-prompts.md"),
    ("misc/tool_use/tool_use.ipynb", "tool-use-guide.md"),
    ("misc/citations/pdf_with_citations.ipynb", "citations-guide.md"),
]

COOKBOOK_RAW_URL = "https://raw.githubusercontent.com/anthropics/anthropic-cookbook/main/"


def extract_notebook_markdown(notebook_json: dict) -> str:
    """Extract markdown and code cells from a Jupyter notebook."""
    lines = []
    for cell in notebook_json.get("cells", []):
        cell_type = cell.get("cell_type", "")
        source = "".join(cell.get("source", []))
        if cell_type == "markdown":
            lines.append(source)
            lines.append("")
        elif cell_type == "code" and source.strip():
            lines.append("```python")
            lines.append(source)
            lines.append("```")
            lines.append("")
    return "\n".join(lines)


def download_cookbook_files():
    """Download files from the Anthropic cookbook repository."""
    if not HAS_HTTPX:
        print("  Skipping cookbook downloads (httpx not installed). Install with: pip install httpx")
        return
    client = httpx.Client(timeout=30.0, follow_redirects=True)

    for remote_path, local_name in COOKBOOK_FILES:
        url = COOKBOOK_RAW_URL + remote_path
        target = CORPUS_DIR / local_name
        if target.exists():
            print(f"  Skipping {local_name} (already exists)")
            continue

        print(f"  Downloading {local_name}...")
        try:
            resp = client.get(url)
            resp.raise_for_status()

            if remote_path.endswith(".ipynb"):
                notebook = resp.json()
                content = extract_notebook_markdown(notebook)
            else:
                content = resp.text

            target.write_text(content, encoding="utf-8")
            print(f"    Saved ({len(content)} chars)")
        except Exception as e:
            print(f"    Failed: {e}")

    client.close()


MANUAL_DOCS = {
    "models-overview.md": """# Claude Models Overview

## Latest Models

### Claude Opus 4.7
Claude Opus 4.7 is Anthropic's most capable model, offering the highest level of intelligence and performance. It excels at complex reasoning, analysis, and creative tasks.

- **Context window**: 200K tokens (up to 1M with extended context)
- **Max output**: 32,768 tokens (up to 128K with extended thinking)
- **Training data cutoff**: January 2026
- **Model ID**: `claude-opus-4-7`

### Claude Sonnet 4.6
Claude Sonnet 4.6 offers the best balance of speed and intelligence. It's the recommended model for most use cases.

- **Context window**: 200K tokens
- **Max output**: 16,384 tokens
- **Training data cutoff**: Early 2025
- **Model ID**: `claude-sonnet-4-6`

### Claude Haiku 4.5
Claude Haiku 4.5 is the fastest and most cost-effective model, ideal for lightweight tasks and high-volume applications.

- **Context window**: 200K tokens
- **Max output**: 8,192 tokens
- **Training data cutoff**: Early 2025
- **Model ID**: `claude-haiku-4-5-20251001`

## Model Selection Guide

Choose **Opus 4.7** when you need:
- Maximum reasoning capability
- Complex multi-step analysis
- Extended thinking for difficult problems
- Creative writing at the highest quality

Choose **Sonnet 4.6** when you need:
- Good balance of speed and intelligence
- Most general-purpose tasks
- Cost-effective performance

Choose **Haiku 4.5** when you need:
- Fast response times
- High throughput
- Simple classification or extraction tasks
- Cost optimization
""",
    "api-basics.md": """# Claude API Basics

## Authentication

All API requests require an API key passed in the `x-api-key` header. You can create API keys in the Anthropic Console.

```bash
curl https://api.anthropic.com/v1/messages \\
  -H "x-api-key: YOUR_API_KEY" \\
  -H "content-type: application/json" \\
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
""",
    "tool-use.md": """# Tool Use (Function Calling)

## Overview

Claude can use tools (also known as function calling) to interact with external systems. You define tools in your API request, and Claude can choose to call them when appropriate.

## Defining Tools

Tools are defined in the `tools` parameter of the Messages API request:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "tools": [
    {
      "name": "get_weather",
      "description": "Get the current weather for a location",
      "input_schema": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City and state, e.g. San Francisco, CA"
          }
        },
        "required": ["location"]
      }
    }
  ],
  "messages": [
    {"role": "user", "content": "What's the weather in San Francisco?"}
  ]
}
```

## Tool Limits

The maximum number of tools that can be defined in a single API request is 128. Each tool definition counts toward the input token limit.

## Tool Use Flow

1. **User sends message** with tool definitions
2. **Claude decides** to use a tool and returns a `tool_use` content block
3. **Your code executes** the tool and returns the result
4. **Claude uses the result** to formulate a final response

### Tool Use Response

When Claude wants to use a tool, it returns:

```json
{
  "content": [
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lh9l",
      "name": "get_weather",
      "input": {"location": "San Francisco, CA"}
    }
  ],
  "stop_reason": "tool_use"
}
```

### Returning Tool Results

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lh9l",
      "content": "65°F, partly cloudy"
    }
  ]
}
```

## Best Practices

- Write clear, specific tool descriptions
- Use descriptive parameter names
- Include examples in descriptions when helpful
- Handle errors gracefully in tool results
- Keep tool definitions focused on a single task
""",
    "prompt-caching.md": """# Prompt Caching

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
""",
    "vision.md": """# Vision

## Overview

Claude can analyze images passed in API requests. This enables use cases like document analysis, image description, visual question answering, and more.

## Supported Formats

Claude supports the following image formats:
- JPEG
- PNG
- GIF
- WebP

## Maximum Image Size

- Maximum file size: 20 MB per image
- Maximum dimensions: 8192 x 8192 pixels
- Up to 20 images per request

## Sending Images

Images can be sent as base64-encoded data or as URLs:

### Base64

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image",
          "source": {
            "type": "base64",
            "media_type": "image/jpeg",
            "data": "/9j/4AAQSkZJRg..."
          }
        },
        {
          "type": "text",
          "text": "What do you see in this image?"
        }
      ]
    }
  ]
}
```

### URL

```json
{
  "type": "image",
  "source": {
    "type": "url",
    "url": "https://example.com/image.jpg"
  }
}
```

## Best Practices

- Place images before text for best results
- Use clear, specific questions about the image
- For document analysis, ensure text is legible
- Consider image size vs. token cost tradeoffs
""",
    "extended-thinking.md": """# Extended Thinking

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
""",
    "embeddings.md": """# Embeddings

## Overview

While Anthropic does not provide a dedicated embeddings API, Claude can be used in conjunction with embedding models for RAG (Retrieval-Augmented Generation) and semantic search workflows.

## Recommended Embedding Models

For use with Claude-based RAG systems:

### Local Models (via Ollama or sentence-transformers)
- **all-MiniLM-L6-v2**: 384 dimensions, fast, good general-purpose quality
- **nomic-embed-text**: 768 dimensions, strong performance on benchmarks
- **bge-small-en-v1.5**: 384 dimensions, optimized for retrieval tasks

### API-based Models
- **Voyage AI**: Recommended by Anthropic for best quality embeddings
- **OpenAI text-embedding-3-small**: 1536 dimensions, widely used

## Best Practices for RAG with Claude

1. **Chunk Size**: Use 256-1024 tokens per chunk depending on content type
2. **Overlap**: 10-20% overlap between chunks preserves context
3. **Metadata**: Store source information with embeddings for citations
4. **Top-K**: Retrieve 3-10 chunks depending on context window budget
5. **Prompt Design**: Clearly delineate retrieved context from the user question
""",
    "streaming.md": """# Streaming

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
""",
    "safety.md": """# Safety and Usage Policies

## Acceptable Use Policy

Claude is designed to be helpful, harmless, and honest. The Acceptable Use Policy prohibits:
- Generating illegal content
- Creating malware or cyber weapons
- Harassment or discrimination
- Deception or fraud
- Violating privacy

## Content Filtering

Claude has built-in content filtering that:
- Refuses harmful requests
- Avoids generating explicit content
- Declines to assist with illegal activities
- Provides safety disclaimers when appropriate

## System Prompt Best Practices

For safer deployments:
1. Set clear behavioral boundaries in the system prompt
2. Specify what topics the assistant should and shouldn't discuss
3. Define the assistant's role and limitations
4. Include instructions for handling edge cases

## Responsible AI Development

Anthropic recommends:
- Testing for bias in your specific use case
- Implementing human oversight for high-stakes decisions
- Monitoring output quality in production
- Establishing feedback mechanisms for users
- Regular evaluation of system behavior
""",
    "batch-api.md": """# Message Batches API

## Overview

The Message Batches API allows you to send multiple message requests in a single batch, processing them asynchronously. This is ideal for high-volume workloads that don't require real-time responses.

## Benefits

- **50% cost reduction** compared to standard API calls
- Process up to 100,000 requests per batch
- Results available within 24 hours (usually much faster)
- No rate limit impact on your real-time API usage

## Creating a Batch

```json
POST /v1/messages/batches

{
  "requests": [
    {
      "custom_id": "request-1",
      "params": {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1024,
        "messages": [
          {"role": "user", "content": "Summarize this article..."}
        ]
      }
    },
    {
      "custom_id": "request-2",
      "params": {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1024,
        "messages": [
          {"role": "user", "content": "Translate this text..."}
        ]
      }
    }
  ]
}
```

## Batch Status

Check batch status:
```
GET /v1/messages/batches/{batch_id}
```

Possible statuses: `in_progress`, `ended`, `canceling`, `canceled`

## Retrieving Results

```
GET /v1/messages/batches/{batch_id}/results
```

Each result includes the `custom_id` from the original request for matching.

## Best Practices

- Use meaningful `custom_id` values for tracking
- Break very large jobs into multiple batches
- Implement polling with exponential backoff for status checks
- Handle partial failures gracefully
""",
    "claude-code.md": """# Claude Code

## Overview

Claude Code is Anthropic's official agentic coding tool that operates directly in your terminal. It understands your codebase, can edit files, run commands, and help with complex software engineering tasks.

## Key Features

- **Agentic coding**: Claude Code can autonomously explore codebases, make multi-file edits, run tests, and fix bugs
- **Terminal integration**: Works directly in your terminal with full shell access
- **Context awareness**: Understands project structure, git history, and dependencies
- **Tool use**: Can read files, write files, execute commands, and search code

## Installation

```bash
npm install -g @anthropic-ai/claude-code
```

## Usage

```bash
# Start an interactive session
claude

# Run a one-shot command
claude -p "explain this codebase"

# Resume a previous session
claude --resume
```

## CLAUDE.md

CLAUDE.md is a special file that Claude Code reads for project-specific context. Place it in your project root to provide:
- Project overview and architecture
- Coding conventions
- Build and test commands
- Important context about the codebase

## Slash Commands

- `/help` — Show available commands
- `/clear` — Clear conversation history
- `/export` — Export the current session
- `/model` — Switch between models
- `/config` — View or modify settings

## Best Practices

- Keep CLAUDE.md concise and up-to-date
- Use clear, specific instructions
- Let Claude explore the codebase before making changes
- Review changes before committing
- Use git for version control as a safety net
""",
    "anthropic-sdks.md": """# Anthropic SDKs

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
""",
    "pricing.md": """# Claude API Pricing

## Model Pricing

### Claude Opus 4.7
| Feature | Price |
|---------|-------|
| Input tokens | $15 / MTok |
| Output tokens | $75 / MTok |
| Prompt caching write | $18.75 / MTok |
| Prompt caching read | $1.50 / MTok |
| Batch input | $7.50 / MTok |
| Batch output | $37.50 / MTok |

### Claude Sonnet 4.6
| Feature | Price |
|---------|-------|
| Input tokens | $3 / MTok |
| Output tokens | $15 / MTok |
| Prompt caching write | $3.75 / MTok |
| Prompt caching read | $0.30 / MTok |
| Batch input | $1.50 / MTok |
| Batch output | $7.50 / MTok |

### Claude Haiku 4.5
| Feature | Price |
|---------|-------|
| Input tokens | $0.80 / MTok |
| Output tokens | $4 / MTok |
| Prompt caching write | $1 / MTok |
| Prompt caching read | $0.08 / MTok |
| Batch input | $0.40 / MTok |
| Batch output | $2 / MTok |

## Token Counting

- 1 token ≈ 4 characters in English
- 1,000 tokens ≈ 750 words
- MTok = Million tokens

## Free Tier

The free tier includes:
- $5 of free API credits upon signup
- Credits expire after 30 days
- Limited to build tier rate limits

## Cost Optimization Tips

1. Use prompt caching for repeated prefixes
2. Use batch API for non-real-time workloads (50% discount)
3. Choose the right model for your task (Haiku for simple tasks)
4. Optimize prompt length — shorter prompts cost less
5. Set appropriate `max_tokens` to avoid unnecessary output
""",
    "context-window.md": """# Context Window and Token Limits

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
""",
    "system-prompts.md": """# System Prompts

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
""",
    "multimodal.md": """# Multimodal Capabilities

## Overview

Claude supports multimodal inputs, allowing you to combine text with images and documents in your requests. This enables rich interactions that leverage both visual and textual understanding.

## Supported Input Types

### Images
- Formats: JPEG, PNG, GIF, WebP
- Max size: 20 MB per image
- Max dimensions: 8192 x 8192 pixels
- Up to 20 images per request

### PDFs
- Max size: 32 MB per PDF
- Max pages: 100 pages
- Rendered as images internally

## Image Understanding Capabilities

Claude can:
- Describe image contents
- Read text in images (OCR)
- Analyze charts and graphs
- Compare multiple images
- Answer questions about visual content
- Extract data from screenshots

## PDF Analysis

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "document",
          "source": {
            "type": "base64",
            "media_type": "application/pdf",
            "data": "JVBERi0xLjcK..."
          }
        },
        {
          "type": "text",
          "text": "Summarize the key findings in this report."
        }
      ]
    }
  ]
}
```

## Best Practices

- Place images before text in the message content array
- Use high-resolution images for text extraction
- Be specific about what you want Claude to analyze
- Consider token costs — images consume tokens based on their size
- For documents, ask focused questions rather than "summarize everything"
""",
}


def write_manual_docs():
    """Write manually curated documentation files."""
    for filename, content in MANUAL_DOCS.items():
        target = CORPUS_DIR / filename
        if target.exists():
            print(f"  Skipping {filename} (already exists)")
            continue
        target.write_text(content.strip(), encoding="utf-8")
        print(f"  Created {filename} ({len(content)} chars)")


def main():
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1: Writing curated documentation files...")
    write_manual_docs()

    print(f"\nStep 2: Downloading from Anthropic Cookbook...")
    download_cookbook_files()

    files = list(CORPUS_DIR.glob("*.md"))
    print(f"\nDone! {len(files)} files in {CORPUS_DIR}")
    for f in sorted(files):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
