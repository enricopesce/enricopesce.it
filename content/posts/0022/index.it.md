---
title: "OCI Generative AI in Python: Tutorial con LangChain, LlamaIndex, LangGraph e API OpenAI"
description: "Tutorial Python passo-passo per OCI Generative AI: SDK diretto, LangChain, LlamaIndex, LangGraph e API compatibile OpenAI. Include setup, variabili d'ambiente e troubleshooting."
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
- question: "Quale versione di Python serve per OCI Generative AI?"
  answer: "Python 3.11 o superiore. Tutti i demo di questa guida sono stati testati su Python 3.11+."
- question: "Qual e' la differenza tra i demo OCI-native e quelli compatibili OpenAI?"
  answer: "I demo OCI-native usano l'OCI Python SDK e OCI_SERVICE_ENDPOINT direttamente. I demo compatibili OpenAI usano la libreria openai con un base URL OCI e autenticazione OCI iniettata, cosi' il codice OpenAI esistente gira su modelli OCI con modifiche minime."
- question: "LangChain supporta OCI Generative AI?"
  answer: "Si'. Il pacchetto langchain-oci fornisce la classe ChatOCIGenAI che wrappa l'endpoint di inferenza OCI Generative AI. Funziona con chain, agent e tutti i pattern LangChain standard."
- question: "Da quale demo conviene iniziare con OCI Generative AI in Python?"
  answer: "Inizia da direct-sdk. Usa solo il pacchetto oci e mostra la chiamata API grezza con il minor numero di dipendenze. Una volta che funziona, puoi passare ai demo LangChain, LlamaIndex o LangGraph."
- question: "Perche' openai-responses richiede un project OCID mentre openai-chat no?"
  answer: "Il demo openai-responses punta al nuovo endpoint OCI OpenAI Responses API, che richiede un Generative AI project OCID e un base URL diverso. Il demo openai-chat usa il classico endpoint chat completions, che ha bisogno solo di OCI_SERVICE_ENDPOINT e OCI_COMPARTMENT_ID."
- question: "Posso eseguire i demo Python di OCI Generative AI in OCI Cloud Shell?"
  answer: "Si'. OCI Cloud Shell ha gia' CLI OCI e credenziali configurate. Basta clonare il repo, creare un virtual environment, installare i requirements e impostare le variabili d'ambiente nel file .env di ogni demo."
---

Ottenere una prima chiamata OCI Generative AI funzionante in Python dovrebbe richiedere minuti, non ore. Ho costruito **[OCI GenAI Python Starters](https://github.com/enricopesce/oci-genai-python-starters)** per raccogliere gli esempi minimi che continuavo a ricostruire ogni volta che iniziavo a sperimentare con un nuovo framework o stile di API su Oracle Cloud.

Sette demo eseguibili, una cartella ciascuno, dalla chiamata SDK grezza agli agent LangGraph e all'API Responses compatibile OpenAI.

## Due percorsi API: OCI-native vs compatibile OpenAI

Prima di scegliere un demo, conviene capire i due modi distinti di chiamare OCI Generative AI da Python:

**OCI-native** — usa l'SDK Python `oci` e il classico endpoint di inferenza OCI Generative AI. L'autenticazione avviene con profili OCI API key o instance principal. E' il percorso piu' diretto e funziona in qualsiasi regione OCI che abbia Generative AI.

**Compatibile OpenAI** — usa la libreria Python `openai` (o wrapper compatibili OpenAI in LangChain/agents framework) puntata su un endpoint OCI che accetta richieste in stile OpenAI. Questo permette di riutilizzare codice OpenAI esistente sui modelli OCI con modifiche minime.

| Approccio | Cosa cambia | Quando usarlo |
|---|---|---|
| OCI-native | SDK `oci`, endpoint OCI, compartment OCID | Nuovi progetti OCI, controllo completo |
| Compatibile OpenAI | libreria `openai`, base URL OCI, auth OCI iniettata | Migrazione da OpenAI, riutilizzo codice esistente |

## I sette demo

| Demo | Stile API | Libreria principale | Prima domanda utile |
|---|---|---|---|
| `direct-sdk` | OCI-native | `oci` | Come appare una chiamata OCI Generative AI grezza? |
| `langchain` | OCI-native | `langchain-oci` | Come appare la stessa chiamata in LangChain? |
| `llamaindex` | OCI-native | `llama-index-llms-oci-genai` | Come chatta LlamaIndex con i modelli OCI? |
| `langgraph` | OCI-native | `langgraph` | Come costruisco un workflow LangGraph minimale su OCI? |
| `openai-chat` | Compatibile OpenAI | `oci-openai` | Come uso le chat completions stile OpenAI con auth OCI? |
| `openai-agents` | Compatibile OpenAI | `openai-agents` | Qual e' l'agent con tool-calling piu' piccolo su OCI? |
| `openai-responses` | Compatibile OpenAI | `openai` | Come uso l'API Responses OpenAI con OCI? |

**Ordine di apprendimento consigliato:** `direct-sdk` → `langchain` o `llamaindex` → `langgraph` → `openai-chat` → `openai-agents` → `openai-responses`. Ogni demo aggiunge un concetto al precedente.

## Setup

### Step 1 — Clone e virtual environment

```bash
git clone https://github.com/enricopesce/oci-genai-python-starters.git
cd oci-genai-python-starters
python -m venv .venv
source .venv/bin/activate
```

Funziona su Linux, macOS e OCI Cloud Shell.

### Step 2 — Installa le dipendenze

Ogni demo ha il proprio `requirements.txt`. Installali tutti nello stesso virtual environment:

```bash
pip install -r demos/direct-sdk/requirements.txt
pip install -r demos/langchain/requirements.txt
pip install -r demos/llamaindex/requirements.txt
pip install -r demos/langgraph/requirements.txt
pip install -r demos/openai-chat/requirements.txt
pip install -r demos/openai-agents/requirements.txt
pip install -r demos/openai-responses/requirements.txt
```

### Step 3 — Verifica le credenziali OCI

Tutti i demo si autenticano con un profilo OCI API key in `~/.oci/config`. Un profilo minimo:

```ini
[DEFAULT]
user=ocid1.user.oc1...
fingerprint=aa:bb:cc:dd:ee:ff
key_file=/percorso/completo/oci_api_key.pem
tenancy=ocid1.tenancy.oc1...
region=us-chicago-1
```

Se non hai ancora questo file, configuralo con la [guida OCI CLI](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm) o esegui `oci setup config` in OCI Cloud Shell.

### Step 4 — Configura il file `.env` di ogni demo

Ogni demo legge il proprio `.env` dalla sua cartella. Copia il template e compila i valori:

```bash
cp demos/direct-sdk/.env.example demos/direct-sdk/.env
# ripeti per ogni demo che vuoi eseguire
```

## Variabili d'ambiente spiegate

Qui si perde piu' tempo. La distinzione chiave e' che **i demo OCI-native e quelli compatibili OpenAI usano variabili diverse**:

| Variabile | Usata da | Cosa e' |
|---|---|---|
| `OCI_COMPARTMENT_ID` | tutti tranne `openai-responses` | OCID del compartimento OCI |
| `OCI_SERVICE_ENDPOINT` | `direct-sdk`, `langchain`, `llamaindex`, `langgraph`, `openai-chat`, `openai-agents` | Endpoint inferenza OCI Generative AI per la tua regione |
| `OCI_MODEL_ID_NATIVE` | `direct-sdk`, `langchain`, `llamaindex`, `langgraph` | Model ID per richieste OCI-native |
| `OCI_MODEL_ID_OPENAI` | `openai-chat`, `openai-agents`, `openai-responses` | Model ID per richieste compatibili OpenAI |
| `OCI_OPENAI_BASE_URL` | solo `openai-responses` | Base URL compatibile OpenAI che termina con `/openai/v1` |
| `OCI_OPENAI_PROJECT_ID` | solo `openai-responses` | OCID del progetto Generative AI |
| `OCI_PROFILE` | opzionale in tutti | Nome del profilo nel config OCI. Default: `DEFAULT` |
| `OCI_CONFIG_FILE` | opzionale in tutti | Percorso custom al file di config OCI |

**La differenza critica:** `openai-chat` e `openai-agents` usano ancora `OCI_SERVICE_ENDPOINT`, non `OCI_OPENAI_BASE_URL`. Solo `openai-responses` usa il base URL compatibile OpenAI e richiede un Generative AI project OCID. Confondere questo e' il motivo piu' comune per cui `openai-responses` fallisce mentre `openai-chat` funziona.

### Dove trovare gli ID

- **`OCI_COMPARTMENT_ID`**: apri il compartimento nella OCI Console → copia l'OCID dalla pagina dettagli.
- **`OCI_SERVICE_ENDPOINT`**: l'endpoint di inferenza OCI Generative AI per la tua regione, ad esempio `https://inference.generativeai.us-chicago-1.oci.oraclecloud.com`.
- **`OCI_MODEL_ID_NATIVE` / `OCI_MODEL_ID_OPENAI`**: apri il catalogo modelli OCI Generative AI nella tua regione e copia un model ID.
- **`OCI_OPENAI_PROJECT_ID`**: apri il tuo progetto Generative AI nella OCI Console → copia l'OCID del progetto.

## Eseguire i demo

Dalla root del progetto, esegui qualsiasi demo direttamente:

```bash
python demos/direct-sdk/main.py
python demos/langchain/main.py
python demos/llamaindex/main.py
python demos/langgraph/main.py
python demos/openai-chat/main.py
python demos/openai-agents/main.py
python demos/openai-responses/main.py
```

Ogni script invia un prompt fisso e stampa una risposta. Per cambiare la domanda, modifica la costante `PROMPT` in cima a `main.py`.

Per eseguire tutti i demo in sequenza, con tutti i file `.env` gia' compilati:

```bash
bash test_all_demos.sh
```

Lo script stampa `PASS` o `FAIL` per ogni demo senza installare nulla.

## Validazione offline

Il repo include unit test che verificano la validazione delle variabili d'ambiente senza fare nessuna chiamata OCI:

```bash
python -m unittest tests.test_env_validation
```

Utile per confermare che i file `.env` siano corretti prima di perdere tempo su problemi di rete.

## Troubleshooting

| Sintomo | Causa probabile | Soluzione |
|---|---|---|
| `ModuleNotFoundError` | Virtual environment non attivo o requirements non installati | Attiva `.venv` e ri-esegui `pip install -r` per quel demo |
| `Missing OCI_...` | File `.env` sbagliato o placeholder non sostituito | Controlla il `.env` del demo rispetto alla tabella variabili sopra |
| `No such file: ~/.oci/config` | Credenziali OCI non configurate | Esegui `oci setup config` o imposta `OCI_CONFIG_FILE` nel `.env` del demo |
| `401` / `403` / errore di firma | Chiave OCI API errata o permessi mancanti | Verifica il percorso della key file e il fingerprint in `~/.oci/config` |
| `400` / `404` dal servizio | Model ID non compatibile con l'endpoint o la regione | Controlla la disponibilita' del modello nella OCI Console per la tua regione |
| `openai-responses` fallisce, `openai-chat` funziona | `OCI_OPENAI_BASE_URL` errato o `OCI_OPENAI_PROJECT_ID` mancante | Imposta il base URL che termina con `/openai/v1` e aggiungi il project OCID |
| Lo script si blocca | Latenza di rete o del servizio OCI | Verifica la connettivita' all'endpoint di inferenza OCI |

## Struttura del progetto

```
oci-genai-python-starters/
├── demos/
│   ├── direct-sdk/        # Chiamata OCI SDK grezza
│   ├── langchain/         # LangChain con OCI
│   ├── llamaindex/        # LlamaIndex con OCI
│   ├── langgraph/         # Workflow LangGraph su OCI
│   ├── openai-chat/       # Chat completions OpenAI via OCI
│   ├── openai-agents/     # OpenAI Agents SDK via OCI
│   └── openai-responses/  # OpenAI Responses API via OCI
├── tests/
│   └── test_env_validation.py
└── test_all_demos.sh
```

Ogni cartella demo contiene `main.py`, `.env.example` e `requirements.txt`. Nient'altro — nessuna utility condivisa, nessuna dipendenza da framework nascosta.

Il repo e' su GitHub: **[enricopesce/oci-genai-python-starters](https://github.com/enricopesce/oci-genai-python-starters)**.
