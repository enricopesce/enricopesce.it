---
title: "OCI GenAI Catalog: Pick the Right Model"
description: "A reference guide covering 30+ LLMs available on Oracle Cloud's Generative AI service, with a model selection wizard."
date: 2026-03-09T09:00:00+01:00
draft: false
cover:
  relative: true
  image: "static/oci-llm-comparison.png"
keywords:
- "oci generative ai"
- "llm comparison"
- "oracle cloud llm"
- "model selection"
---

OCI Generative AI has grown fast—Cohere, Google, Meta, OpenAI, xAI—all available, each with multiple variants. Every time I started a new project I had to dig through documentation to find the right model.

So I built **[OCI GenAI Catalog](https://enricopesce.github.io/oci-genai-catalog/)**: a reference guide covering 30+ models with a guided selection wizard.

## What's inside

- **24 chat models** from 5 providers, with specs: context window, multimodal, tool use, reasoning, fine-tuning support
- **9 embedding models** and 1 reranking model for RAG pipelines
- A **model selection wizard** — filter by task, performance tier, and context needs to get a top-3 recommendation

## Provider summary

| Provider | Models | Strength |
|----------|--------|----------|
| Cohere | 5 | RAG, fine-tuning |
| Google Gemini | 3 | Multimodal, long context (up to 1M tokens) |
| Meta Llama | 5 | Open weights, MoE efficiency |
| OpenAI gpt-oss | 2 | Reasoning, agents |
| xAI Grok | 6 | 2M context, code specialization |

Data is sourced from OCI official docs and kept up to date. Check it out at **[OCI GenAI Catalog](https://enricopesce.github.io/oci-genai-catalog/)**.
