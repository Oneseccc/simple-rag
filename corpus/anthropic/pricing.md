# Claude API Pricing

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