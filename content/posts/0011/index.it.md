---
title: "OCI Compute Standard Flex Shapes: un altro benchmark CPU multicore"
description: "Analisi prezzo-prestazioni OCI Compute con Geekbench 6: confronto tra shape AMD, Intel e ARM."
date: 2024-02-10T18:00:00+01:00
lastmod: 2026-06-12T00:00:00+00:00
slug: "un-altro-benchmark-cpu-multicore-delle-shape-oci-compute-standard-flex"
draft: false
keywords:
- "oci flex shapes benchmark"
- "ampere a1 performance"
- "oracle cloud vm comparison"
- "oci price performance"
tags:
- "OCI"
- "Compute"
- "Ampere"
- "Geekbench"
- "Benchmark"
categories:
- "Benchmark"
faq:
  - question: "Cosa sono le OCI Flex Shape?"
    answer: "Le OCI Flex Shape sono istanze compute in cui si configurano indipendentemente il numero di OCPU e la RAM invece di scegliere una dimensione fissa. Le shape disponibili includono VM.Standard.E4.Flex (AMD), VM.Standard.E5.Flex (AMD), VM.Standard3.Flex (Intel), VM.Optimized3.Flex (Intel) e VM.Standard.A1.Flex (ARM Ampere)."
  - question: "Come si confronta VM.Standard.E5.Flex con E4.Flex nei benchmark multicore?"
    answer: "Nei test multicore Geekbench 6, E5.Flex (AMD EPYC 9J14) supera E4.Flex (AMD EPYC 7J13) di circa il 20-30% con lo stesso numero di OCPU. E5 ha anche una frequenza boost massima più alta a 3,7 GHz contro 3,5 GHz per E4."
  - question: "Quale shape OCI è migliore per carichi di lavoro multicore?"
    answer: "Per le massime prestazioni multicore pure, VM.Standard.E5.Flex è la migliore opzione x86. Per il miglior rapporto prezzo-per-core, VM.Standard.A1.Flex (Ampere) è molto competitivo, specialmente quando i carichi possono utilizzare molti core contemporaneamente."
related:
- "/posts/0010"
- "/posts/0021"
- "/posts/0012"
---

Quando si sceglie un'istanza compute, fattori come potenza di calcolo, rapporto prezzo-prestazioni e ottimizzazione del workload hanno un ruolo significativo. Concentriamoci sulle seguenti shape standard flex disponibili nella maggior parte delle region OCI:

* **VM.Standard.E4.Flex** (Processore: AMD EPYC 7J13. Frequenza base 2,55 GHz, boost massimo 3,5 GHz)
* **VM.Standard.E5.Flex** (Processore: AMD EPYC 9J14. Frequenza base 2,4 GHz, boost massimo 3,7 GHz)
* **VM.Standard3.Flex** (Processore: Intel Xeon Platinum 8358. Frequenza base 2,6 GHz, turbo massimo 3,4 GHz)
* **VM.Optimized3.Flex** (Processore: Intel Xeon 6354. Frequenza base 3,0 GHz, turbo massimo 3,6 GHz)
* **VM.Standard.A1.Flex** (ogni OCPU corrisponde a un singolo thread hardware. Processore: Ampere Altra Q80-30. Frequenza massima 3,0 GHz)

Ho eseguito benchmark con **Geekbench 6** su tre configurazioni CPU: 2, 4 e 8 core.

Per ulteriori informazioni sui [test interni eseguiti](https://www.geekbench.com/doc/geekbench6-benchmark-internals.pdf), consulta il link.

Esploriamo i risultati in performance multi-thread:

{{< plotly "//plotly.com/~enricopesce/7.embed" >}}

Possiamo vedere che la shape piu' potente e' **VM.Standard.E5.Flex**. Questa nuova shape basata su AMD supera in modo significativo le altre shape; i risultati, in alcuni casi, sono comunque vicini.

Ma non possiamo valutare solo le performance: nel mondo reale il rapporto prezzo-prestazioni e' un fattore decisivo.

### **Confronto Costi Mensili**

Analizziamo i costi mensili approssimativi per ogni shape, basati sui prezzi Oracle di febbraio 2024:

{{< plotly "//plotly.com/~enricopesce/5.embed" >}}

Possiamo osservare che i prezzi variano e non tutte le shape hanno lo stesso costo. Considerando la shape ARM Ampere **VM.Standard.A1.Flex**, si puo' ottenere una performance simile con circa il 90% del costo di **VM.Optimized3.Flex** o il 75% del costo di **VM.Standard3.Flex**.

### **Raccomandazioni**

Scegli la tua istanza OCI Compute valutando con attenzione performance, costo e requisiti del workload. Che tu stia eseguendo database, analytics o workload AI, comprendere le performance CPU multicore aiuta a prendere decisioni piu' consapevoli.

La shape giusta dipende dal workload, dall'obiettivo di performance e dal budget.
