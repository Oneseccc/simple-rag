# Rate Limits

## Overview

Anthropic enforces rate limits to ensure fair usage and API stability. Limits are applied per organization and vary by usage tier and model.

## Usage Tiers

| Tier | Requirement | Requests/min | Tokens/min (Input) | Tokens/min (Output) |
|------|------------|-------------|--------------------|--------------------|
| Free | API key created | 5 | 25,000 | 10,000 |
| Build | Credit purchase ($5+) | 50 | 50,000 | 20,000 |
| Scale | $1,000+ spend history | 1,000 | 200,000 | 80,000 |
| Custom | Contact sales | Custom | Custom | Custom |

## Per-Model Limits

Higher-capability models have separate, often lower limits:

- **claude-opus-4-7**: Lower RPM due to higher compute cost. Build tier gets 20 RPM.
- **claude-sonnet-4-6**: Standard limits as listed in the tier table above.
- **claude-haiku-4-5-20251001**: Higher RPM allowed. Build tier gets 100 RPM.

## Rate Limit Headers

Every API response includes rate limit headers:

```
x-ratelimit-limit-requests: 50
x-ratelimit-limit-tokens: 50000
x-ratelimit-remaining-requests: 48
x-ratelimit-remaining-tokens: 42500
x-ratelimit-reset-requests: 2026-05-04T12:00:30Z
x-ratelimit-reset-tokens: 2026-05-04T12:00:30Z
```

## Handling 429 Errors

When you exceed a rate limit, the API returns HTTP 429 with a `retry-after` header:

```json
{
  "type": "error",
  "error": {
    "type": "rate_limit_error",
    "message": "Rate limit exceeded. Please retry after 12 seconds."
  }
}
```

Use exponential backoff and respect the `retry-after` header value.

## Daily Token Limits

In addition to per-minute limits, each tier has a daily token budget. Free tier accounts are limited to 300,000 tokens per day. Build and Scale tiers have significantly higher daily allowances.

## Increasing Your Limits

To move to a higher tier, increase your spend with Anthropic. For Scale and Custom tiers, contact the Anthropic sales team to discuss your usage needs.
