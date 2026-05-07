# JSON Mode and Structured Output

## Overview

Claude can produce structured JSON output reliably. You can instruct Claude to respond in JSON by using system prompts, prefilling, or tool use with a defined schema.

## Prefill Technique

The most straightforward approach is to prefill the assistant response with an opening brace to force JSON output:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "system": "Respond only with valid JSON. No additional text.",
  "messages": [
    {"role": "user", "content": "Extract the name and age from: 'John is 30 years old.'"},
    {"role": "assistant", "content": "{"}
  ]
}
```

Claude will continue the JSON object, producing something like:

```json
{"name": "John", "age": 30}
```

## Using Tool Use for Structured Output

For strict schema enforcement, define a tool whose input schema matches your desired output format. Claude will return structured data that conforms to the JSON Schema:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "tools": [
    {
      "name": "extract_person",
      "description": "Extract person details from text",
      "input_schema": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "age": {"type": "integer"},
          "occupation": {"type": "string"}
        },
        "required": ["name", "age"]
      }
    }
  ],
  "tool_choice": {"type": "tool", "name": "extract_person"},
  "messages": [
    {"role": "user", "content": "John is a 30-year-old engineer."}
  ]
}
```

Setting `tool_choice` to a specific tool forces Claude to call it, ensuring structured output every time.

## Best Practices

- Use the tool-use approach when you need guaranteed schema conformance.
- Use prefilling with `{` for simpler cases where strict validation is less critical.
- Always include `"Respond only with valid JSON"` in the system prompt when using the prefill method.
- Validate the returned JSON in your application code regardless of method.
