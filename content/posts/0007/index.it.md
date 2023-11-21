---
title: Data ingestion scalabile e serverless
date: 2023-10-20T19:00:00+01:00
draft: false
tags:
  - functions
categories:
  - serverless
cover:
  alt: Data ingestion scalabile e serverless
  caption: Data ingestion scalabile e serverless
  relative: true
  image: "static/architecture.png"
---

In questo articolo andremo a sfruttare al meglio le capacita' di OCI sfruttando appieno i seguenti principi:

* scalabilita'
* resilenza
* flessibilita
* sicurezza
* automazione

Il progetto "loadfileintoadw" si trova nello stesso repository GitHub utilizzato finora per parlare di OCI Function [fn-examples](https://github.com/enricopesce/fn-examples/tree/main/loadfileintoadw).

Questo esempio vi aiutara' a capire come integrare piu servizi OCI e sfruttare il cloud provider il massimo possibile.

Simuleremo una serie di stazioni meteo che andranno a scrivere un file CSV con dei dati di campionamento (temperatura, umidita' etc) il sensore andra' in automatico a inserire il file in un bucket di Object Storage.

L'elaborazione verra invocata automaticamente attraverso una [Function](https://github.com/enricopesce/fn-examples/blob/main/loadfileintoadw/func.py) che in questo caso convertita' il file di formato, da CSV a JSON, e salvato nativamente su un database serverlesee Autonomous.

Il codice [IaC](https://github.com/enricopesce/fn-examples/blob/main/loadfileintoadw/infrastructure.tf) e' stato sviluppato per eseguire tutto il deployment da quello infrastrutturale a quello della function, quindi bastera' all'interno della folder del progetto lanciare il comando per creare tutto quanto:

```console
terraform apply
```

Se non conosci terraform ti consiglio di consultare la [documentazione ufficiale](https://registry.terraform.io/providers/oracle/oci/latest/docs) e il nostro [tutorial](https://docs.oracle.com/en-us/iaas/developer-tutorials/tutorials/tf-simple-infrastructure/01-summary.htm) e [video](https://www.youtube.com/watch?v=MjmikFgvKvI)
