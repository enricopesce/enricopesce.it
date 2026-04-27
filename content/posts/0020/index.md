---
title: "OCI GenAI Python Starters: a few small demos to get started"
description: "A small collection of Python examples for OCI Generative AI, from direct SDK calls to LangChain, LangGraph, and OpenAI-compatible APIs."
date: 2026-04-27T09:00:00+01:00
draft: false
cover:
  alt: "OCI GenAI Python Starters"
  caption: "OCI GenAI Python Starters"
  relative: true
  image: "static/oci-genai-python-starters.svg"
keywords:
- "oci generative ai python"
- "oci genai starter"
- "langchain oci example"
- "oci openai compatible"
---

Every time I want to try something new on OCI Generative AI, I end up needing the same thing: one tiny Python example that actually works.

Not a full framework. Not a polished app. Just a small script with the right config, the right endpoint, and one clear path from “I have credentials” to “okay, it runs.”

After rebuilding those snippets a few times, I put them in one repo: **[OCI GenAI Python Starters](https://github.com/enricopesce/oci-genai-python-starters)**.

Nothing fancy, just a bunch of small demos you can run, break, tweak, and reuse.

## What's in there

- `direct-sdk` if you want to start from the bare minimum
- `langchain`, `llamaindex`, and `langgraph` if you want to see the same idea through higher-level tools
- `openai-chat`, `openai-agents`, and `openai-responses` if you prefer the OpenAI-style route
- One folder per demo, with its own `requirements.txt` and `.env.example`
- A `test_all_demos.sh` script if you want to run through everything once the environment variables are in place

I also tried to keep the order sensible: start from the raw SDK, then move to the framework examples once the basic OCI flow is clear.

## One thing that tripped me up

The OpenAI-compatible examples are not all wired the same way.

`openai-chat` and `openai-agents` still use the regular OCI Generative AI endpoint. `openai-responses` is the odd one out: it uses the OpenAI-compatible base URL and also needs a Generative AI project OCID.

It is a small difference, but it is exactly the kind of detail that can waste half an hour when all you wanted was a quick hello-world.

Anyway, if you're playing with OCI GenAI in Python and want a few simple starting points, the repo is here: **[OCI GenAI Python Starters](https://github.com/enricopesce/oci-genai-python-starters)**.
