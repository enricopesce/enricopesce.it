---
title: "Ottieni un cluster Kubernetes in pochi minuti su OCI"
description: "Distribuisci cluster OKE pronti per produzione in pochi minuti con OKED, senza competenze approfondite su OCI."
date: 2024-09-15T18:00:00+01:00
lastmod: 2026-06-12T00:00:00+00:00
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
faq:
  - question: "Cos'è Oracle Kubernetes Engine (OKE)?"
    answer: "OKE è il servizio Kubernetes gestito di Oracle Cloud Infrastructure. Provvede e gestisce il control plane, gestisce gli aggiornamenti dei nodi e si integra con i servizi OCI come Load Balancer, Block Volume e Container Registry. Si paga solo per i worker node, non per il control plane."
  - question: "Posso eseguire OKE nel Free Tier OCI?"
    answer: "Il control plane OKE è gratuito. I worker node usano istanze compute, che possono essere Always Free A1.Flex (fino a 4 OCPU e 24 GB di RAM combinati). Con i nodi Ampere si può eseguire un cluster Kubernetes piccolo ma funzionale a costo zero."
  - question: "Cos'è OKED e come semplifica il deployment OKE?"
    answer: "OKED (Oracle Kubernetes Engine Deploy) è uno strumento CLI open-source che automatizza il provisioning di un cluster OKE production-ready con impostazioni best-practice. Gestisce networking, policy IAM, node pool e add-on del cluster, riducendo il deployment a un singolo comando."
---

## Il mio primo progetto di automazione OCI

Dopo 10 anni di esperienza con pratiche DevOps, automazione, infrastructure as code e molte discussioni con clienti, ho deciso di costruire uno strumento che aiuti a distribuire un'architettura Kubernetes ben definita senza richiedere competenze infrastrutturali profonde.

### Progetto Oracle Kubernetes Engine Deploy (OKED)

OKED aiuta a distribuire un'infrastruttura Kubernetes completa su OCI, incluse le dipendenze di rete necessarie, senza richiedere esperienza specifica su OCI.

Questa e' l'edizione **Terraform** di OKED. Se preferisci infrastructure as code basato su Python, vedi l'[edizione Pulumi di OKED]({{< relref "/posts/0017/index.md" >}}).

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

![Demo deployment OKED](static/demo.webp)
