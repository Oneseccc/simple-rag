# Error Handling

## Error Response Format

All API errors return a consistent JSON structure with an `error` object containing a `type` and `message` field:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "max_tokens: Field required"
  }
}
```

## HTTP Error Codes

| Status Code | Error Type | Description |
|-------------|-----------|-------------|
| 400 | `invalid_request_error` | The request body is malformed or missing required fields. |
| 401 | `authentication_error` | The API key is invalid, expired, or missing. |
| 403 | `permission_error` | The API key lacks permission for the requested resource. |
| 404 | `not_found_error` | The requested resource (e.g., model) does not exist. |
| 429 | `rate_limit_error` | You have exceeded your rate limit or token quota. |
| 500 | `api_error` | An unexpected internal server error occurred. |
| 529 | `overloaded_error` | The API is temporarily overloaded. |

## Retry Strategy

Implement exponential backoff with jitter for retryable errors (429, 500, 529):

```python
import anthropic
import time
import random

client = anthropic.Anthropic()

def call_with_retry(messages, max_retries=5):
    for attempt in range(max_retries):
        try:
            return client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                messages=messages
            )
        except anthropic.RateLimitError:
            delay = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
        except anthropic.APIStatusError as e:
            if e.status_code in (500, 529):
                delay = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(delay)
            else:
                raise
    raise Exception("Max retries exceeded")
```

## Rate Limit Headers

Every response includes headers indicating your current rate limit status:

- `retry-after`: Seconds to wait before retrying (on 429 responses)
- `x-ratelimit-limit-requests`: Your request-per-minute limit
- `x-ratelimit-remaining-requests`: Remaining requests in the current window

## Best Practices

- Always check the `error.type` field to determine the category of error.
- Do not retry 400 or 401 errors, as they indicate a problem with your request.
- Use the `retry-after` header value when available instead of a fixed delay.
- Log the full error response body for debugging purposes.
