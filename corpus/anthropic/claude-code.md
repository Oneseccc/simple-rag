# Claude Code

## Overview

Claude Code is Anthropic's official agentic coding tool that operates directly in your terminal. It understands your codebase, can edit files, run commands, and help with complex software engineering tasks.

## Key Features

- **Agentic coding**: Claude Code can autonomously explore codebases, make multi-file edits, run tests, and fix bugs
- **Terminal integration**: Works directly in your terminal with full shell access
- **Context awareness**: Understands project structure, git history, and dependencies
- **Tool use**: Can read files, write files, execute commands, and search code

## Installation

```bash
npm install -g @anthropic-ai/claude-code
```

## Usage

```bash
# Start an interactive session
claude

# Run a one-shot command
claude -p "explain this codebase"

# Resume a previous session
claude --resume
```

## CLAUDE.md

CLAUDE.md is a special file that Claude Code reads for project-specific context. Place it in your project root to provide:
- Project overview and architecture
- Coding conventions
- Build and test commands
- Important context about the codebase

## Slash Commands

- `/help` — Show available commands
- `/clear` — Clear conversation history
- `/export` — Export the current session
- `/model` — Switch between models
- `/config` — View or modify settings

## Best Practices

- Keep CLAUDE.md concise and up-to-date
- Use clear, specific instructions
- Let Claude explore the codebase before making changes
- Review changes before committing
- Use git for version control as a safety net