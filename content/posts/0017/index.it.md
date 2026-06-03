---
title: "Distribuire cluster Oracle Kubernetes Engine in pochi minuti"
description: "OKED con Pulumi: distribuisci cluster OKE su Oracle Cloud Free Tier. Kubernetes su OCI senza esperienza approfondita e con buone pratiche di sicurezza."
date: 2025-04-25T18:00:00+01:00
draft: false
slug: "distribuire-cluster-oracle-kubernetes-engine-in-pochi-minuti"
cover:
  alt: "Distribuire cluster Oracle Kubernetes Engine in pochi minuti"
  caption: "Distribuire cluster Oracle Kubernetes Engine in pochi minuti"
  relative: true
  image: "static/logo.png"
keywords:
- "oke pulumi deploy"
- "oracle kubernetes free tier"
- "oked automation tool"
- "kubernetes oracle cloud"
tags:
- "OCI"
- "OKE"
- "Kubernetes"
- "Pulumi"
- "Automation"
categories:
- "Kubernetes"
---

Nel panorama cloud-native di oggi, Kubernetes e' diventato lo standard *de facto* per l'orchestrazione dei container. Configurare un cluster Kubernetes pronto per la produzione puo' pero' essere ancora complesso e richiedere tempo, soprattutto per chi e' nuovo nell'ecosistema. **OKED** (*Oracle Kubernetes Engine Deploy*) e' una soluzione che semplifica la distribuzione di cluster Kubernetes su Oracle Cloud Infrastructure.

![Demo distribuzione OKED](https://github.com/enricopesce/oracle-kubernetes-engine-deploy/blob/main/demo.gif?raw=true)

## Cos'e' OKED?

OKED e' uno strumento automatico che semplifica la distribuzione di cluster Oracle Kubernetes Engine (OKE). Costruito su Pulumi, consente di avere un ambiente Kubernetes funzionante in pochi minuti, senza richiedere competenze approfondite su OCI o Kubernetes.

> "Up and running in minutes without any prompt and OCI expertise."

Lo strumento gestisce tutti gli aspetti della distribuzione del cluster, dal provisioning infrastrutturale alla configurazione di rete. E' utile sia per principianti che vogliono sperimentare con Kubernetes, sia per sviluppatori esperti che cercano una base affidabile per ambienti di produzione.

## Funzionalita' principali

Cosa rende OKED diverso da altri metodi di deployment, incluso il wizard della console OCI?

* **Deployment senza esperienza approfondita**: ottieni un cluster funzionante senza conoscenza profonda di OCI o Kubernetes
* **Creazione automatica della VCN**: definisci una supernet CIDR e OKED calcola le subnet
* **Configurazione multi-availability domain**: scoperta e configurazione automatica degli availability domain per aumentare la resilienza del cluster
* **Immagini nodo ottimizzate**: selezione automatica delle immagini OKE piu' recenti e ottimizzate
* **Configurazione pronta all'uso**: genera un file Kubernetes config utilizzabile subito con `kubectl`
* **Sicurezza well-architected**: applica buone pratiche di sicurezza basate sulle raccomandazioni ufficiali OCI
* **Estensibilita'**: essendo basato su Pulumi, e' semplice personalizzarlo ed estenderlo per esigenze specifiche

## Architettura

OKED distribuisce un cluster di tipo `BASIC`, che non comporta costi di gestione, seguendo l'architettura raccomandata nella [documentazione Oracle](https://docs.oracle.com/en-us/iaas/Content/ContEng/Concepts/contengnetworkconfigexample.htm#example-oci-cni-publick8sapi_privateworkers_publiclb).

![Architettura OKED](https://github.com/enricopesce/oracle-kubernetes-engine-deploy/blob/main/arch.png?raw=true)

L'ambiente distribuito include:

1. Endpoint pubblico per la Kubernetes API con worker node privati
2. Supporto per load balancer pubblici
3. Segmentazione di rete corretta con security list e route table
4. Alta disponibilita' su piu' availability domain

Con le impostazioni predefinite puoi distribuire un cluster semplice usando risorse **Oracle Cloud Free Tier** a **costo zero**, sfruttando le istanze ARM Ampere A1 gratuite.

## Come iniziare

Per partire con OKED serve una configurazione minima:

```bash
# Clone the repository
git clone https://github.com/enricopesce/oracle-kubernetes-engine-deploy.git
cd oracle-kubernetes-engine-deploy

# Set up environment
python -m venv .venv
source .venv/bin/activate
pip install poetry
pulumi install

# Configure and deploy
pulumi stack init testing
pulumi config set compartment_ocid "your-compartment-ocid"
pulumi up
```

In 10-15 minuti avrai un cluster Kubernetes operativo e pronto per le applicazioni:

```bash
chmod 600 kubeconfig
export KUBECONFIG=$PWD/kubeconfig
kubectl get pods -A
```

## Perche' scegliere OKED?

OKED nasce dalla frustrazione verso soluzioni esistenti spesso complesse da capire o non funzionanti. Il progetto risponde a tre requisiti principali:

1. **Semplicita'**: deploy rapido senza conoscenza estesa o configurazione manuale
2. **Affidabilita'**: a differenza di molti esempi online, OKED funziona davvero come dichiarato
3. **Best practice**: segue le raccomandazioni dell'Oracle Well-Architected Framework

Per team che vogliono avviare velocemente ambienti Kubernetes su OCI, per sviluppo, test o produzione, OKED offre un percorso diretto che riduce complessita' ed errori potenziali.

## Provalo

Che tu voglia sperimentare con Kubernetes su Oracle Cloud Free Tier o distribuire cluster pronti per la produzione, OKED e' un buon punto di partenza. Il progetto e' open-source e cerca feedback e contributi dalla community.

Il progetto completo e' disponibile su GitHub: [github.com/enricopesce/oracle-kubernetes-engine-deploy](https://github.com/enricopesce/oracle-kubernetes-engine-deploy).

---

Usi Kubernetes su Oracle Cloud? Sono interessato a feedback pratici sui pattern di automazione del deployment e sui relativi tradeoff.
