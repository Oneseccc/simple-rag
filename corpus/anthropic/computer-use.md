# Computer Use

## Overview

Computer use is a beta feature that allows Claude to interact with a computer desktop environment. Claude can view screenshots, move the mouse, click elements, type text, and execute keyboard shortcuts to accomplish tasks in graphical user interfaces.

## How It Works

Computer use extends the tool use framework with three built-in tools:

- **computer**: Controls mouse movement, clicks, typing, and screenshots.
- **text_editor**: Views and edits text files on the computer.
- **bash**: Executes shell commands.

## Enabling Computer Use

Add the `computer-use-2025-01-24` beta header and define the computer tool:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 4096,
  "anthropic-beta": ["computer-use-2025-01-24"],
  "tools": [
    {
      "type": "computer_20241022",
      "name": "computer",
      "display_width_px": 1920,
      "display_height_px": 1080,
      "display_number": 1
    }
  ],
  "messages": [
    {"role": "user", "content": "Open Firefox and navigate to anthropic.com"}
  ]
}
```

## The Interaction Loop

1. Claude analyzes the current screenshot and decides on an action.
2. Claude returns a `tool_use` block specifying the action (e.g., click at coordinates, type text).
3. Your system executes the action and captures a new screenshot.
4. The new screenshot is returned to Claude as a `tool_result`.
5. Claude evaluates the result and decides the next action.

## Safety Considerations

Computer use gives Claude direct control over a system. Always:

- Run in a sandboxed virtual machine or container with no access to sensitive data.
- Limit network access to prevent unintended external interactions.
- Implement human-in-the-loop confirmation for irreversible actions.
- Never expose production systems or credentials.

## Best Practices

- Use a dedicated virtual environment with minimal installed software.
- Set the display resolution to match common desktop sizes (1920x1080).
- Provide clear, specific instructions for the task to minimize unnecessary exploration.
- Monitor Claude's actions in real time during development.
