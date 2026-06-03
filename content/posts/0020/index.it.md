---
title: "OCI GenAI Python Starters: piccole demo per iniziare"
description: "Una raccolta di esempi Python per OCI Generative AI, dalle chiamate dirette SDK a LangChain, LangGraph e API compatibili OpenAI."
date: 2026-04-27T09:00:00+01:00
lastmod: 2026-06-03T00:00:00+00:00
draft: false
slug: "oci-genai-python-starters-demo-python-per-iniziare"
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
tags:
- "OCI"
- "Generative AI"
- "Python"
- "LangChain"
- "OpenAI API"
categories:
- "AI and Machine Learning"
inLanguage: "it-IT"
codeRepository: "https://github.com/enricopesce/oci-genai-python-starters"
softwareRequirements:
- "Python"
- "OCI Generative AI"
- "OCI Python SDK"
- "LangChain"
- "LlamaIndex"
- "LangGraph"
faq:
- question: "Che cos'e' OCI GenAI Python Starters?"
  answer: "OCI GenAI Python Starters e' una raccolta di piccoli esempi Python eseguibili per Oracle Cloud Infrastructure Generative AI, inclusi SDK diretto, LangChain, LlamaIndex, LangGraph e flussi API compatibili OpenAI."
- question: "Chi dovrebbe usare OCI GenAI Python Starters?"
  answer: "Cloud engineer, sviluppatori e solution architect possono usarlo quando serve un punto di partenza funzionante per esperimenti OCI Generative AI in Python."
- question: "Quale esempio OCI compatibile OpenAI richiede un Generative AI project OCID?"
  answer: "L'esempio openai-responses usa la base URL compatibile OpenAI e richiede un Generative AI project OCID."
---

## In breve

**OCI GenAI Python Starters** e' una raccolta di piccole demo Python eseguibili per Oracle Cloud Infrastructure Generative AI. Aiuta gli sviluppatori a passare dalle credenziali a un esempio funzionante usando OCI SDK, LangChain, LlamaIndex, LangGraph o flussi API compatibili OpenAI.

Ogni volta che voglio provare qualcosa di nuovo su OCI Generative AI, mi serve sempre la stessa cosa: un piccolo esempio Python che funzioni davvero.

Non un framework completo. Non un'app rifinita. Solo uno script piccolo, con la configurazione giusta, l'endpoint giusto e un percorso chiaro da "ho le credenziali" a "ok, gira".

Dopo aver ricostruito questi snippet alcune volte, li ho raccolti in un unico repository: **[OCI GenAI Python Starters](https://github.com/enricopesce/oci-genai-python-starters)**.

Niente di sofisticato, solo una serie di piccole demo che puoi eseguire, rompere, modificare e riutilizzare.

## Cosa trovi dentro

- `direct-sdk` se vuoi partire dal minimo indispensabile
- `langchain`, `llamaindex` e `langgraph` se vuoi vedere la stessa idea attraverso strumenti di livello piu' alto
- `openai-chat`, `openai-agents` e `openai-responses` se preferisci il percorso in stile OpenAI
- Una cartella per ogni demo, con il proprio `requirements.txt` e `.env.example`
- Uno script `test_all_demos.sh` se vuoi eseguire tutto una volta configurate le variabili d'ambiente

Ho cercato anche di mantenere un ordine sensato: prima SDK diretto, poi gli esempi con framework quando il flusso OCI di base e' chiaro.

## Una cosa che mi ha fatto perdere tempo

Gli esempi compatibili OpenAI non sono tutti collegati nello stesso modo.

`openai-chat` e `openai-agents` usano ancora il normale endpoint OCI Generative AI. `openai-responses` e' quello diverso: usa la base URL compatibile OpenAI e richiede anche un Generative AI project OCID.

E' una piccola differenza, ma e' esattamente il tipo di dettaglio che puo' far perdere mezz'ora quando si voleva solo un hello-world veloce.

Se stai sperimentando con OCI GenAI in Python e vuoi qualche punto di partenza semplice, il repository e' qui: **[OCI GenAI Python Starters](https://github.com/enricopesce/oci-genai-python-starters)**.

## FAQ

### Che cos'e' OCI GenAI Python Starters?

OCI GenAI Python Starters e' una raccolta di piccoli esempi Python eseguibili per Oracle Cloud Infrastructure Generative AI, inclusi SDK diretto, LangChain, LlamaIndex, LangGraph e flussi API compatibili OpenAI.

### Chi dovrebbe usare OCI GenAI Python Starters?

Cloud engineer, sviluppatori e solution architect possono usarlo quando serve un punto di partenza funzionante per esperimenti OCI Generative AI in Python.

### Quale esempio OCI compatibile OpenAI richiede un Generative AI project OCID?

L'esempio `openai-responses` usa la base URL compatibile OpenAI e richiede un Generative AI project OCID.
