---
title: Invocare una funzione con Object Storage service
date: 2022-11-20T09:03:20-08:00
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

Il servizio OCI Function permette di eseguire del codice su una infrastruttura che non devi gestire, in modo scalabile e automatizzato. 

Questo concetto viene chiamato "serverless" perche' l'utente finale non dovra' piu' preoccuparsi di gestire alcuna infrastruttura per eseguire il proprio codice.

Le funzioni possono essere invocate manualmente o anche automaticamente da altri servizi attraverso un trigger, in questo caso andremo a vedere come invocare una funzione quando copiamo un file all'interno di un altro servizio OCI, l'Object Storage e ad esempio leggere tale file attraverso la funzione stessa appena invocata.


