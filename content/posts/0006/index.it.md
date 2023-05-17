---
title: Usare OCI Function con una immagine custom
date: 2023-05-12T19:00:00+01:00
draft: true
tags:
  - functions
categories:
  - serverless
cover:
  alt: Usare OCI Function con una immagine custom
  caption: Usare OCI Function con una immagine custom
  relative: true
---

Come abbiamo visto da altri miei articoli, e' possibile semplicemente utilizzare il progetto FN sfruttando delle immagini container predefinite, i linguaggi ufficialmente supportati sono:

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
name: helloworld
version: 0.0.1
runtime: python
build_image: fnproject/python:3.9-dev
run_image: fnproject/python:3.9
entrypoint: /python/bin/fdk /function/func.py handler
memory: 256
{{< / highlight >}}

Molto spesso pero' le immagini predefinite non sono sufficienti, sia per supporto alle varie versioni del linguaggio o per alcune dipendenze che derivano dal sistema operativo come driver extra da installare o altri tool mancanti.

Per risolvere questa problematica e' possibile utilizzare un proprio Dockerfile per poter cosi utilizzare il proprio environment custom, e' quindi possibile estendere l'immagine di base o partire da una immagine totalmente diversa.

A supporto di questo articolo ho creato un esempio in [questo]() repoistory