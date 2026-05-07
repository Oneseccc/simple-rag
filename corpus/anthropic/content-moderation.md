# Content Moderation

## Overview

Claude can be used to build content moderation systems that detect harmful, inappropriate, or policy-violating content. Its nuanced understanding of language makes it effective at distinguishing between genuinely harmful content and benign edge cases.

## Basic Moderation

```json
{
  "model": "claude-haiku-4-5-20251001",
  "max_tokens": 200,
  "system": "You are a content moderator. Analyze the text and return a JSON object with: 'safe' (boolean), 'categories' (array of violated categories from: hate_speech, violence, sexual_content, self_harm, spam, harassment), and 'confidence' (float 0-1).",
  "messages": [
    {"role": "user", "content": "Review this post: 'Great product, highly recommend it to everyone!'"}
  ]
}
```

Response:
```json
{"safe": true, "categories": [], "confidence": 0.98}
```

## Multi-Tier Moderation

For production systems, implement a two-tier approach:

1. **Tier 1 (Haiku)**: Fast, cheap first pass on all content. Flag anything scoring below a confidence threshold.
2. **Tier 2 (Sonnet)**: Re-evaluate flagged content with a more capable model for final decisions.

This balances cost and accuracy for high-volume applications.

## Custom Policy Enforcement

Define your platform-specific policies in the system prompt:

```json
{
  "system": "You are a content moderator for an educational platform aimed at children aged 8-12. Flag content that contains: profanity, adult themes, bullying, personal information sharing, or external links. Return JSON with 'action' (approve/flag/reject) and 'reason'."
}
```

## Best Practices

- Use Haiku for high-volume moderation to keep costs low.
- Always include a human review step for content flagged at the boundary.
- Define clear, specific policies in the system prompt rather than relying on general moderation.
- Log moderation decisions for auditing and model evaluation.
- Combine Claude-based moderation with rule-based filters for known patterns (e.g., regex for URLs or phone numbers).
- Test your moderation system against adversarial inputs designed to bypass detection.
