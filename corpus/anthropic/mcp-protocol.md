# Model Context Protocol (MCP)

## Overview

The Model Context Protocol (MCP) is an open standard developed by Anthropic for connecting AI models to external data sources and tools. It provides a unified interface so that AI applications can access context from any MCP-compatible server.

## Architecture

MCP uses a client-server architecture:

- **MCP Host**: The AI application (e.g., Claude Desktop, an IDE plugin) that needs external context.
- **MCP Client**: A protocol client within the host that connects to MCP servers.
- **MCP Server**: A lightweight service that exposes data or tools through the MCP standard.

## Core Capabilities

MCP servers can expose three types of features:

### Resources

Static or dynamic data that the AI can read:

```json
{
  "uri": "file:///project/README.md",
  "name": "Project README",
  "mimeType": "text/markdown"
}
```

### Tools

Functions the AI can invoke:

```json
{
  "name": "query_database",
  "description": "Run a read-only SQL query against the project database",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"}
    },
    "required": ["query"]
  }
}
```

### Prompts

Reusable prompt templates:

```json
{
  "name": "summarize_changes",
  "description": "Summarize recent code changes",
  "arguments": [
    {"name": "since", "description": "Date to start from", "required": true}
  ]
}
```

## Transport

MCP supports two transport mechanisms:

- **stdio**: Communication over standard input/output. Ideal for local tools.
- **SSE (Server-Sent Events)**: HTTP-based transport for remote servers.

## Integration with Claude

Claude Desktop and Claude Code natively support MCP. Configure servers in the application settings to give Claude access to external tools, databases, file systems, and APIs.

## Best Practices

- Keep MCP servers focused on a single domain or data source.
- Use descriptive names and descriptions for tools and resources.
- Implement proper authentication for remote MCP servers.
- Log all tool invocations for auditing and debugging.
