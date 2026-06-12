---
title: "Arrestare una VM OCI dall'interno dell'istanza"
description: "Arresta in modo ordinato una VM OCI dall'interno usando instance metadata e autenticazione instance principal. Include un semplice alias bash."
date: 2024-12-09T18:00:00+01:00
lastmod: 2026-06-12T00:00:00+00:00
draft: false
slug: "arrestare-vm-oci-dall-interno-dell-istanza"
cover:
  alt: "Arrestare una VM OCI"
  caption: "Arrestare una VM OCI"
  relative: true
  image: "static/switch.webp"
keywords:
- "oci instance principal"
- "stop vm oracle cloud"
- "oci metadata api"
- "oci cli instance action"
tags:
- "OCI"
- "Compute"
- "CLI"
- "Instance Principal"
categories:
- "Cloud Operations"
faq:
  - question: "Cos'è l'autenticazione Instance Principal in OCI?"
    answer: "Instance Principal permette a un'istanza compute OCI di autenticarsi alle API OCI senza archiviare credenziali. L'istanza viene aggiunta a un dynamic group e una policy IAM concede a quel gruppo permessi specifici. L'OCI SDK legge automaticamente il certificato dell'istanza."
  - question: "Come si ferma un'istanza OCI dall'interno dell'istanza stessa?"
    answer: "Si interroga l'OCI Instance Metadata Service per ottenere l'OCID e la regione dell'istanza, poi si usa l'OCI CLI o SDK con autenticazione Instance Principal per chiamare l'API instance action con l'azione STOP. Non è necessario archiviare API key o credenziali su disco."
  - question: "Cos'è l'OCI Instance Metadata Service (IMDS)?"
    answer: "L'OCI IMDS è un endpoint HTTP all'indirizzo 169.254.169.254 accessibile dall'interno di qualsiasi istanza OCI. Fornisce metadati come l'OCID dell'istanza, la regione, il dominio di disponibilità, la shape e i dettagli VNIC senza richiedere autenticazione."
---

## Introduzione

Quando esegui workload su Oracle Cloud Infrastructure (OCI), gestire le istanze in modo efficiente e' fondamentale. Questa guida mostra come creare un metodo semplice per spegnere una VM OCI dall'interno dell'istanza stessa, usando instance metadata e autenticazione instance principal.

## Prerequisiti

- Un'istanza OCI con autenticazione instance principal abilitata
- OCI CLI installata sull'istanza
- Conoscenza base delle operazioni da riga di comando

## Capire i componenti

### Instance Metadata

Ogni istanza OCI puo' accedere ai propri metadata tramite un endpoint locale. Questi metadata includono informazioni importanti come:

- Instance OCID, cioe' Oracle Cloud Identifier
- Region
- Compartment ID
- Availability Domain

Puoi accedere a queste informazioni senza autenticazione quando fai la richiesta dall'interno dell'istanza:

```bash
curl http://169.254.169.254/opc/v1/instance/id
curl http://169.254.169.254/opc/v1/instance/region
```

### Autenticazione Instance Principal

Instance Principal e' un modo sicuro per autenticare chiamate API OCI senza gestire file di configurazione o API key. Quando e' abilitato, l'istanza puo' effettuare chiamate API usando la propria identita'.

## Il comando base

Questo e' il comando base per eseguire uno shutdown ordinato:

```bash
oci compute instance action \
    --action SOFTSTOP \
    --instance-id $(curl -s http://169.254.169.254/opc/v1/instance/id) \
    --auth instance_principal \
    --region $(curl -s http://169.254.169.254/opc/v1/instance/region)
```

Vediamo cosa fa ogni parte:

- `oci compute instance action`: comando base per le operazioni sulle istanze
- `--action SOFTSTOP`: specifica uno shutdown ordinato
- `--instance-id $(...)`: recupera l'ID dell'istanza corrente dai metadata
- `--auth instance_principal`: usa l'identita' dell'istanza per l'autenticazione
- `--region $(...)`: recupera la region corrente dai metadata

## Semplificare tutto con un alias

Per semplificare il processo puoi creare un alias. Ecco come:

1. Apri il file di configurazione della shell:

```bash
nano ~/.bashrc  # per utenti bash
# oppure
nano ~/.zshrc   # per utenti zsh
```

2. Aggiungi l'alias:

```bash
alias ocishutdown='oci compute instance action \
    --action SOFTSTOP \
    --instance-id $(curl -s http://169.254.169.254/opc/v1/instance/id) \
    --auth instance_principal \
    --region $(curl -s http://169.254.169.254/opc/v1/instance/region)'
```

3. Ricarica la configurazione:

```bash
source ~/.bashrc  # per bash
# oppure
source ~/.zshrc   # per zsh
```

Ora puoi digitare semplicemente `ocishutdown` per arrestare in modo ordinato la tua istanza.

## Conclusione

Usando instance metadata e autenticazione instance principal puoi creare metodi efficienti e sicuri per gestire le istanze OCI. Questo approccio elimina la necessita' di salvare credenziali e semplifica le attivita' operative.

Anche se questa guida si concentra sullo shutdown, gli stessi principi valgono per altre operazioni di gestione, come start, reset o raccolta di informazioni sull'istanza. Puoi adattare questi esempi alle tue esigenze.
