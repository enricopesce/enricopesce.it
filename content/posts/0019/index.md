---
title: "OCI GenAI Catalog: Pick the Right Model"
description: "A reference guide covering 30+ LLMs available on Oracle Cloud's Generative AI service, with a model selection wizard."
date: 2026-03-09T09:00:00+01:00
lastmod: 2026-06-12T00:00:00+00:00
draft: false
cover:
  alt: "OCI GenAI Catalog model comparison"
  caption: "OCI GenAI Catalog model comparison"
  relative: true
  image: "static/oci-llm-comparison.png"
keywords:
- "oci generative ai"
- "llm comparison"
- "oracle cloud llm"
- "model selection"
tags:
- "OCI"
- "Generative AI"
- "LLM"
- "Model Selection"
categories:
- "AI and Machine Learning"
faq:
  - question: "What LLM providers are available on OCI Generative AI?"
    answer: "OCI Generative AI offers models from Cohere (Command R, Command R+), Meta (Llama 3, 3.1, 3.2, 3.3), xAI (Grok), Google (Gemma), and other providers. The catalog includes 30+ model variants across different sizes and capabilities."
  - question: "How do I choose the right LLM model on OCI Generative AI?"
    answer: "Choose based on the primary task: Cohere Command R+ for RAG and enterprise documents, Llama 3.1/3.3 70B for general reasoning and coding, smaller Llama models for low-latency use cases, and embedding models for vector search. Context window size and output quality matter more than parameter count alone."
  - question: "Are all OCI Generative AI models available in all regions?"
    answer: "No. Model availability varies by OCI region. US East (Ashburn) and EU Frankfurt typically have the broadest selection. Check the OCI Generative AI documentation or the OCI GenAI Catalog tool for current regional availability."
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
