# Retrieval-Augmented Generation (RAG)

## Overview

RAG combines information retrieval with Claude's generation capabilities. By injecting relevant documents into the prompt, you ground Claude's responses in your specific data, reducing hallucinations and providing up-to-date information.

## Basic RAG Pattern

1. User submits a query.
2. Your retrieval system searches a vector database for relevant documents.
3. Retrieved documents are injected into the prompt context.
4. Claude generates a response grounded in the retrieved documents.

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "system": "Answer the user's question based only on the provided context. If the context does not contain enough information, say so.",
  "messages": [
    {
      "role": "user",
      "content": "<context>\n<doc id='1'>Anthropic was founded in 2021 by former OpenAI researchers...</doc>\n<doc id='2'>Claude is Anthropic's family of AI models...</doc>\n</context>\n\nQuestion: When was Anthropic founded?"
    }
  ]
}
```

## Structuring Retrieved Context

Use XML tags to clearly delineate retrieved documents:

```xml
<context>
  <document source="FAQ" id="42">
    Return policy: Items can be returned within 30 days...
  </document>
  <document source="Terms" id="15">
    Refunds are processed within 5-7 business days...
  </document>
</context>
```

Including metadata like source and ID helps Claude cite its sources accurately.

## Chunking Strategies

- **Fixed-size chunks**: Simple but may split sentences. Use 200-500 tokens per chunk.
- **Semantic chunks**: Split at paragraph or section boundaries for better coherence.
- **Overlapping chunks**: Add 10-20% overlap to prevent losing context at boundaries.

## Prompt Caching for RAG

If your system prompt or a large static knowledge base is included in every request, use prompt caching to avoid re-processing:

```json
{
  "system": [
    {
      "type": "text",
      "text": "You are a support agent. Use the knowledge base to answer questions.",
      "cache_control": {"type": "ephemeral"}
    }
  ]
}
```

## Best Practices

- Retrieve 3-10 relevant chunks to balance context richness and noise.
- Instruct Claude to cite which documents it used in its answer.
- Use `claude-sonnet-4-6` for a good balance of quality and cost in RAG pipelines.
- Test retrieval quality independently from generation quality.
