# Vision

## Overview

Claude can analyze images passed in API requests. This enables use cases like document analysis, image description, visual question answering, and more.

## Supported Formats

Claude supports the following image formats:
- JPEG
- PNG
- GIF
- WebP

## Maximum Image Size

- Maximum file size: 20 MB per image
- Maximum dimensions: 8192 x 8192 pixels
- Up to 20 images per request

## Sending Images

Images can be sent as base64-encoded data or as URLs:

### Base64

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image",
          "source": {
            "type": "base64",
            "media_type": "image/jpeg",
            "data": "/9j/4AAQSkZJRg..."
          }
        },
        {
          "type": "text",
          "text": "What do you see in this image?"
        }
      ]
    }
  ]
}
```

### URL

```json
{
  "type": "image",
  "source": {
    "type": "url",
    "url": "https://example.com/image.jpg"
  }
}
```

## Best Practices

- Place images before text for best results
- Use clear, specific questions about the image
- For document analysis, ensure text is legible
- Consider image size vs. token cost tradeoffs