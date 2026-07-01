---
title: "OCI Generative AI in Python: da dove iniziare"
description: "Demo Python minimali per OCI Generative AI, e cosa sapere prima di scegliere tra SDK OCI-native e API compatibile OpenAI."
date: 2026-06-29T10:00:00+01:00
lastmod: 2026-06-29T10:00:00+01:00
slug: "tutorial-python-oci-generative-ai"
draft: false
cover:
  alt: "Tutorial Python OCI Generative AI"
  caption: "Tutorial Python OCI Generative AI"
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
- "oci openai compatibile python"
- "oracle generative ai python esempio"
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
- "AI e Machine Learning"
inLanguage: "it-IT"
codeRepository: "https://github.com/enricopesce/oci-genai-python-starters"
softwareRequirements:
- "Python 3.11+"
- "OCI Generative AI"
- "OCI Python SDK"
- "LangChain"
- "LlamaIndex"
- "LangGraph"
faq:
- question: "Cos'è OCI GenAI Python Starters?"
  answer: "Una raccolta di sette demo Python minimali ed eseguibili per OCI Generative AI. Ogni demo vive nella propria cartella e mostra un modo specifico di chiamare i modelli OCI: SDK diretto, LangChain, LlamaIndex, LangGraph e tre approcci compatibili OpenAI."
- question: "Qual è la differenza tra i demo OCI-native e quelli compatibili OpenAI?"
  answer: "I demo OCI-native usano l'SDK Python oci e il classico endpoint OCI Generative AI. I demo compatibili OpenAI usano la libreria openai puntata su un endpoint OCI, così il codice OpenAI esistente gira sui modelli OCI con modifiche minime. I due approcci usano variabili d'ambiente e base URL diversi."
- question: "Da quale demo conviene iniziare?"
  answer: "Inizia da direct-sdk. Usa solo il pacchetto oci, non ha framework sopra e mostra esattamente come appare una chiamata OCI Generative AI grezza. Una volta che funziona, aggiungi LangChain o il demo compatibile OpenAI a seconda di dove sta andando il tuo progetto."
- question: "Perché openai-responses richiede un project OCID mentre openai-chat no?"
  answer: "openai-responses punta al nuovo endpoint OCI Responses API, che richiede un Generative AI project OCID e un base URL diverso. openai-chat usa il classico endpoint chat completions e ha bisogno solo di un service endpoint e un compartment OCID."
- question: "Posso eseguire questi demo in OCI Cloud Shell?"
  answer: "Sì. OCI Cloud Shell ha già le credenziali configurate. Basta clonare il repo, creare un virtual environment, installare i requirements del demo e compilare il file .env."
---

Ogni volta che inizio a sperimentare con un nuovo framework o stile di API su OCI Generative AI, perdo la stessa ora a ricostruire lo stesso boilerplate: credenziali giuste, endpoint giusto, formato del model ID giusto, variabili d'ambiente giuste. Poi scopro che LangChain e l'API compatibile OpenAI usano una variabile diversa rispetto all'SDK diretto. Poi trovo che il nuovo Responses API richiede un project OCID che l'endpoint chat completions non richiede.

Nessuna di queste cose è spiegata in un posto solo nella documentazione ufficiale. Così ho smesso di ricostruire da zero e ho messo tutto in **[OCI GenAI Python Starters](https://github.com/enricopesce/oci-genai-python-starters)**.

## Cos'è

Sette piccoli demo Python, una cartella ciascuno. Ogni demo fa una cosa sola: inviare un prompt a un modello OCI Generative AI e stampare la risposta. Nessuna utility condivisa, nessun framework nascosto, nessun scaffolding da produzione. Solo il percorso più breve dalle credenziali all'output per ogni approccio specifico.

I demo coprono i due modi distinti di chiamare OCI Generative AI da Python:

**OCI-native** usa l'SDK `oci` direttamente. Si parla con l'endpoint di inferenza OCI, ci si autentica con il profilo OCI e si passa un compartment OCID. È l'approccio più diretto, quello che mostra la maggior parte della documentazione OCI.

**Compatibile OpenAI** usa la libreria `openai`, puntata su un endpoint OCI che accetta richieste in stile OpenAI. Il motivo per cui esiste è pratico: molto codice Python è già scritto contro le API OpenAI. Con il percorso compatibile OpenAI, quel codice gira sui modelli OCI cambiando il base URL e iniettando l'autenticazione OCI — senza riscrivere nulla.

I demo seguono esattamente questa divisione:

| Demo | Approccio |
|---|---|
| `direct-sdk` | OCI-native, senza framework |
| `langchain` | OCI-native via LangChain |
| `llamaindex` | OCI-native via LlamaIndex |
| `langgraph` | OCI-native via LangGraph |
| `openai-chat` | Compatibile OpenAI, chat completions |
| `openai-agents` | Compatibile OpenAI, Agents SDK |
| `openai-responses` | Compatibile OpenAI, Responses API |

## Il dettaglio che fa perdere più tempo

I due approcci sembrano simili in superficie ma usano configurazioni diverse. I demo OCI-native richiedono `OCI_SERVICE_ENDPOINT` e `OCI_COMPARTMENT_ID`. Quelli compatibili OpenAI richiedono gli stessi — tranne `openai-responses`, che usa un base URL completamente diverso (`OCI_OPENAI_BASE_URL`) e richiede un Generative AI project OCID che gli altri non richiedono.

Questo è il dettaglio che costa più tempo. `openai-chat` e `openai-responses` sembrano lo stesso tipo di demo ma sono collegati in modo diverso. Il repo lo rende esplicito nel file `.env.example` di ogni demo, così si vede esattamente cosa serve prima di eseguire.

## Per chi è

Se sei nuovo a OCI Generative AI e vuoi capire come funziona l'API prima di aggiungere un framework sopra, inizia da `direct-sdk`. Mostra la chiamata grezza senza niente di nascosto.

Se stai già usando LangChain o LlamaIndex in un progetto e vuoi usare i modelli OCI, i demo con framework mostrano la configurazione minima necessaria.

Se hai codice OpenAI esistente e vuoi eseguirlo su OCI senza riscriverlo, i demo compatibili OpenAI mostrano le differenze esatte — inclusa quella meno ovvia tra `openai-chat` e `openai-responses`.

Il repo è su GitHub: **[enricopesce/oci-genai-python-starters](https://github.com/enricopesce/oci-genai-python-starters)**.
