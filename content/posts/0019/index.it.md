---
title: "OCI GenAI Catalog: scegliere il modello giusto"
description: "Una guida di riferimento a oltre 30 LLM disponibili nel servizio Generative AI di Oracle Cloud, con wizard per la scelta del modello."
date: 2026-03-09T09:00:00+01:00
lastmod: 2026-06-12T00:00:00+00:00
draft: false
slug: "oci-genai-catalog-scegliere-modello-giusto"
cover:
  alt: "Confronto modelli OCI GenAI Catalog"
  caption: "Confronto modelli OCI GenAI Catalog"
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
  - question: "Quali provider LLM sono disponibili su OCI Generative AI?"
    answer: "OCI Generative AI offre modelli di Cohere (Command R, Command R+), Meta (Llama 3, 3.1, 3.2, 3.3), xAI (Grok), Google (Gemma) e altri provider. Il catalogo include oltre 30 varianti di modelli con diverse dimensioni e capacità."
  - question: "Come scelgo il modello LLM giusto su OCI Generative AI?"
    answer: "Scegli in base al compito principale: Cohere Command R+ per RAG e documenti enterprise, Llama 3.1/3.3 70B per ragionamento generale e coding, modelli Llama più piccoli per casi d'uso a bassa latenza, e modelli di embedding per la ricerca vettoriale. La dimensione della finestra di contesto e la qualità dell'output contano più del numero di parametri."
  - question: "Tutti i modelli OCI Generative AI sono disponibili in tutte le regioni?"
    answer: "No. La disponibilità dei modelli varia per regione OCI. US East (Ashburn) e EU Francoforte hanno tipicamente la selezione più ampia. Consulta la documentazione OCI Generative AI o lo strumento OCI GenAI Catalog per la disponibilità regionale aggiornata."
related:
- "/posts/0016"
- "/posts/0018"
- "/posts/0022"
---

OCI Generative AI e' cresciuto rapidamente: Cohere, Google, Meta, OpenAI, xAI, tutti disponibili, ciascuno con piu' varianti. Ogni volta che iniziavo un nuovo progetto dovevo consultare la documentazione per trovare il modello corretto.

Cosi' ho creato **[OCI GenAI Catalog](https://enricopesce.github.io/oci-genai-catalog/)**: una guida di riferimento con oltre 30 modelli e un wizard guidato per la selezione.

## Cosa contiene

- **24 modelli chat** da 5 provider, con specifiche su context window, multimodalita', tool use, reasoning e supporto al fine-tuning
- **9 modelli embedding** e 1 modello reranking per pipeline RAG
- Un **wizard di selezione modello**: filtra per task, livello di performance e necessita' di contesto per ottenere una top 3 raccomandata

## Sintesi provider

| Provider | Modelli | Punto di forza |
|----------|---------|----------------|
| Cohere | 5 | RAG, fine-tuning |
| Google Gemini | 3 | Multimodale, long context fino a 1M token |
| Meta Llama | 5 | Open weights, efficienza MoE |
| OpenAI gpt-oss | 2 | Reasoning, agenti |
| xAI Grok | 6 | Contesto 2M, specializzazione codice |

I dati provengono dalla documentazione ufficiale OCI e vengono mantenuti aggiornati. Provalo qui: **[OCI GenAI Catalog](https://enricopesce.github.io/oci-genai-catalog/)**.
