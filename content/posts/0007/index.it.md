---
title: Ingestion dati scalabile e serverless con OCI Functions
description: "Costruisci una pipeline dati scalabile: CSV da stazioni meteo verso Autonomous Database usando OCI Functions, Object Storage e Terraform."
date: 2023-10-20T19:00:00+01:00
lastmod: 2026-06-12T00:00:00+00:00
draft: false
cover:
  alt: Ingestion dati scalabile e serverless con OCI Functions
  caption: Ingestion dati scalabile e serverless con OCI Functions
  relative: true
  image: "static/architecture.webp"
keywords:
- "oci data ingestion"
- "csv to autonomous database"
- "serverless etl oracle"
- "oci function pipeline"
tags:
- "OCI"
- "Functions"
- "Object Storage"
- "Autonomous Database"
- "Terraform"
categories:
- "Serverless"
faq:
  - question: "Come si costruisce una pipeline ETL serverless su Oracle Cloud?"
    answer: "Il pattern OCI standard usa Object Storage come zona di atterraggio, una Event Rule per triggerare una OCI Function all'upload del file, e la Function per analizzare e caricare i dati in Autonomous Database. Terraform provvede l'intera pipeline come infrastruttura come codice."
  - question: "OCI Functions può elaborare file CSV di grandi dimensioni da Object Storage?"
    answer: "Sì. OCI Functions può scaricare oggetti direttamente da Object Storage usando l'OCI Python SDK, analizzare i dati CSV con pandas o il modulo csv standard, e inserire righe in Autonomous Database. Per file molto grandi, considera il chunking o OCI Data Integration."
  - question: "Una pipeline di data ingestion serverless su OCI è conveniente economicamente?"
    answer: "Sì. Con OCI Functions si paga solo il tempo di esecuzione effettivo. I costi di Object Storage sono minimi per carichi CSV tipici. Per pattern di ingestione intermittenti o batch, questo approccio è molto più economico di una VM in esecuzione continua o di un servizio ETL gestito."
---

In questo articolo sfrutteremo al massimo le capacita' di OCI, abbracciando questi principi:

* Scalabilita'
* Resilienza
* Flessibilita'
* Sicurezza
* Automazione

Il progetto `loadfileintoadw` si trova nello stesso repository GitHub usato finora per parlare di OCI Functions: [fn-examples](https://github.com/enricopesce/fn-examples/tree/main/loadfileintoadw).

Questo esempio aiuta a capire come integrare piu' servizi OCI e sfruttare meglio il cloud provider.

Simuleremo una serie di stazioni meteo che scrivono un file CSV con dati di campionamento, come temperatura e umidita'. Il sensore carica automaticamente il file in un bucket Object Storage.

L'elaborazione viene invocata automaticamente tramite una [Function](https://github.com/enricopesce/fn-examples/blob/main/loadfileintoadw/func.py) che, in questo caso, converte il formato del file da CSV a JSON e lo salva in modo nativo in un Autonomous Database serverless.

Il codice [IaC](https://github.com/enricopesce/fn-examples/blob/main/loadfileintoadw/infrastructure.tf) e' stato sviluppato per eseguire l'intero deployment, dall'infrastruttura alla funzione. Dentro la cartella del progetto basta eseguire il comando:

```console
terraform apply
```

Se non hai familiarita' con Terraform, ti consiglio di consultare la [documentazione ufficiale](https://registry.terraform.io/providers/oracle/oci/latest/docs), il [tutorial](https://docs.oracle.com/en-us/iaas/developer-tutorials/tutorials/tf-simple-infrastructure/01-summary.htm) e il [video](https://www.youtube.com/watch?v=MjmikFgvKvI).
