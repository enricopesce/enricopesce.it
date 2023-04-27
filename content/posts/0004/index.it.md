---
title: Invocare una funzione con Object Storage service
date: 2023-04-20T19:00:00+01:00
draft: true
tags:
  - functions
categories:
  - serverless
cover:
  alt: Invocare una funzione con Object Storage service
  caption: Invocare una funzione con Object Storage service
  image: static/objectstoragefunction.webp
  relative: true
---

Il servizio OCI Function permette di eseguire del codice su una infrastruttura che non devi gestire, in modo scalabile e automatizzato. In questo [link]() ho presentato un esempio di una OCI function sviluppata in Python.

Le funzioni possono essere invocate manualmente o anche automaticamente da altri servizi attraverso un trigger, quindi possiamo eseguire del codice anche in risposta ad una azione nel cloud di OCI.

In questo caso andremo a vedere come invocare una funzione quando copiamo un file all'interno di un Object Storage e ad esempio leggere tale file attraverso la funzione stessa appena invocata.

