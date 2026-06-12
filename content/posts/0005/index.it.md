---
title: OCI Function con immagine custom
description: "Costruisci immagini Docker custom per OCI Functions e aggiungi Oracle Database Client o altre dipendenze alle tue funzioni Python serverless."
date: 2023-05-12T19:00:00+01:00
lastmod: 2026-06-12T00:00:00+00:00
draft: false
cover:
  alt: OCI Function con immagine custom
  caption: OCI Function con immagine custom
  image: static/fn.webp
  relative: true
keywords:
- "oci function custom docker"
- "fn project dockerfile"
- "oracle instant client function"
- "custom container serverless"
tags:
- "OCI"
- "Functions"
- "Docker"
- "Serverless"
categories:
- "Serverless"
faq:
  - question: "Posso usare un'immagine Docker personalizzata con OCI Functions?"
    answer: "Sì. OCI Functions supporta immagini container personalizzate. Costruisci un Dockerfile che estende una delle immagini base del Fn Project o parte da zero, la pubblichi su OCI Container Registry (OCIR) e la referenzi nella configurazione della funzione."
  - question: "Perché potrei aver bisogno di un'immagine Docker personalizzata per una OCI Function?"
    answer: "Hai bisogno di un'immagine personalizzata quando la tua funzione dipende da librerie di sistema non disponibili nelle immagini base standard del Fn Project, come Oracle Instant Client per la connettività al database o pacchetti OS specifici."
  - question: "Qual è la dimensione massima dell'immagine container per OCI Functions?"
    answer: "OCI raccomanda di mantenere le immagini sotto i 256 MB per cold start veloci. Immagini più grandi sono tecnicamente supportate ma aumentano significativamente la latenza di cold start."
---

Come abbiamo visto in altri articoli, e' possibile usare il progetto FN con diversi linguaggi di programmazione tramite immagini container predefinite. I linguaggi ufficialmente supportati sono:

* go
* java
* Node.js
* ruby
* Python
* C#

Puoi farlo con la direttiva runtime, ad esempio:

```console
fn init --runtime python test
```

Il comando produce un file `func.yaml` di questo tipo:

{{< highlight yaml "linenos=table" >}}
schema_version: 20180708
name: hello
version: 0.0.1
runtime: python
build_image: fnproject/python:3.9-dev
run_image: fnproject/python:3.9
entrypoint: /python/bin/fdk /function/func.py handler
memory: 256
{{< / highlight >}}

In alcuni casi, pero', le immagini predefinite non sono sufficienti: puo' servire supporto extra per un linguaggio, driver aggiuntivi o strumenti non presenti.

Per risolvere il problema possiamo usare un Dockerfile e un ambiente custom. Possiamo estendere l'immagine FN di base oppure partire da un'immagine completamente diversa.

Come demo ho creato [questo esempio](https://github.com/enricopesce/fn-examples/tree/main/customimage). In particolare il file `func.yaml` e' il seguente:

{{< highlight yaml "linenos=inline" >}}
schema_version: 20180708
name: customimage
version: 0.0.1
runtime: docker
memory: 256
{{< / highlight >}}

In questo modo FN usa un Dockerfile locale, salvato allo stesso livello, per creare l'ambiente di esecuzione della funzione. Nell'esempio il Dockerfile e' questo:

{{< highlight docker "linenos=inline,hl_lines=1 10-12" >}}
FROM fnproject/python:3.9
WORKDIR /function
ADD requirements.txt /function/

RUN pip3 install --target /python/ --no-cache --no-cache-dir -r requirements.txt &&\
    rm -fr ~/.cache/pip /tmp* requirements.txt func.yaml Dockerfile .venv &&\
    chmod -R o+r /python

# install Oracle database client
RUN microdnf install oracle-instantclient-release-el8 &&\
    microdnf install oracle-instantclient-basic &&\
    microdnf clean all

ADD . /function/

RUN chmod -R o+r /function

ENV PYTHONPATH=/function:/python

ENTRYPOINT ["/python/bin/fdk", "/function/func.py", "handler"]
{{< / highlight >}}

In questo Dockerfile abbiamo personalizzato l'immagine ufficiale Python 3.9 con il client database Oracle.

E' possibile fare test locali senza distribuire ogni volta l'immagine nel repository remoto usando l'opzione `--local` nella fase di deploy:

```console
fn deploy --app app --local
```

Eseguendo il server FN in locale sara' possibile eseguire il codice della funzione come su OCI, ma localmente.

Avvia quindi in un terminale separato l'istanza del server FN:

```console
fn start
```

E in un altro terminale il classico comando di invocazione, per esempio:

```console
echo -n '{"name": "Oracle"}' | fn invoke app hello
```
