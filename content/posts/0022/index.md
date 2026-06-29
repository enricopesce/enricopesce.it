---
title: "OCI Generative AI in Python: Tutorial with LangChain, LlamaIndex, LangGraph and OpenAI API"
description: "Step-by-step Python tutorial for OCI Generative AI covering direct SDK, LangChain, LlamaIndex, LangGraph, and the OpenAI-compatible API. Includes setup, environment variables, and troubleshooting."
date: 2026-06-29T10:00:00+01:00
lastmod: 2026-06-29T10:00:00+01:00
slug: "oci-generative-ai-python-tutorial"
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
- question: "What Python version does OCI Generative AI require?"
  answer: "Python 3.11 or newer is recommended. All demos in this guide have been tested on Python 3.11+."
- question: "What is the difference between OCI-native and OpenAI-compatible OCI demos?"
  answer: "OCI-native demos use the OCI Python SDK and OCI_SERVICE_ENDPOINT directly. OpenAI-compatible demos use the OpenAI client library with an OCI base URL and OCI authentication, so existing OpenAI code can run against OCI models with minimal changes."
- question: "Does LangChain support OCI Generative AI?"
  answer: "Yes. The langchain-oci package provides a ChatOCIGenAI class that wraps the OCI Generative AI inference endpoint. It works with chains, agents, and other standard LangChain patterns."
- question: "Which demo should I start with for OCI Generative AI in Python?"
  answer: "Start with the direct-sdk demo. It uses only the oci Python package and shows the raw API call with the fewest moving parts. Once that works you can move to the LangChain, LlamaIndex, or LangGraph demos."
- question: "Why does openai-responses need a Generative AI project OCID while openai-chat does not?"
  answer: "The openai-responses demo targets the newer OCI OpenAI Responses API endpoint, which requires a Generative AI project OCID and a different base URL. The openai-chat demo uses the standard chat completions endpoint, which only needs OCI_SERVICE_ENDPOINT and OCI_COMPARTMENT_ID."
- question: "Can I run OCI Generative AI Python demos in OCI Cloud Shell?"
  answer: "Yes. OCI Cloud Shell already has the OCI CLI and credentials configured. Clone the repo, create a virtual environment, install requirements, and set the environment variables in each demo's .env file."
---

Getting a first working OCI Generative AI call in Python should take minutes, not hours. I built **[OCI GenAI Python Starters](https://github.com/enricopesce/oci-genai-python-starters)** to collect the minimal examples I kept rebuilding every time I started experimenting with a new framework or API style on Oracle Cloud.

Seven runnable demos, one folder each, from a bare SDK call to LangGraph agents and the OpenAI-compatible Responses API.

## Two API paths: OCI-native vs OpenAI-compatible

Before choosing a demo, it helps to understand the two distinct ways to call OCI Generative AI from Python:

**OCI-native** — uses the `oci` Python SDK and the standard OCI Generative AI inference endpoint. Authentication is done with OCI API key profiles or instance principals. This is the most direct path and works in any OCI region that has Generative AI.

**OpenAI-compatible** — uses the `openai` Python library (or OpenAI-compatible wrappers in LangChain/agents frameworks) pointed at an OCI endpoint that accepts OpenAI-style requests. This lets you reuse existing OpenAI-shaped code against OCI models with minimal changes.

| Approach | What changes | When to use |
|---|---|---|
| OCI-native | `oci` SDK, OCI endpoint, OCI compartment OCID | New OCI projects, full control |
| OpenAI-compatible | `openai` library, OCI base URL, OCI auth injected | Migrating from OpenAI, reusing existing code |

## The seven demos

| Demo | API style | Main library | Best first question |
|---|---|---|---|
| `direct-sdk` | OCI-native | `oci` | How does a raw OCI Generative AI call look? |
| `langchain` | OCI-native | `langchain-oci` | How does the same call look in LangChain? |
| `llamaindex` | OCI-native | `llama-index-llms-oci-genai` | How does LlamaIndex chat with OCI models? |
| `langgraph` | OCI-native | `langgraph` | How do I build a minimal LangGraph workflow on OCI? |
| `openai-chat` | OpenAI-compatible | `oci-openai` | How do I use OpenAI chat completions style with OCI auth? |
| `openai-agents` | OpenAI-compatible | `openai-agents` | What is the smallest tool-calling agent on OCI? |
| `openai-responses` | OpenAI-compatible | `openai` | How do I use the OpenAI Responses API shape with OCI? |

**Recommended learning order:** `direct-sdk` → `langchain` or `llamaindex` → `langgraph` → `openai-chat` → `openai-agents` → `openai-responses`. Each demo adds one concept over the previous one.

## Setup

### Step 1 — Clone and create a virtual environment

```bash
git clone https://github.com/enricopesce/oci-genai-python-starters.git
cd oci-genai-python-starters
python -m venv .venv
source .venv/bin/activate
```

Works on Linux, macOS and OCI Cloud Shell.

### Step 2 — Install dependencies

Each demo has its own `requirements.txt`. Install them all into the same virtual environment:

```bash
pip install -r demos/direct-sdk/requirements.txt
pip install -r demos/langchain/requirements.txt
pip install -r demos/llamaindex/requirements.txt
pip install -r demos/langgraph/requirements.txt
pip install -r demos/openai-chat/requirements.txt
pip install -r demos/openai-agents/requirements.txt
pip install -r demos/openai-responses/requirements.txt
```

### Step 3 — Verify OCI credentials

All demos authenticate with an OCI API key profile from `~/.oci/config`. A minimal profile looks like this:

```ini
[DEFAULT]
user=ocid1.user.oc1...
fingerprint=aa:bb:cc:dd:ee:ff
key_file=/full/path/to/oci_api_key.pem
tenancy=ocid1.tenancy.oc1...
region=us-chicago-1
```

If you do not have this file yet, set it up with the [OCI CLI setup guide](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm) or run `oci setup config` in OCI Cloud Shell.

### Step 4 — Configure each demo's `.env`

Each demo reads its own `.env` from its folder. Copy the template and fill in the values:

```bash
cp demos/direct-sdk/.env.example demos/direct-sdk/.env
# repeat for each demo you want to run
```

## Environment variables explained

This is where most beginners lose time. The key distinction is that **OCI-native demos and OpenAI-compatible demos use different variables**:

| Variable | Used by | What it is |
|---|---|---|
| `OCI_COMPARTMENT_ID` | all except `openai-responses` | OCI compartment OCID |
| `OCI_SERVICE_ENDPOINT` | `direct-sdk`, `langchain`, `llamaindex`, `langgraph`, `openai-chat`, `openai-agents` | OCI Generative AI inference endpoint for your region |
| `OCI_MODEL_ID_NATIVE` | `direct-sdk`, `langchain`, `llamaindex`, `langgraph` | Model ID for OCI-native requests |
| `OCI_MODEL_ID_OPENAI` | `openai-chat`, `openai-agents`, `openai-responses` | Model ID for OpenAI-compatible requests |
| `OCI_OPENAI_BASE_URL` | `openai-responses` only | OpenAI-compatible base URL ending in `/openai/v1` |
| `OCI_OPENAI_PROJECT_ID` | `openai-responses` only | Generative AI project OCID |
| `OCI_PROFILE` | optional in all | Profile name in OCI config. Default: `DEFAULT` |
| `OCI_CONFIG_FILE` | optional in all | Custom path to OCI config file |

**The critical difference:** `openai-chat` and `openai-agents` still use `OCI_SERVICE_ENDPOINT`, not `OCI_OPENAI_BASE_URL`. Only `openai-responses` uses the OpenAI-compatible base URL and needs a Generative AI project OCID. Missing this distinction is the most common reason `openai-responses` fails while `openai-chat` works fine.

### Where to find the IDs

- **`OCI_COMPARTMENT_ID`**: open the target compartment in the OCI Console → copy the OCID from the compartment details page.
- **`OCI_SERVICE_ENDPOINT`**: the OCI Generative AI inference endpoint for your region, for example `https://inference.generativeai.us-chicago-1.oci.oraclecloud.com`.
- **`OCI_MODEL_ID_NATIVE` / `OCI_MODEL_ID_OPENAI`**: open the OCI Generative AI model catalog in your region and copy a model ID.
- **`OCI_OPENAI_PROJECT_ID`**: open your Generative AI project in the OCI Console → copy the project OCID.

## Running the demos

From the project root, run any demo directly:

```bash
python demos/direct-sdk/main.py
python demos/langchain/main.py
python demos/llamaindex/main.py
python demos/langgraph/main.py
python demos/openai-chat/main.py
python demos/openai-agents/main.py
python demos/openai-responses/main.py
```

Each script sends one hardcoded prompt and prints one response. To change the question, edit the `PROMPT` constant near the top of `main.py`.

To run all demos sequentially once all `.env` files are filled in:

```bash
bash test_all_demos.sh
```

The script prints `PASS` or `FAIL` per demo without installing anything.

## Offline validation

The repo includes unit tests that check environment variable validation without making any OCI requests:

```bash
python -m unittest tests.test_env_validation
```

This is useful to confirm your `.env` files are set correctly before spending time on network issues.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError` | Virtual environment not active or requirements not installed | Activate `.venv` and re-run `pip install -r` for that demo |
| `Missing OCI_...` | Wrong `.env` file or placeholder not replaced | Check the demo's `.env` against the variable table above |
| `No such file: ~/.oci/config` | OCI credentials not configured | Run `oci setup config` or set `OCI_CONFIG_FILE` in the demo's `.env` |
| `401` / `403` / signing error | Wrong OCI API key or missing permissions | Verify the key file path and fingerprint in `~/.oci/config` |
| `400` / `404` from the service | Model ID does not match endpoint or region | Check model availability in the OCI Console for your region |
| `openai-responses` fails, `openai-chat` works | `OCI_OPENAI_BASE_URL` wrong or missing `OCI_OPENAI_PROJECT_ID` | Set base URL ending with `/openai/v1` and add the project OCID |
| Script hangs | Network or OCI service latency | Check connectivity to the OCI inference endpoint |

## Project layout

```
oci-genai-python-starters/
├── demos/
│   ├── direct-sdk/        # Raw OCI SDK call
│   ├── langchain/         # LangChain with OCI
│   ├── llamaindex/        # LlamaIndex with OCI
│   ├── langgraph/         # LangGraph workflow on OCI
│   ├── openai-chat/       # OpenAI chat completions via OCI
│   ├── openai-agents/     # OpenAI Agents SDK via OCI
│   └── openai-responses/  # OpenAI Responses API via OCI
├── tests/
│   └── test_env_validation.py
└── test_all_demos.sh
```

Each demo folder contains `main.py`, `.env.example`, and `requirements.txt`. Nothing else — no shared utilities, no hidden framework dependencies.

The repo is on GitHub: **[enricopesce/oci-genai-python-starters](https://github.com/enricopesce/oci-genai-python-starters)**.
