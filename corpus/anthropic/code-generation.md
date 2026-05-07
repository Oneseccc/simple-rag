# Code Generation

## Overview

Claude can generate, explain, debug, and refactor code across many programming languages. It supports Python, JavaScript, TypeScript, Java, C++, Go, Rust, Ruby, PHP, SQL, and many others.

## Basic Code Generation

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 2048,
  "system": "You are an expert software engineer. Write clean, well-documented code.",
  "messages": [
    {"role": "user", "content": "Write a Python function that implements binary search on a sorted list."}
  ]
}
```

## Specifying Language and Framework

Be explicit about the language, version, and framework:

```json
{
  "messages": [
    {"role": "user", "content": "Write a REST API endpoint in Node.js using Express that accepts a POST request with a JSON body containing 'name' and 'email', validates the inputs, and returns 201 on success."}
  ]
}
```

## Code Review and Debugging

Claude can review code for bugs, security issues, and style:

```json
{
  "system": "Review the following code. Identify bugs, security issues, and suggest improvements. Format your response as a numbered list.",
  "messages": [
    {"role": "user", "content": "```python\ndef login(username, password):\n    query = f\"SELECT * FROM users WHERE name='{username}' AND pass='{password}'\"\n    return db.execute(query)\n```"}
  ]
}
```

Claude will identify the SQL injection vulnerability and suggest parameterized queries.

## Model Selection for Code Tasks

- **claude-opus-4-7**: Best for complex architectural decisions, multi-file refactoring, and system design.
- **claude-sonnet-4-6**: Strong for everyday code generation, debugging, and code review. Best cost-performance ratio.
- **claude-haiku-4-5-20251001**: Suitable for simple completions, boilerplate, and inline suggestions.

## Best Practices

- Provide context about the codebase, dependencies, and constraints.
- Ask for code with type annotations and docstrings for maintainability.
- Use system prompts to set coding style preferences (e.g., "Follow PEP 8").
- For large refactors, break the task into smaller steps and iterate.
- Always review generated code before deploying to production.
