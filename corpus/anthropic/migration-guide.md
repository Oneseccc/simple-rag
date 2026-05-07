# Migration Guide

## Overview

When Anthropic releases new Claude models, older versions are eventually deprecated. This guide covers how to migrate between model versions with minimal disruption.

## Current Model Identifiers

| Model Family | Latest ID | Previous ID |
|-------------|----------|-------------|
| Opus | `claude-opus-4-7` | `claude-opus-4-5-20250120` |
| Sonnet | `claude-sonnet-4-6` | `claude-sonnet-4-5-20241022` |
| Haiku | `claude-haiku-4-5-20251001` | `claude-haiku-3-5-20241022` |

## Migration Steps

### 1. Update the Model ID

Change the `model` parameter in your API requests:

```python
# Before
response = client.messages.create(
    model="claude-sonnet-4-5-20241022",
    max_tokens=1024,
    messages=messages
)

# After
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=messages
)
```

### 2. Review Prompt Behavior

Newer models may respond differently to the same prompts. Test your critical prompts and adjust if needed:

- Output formatting may differ slightly.
- The model may be more or less verbose.
- Tool use behavior and parameter extraction may improve.

### 3. Check for New Features

Newer models often support features unavailable in older versions. Review the changelog for:

- Extended thinking support
- Improved tool use capabilities
- Better instruction following
- New content types or modalities

### 4. Update Token Budgets

Newer models may be more or less token-efficient. Monitor your `usage` fields after migration and adjust `max_tokens` if needed.

## Deprecation Timeline

Anthropic provides at least 60 days notice before deprecating a model version. During this period:

- The deprecated model continues to function.
- API responses include a deprecation warning header.
- After the deprecation date, requests to the old model ID return a 404 error.

## Best Practices

- Use model aliases (e.g., `claude-sonnet-4-6`) instead of dated versions to automatically receive updates.
- Run your evaluation suite against the new model before switching production traffic.
- Migrate gradually using traffic splitting if your system supports it.
