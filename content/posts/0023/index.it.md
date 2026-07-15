---
title: "RAM a prezzi record: misurare la memoria Linux prima di comprarne altra"
description: "Perché nel 2026 la DRAM costa oltre quattro volte rispetto al 2025 e come misurare pressione, cache e processi Linux prima di espandere la RAM."
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
- question: "Nel 2026 la RAM costa davvero quattro volte di più?"
  answer: "Per la DRAM convenzionale a contratto, componendo il +45-50% del quarto trimestre 2025, il +93-98% rilevato nel primo trimestre 2026 e il +58-63% previsto per il secondo trimestre, il livello risultante è circa 4,4-4,8 volte quello del terzo trimestre 2025. I prezzi retail dei singoli moduli possono seguire traiettorie diverse."
- question: "Linux usa troppa RAM quando la colonna free è bassa?"
  answer: "Non necessariamente. Linux usa la memoria libera per page cache recuperabile. In free -h, available è normalmente un indicatore più utile di free; la pressione PSI e lo swap-in mostrano se la memoria sta davvero causando rallentamenti."
- question: "Qual è il primo comando per diagnosticare la RAM su Linux?"
  answer: "Inizia con free -h, cat /proc/pressure/memory, vmstat 1 e ps ordinato per RSS. Registrali durante il carico reale, non soltanto su un sistema inattivo."
---

La prima volta che quest'anno ho guardato il prezzo di un upgrade di memoria, ho dato per scontato che il listino fosse sbagliato. Non lo era. I prezzi contrattuali della DRAM sono oggi oltre quattro volte quelli del terzo trimestre 2025, e improvvisamente una domanda che non richiedeva nemmeno di pensarci — "aggiungo RAM e via?" — merita di nuovo tempo da ingegnere.

Questa serie nasce da lì. Per anni buttare memoria sul problema è stata la mossa razionale: la RAM costava poco, le ore di lavoro no. Nel 2026 quel conto si è ribaltato, e prima di spendere a questi prezzi conviene capire se il limite è vera pressione di memoria, cache recuperabile che *sembra* solo consumo, o un singolo processo che nessuno guarda da mesi. Questa prima parte costruisce la risposta — una baseline attendibile. La [parte 2 configura swap, zram e zswap](/it/zram-zswap-swap-linux-configurazione/), la [parte 3 contiene i servizi con i cgroup](/it/limitare-ram-servizi-linux-systemd-cgroup-v2/) e la [parte 4 mette tutto insieme in un piano e in una decisione compro/ottimizzo](/it/ridurre-consumo-ram-linux-piano-benchmark/).

## Oltre quattro volte — ma quale prezzo?

"La RAM costa quattro volte tanto" è il tipo di affermazione che merita una fonte, perché può mescolare cose molto diverse: prezzi spot dei chip, contratti con gli OEM, DIMM retail, DDR4 contro DDR5 contro HBM. Per tenere il confronto onesto, questa serie usa una metrica sola e coerente — i prezzi contrattuali della DRAM convenzionale rilevati da TrendForce:

| Periodo | Variazione sul trimestre precedente | Stato del dato |
|---|---:|---|
| Q4 2025 | +45–50% | rilevato |
| Q1 2026 | +93–98% | rilevato |
| Q2 2026 | +58–63% | previsione pubblicata il 1° giugno 2026 |

Le variazioni trimestrali si moltiplicano, non si sommano. Il limite inferiore fa `1,45 × 1,93 × 1,58 = 4,42`, quello superiore `1,50 × 1,98 × 1,63 = 4,84`. Il prezzo contrattuale implicito a fine Q2 è quindi **4,4–4,8 volte il livello del Q3 2025**.

Questo non significa che ogni kit in ogni negozio sia salito esattamente di 4,4 volte. Inventario, IVA, cambio, marca e promozioni piegano il passaggio al retail in entrambe le direzioni. Ma documenta che il costo industriale sottostante ha cambiato ordine di grandezza, ed è quello che conta per la decisione di cui parla questa serie.

E la causa non è una fabbrica in panne. TrendForce collega il rialzo alla domanda dei cloud provider e dei data center AI, alle scorte eccezionalmente basse dei fornitori e alla priorità produttiva assegnata a RDIMM ad alta capacità, DRAM server e HBM — il che lascia PC e tutto ciò che è legacy a contendersi una fetta più stretta dell'offerta.

## Prima regola: la memoria `free` non è memoria sprecata

Il punto di partenza naturale:

```bash
free -h
```

E l'errore naturale: cercare di far crescere la colonna `free`. Linux usa deliberatamente la RAM altrimenti inattiva come page cache — quella memoria sta facendo lavoro utile e viene recuperata nel momento in cui serve ad altro. I numeri che meritano attenzione sono:

- `available` — una stima di quanta memoria si può usare prima che il sistema inizi a swappare;
- `buff/cache` — in gran parte recuperabile, ma non "sprecata" finché è lì;
- `Swap used` — significativo solo insieme all'attività corrente, perché pagine fredde possono stare in swap per sempre senza dare alcun fastidio.

Già che ci siamo: non schedulare `echo 3 > /proc/sys/vm/drop_caches` come "ottimizzazione". Butta via cache utile, corrompe le misure e di solito rende più lento il prossimo accesso ai file. È uno strumento da test, niente di più.

## Misura la pressione, non i gigabyte

Ecco la parte controintuitiva che rende sbagliate la maggior parte delle diagnosi veloci: una macchina al 90% di memoria occupata può essere perfettamente sana, e una con memoria apparentemente abbondante può stare in stallo sul reclaim. L'occupazione dice dove è finita la memoria; non dice se qualcuno la sta *aspettando*. A questo serve la Pressure Stall Information (PSI):

```bash
cat /proc/pressure/memory
```

```text
some avg10=0.21 avg60=0.08 avg300=0.03 total=1847331
full avg10=0.04 avg60=0.01 avg300=0.00 total=122840
```

`some` è la quota di tempo in cui almeno un task era fermo in attesa di memoria; `full` quella in cui *tutti* i task non idle erano fermi — i dintorni del thrashing. Non esiste una soglia sicura universale, e diffida di chi te ne vende una: costruisci la tua baseline e correla gli aumenti con latenza e throughput dell'applicazione.

Accanto al PSI, tieni d'occhio il paging vero e proprio:

```bash
vmstat 1
```

Le colonne che contano sono `si` e `so` (swap-in e swap-out), `r` (task eseguibili), `wa` (attesa I/O) e la memoria libera. Swap allocata ma con `si`/`so` quasi a zero è una situazione completamente diversa dal paging continuo a ogni picco — la prima va benissimo, la seconda è il problema che stai cercando.

## Scopri chi si sta mangiando davvero la memoria

Parti da una classifica semplice:

```bash
ps -eo pid,user,comm,rss,vsz,%mem --sort=-rss | head -n 20
```

Un'avvertenza prima di fidarti di quei numeri: l'RSS conta le pagine condivise una volta per processo, quindi sommare gli RSS sovrastima. Se `smem` è disponibile, riporta il PSS, che ripartisce le pagine condivise in modo equo:

```bash
smem -tk
```

Per un servizio systemd, chiedi direttamente a systemd:

```bash
systemctl show nome.service -p MemoryCurrent -p MemoryPeak -p MemorySwapCurrent
```

E per capire la composizione globale:

```bash
grep -E 'MemAvailable|AnonPages|Cached|SReclaimable|Slab|Swap' /proc/meminfo
```

I pattern da riconoscere: `AnonPages` che cresce punta di solito agli heap applicativi; `Slab` o `SReclaimable` che crescono puntano alle cache del kernel; una page cache grande, da sola, non giustifica proprio niente.

## La baseline minima: 24 ore

Raccogli almeno queste misure lungo una giornata rappresentativa:

| Misura | Comando | Domanda a cui risponde |
|---|---|---|
| Memoria disponibile | `free -h` | Quanto margine resta? |
| Pressione reale | `cat /proc/pressure/memory` | I task si fermano per reclaim? |
| Paging attivo | `vmstat 1` | Il sistema sta swappando adesso? |
| Processi maggiori | `ps ... --sort=-rss` | Chi domina l'RSS? |
| Eventi OOM | `journalctl -k -g 'oom\|Out of memory'` | Il kernel ha già ucciso qualcosa? |
| Picco dei servizi | `systemctl show ...` | Il responsabile è un servizio specifico? |

E scrivi il carico accanto ai numeri — richieste al secondo, job paralleli, utenti attivi, dimensione del dataset. Un valore di RAM senza il carico che lo ha prodotto non è una baseline; è uno screenshot.

## Cosa ti dice la baseline

Alla fine delle 24 ore, i numeri puntano in una di poche direzioni, e ognuna corrisponde a un passo successivo diverso:

- **PSI basso, niente swap-in, available stabile:** non comprare RAM solo perché `used` sembra alto. Qui non c'è nessun problema.
- **Un processo cresce e non torna mai indietro:** caccia a leak e cache senza limite, prima di toccare l'hardware.
- **Picchi brevi di pagine fredde comprimibili:** zram o zswap possono assorbirli — è la [parte 2](/it/zram-zswap-swap-linux-configurazione/).
- **Un servizio affama tutti gli altri:** è un problema di contenimento per i limiti cgroup — parte 3.
- **PSI e swap-in restano alti dopo il tuning, a carico utile stabile:** ora, e solo ora, l'espansione fisica è sostenuta dai dati.

Ai prezzi del 2026, quell'ultimo punto è quello a cui vuoi arrivare onestamente — non saltando i passaggi in mezzo.

## Fonti

- [TrendForce: prezzi contrattuali DRAM Q4 2025 e previsione Q1 2026](https://www.trendforce.com/presscenter/news/20260226-12937.html)
- [TrendForce: risultati Q1 2026 e previsione Q2 2026](https://www.trendforce.com/presscenter/news/20260601-13070.html)
- [Documentazione Linux kernel: Pressure Stall Information](https://docs.kernel.org/accounting/psi.html)
- [Documentazione Linux kernel: `/proc` e `/proc/meminfo`](https://docs.kernel.org/filesystems/proc.html)
