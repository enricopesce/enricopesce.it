---
title: OCI Functions un esempio con Python
date: 2023-03-20T19:00:00+01:00
draft: false
tags:
  - functions
categories:
  - serverless
cover:
  alt: OCI Functions un esempio con Python
  caption: OCI Functions un esempio con Python
  image: static/oci-fn.png
  relative: true
---

Il servizio [OCI Function](https://www.oracle.com/cloud/cloud-native/functions/) permette di eseguire del codice su una infrastruttura che non devi gestire, in modo scalabile e automatizzato.

Questo concetto viene chiamato "serverless" perche' l'utente finale non dovra' piu' preoccuparsi di gestire alcuna infrastruttura per eseguire il proprio codice.

OCI implementa quello che e' il progetto open source [FN](https://fnproject.io/) il progetto e' stato integrato con i servizi di Oracle cloud e si basa su l'esecuzione di codice all'interno di un container, quindi puo' supportare potenzialmente qualsiasi linguaggio di programmazione e qualsiasi tipo di container su architettura x86, inoltre non e' strettamente legato con l'infrastruttura di Oracle e si puo passare tranquillamente tra ambienti FN diversi senza grosse limitiazioni.

Per creare una function vi consiglio di leggere la pagina ufficiale del servizio e di seguire il [quick start](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsquickstartguidestop.htm) nel mio caso ho preferito seguire il deployment dal mio computer che e' anche il mio ambiente di sviluppo abituale ma e' possibile fare lo stesso dalla cloud shell di OCI con tempi molto piu' brevi visto che verra' eseguita in un datacenter con altissime performance di rete.

L'esempio di questa function e' su Python, installazione e preconfigurazione di tutto l'ambiente e' gia stato creato, se hai bisogno di una guida specifica ti consiglio di cercare nella [Developer Guide](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/devtoolslanding.htm) o nella OCI [Getting started](https://docs.oracle.com/en-us/iaas/Content/GSG/Concepts/get-account.htm)

I comandi per configurare l'ambiente locale con fn sono i seguenti

```console
fn create context <my-context> --provider oracle
fn use context <my-context>
fn update context oracle.profile <profile-name>
fn update context oracle.compartment-id <compartment-ocid>
fn update context api-url <api-endpoint>
fn update context registry <region-key>.ocir.io/<tenancy-namespace>/<repo-name-prefix>
docker login -u '<tenancy-namespace>/<user-name>' <region-key>.ocir.io
```

Allo stesso modo andiamo a configurare l'applicazione fn lato OCI:

```console
fn create app pythonexamples --annotation oracle.com/oci/subnetIds='[<sunbet-ocid>]'
```

Successivamente andremo a creare uno scheletro della function localmente:

```console
fn init --runtime python helloworld
```

Verranno creati dei file all'interno di una nuova directory

<pre>
─ helloworld
  ├── func.py
  ├── func.yaml
  └── requirements.txt
</pre>

il file func.py conterra' il codice eseguito e il suo relativo file requirements.txt di dipendenze mentre il file func.yaml e' il file di configurazione per eseguire con FN il codice.

Nello specifico il codice di esempio e' un "Hello world" che potete visionare [qui](https://github.com/enricopesce/fn-examples/blob/main/helloworld/func.py)

Step successivo propedeutico all'esecuzione della funzione e' quello di build e deploy, dove da riga di comando il tool fn andra' ad orchestrare la build del container, il suo rilascio sul repository docker di OCI e la sua configurazione su OCI Functions.

```console
fn -v deploy --app hello
```

Da ora e' possibile eseguire il codice remotamente

```console
echo -n '{"name": "Oracle"}' | fn invoke pythonexamples hello
```

con questo comando passeremo ad esempio un parametro e verra' eseguita la funzione nella region OCI di destinazione, se abilitati sara' possibile visionare l'output generato dalla funzione nel servizio OCI logging.

In questo articolo abbiamo visto un semplice esempio di function e come utlizzarle, e' possibile anche eseguire una funzione attraverso altri servizi OCI con degli eventi specifici o utilizzare le function come servizio API, utilizzare altri linguaggi oltre Python o altre versioni di container.

Per altri esempi di funzioni su OCI in Python vi consiglio [questo repository](https://github.com/oracle-samples/oracle-functions-samples)