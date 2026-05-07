# Message Batches API

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