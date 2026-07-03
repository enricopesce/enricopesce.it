---
title: "OCI Generative AI in Python: Where to Start"
description: "Minimal Python demos for OCI Generative AI, and what to know before choosing between the OCI-native SDK and the OpenAI-compatible API."
date: 2026-06-29T10:00:00+01:00
lastmod: 2026-06-29T10:00:00+01:00
slug: "oci-generative-ai-python-tutorial"
aliases:
- "/oci-genai-python-starters-a-few-small-demos-to-get-started/"
draft: false
cover:
  alt: "OCI Generative AI Python Tutorial"
  caption: "OCI Generative AI Python Tutorial"
  relative: true
  image: "static/oci-genai-python-starters.svg"
  width: 1200
  height: 630
keywords:
- "oci generative ai python"
- "oracle cloud generative ai python tutorial"
- "langchain oci generative ai"
- "oci genai sdk python"
- "llamaindex oci"
- "langgraph oracle cloud"
- "oci openai compatible python"
- "oracle generative ai python example"
- "oci genai python starter"
- "oci python sdk generative ai"
tags:
- "OCI"
- "Generative AI"
- "Python"
- "LangChain"
- "LlamaIndex"
- "LangGraph"
- "OpenAI API"
categories:
- "AI and Machine Learning"
inLanguage: "en"
codeRepository: "https://github.com/enricopesce/oci-genai-python-starters"
softwareRequirements:
- "Python 3.11+"
- "OCI Generative AI"
- "OCI Python SDK"
- "LangChain"
- "LlamaIndex"
- "LangGraph"
faq:
- question: "What is OCI GenAI Python Starters?"
  answer: "A collection of seven minimal, runnable Python demos for OCI Generative AI. Each demo lives in its own folder and shows one specific way to call OCI models: direct SDK, LangChain, LlamaIndex, LangGraph, and three OpenAI-compatible approaches."
- question: "What is the difference between OCI-native and OpenAI-compatible demos?"
  answer: "OCI-native demos use the oci Python SDK and the standard OCI Generative AI endpoint. OpenAI-compatible demos use the openai library pointed at an OCI endpoint, so existing OpenAI code runs against OCI models with minimal changes. The two approaches use different environment variables and different base URLs."
- question: "Which demo should I start with?"
  answer: "Start with direct-sdk. It uses only the oci package, has no framework on top, and shows exactly what a raw OCI Generative AI call looks like. Once that works, add LangChain or the OpenAI-compatible demo depending on where your project is going."
- question: "Why does openai-responses need a project OCID while openai-chat does not?"
  answer: "openai-responses targets the newer OCI Responses API endpoint, which requires a Generative AI project OCID and a different base URL. openai-chat uses the standard chat completions endpoint and only needs a service endpoint and compartment OCID."
- question: "Can I run these demos in OCI Cloud Shell?"
  answer: "Yes. OCI Cloud Shell already has credentials configured. Clone the repo, create a virtual environment, install the demo's requirements, and fill in the .env file."
related:
- "/posts/0016"
- "/posts/0019"
- "/posts/0018"
---

Every time I start experimenting with a new framework or API style on OCI Generative AI, I waste the same hour rebuilding the same boilerplate: right credentials, right endpoint, right model ID format, right environment variables. Then I discover that LangChain and the OpenAI-compatible API use a different variable than the raw SDK. Then I find that the newer Responses API needs a project OCID that the chat completions endpoint does not.

None of this is in the official docs in one place. So I stopped rebuilding from scratch and put everything into **[OCI GenAI Python Starters](https://github.com/enricopesce/oci-genai-python-starters)**.

## What it is

Seven small Python demos, one folder each. Every demo does one thing: send a prompt to an OCI Generative AI model and print the response. No shared utilities, no hidden framework, no production scaffolding. Just the shortest path from credentials to output for each specific approach.

The demos cover the two distinct ways you can call OCI Generative AI from Python:

**OCI-native** uses the `oci` SDK directly. You talk to the OCI inference endpoint, authenticate with your OCI profile, and pass an OCI compartment OCID. This is the most direct approach and the one most OCI documentation shows.

**OpenAI-compatible** uses the `openai` library, pointed at an OCI endpoint that accepts OpenAI-shaped requests. The reason this exists is practical: a lot of Python code is already written against the OpenAI API. With the OpenAI-compatible path, that code runs against OCI models with a base URL change and OCI authentication injected — no rewrite needed.

The demos map directly to that split:

| Demo | Approach |
|---|---|
| `direct-sdk` | OCI-native, no framework |
| `langchain` | OCI-native via LangChain |
| `llamaindex` | OCI-native via LlamaIndex |
| `langgraph` | OCI-native via LangGraph |
| `openai-chat` | OpenAI-compatible, chat completions |
| `openai-agents` | OpenAI-compatible, Agents SDK |
| `openai-responses` | OpenAI-compatible, Responses API |

## The thing that actually trips people up

The two approaches look similar on the surface but use different configuration. OCI-native demos need `OCI_SERVICE_ENDPOINT` and `OCI_COMPARTMENT_ID`. The OpenAI-compatible demos need those too — except `openai-responses`, which uses a completely different base URL (`OCI_OPENAI_BASE_URL`) and requires a Generative AI project OCID that the others do not.

This is the detail that costs the most time. `openai-chat` and `openai-responses` look like the same kind of demo but they are wired differently. The repo makes this explicit in each demo's `.env.example` so you can see exactly what each one needs before you run it.

## Who it is for

If you are new to OCI Generative AI and want to understand how the API works before adding a framework on top, start with `direct-sdk`. It shows the raw call with nothing hidden.

If you are already using LangChain or LlamaIndex in a project and want to swap in OCI models, the framework demos show the minimum config needed to make that work.

If you have existing OpenAI code and want to run it against OCI without rewriting it, the OpenAI-compatible demos show the exact differences — including the less obvious one between `openai-chat` and `openai-responses`.

The repo is on GitHub: **[enricopesce/oci-genai-python-starters](https://github.com/enricopesce/oci-genai-python-starters)**.
