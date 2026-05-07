# Tool Use (Function Calling)

## Overview

Claude can use tools (also known as function calling) to interact with external systems. You define tools in your API request, and Claude can choose to call them when appropriate.

## Defining Tools

Tools are defined in the `tools` parameter of the Messages API request:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "tools": [
    {
      "name": "get_weather",
      "description": "Get the current weather for a location",
      "input_schema": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City and state, e.g. San Francisco, CA"
          }
        },
        "required": ["location"]
      }
    }
  ],
  "messages": [
    {"role": "user", "content": "What's the weather in San Francisco?"}
  ]
}
```

## Tool Limits

The maximum number of tools that can be defined in a single API request is 128. Each tool definition counts toward the input token limit.

## Tool Use Flow

1. **User sends message** with tool definitions
2. **Claude decides** to use a tool and returns a `tool_use` content block
3. **Your code executes** the tool and returns the result
4. **Claude uses the result** to formulate a final response

### Tool Use Response

When Claude wants to use a tool, it returns:

```json
{
  "content": [
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lh9l",
      "name": "get_weather",
      "input": {"location": "San Francisco, CA"}
    }
  ],
  "stop_reason": "tool_use"
}
```

### Returning Tool Results

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lh9l",
      "content": "65°F, partly cloudy"
    }
  ]
}
```

## Best Practices

- Write clear, specific tool descriptions
- Use descriptive parameter names
- Include examples in descriptions when helpful
- Handle errors gracefully in tool results
- Keep tool definitions focused on a single task