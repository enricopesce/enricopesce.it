---
title: Accedere ad Autonomous Database da una OCI Function
description: "Connetti OCI Functions ad Autonomous Database in modo sicuro usando Vault secrets e Terraform, con esempio IaC e codice Python."
date: 2023-09-01T19:00:00+01:00
draft: false
cover:
  alt: Accedere ad Autonomous Database da una OCI Function
  caption: Accedere ad Autonomous Database da una OCI Function
  relative: true
  image: static/fn.webp
keywords:
- "oci function autonomous database"
- "python oracledb serverless"
- "oci vault secrets"
- "terraform oracle function"
tags:
- "OCI"
- "Functions"
- "Autonomous Database"
- "Terraform"
- "Serverless"
categories:
- "Serverless"
---

Dopo aver visto come creare un'immagine custom nel [caso precedente]({{< ref "/posts/0005" >}}), dove abbiamo installato il client Oracle, ora proviamo a usare questa immagine custom per connetterci a un database Oracle.

Sfrutteremo al massimo le capacita' del cloud. In questo esempio useremo la metodologia Infrastructure as Code (IaC) per fornire un'architettura reale, facilmente replicabile da chiunque.

Il progetto `toautonomous` si trova nello stesso repository GitHub usato finora per parlare di OCI Functions: [fn-examples](https://github.com/enricopesce/fn-examples/tree/main/toautonomous). Il README del progetto descrive la procedura di configurazione dell'infrastruttura.

Se non hai familiarita' con Terraform, ti consiglio di consultare la [documentazione ufficiale](https://registry.terraform.io/providers/oracle/oci/latest/docs), il [tutorial](https://docs.oracle.com/en-us/iaas/developer-tutorials/tutorials/tf-simple-infrastructure/01-summary.htm) e il [video](https://www.youtube.com/watch?v=MjmikFgvKvI).

Nel mio caso il file `terraform.tfvars` sara' simile a questo, con valori modificati:

{{< highlight hcl "linenos=table" >}}
tenancy_ocid = "ocid1.tenancy.oc1..aaaaaaaao4a5a"
region = "eu-frankfurt—l"
compartment_id = "ocid1.compartment.oc1..aaaaaaaawdnpdyjvbala"
root_compartment_id = "ocid1.tenancy.oc1..aaaaaaaa2h4xgua7d4a5a"
registry = "fra.ocir.io/frddomvd8z4q/functions"
application_name = "toautonomous"
vault_ocid = "ocid1.vault.oc1.eu-frankfurt-1.dzsgmkchaafmg.abthe2a"
vault_key_ocid = "ocid1.key.oc1.eu-frankfurt-1.dzsgmkchaafmga2ra"
{{< / highlight >}}

Il codice [IaC](https://github.com/enricopesce/fn-examples/blob/main/toautonomous/infrastructure.tf) e' stato sviluppato per gestire l'intero deployment: infrastruttura, build del container custom per la funzione e rilascio. Dentro la cartella del progetto e' quindi sufficiente eseguire il comando indicato nel README.

Verranno create diverse risorse, non facilmente rappresentabili da questo grafo di dipendenze generato con Terraform:

![Risorse create](static/graph.webp "Log della Function")

La situazione e' piu' semplice di quanto sembri. Le principali risorse OCI usate sono:

- VCN
- Autonomous DB
- Function
- Vault
- Logging

Vale la pena notare che prima della build la funzione attende la creazione del database e include il wallet di autenticazione dentro l'immagine della funzione. Allo stesso modo, la password dell'utente amministrativo viene salvata e cifrata nel servizio Vault e recuperata a runtime dalla funzione quando necessario, senza salvare credenziali nel codice.

Queste implementazioni rendono il progetto di esempio molto sicuro.

Qui trovi il [file della funzione](https://github.com/enricopesce/fn-examples/blob/main/toautonomous/func.py) per comprenderne meglio il funzionamento.
