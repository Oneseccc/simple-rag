# Multimodal Capabilities

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