# Summarization

## Overview

Claude is well-suited for document summarization tasks ranging from brief abstracts to detailed outlines. Its large context window allows it to process lengthy documents in a single request.

## Basic Summarization

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 512,
  "system": "Summarize the following document in 2-3 concise paragraphs.",
  "messages": [
    {"role": "user", "content": "<document>...full text here...</document>"}
  ]
}
```

## Controlling Summary Length

Use `max_tokens` and explicit instructions to control output length:

- **Short summary**: "Summarize in one sentence." with `max_tokens: 100`
- **Medium summary**: "Summarize in 2-3 paragraphs." with `max_tokens: 512`
- **Detailed outline**: "Create a bullet-point outline of key points." with `max_tokens: 1024`

## Structured Summaries

Request structured output for integration into downstream systems:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "system": "Extract the following from the document and return as JSON: title, main_argument, key_points (array), conclusion.",
  "messages": [
    {"role": "user", "content": "<document>...full text here...</document>"}
  ]
}
```

## Long Document Summarization

For documents exceeding the context window, use a hierarchical approach:

1. Split the document into chunks that fit within the context window.
2. Summarize each chunk individually.
3. Combine the chunk summaries into a final summary request.

With claude-opus-4-7 and its 200K token context window, most single documents can be processed without chunking.

## Best Practices

- Wrap the source document in XML tags like `<document>` for clarity.
- Specify the target audience (e.g., "for a technical reader" or "for a general audience").
- Ask Claude to preserve key facts and figures when accuracy is critical.
- Use prompt caching when summarizing the same base document with different instructions.
- For factual documents, instruct Claude to avoid adding interpretation or opinions.
