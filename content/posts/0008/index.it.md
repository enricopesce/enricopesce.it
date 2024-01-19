---
title: Alcuni test di performance con PHP e OCI Compute instance
date: 2024-01-19T19:00:00+01:00
draft: false
tags:
  - php
  - performance
categories:
  - compute
cover:
  alt: Alcuni test di performance con PHP e OCI Compute instance
  caption: Alcuni test di performance con PHP e OCI Compute instance
  relative: true
  image: "static/Oracle-PHP.png"
---

Diverso tempo fa ho sviluppato un [tool](https://github.com/enricopesce/php-performance) con l'obiettivo di verificare il vero miglioramento di performance tra le versioni di PHP e successivamente capire quale AWS instance type era la piu' performante, visto che su AWS non e' possibile scegliere un dimensionamento personalizzato delle risorse CPU e RAM ho voluto comprendere tra le diverse decine di instance type cosa cambiasse e quale mi sarebbe piu' convenuta scegliere.

In queste vacanze natalizie mi sono dedicato ad estendere questo progetto e di fare la stessa cosa con [OCI](https://www.oracle.com/it/cloud/), Oracle Cloud Infrastructure.

La grande differenza rispetto ad AWS e' che su OCI e' possibile scegliere la shape cioe' la tecnologia di base e poi poter selezionare quanta CPU e RAM utilizzare in modo flessibile, quindi i test saranno eseguiti su le differenti singole shape e non su un sterminato numero di instance types.

Per appprofondire, le shape disponibili sono le seguenti:

#### Shape basate su tecnologia AMD

* **VM.Standard.E4.Flex** (Processor: AMD EPYC 7J13. Base frequency 2.55 GHz, max boost frequency 3.5 GHz)
* **VM.Standard.E5.Flex** (Processor: AMD EPYC 9J14. Base frequency 2.4 GHz, max boost frequency 3.7 GHz)

#### Shape basate su tecnologia INTEL

* **VM.Standard3.Flex** (Processor: Intel Xeon Platinum 8358. Base frequency 2.6 GHz, max turbo frequency 3.4 GHz)
* **VM.Optimized3.Flex** (Processor: Intel Xeon 6354. Base frequency 3.0 GHz, max turbo frequency 3.6 GHz)

#### Shape basate su tecnologia ARM64 AMPERE

* **VM.Standard.A1.Flex** (Each OCPU corresponds to a single hardware execution thread. Processor: Ampere Altra Q80-30. Max frequency 3.0 GHz.)

Da specificare che non sono state selezionate shape bare metal in questo test ma solo virtual machine.

Il nostro test andra' ad eseguire attraverso una suite di benchmark open source [Phornoix test suite](https://www.phoronix-test-suite.com/) due test specifici di PHP 

* [PHP Micro Benchmarks](https://openbenchmarking.org/test/pts/php)
* [PHPBench](https://openbenchmarking.org/test/pts/phpbench)

Il test e' di tipo Single-Threaded quindi non andremo a testare quanto potra' scalare un server su piu thread cioe' su multiple CPU, invece andremo esattamente a vedere quanto velocemente verra' eseguito uno script PHP nella sua naturale singola esecuzione single threaded.

In sintesi il test verra' eseguito con una singola OCPU e 16 Giga di RAM valore ininfluente per il tipo di test computazionale, test con un numero maggiore di OCPU non dara' alcu tipo di ottimizzazione nelle prestazioni perche' non verranno ovviamente usate.

Al momento non ho utilizzato le ultime verisioni di PHP utlizzando il famoso repository di [Remi's](https://blog.remirepo.net/) ma ho utilizzato le versioni ufficiali di PHP incluse nella versione di [Oracle Linux](https://yum.oracle.com/oracle-linux-php.html). Nel futuro vorrei testare anche soluzioni esterne piu recenti.

### I risultati di PHP 8.0 sono i seguenti:

![PHP 8.0 performance](static/PHP80.png "PHP 8.0 performance")

Possiamo notare che la nuova shape **VM.Standard.E5.Flex** vince (di poco) anche su Intel affermandosi come la shape piu' veloce per eseguire i propri script PHP, al secondo e terzo posto **VM.Optimized3.Flex** e **VM.Standard3.Flex** cioe' le due shape Intel disponibili.

Alla fine penultimo classificato la precendente tecnologia shape AMD **VM.Standard.E4.Flex**, ultima posizione per la **VM.Standard.A1.Flex**, in questo caso da comprendere meglio se dovuto anche a qualche scarsa ottimizzazione delle vecchie versioni di PHP su tecnologia ARM.

Possiamo proclamare quindi vincitrice assoluta la nuova shape **VM.Standard.E5.Flex** non solo in termini di performance ma anche di costo infatti nel podio i costi di ogni shape sono i seguenti:

1) B97384 Compute - Standard - E5 - OCPU **20,76 € costo mensile** 
2) B93311 Compute - Optimized - X9 - OCPU **37,36 € costo mensile**
3) B94176 Compute - Standard - X9 - OCPU **27,68 € costo mensile**

*I costi sono deirvati dal [cloud cost estimator](https://www.oracle.com/it/cloud/costestimator.html) in data Gennaio 2024*

La tecnologia E5 oltre ad essere la piu' veloce e' anche la piu' economica del podio!

Vorrei pero' evidenziare che l'ultimo in classifica **VM.Standard.A1.Flex** e' anche la piu' economica in assoluto soli **6,70 €** menisle stimato..

Spunti per un prossimo articolo sono quelli di testare le ultime versioni di PHP da repository Remi https://blog.remirepo.net/ e comprendere se con tecnologia ARM possiamo ottenere maggiori performance.