# Text Classification

## Overview

Claude excels at text classification tasks such as sentiment analysis, topic labeling, intent detection, and content categorization. You can achieve high accuracy with clear prompts and no training data.

## Basic Classification

Use a system prompt to define the categories and instruct Claude to return only the label:

```json
{
  "model": "claude-haiku-4-5-20251001",
  "max_tokens": 50,
  "system": "Classify the following text into exactly one category: positive, negative, or neutral. Respond with only the category name.",
  "messages": [
    {"role": "user", "content": "The product arrived on time and works great!"}
  ]
}
```

Response: `positive`

## Multi-Label Classification

For tasks where multiple labels can apply:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 100,
  "system": "Classify the text into one or more of these categories: billing, technical, account, shipping. Return a JSON array of matching categories.",
  "messages": [
    {"role": "user", "content": "I was charged twice and my package hasn't arrived yet."}
  ]
}
```

Response: `["billing", "shipping"]`

## Few-Shot Classification

Providing examples in the prompt improves consistency:

```json
{
  "model": "claude-haiku-4-5-20251001",
  "max_tokens": 20,
  "messages": [
    {"role": "user", "content": "Text: 'I love this!' -> Sentiment:"},
    {"role": "assistant", "content": "positive"},
    {"role": "user", "content": "Text: 'Terrible experience.' -> Sentiment:"},
    {"role": "assistant", "content": "negative"},
    {"role": "user", "content": "Text: 'It was okay, nothing special.' -> Sentiment:"}
  ]
}
```

## Model Selection

- **claude-haiku-4-5-20251001**: Best for high-volume classification. Fast and cost-effective.
- **claude-sonnet-4-6**: Good balance of accuracy and speed for nuanced classification.
- **claude-opus-4-7**: Use for ambiguous or complex classification requiring deep reasoning.

## Best Practices

- Constrain the output to predefined labels to avoid free-form responses.
- Use Haiku for high-throughput classification pipelines to minimize cost.
- Provide 2-5 few-shot examples for edge-case-heavy categories.
- Use the Batch API for large-scale classification jobs to get 50% cost savings.
