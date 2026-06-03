---
title: Confronto performance multicore delle shape OCI Compute Standard Flex
description: "Benchmark multicore Geekbench 6 per shape OCI: AMD EPYC E5, Intel Xeon e ARM Ampere, con analisi performance e costi."
date: 2024-03-19T18:00:00+01:00
draft: false
cover:
  alt: Confronto performance multicore delle shape OCI Compute Standard Flex
  caption: Confronto performance multicore delle shape OCI Compute Standard Flex
  relative: true
  image: "static/logo.webp"
keywords:
- "geekbench oci shapes"
- "oci multicore benchmark"
- "arm vs x86 oracle cloud"
- "oci compute cost performance"
tags:
- "OCI"
- "Compute"
- "Ampere"
- "Geekbench"
- "Benchmark"
categories:
- "Benchmark"
---

Quando si sceglie un'istanza compute, fattori come potenza di calcolo pura, rapporto prezzo-prestazioni e ottimizzazione per il workload hanno un ruolo importante.

Le seguenti shape standard flex sono disponibili nella maggior parte delle region OCI:

* **VM.Standard.E4.Flex** (Processore: AMD EPYC 7J13. Frequenza base 2,55 GHz, boost massimo 3,5 GHz)
* **VM.Standard.E5.Flex** (Processore: AMD EPYC 9J14. Frequenza base 2,4 GHz, boost massimo 3,7 GHz)
* **VM.Standard3.Flex** (Processore: Intel Xeon Platinum 8358. Frequenza base 2,6 GHz, turbo massimo 3,4 GHz)
* **VM.Optimized3.Flex** (Processore: Intel Xeon 6354. Frequenza base 3,0 GHz, turbo massimo 3,6 GHz)
* **VM.Standard.A1.Flex** (ogni OCPU corrisponde a un singolo thread hardware. Processore: Ampere Altra Q80-30. Frequenza massima 3,0 GHz)

Nell'articolo [Test di performance PHP con istanze OCI Compute]({{< relref "/posts/0008/index.md" >}}) ho testato l'esecuzione single-thread PHP su tutte le shape OCI standard flex. Ora ho eseguito benchmark multicore con **Geekbench 6** usando 2, 4 e 8 CPU.

Per ulteriori informazioni sui [test interni eseguiti](https://www.geekbench.com/doc/geekbench6-benchmark-internals.pdf), consulta il link.

### **Confronto Performance**

Esploriamo i risultati del test multi-thread sulle diverse shape:

{{< plotly "//plotly.com/~enricopesce/1.embed" >}}

Possiamo vedere che la shape piu' potente e' **VM.Standard.E5.Flex**.

Questa nuova shape basata su AMD supera in modo significativo le altre shape: una CPU molto potente per esigenze di performance elevate.

Ma non dobbiamo valutare solo le prestazioni. Nel mondo reale il rapporto prezzo-prestazioni e' un altro fattore decisivo.

### **Confronto Costi Mensili**

Analizziamo i costi mensili per ogni shape con 8 CPU e Oracle Linux, basati sui prezzi Oracle a marzo 2024:

Possiamo osservare che i prezzi variano: non tutte le shape hanno lo stesso costo.

| **Shape**           | **Score multicore** | **Prezzo mensile** | **Risparmio** |
|---------------------|---------------------|--------------------|---------------|
| VM.Standard.A1.Flex | 6275                |  $59,52            | 0%            |
| VM.Standard.E4.Flex | 6266                |  $74,40            | 20%           |
| VM.Standard.E5.Flex | 8335                |  $89,28            | 33%           |
| VM.Standard3.Flex   | 5925                |  $119,04           | 50%           |
| VM.Optimized3.Flex  | 6365                |  $149,45           | 60%           |

In questa tabella ho aggiunto una colonna "Risparmio" per rappresentare la differenza di costo, in percentuale, rispetto a **VM.Standard.A1.Flex**.

### **Considerazioni**

Se consideri la shape ARM **VM.Standard.A1.Flex**, puoi risparmiare il 60% rispetto a **VM.Optimized3.Flex** mantenendo risultati di performance molto simili.

Se il focus principale sono le prestazioni, **VM.Standard.E5.Flex** e' la vincitrice: buon prezzo e risultati molto forti.

L'architettura ARM non e' solo per mobile o dispositivi a basso consumo. I processori ARM sono una reale alternativa alle CPU server x86 classiche. Leggi la pagina [What is Arm?](https://www.oracle.com/hk/cloud/compute/arm/what-is-arm/) sul sito OCI per capire meglio i benefici delle shape OCI A1.

Ricorda: la shape giusta dipende dal tuo caso d'uso specifico.

### **Risultati Dettagliati**

Se vuoi approfondire i test **Geekbench 6** e i risultati eseguiti da me, ecco una tabella con i relativi test:

| **SHAPE**           | **Tipo CPU**                                  | **Geekbench browser**                        |
|---------------------|----------------------------------------------|----------------------------------------------|
| VM.Optimized3.Flex  | Intel(R) Xeon(R) Gold 6354 CPU @ 3.00GHz     | https://browser.geekbench.com/v6/cpu/4837669 |
| VM.Standard.A1.Flex | Neoverse-N1 BIOS virt-4.2                    | https://browser.geekbench.com/v6/cpu/4837683 |
| VM.Standard.E4.Flex | AMD EPYC 7J13 64-Core Processor              | https://browser.geekbench.com/v6/cpu/4837682 |
| VM.Standard.E5.Flex | AMD EPYC 9J14 96-Core Processor              | https://browser.geekbench.com/v6/cpu/4837947 |
| VM.Standard3.Flex   | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | https://browser.geekbench.com/v6/cpu/4837679 |

Buon computing.
