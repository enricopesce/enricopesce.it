---
title: "Ottieni un cluster Kubernetes in pochi minuti su OCI"
description: "Distribuisci cluster OKE pronti per produzione in pochi minuti con OKED, senza competenze approfondite su OCI."
date: 2024-09-15T18:00:00+01:00
draft: false
slug: "ottieni-un-cluster-kubernetes-in-pochi-minuti-su-oci"
cover:
  alt: "Ottieni un cluster Kubernetes in pochi minuti su OCI"
  caption: "Ottieni un cluster Kubernetes in pochi minuti su OCI"
  relative: true
  image: "static/logo.webp"
keywords:
- "oke terraform deploy"
- "oracle kubernetes engine"
- "oked automation"
- "oci kubernetes cluster"
tags:
- "OCI"
- "OKE"
- "Kubernetes"
- "Automation"
- "Terraform"
categories:
- "Kubernetes"
---

## Il mio primo progetto di automazione OCI

Dopo 10 anni di esperienza con pratiche DevOps, automazione, infrastructure as code e molte discussioni con clienti, ho deciso di costruire uno strumento che aiuti a distribuire un'architettura Kubernetes ben definita senza richiedere competenze infrastrutturali profonde.

### Progetto Oracle Kubernetes Engine Deploy (OKED)

OKED aiuta a distribuire un'infrastruttura Kubernetes completa su OCI, incluse le dipendenze di rete necessarie, senza richiedere esperienza specifica su OCI.

I requisiti principali che mi hanno spinto a sviluppare il progetto sono:

- **Semplicita'**: i clienti chiedono di essere operativi in pochi minuti senza prompt complessi o competenze infrastrutturali profonde.
- **Funzionante**: molti esempi online sono complessi da capire e alcuni non funzionano.
- **Well-architected**: i clienti vogliono sicurezza e design corretti applicati di default.

Le funzionalita' che differenziano questo tool dal wizard della console OCI e da altri progetti Terraform sono:

- Creazione automatica di VCN e subnetting: basta definire il CIDR della supernet.
- Discovery e configurazione automatica di tutti gli availability domain per distribuire i nodi e migliorare la disponibilita'.
- Discovery e configurazione automatica dell'immagine OKE node piu' recente, corretta e ottimizzata.
- File di configurazione Kubernetes generato e pronto da usare, ad esempio con `export KUBECONFIG=$PWD/kubeconfig`.
- Codice estendibile man mano che crescono le competenze su OCI.

Trovi tutte le informazioni nella [pagina GitHub del progetto](https://github.com/enricopesce/oracle-kubernetes-engine-deploy).

Ecco una breve demo:

![Demo deployment OKED](static/demo.gif)
