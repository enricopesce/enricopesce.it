---
title: "RAM a prezzi record: misurare la memoria Linux prima di comprarne altra"
description: "Perche' nel 2026 la DRAM costa oltre quattro volte rispetto al 2025 e come misurare pressione, cache e processi Linux prima di espandere la RAM."
date: 2026-07-10T09:00:00+00:00
lastmod: 2026-07-08T00:00:00+00:00
slug: "ram-prezzi-record-misurare-memoria-linux"
draft: false
cover:
  alt: "Prezzi DRAM e analisi della memoria Linux"
  caption: "Serie RAM Linux, parte 1: misurare prima di comprare"
  relative: true
  image: "static/linux-ram-part-1.svg"
  width: 1200
  height: 630
keywords:
- "prezzo RAM 2026"
- "ottimizzare RAM Linux"
- "controllare consumo RAM Linux"
- "Linux memory pressure"
- "free available memory Linux"
- "PSI memoria Linux"
- "DRAM prezzi quattro volte"
tags:
- "Linux"
- "RAM"
- "Performance"
- "Ottimizzazione"
- "Monitoring"
categories:
- "Linux"
inLanguage: "it-IT"
isBasedOn:
- "https://www.trendforce.com/presscenter/news/20260226-12937.html"
- "https://www.trendforce.com/presscenter/news/20260601-13070.html"
- "https://docs.kernel.org/accounting/psi.html"
- "https://docs.kernel.org/filesystems/proc.html"
faq:
- question: "Nel 2026 la RAM costa davvero quattro volte di piu'?"
  answer: "Per la DRAM convenzionale a contratto, componendo il +45-50% del quarto trimestre 2025, il +93-98% rilevato nel primo trimestre 2026 e il +58-63% previsto per il secondo trimestre, il livello risultante e' circa 4,4-4,8 volte quello del terzo trimestre 2025. I prezzi retail dei singoli moduli possono seguire traiettorie diverse."
- question: "Linux usa troppa RAM quando la colonna free e' bassa?"
  answer: "Non necessariamente. Linux usa la memoria libera per page cache recuperabile. In free -h, available e' normalmente un indicatore piu' utile di free; la pressione PSI e lo swap-in mostrano se la memoria sta davvero causando rallentamenti."
- question: "Qual e' il primo comando per diagnosticare la RAM su Linux?"
  answer: "Inizia con free -h, cat /proc/pressure/memory, vmstat 1 e ps ordinato per RSS. Registrali durante il carico reale, non soltanto su un sistema inattivo."
---

## In breve

Nel 2026 **ottimizzare la RAM su Linux e' di nuovo una decisione economica**, non solo tecnica. I dati TrendForce indicano che i prezzi contrattuali della DRAM convenzionale sono arrivati, su base composta, a circa **4,4–4,8 volte il livello del Q3 2025**; prima di comprare memoria a questi prezzi conviene capire se il limite e' vera pressione, cache recuperabile o un singolo processo fuori controllo.

Questa e' la prima di quattro parti. Qui costruiamo una baseline attendibile; nella [parte 2 configureremo swap, zram e zswap]({{< relref "/posts/0024/index.it.md" >}}), nella [parte 3 limiteremo servizi e cgroup]({{< relref "/posts/0025/index.it.md" >}}), nella [parte 4 applicheremo un piano di ottimizzazione]({{< relref "/posts/0026/index.it.md" >}}).

## Il dato: oltre quattro volte, ma quale prezzo?

Dire semplicemente “la RAM costa quattro volte” rischia di confrontare oggetti diversi. Esistono prezzi spot dei chip, contratti tra produttori e OEM, moduli DIMM retail, memorie DDR4, DDR5, RDIMM e HBM. Per avere una serie omogenea uso qui **i prezzi contrattuali della DRAM convenzionale** rilevati da TrendForce:

| Periodo | Variazione sul trimestre precedente | Stato del dato |
|---|---:|---|
| Q4 2025 | +45–50% | rilevato |
| Q1 2026 | +93–98% | rilevato |
| Q2 2026 | +58–63% | previsione pubblicata il 1 giugno 2026 |

Le percentuali trimestrali vanno moltiplicate, non sommate. Il limite inferiore e' `1,45 × 1,93 × 1,58 = 4,42`; quello superiore e' `1,50 × 1,98 × 1,63 = 4,84`. Quindi il prezzo contrattuale indicativo di fine Q2 e' **4,4–4,8× rispetto al livello del Q3 2025**.

Questa non e' la prova che ogni kit nel negozio sotto casa costi esattamente 4,4 volte: inventario, IVA, cambio, marca e promozioni attenuano o amplificano il passaggio al retail. E' pero' una prova documentata che il costo industriale sottostante ha cambiato ordine di grandezza.

La causa non e' una singola fabbrica. TrendForce collega il rialzo alla domanda dei cloud provider e dei data center AI, alle scorte molto basse dei fornitori e alla priorita' produttiva assegnata a RDIMM ad alta capacita', server DRAM e HBM. Cosi' PC, dispositivi e prodotti legacy competono per una disponibilita' piu' stretta.

## Prima regola: `free` non significa sprecata

Questo comando e' un buon punto di partenza:

```bash
free -h
```

Non ottimizzare mirando ad aumentare la colonna `free`. Linux usa intenzionalmente la RAM non occupata dai processi come page cache; quella memoria puo' essere recuperata. Guarda soprattutto:

- `available`: stima di quanta memoria puo' essere usata senza iniziare a scambiare pagine;
- `buff/cache`: cache, in buona parte recuperabile ma non istantaneamente “inutile”;
- `Swap used`: utile solo insieme all'attivita' corrente, perche' pagine fredde possono restare in swap senza creare un problema.

E non usare `echo 3 > /proc/sys/vm/drop_caches` come ottimizzazione periodica: svuota cache utili, altera le misure e spesso rende il sistema piu' lento al successivo accesso ai file.

## Misurare la pressione, non solo i gigabyte

Un sistema con il 90% di RAM occupata puo' essere sano; uno con memoria apparentemente disponibile puo' subire picchi di reclaim. Linux espone **Pressure Stall Information (PSI)**:

```bash
cat /proc/pressure/memory
```

Esempio:

```text
some avg10=0.21 avg60=0.08 avg300=0.03 total=1847331
full avg10=0.04 avg60=0.01 avg300=0.00 total=122840
```

`some` indica il tempo in cui almeno alcuni task sono bloccati per scarsita' di memoria; `full` il tempo in cui tutti i task non idle sono fermi, condizione vicina al thrashing. Non esiste una soglia universale: crea una baseline e correla gli aumenti con latenza e throughput dell'applicazione.

In parallelo usa:

```bash
vmstat 1
```

Le colonne piu' interessanti sono `si` e `so` (swap-in e swap-out), `r` (task eseguibili), `wa` (attesa I/O) e la memoria libera. Swap usata ma `si`/`so` quasi sempre a zero e' molto diversa da scambio continuo durante ogni picco.

## Trovare chi occupa davvero la memoria

Per una prima classifica:

```bash
ps -eo pid,user,comm,rss,vsz,%mem --sort=-rss | head -n 20
```

`RSS` rappresenta le pagine residenti associate al processo, ma la somma degli RSS puo' contare piu' volte memoria condivisa. Per processi complessi usa anche `smem` se disponibile, che espone il **PSS** ripartendo le pagine condivise:

```bash
smem -tk
```

Per un servizio systemd:

```bash
systemctl show nome.service -p MemoryCurrent -p MemoryPeak -p MemorySwapCurrent
```

Per capire la composizione globale:

```bash
grep -E 'MemAvailable|AnonPages|Cached|SReclaimable|Slab|Swap' /proc/meminfo
```

Una crescita di `AnonPages` punta spesso a heap applicativi; una crescita di `Slab` o `SReclaimable` porta verso cache kernel; una page cache elevata da sola non giustifica un upgrade.

## La baseline minima di 24 ore

Raccogli almeno queste misure durante un giorno rappresentativo:

| Misura | Comando | Domanda a cui risponde |
|---|---|---|
| Memoria disponibile | `free -h` | Quanto margine resta? |
| Pressione reale | `cat /proc/pressure/memory` | I task si fermano per reclaim? |
| Swap attiva | `vmstat 1` | Il sistema sta scambiando ora? |
| Processi maggiori | `ps ... --sort=-rss` | Chi domina l'RSS? |
| Eventi OOM | `journalctl -k -g 'oom\|Out of memory'` | Il kernel ha gia' ucciso processi? |
| Picco dei servizi | `systemctl show ...` | Il problema e' un servizio specifico? |

Annota anche richieste al secondo, job paralleli, utenti attivi o dimensione del dataset. Un valore RAM senza il carico che lo ha prodotto non e' una baseline.

## Decisione alla fine della parte 1

- **PSI basso, niente swap-in e memoria available stabile:** non comprare RAM solo perche' `used` e' alto.
- **Un processo cresce senza tornare indietro:** cerca leak o cache senza limite prima di cambiare hardware.
- **Picchi brevi e pagine comprimibili:** zram o zswap possono assorbire il picco; e' il tema della parte 2.
- **Un servizio sacrifica tutti gli altri:** applica limiti e protezioni cgroup; parte 3.
- **PSI e swap-in restano alti dopo il tuning, con carico utile stabile:** l'espansione fisica e' giustificata da dati.

## Fonti

- [TrendForce: prezzi contrattuali DRAM Q4 2025 e previsione Q1 2026](https://www.trendforce.com/presscenter/news/20260226-12937.html)
- [TrendForce: risultati Q1 2026 e previsione Q2 2026](https://www.trendforce.com/presscenter/news/20260601-13070.html)
- [Documentazione Linux kernel: Pressure Stall Information](https://docs.kernel.org/accounting/psi.html)
- [Documentazione Linux kernel: `/proc` e `/proc/meminfo`](https://docs.kernel.org/filesystems/proc.html)
