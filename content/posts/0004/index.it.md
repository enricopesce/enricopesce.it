---
title: Invocare una funzione con Object Storage service
date: 2023-04-20T19:00:00+01:00
draft: false
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

Il servizio OCI Function permette di eseguire del codice su una infrastruttura che non devi gestire. In questo [link]({{< relref path="0003/index.md" lang="it" >}}) ho presentato un esempio base di una OCI function sviluppata in Python.

Una funzionalita' molto interessante e' che le funzioni possono essere invocate automaticamente da altri servizi attraverso un evento, quindi possiamo eseguire del codice anche in risposta ad una azione nel cloud di OCI, oppure usare una funzione come tramite tra piu' servizi cloud che potranno formare un workload complesso.

In questo caso andremo a vedere come invocare una funzione tramite un evento scatenato da un altro servizio di OCI, nello specifico quando copiamo un file all'interno di un Object Storage. 

Visto l'aumento della complessita dell'infrastruttura introdurremmo anche un nuovo concetto chiamato [IaC](https://it.wikipedia.org/wiki/Infrastructure_as_Code) cosi da poter facilitare il deployment di tutte le configurazioni nel cloud, nello specifico useremo un [template Terraform](https://github.com/enricopesce/fn-examples/tree/main/bucket-event), ampliamente supportato su OCI.

Andiamo quindi a lanciare i due comandi per creare l'infrastruttura su OCI

```console
terraform init
terraform apply
```

Una volta creata l'infrastruttura possiamo testare l'esecuzione della funzione func.py inserendo un file all'interno di un bucket.

```console
echo "Hello world!" > hello.txt
oci os object put --bucket-name test --file hello.txt
```

Una volta copiato il file verra' quindi azionata la funzione e attraverso i log potremmo verificare l'esecuzione e l'output

![Log della funzione](static/functionlog.jpg "Log della funzione")

Questo esempio abbastanza banale puo' far comprendere come attraverso gli eventi si possa creare automatismi ed accedere in questo caso ai file in modo dinamico e scalabile.

In scenari piu complessi sara' possibile integrare altri servizi di OCI per elaborare o estrarre dati dai documenti salvati in un Bucket e salvarli ad esempio in altri servizi come Autonomous DB.

Una volta terminati i vostri test sara' possibile eliminare l'infrastruttura con terraform

```console
terraform destroy
```