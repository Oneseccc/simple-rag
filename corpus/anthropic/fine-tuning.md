# Fine-Tuning

## Current Status

Anthropic does not currently offer fine-tuning for Claude models. Unlike some other providers, you cannot train Claude on custom datasets to modify its weights.

## Alternatives to Fine-Tuning

Claude's strong baseline performance and large context window make several alternatives viable:

### Prompt Engineering

Craft detailed system prompts that define Claude's behavior, tone, and output format:

```json
{
  "model": "claude-sonnet-4-6",
  "system": "You are a customer support agent for Acme Corp. Always greet the customer by name. Use a friendly but professional tone. If you cannot resolve the issue, escalate to a human agent by saying 'Let me connect you with a specialist.'",
  "max_tokens": 1024,
  "messages": [
    {"role": "user", "content": "Hi, I'm Sarah. My order hasn't arrived."}
  ]
}
```

### Few-Shot Learning

Include examples directly in the prompt to demonstrate the desired behavior:

```json
{
  "system": "Extract product entities from customer reviews. Return JSON.",
  "messages": [
    {"role": "user", "content": "Review: 'The Sony WH-1000XM5 headphones have amazing noise cancellation.'"},
    {"role": "assistant", "content": "{\"products\": [{\"name\": \"Sony WH-1000XM5\", \"category\": \"headphones\"}]}"},
    {"role": "user", "content": "Review: 'I bought an iPhone 15 Pro and an Apple Watch Ultra.'"}
  ]
}
```

### Retrieval-Augmented Generation (RAG)

Instead of encoding knowledge into model weights, retrieve relevant information at query time and include it in the context. This is especially effective for domain-specific knowledge that changes over time.

### Prompt Caching

Use prompt caching to make few-shot examples and large system prompts cost-effective. Cached tokens are charged at a reduced rate, making it economical to include detailed instructions in every request.

## When Fine-Tuning Might Be Needed

If you require deeply specialized model behavior that prompt engineering and RAG cannot achieve, contact Anthropic's sales team to discuss your use case. Anthropic continues to evaluate fine-tuning as a future offering.
