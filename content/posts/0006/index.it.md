---
title: Usare OCI Function con una immagine custom
date: 2023-05-12T19:00:00+01:00
draft: false
tags:
  - functions
categories:
  - serverless
cover:
  alt: Usare OCI Function con una immagine custom
  caption: Usare OCI Function con una immagine custom
  image: static/fn.png
  relative: true
---

Come abbiamo visto da altri miei [articoli]({{< ref "/tags/functions/" >}}), e' possibile utilizzare il progetto FN sfruttando delle immagini container predefinite, i linguaggi ufficialmente supportati sono:

* Go
* Java
* Node.js
* Ruby
* Python
* C#

vengono supportati attraverso della immagini predefinite che verranno automaticamente utilizzate specificiando la direttiva runtime, ad esempio:

```console
fn init --runtime python test
```

il comando produrra' un file func.yaml di questo tipo

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

Molto spesso pero' le immagini predefinite non sono sufficienti, sia per supporto alle varie versioni del linguaggio o per alcune dipendenze che derivano dal sistema operativo come driver extra da installare o altri tool mancanti.

Per risolvere questa problematica e' possibile utilizzare un proprio Dockerfile per poter utilizzare un proprio environment custom, possiamo estendere l'immagine FN di base o partire da una immagine totalmente diversa.

A supporto di questo articolo ho creato [questo esempio](https://github.com/enricopesce/fn-examples/tree/main/customimage)
nello specifico il file func.yaml sara' cosi formato:

{{< highlight yaml "linenos=inline" >}}
schema_version: 20180708
name: customimage
version: 0.0.1
runtime: docker
memory: 256
{{< / highlight >}}

in questo modo FN utilizzera' un file Dockerfile locale salvato allo stesso suo livello per creare l'environment di esecuzione della funzione, dall'esempio il Dockerfile si presentera' cosi:

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

Dove andremmo a personalizzare l'immagine ufficiale di Python 3.9 installando il client database di Oracle.

E' possibile fare dei test locali senza dover ogni volta dover distribuire l'immagine nel repository remoto utilizzando l'opzione specifica --local nella fase di deploy

```console
fn deploy --app app --local
```

lanciando il server FN localmente sara' possibile eseguire il codice della function allo stesso modo come su OCI ma localmente

Quindi lanciare su una sessione distinta del terminale

```console
fn start
```

e in un altra il classico comando di invocazione, ad esempio

```console
echo -n '{"name": "Oracle"}' | fn invoke app hello
```