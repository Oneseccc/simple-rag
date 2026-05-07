# Citations

## Overview

The citations feature allows Claude to reference specific passages from source documents in its responses. When enabled, Claude returns structured citation objects that point back to exact locations in the provided content, making it easy to verify claims against source material.

## Enabling Citations

Pass documents as content blocks with the `citations` parameter enabled:

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
            "type": "text",
            "text": "Anthropic was founded in 2021 by Dario Amodei and Daniela Amodei. The company is headquartered in San Francisco."
          },
          "title": "Company Overview",
          "citations": {"enabled": true}
        },
        {
          "type": "text",
          "text": "When was Anthropic founded and where is it located?"
        }
      ]
    }
  ]
}
```

## Citation Response Format

When citations are enabled, Claude's response includes citation markers linked to source spans:

```json
{
  "content": [
    {
      "type": "text",
      "text": "Anthropic was founded in 2021",
      "citations": [
        {
          "type": "text_location",
          "cited_text": "Anthropic was founded in 2021 by Dario Amodei and Daniela Amodei.",
          "document_index": 0,
          "start_char_index": 0,
          "end_char_index": 65
        }
      ]
    }
  ]
}
```

## Supported Document Types

- **Plain text**: Passed directly as a `text` source.
- **PDF documents**: Passed as base64-encoded content with `media_type: "application/pdf"`.
- **HTML content**: Claude can parse and cite from HTML sources.

## Best Practices

- Use the `title` field to give documents meaningful names for clearer citations.
- Enable citations when building applications that require source verification, such as legal research or academic tools.
- Combine citations with RAG for grounded, verifiable responses.
- Process citation spans programmatically to build interactive source highlighting in your UI.
