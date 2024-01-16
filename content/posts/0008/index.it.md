---
title: Alcuni test di performance con PHP e OCI Compute instance
date: 2024-01-17T19:00:00+01:00
draft: true
tags:
  - php
  - performance
categories:
  - compute
cover:
  alt: Alcuni test di performance con PHP e OCI Compute instance
  caption: Alcuni test di performance con PHP e OCI Compute instance
  relative: true
  image: "static/architecture.png"
---

Diverso tempo fa ho sviluppato un tool con l'obiettivo di verificare il vero miglioramento di performance tra le versioni di PHP e successivamente capire quale AWS instance type era la piu' performante, visto che su AWS non e' possibile scegliere un dimensionamento personalizzato delle risorse CPU e RAM ho voluto comprendere tra le diverse decine di instance type cosa cambiasse.

In queste vacanze natalizie mi sono dedicato ad esterndere questo progetto e di fare la stessa cosa con OCI, Oracle Cloud Infrastructure.

La grande differenza con AWS e' che su OCI e' possibile scegliere la shape (instance type) di base e poter selezionare quanta CPU e RAM utilizzare in modo flessibile, quindi i test saranno eseguiti su le differenti shape, visto che il test non e' di scalabilita' ma di performance di esecuzione di un singolo thread usero' il taglio minimo di 1 OCPU e 16 GB di RAM per ogni shape type.

Per capire meglio, lee shape disponibili sono le seguenti, ogni shape puo essere usata scegliendo in modo granulare OCPU e RAM.

Shape basate su tecnologia AMD

* VM.Standard.E4.Flex (Processor: AMD EPYC 7J13. Base frequency 2.55 GHz, max boost frequency 3.5 GHz)
* VM.Standard.E5.Flex (Processor: AMD EPYC 9J14. Base frequency 2.4 GHz, max boost frequency 3.7 GHz)

Shape basate su tecnologia INTEL

* VM.Standard3.Flex (Processor: Intel Xeon Platinum 8358. Base frequency 2.6 GHz, max turbo frequency 3.4 GHz)
* VM.Optimized3.Flex (Processor: Intel Xeon 6354. Base frequency 3.0 GHz, max turbo frequency 3.6 GHz)

Shape basate su tecnologia ARM AMPERE

* VM.Standard.A1.Flex (Each OCPU corresponds to a single hardware execution thread. Processor: Ampere Altra Q80-30. Max frequency 3.0 GHz.)


