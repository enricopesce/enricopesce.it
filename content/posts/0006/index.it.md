---
title: Accedere ad un database Autonomous da una OCI Function
date: 2023-05-20T19:00:00+01:00
draft: false
tags:
  - functions
categories:
  - serverless
cover:
  alt: Accedere ad un database Autonomous da una OCI Function
  caption: Accedere ad un database Autonomous da una OCI Function
  relative: true
---


Una volta eseguiti alcuni semplici test con FN elencati  [qui]({{< ref "/tags/functions/" >}}), e' ora il momento di implementare qualcosa di piu' complesso e articolato, sfruttando al meglio le capacita' del cloud, quindi introdurre automazione e infrastructure as cloud (IaC)

In questo articolo vedremo come attraverso un template Terraform creare uno stack architetturale piu' complesso di una funzione OCI che andra' a collegarsi ad un database OCI Autonomous con la gestione di credenziali di autenticazione direttamente integrate.

Il progetto "toautonomous" si trova nello stesso repository GitHub utilizzato finora per parlare di OCI Function [fn-examples](https://github.com/enricopesce/fn-examples/tree/main/toautonomous) nel README del progetto e' descritto la procedura di configurazione.

nel mio caso il file terraform.tfvars sara simile a questo (vlori alterati):

{{< highlight hcl "linenos=table" >}}
tenancy_ocid     = "ocid1.tenancy.oc1..aaaaaaaao4a5a"
region           = "eu-frankfurt—l"
compartment_id   = "ocid1.compartment.oc1..aaaaaaaawdnpdyjvbala"
root_compartment_id   = "ocid1.tenancy.oc1..aaaaaaaa2h4xgua7d4a5a"
registry         = "fra.ocir.io/frddomvd8z4q/functions"
application_name = "toautonomous"
vault_ocid       = "ocid1.vault.oc1.eu-frankfurt-1.dzsgmkchaafmg.abthe2a"
vault_key_ocid   = "ocid1.key.oc1.eu-frankfurt-1.dzsgmkchaafmga2ra"
{{< / highlight >}}

Il codice [IaC](https://github.com/enricopesce/fn-examples/blob/main/toautonomous/infrastructure.tf) e' stato sviluppato per eseguire tutto il deployment da quello infrastrutturale a quello legato alla build del container e il suo rilascio, quindi bastera' all'interno della folder del progetto lanciare il comando

```console
terraform apply
```

Verranno create diverse risorse, non facilmente rappresentate da questo grafico di dipendenze creato con Terraform

![Risorse create](static/graph.png "Log della funzione")

La situazione e' piu' semplice di quanto si creda, le risorse OCI principali che andremo a utilizzare sono:

* VCN
* Autonomous DB
* Function
* Vault
* Logging

Terraform fara' tutto il resto, se non hai mai usato terraform qui una [guida OCI](https://docs.oracle.com/en-us/iaas/developer-tutorials/tutorials/tf-provider/01-summary.htm)

La funzione prima di essere costruita attendera' la creazione del database e includera' il wallett di autenticazione all'interno della function image, in modo similare la password di amministrazione dell'utente verra' salvata e crittografata all'interno del servizio Vault e ottenuta run-time dalla funzione quando necessario senza dover salvare dati di credenziali nel codice.

Qui il file della [funzione](https://github.com/enricopesce/fn-examples/blob/main/toautonomous/func.py)



