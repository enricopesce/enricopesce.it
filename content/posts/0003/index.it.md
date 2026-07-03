---
title: "OCI Functions: un esempio Python"
description: "Guida passo passo per creare OCI Functions serverless con Python e distribuire il primo progetto FN su Oracle Cloud Infrastructure."
date: 2023-03-20T19:00:00+01:00
lastmod: 2026-06-12T00:00:00+00:00
draft: false
cover:
  alt: "OCI Functions: un esempio Python"
  caption: "OCI Functions: un esempio Python"
  image: static/oci-fn.webp
  relative: true
keywords:
- "oci functions python"
- "oracle serverless"
- "fn project oracle"
- "faas oracle cloud"
tags:
- "OCI"
- "Functions"
- "Python"
- "Serverless"
categories:
- "Serverless"
faq:
  - question: "Cos'è OCI Functions?"
    answer: "OCI Functions è il servizio di compute serverless di Oracle Cloud Infrastructure, basato sul progetto open-source Fn Project. Permette di eseguire codice senza gestire server. Si paga solo il tempo di esecuzione e il servizio scala automaticamente da zero."
  - question: "Quali linguaggi di programmazione supporta OCI Functions?"
    answer: "OCI Functions supporta nativamente Go, Java, Node.js, Ruby e Python. Poiché le funzioni girano su immagini container, è possibile usare qualsiasi linguaggio con un runtime compatibile Docker tramite immagini personalizzate."
  - question: "OCI Functions è disponibile nel tier Always Free OCI?"
    answer: "Sì. OCI Always Free include 2 milioni di invocazioni e 400.000 GB-secondi di compute al mese. È sufficiente per la maggior parte degli scenari di sviluppo e produzione a basso traffico."
related:
- "/posts/0004"
- "/posts/0005"
- "/posts/0006"
---

Il servizio [OCI Functions](https://www.oracle.com/cloud/cloud-native/functions/) permette di eseguire codice su un'infrastruttura che non devi gestire, in modo scalabile e automatizzato.

Questo concetto viene chiamato "serverless" perche' l'utente finale non deve preoccuparsi di gestire infrastruttura per eseguire il proprio codice.

OCI implementa il progetto open source [FN](https://fnproject.io/). Il progetto e' integrato con i servizi Oracle Cloud ed e' basato sull'esecuzione di codice dentro container. Puo' quindi supportare potenzialmente qualsiasi linguaggio di programmazione e qualsiasi tipo di container su architettura x86; inoltre non e' strettamente legato all'infrastruttura Oracle e puo' essere usato anche con altri ambienti FN.

Per creare una funzione ti consiglio di leggere la pagina ufficiale del servizio e seguire la [quick start](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsquickstartguidestop.htm). Nel mio caso ho preferito seguire il deployment dal mio computer, che e' anche il mio ambiente di sviluppo abituale, ma e' possibile fare lo stesso da OCI Cloud Shell con tempi piu' brevi grazie alla rete del data center.

L'esempio di questa funzione e' basato su Python. Le credenziali OCI di base sono gia' state create; se ti serve una guida specifica puoi consultare la [Developer Guide](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/devtoolslanding.htm) o la guida OCI [Getting started](https://docs.oracle.com/en-us/iaas/Content/GSG/Concepts/get-account.htm).

I comandi per configurare l'ambiente FN locale sono:

```console
fn create context <my-context> --provider oracle
fn use context <my-context>
fn update context oracle.profile <profile-name>
fn update context oracle.compartment-id <compartment-ocid>
fn update context api-url <api-endpoint>
fn update context registry <region-key>.ocir.io/<tenancy-namespace>/<repo-name-prefix>
docker login -u '<tenancy-namespace>/<user-name>' <region-key>.ocir.io
```

Con questi comandi abbiamo istruito FN a usare il cloud OCI e configurato un repository OCI in cui salvare il container usato da FN per eseguire il nostro codice.

Allo stesso modo creiamo l'applicazione Function sul lato OCI:

```console
fn create app pythonexamples --annotation oracle.com/oci/subnetIds='["<sunbet-ocid>"]'
```

Come puoi vedere, il comando non e' dell'OCI CLI ma continuiamo a usare FN. Se vogliamo possiamo usare il comando OCI nativo per creare l'applicazione, ma vista la compatibilita' del progetto open source possiamo usare anche quello FN.

Il passaggio successivo e' creare localmente lo scheletro dei file applicativi per FN specificando il linguaggio, in questo caso Python:

```console
fn init --runtime python helloworld
```

I file verranno creati in una nuova directory:

```text
helloworld
├── func.py
├── func.yaml
└── requirements.txt
```

Il file `func.py` contiene il codice eseguito, `requirements.txt` le dipendenze e `func.yaml` la configurazione FN.

In particolare, il codice di esempio e' un "Hello world" visibile [qui](https://github.com/enricopesce/fn-examples/blob/main/helloworld/func.py).

Il passaggio preparatorio all'esecuzione della funzione e' build e deploy: dal terminale il comando `fn` orchestra la build del container, il rilascio nel repository OCI e la configurazione su OCI Functions.

```console
fn -v deploy --app hello
```

Al termine del comando, se tutto e' andato bene, e' possibile eseguire la funzione da remoto su OCI:

```console
echo -n '{"name": "Oracle"}' | fn invoke pythonexamples hello
```

In questo esempio passiamo un parametro alla funzione, che verra' letto dalla funzione remota. Se abilitato, sara' possibile visualizzare l'output generato nel servizio OCI Logging.

In questo articolo abbiamo visto un esempio semplice di funzione e come usarla. E' possibile eseguire una funzione tramite eventi di altri servizi OCI, usarla come API service, usare altri linguaggi o versioni diverse dei container.

Per altri esempi di funzioni OCI in Python consiglio [questo repository](https://github.com/oracle-samples/oracle-functions-samples) oppure il repository di supporto agli articoli a questo [link](https://github.com/enricopesce/fn-examples).
