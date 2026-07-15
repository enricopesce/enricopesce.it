---
title: "Zram, zswap e swap su Linux: configurazione pratica senza comprare RAM"
description: "Come scegliere e configurare zram, zswap e swap su Linux, impostare swappiness e misurare compressione, latenza e paging."
date: 2026-07-17T09:00:00+00:00
lastmod: 2026-07-08T00:00:00+00:00
slug: "zram-zswap-swap-linux-configurazione"
draft: false
cover:
  alt: "Configurazione zram zswap e swap su Linux"
  caption: "Serie RAM Linux, parte 2: comprimere le pagine fredde"
  relative: true
  image: "static/linux-ram-part-2.svg"
  width: 1200
  height: 630
keywords:
- "configurare zram Linux"
- "zram vs zswap"
- "swappiness zram"
- "ottimizzare swap Linux"
- "zswap Linux configurazione"
- "aumentare RAM Linux compressione"
tags: ["Linux", "RAM", "zram", "zswap", "Swap"]
categories: ["Linux"]
inLanguage: "it-IT"
isBasedOn:
- "https://docs.kernel.org/admin-guide/blockdev/zram.html"
- "https://docs.kernel.org/admin-guide/mm/zswap.html"
- "https://docs.kernel.org/admin-guide/sysctl/vm.html"
faq:
- question: "È meglio zram o zswap su Linux?"
  answer: "Zram è uno swap device compresso interamente in RAM; zswap è una cache compressa davanti a uno swap device reale e può espellere pagine sul disco. Zram è semplice per desktop e host piccoli, zswap è adatto quando serve anche una capacità di fallback su disco."
- question: "Quale valore di swappiness usare con zram?"
  answer: "La documentazione del kernel ammette valori superiori a 100 per swap in memoria più veloce del filesystem. Un punto di partenza prudente è 100-133, da validare con PSI, vmstat e latenza del workload."
- question: "Zram sostituisce RAM fisica?"
  answer: "No. Scambia cicli CPU per comprimere pagine fredde e assorbire picchi; dati incomprimibili e working set attivi continuano a richiedere RAM fisica."
---

Nella [parte 1 di questa serie]({{< relref "/posts/0023/index.it.md" >}}) ho spiegato perché conviene misurare la pressione di memoria prima di spendere soldi in RAM che oggi costa oltre quattro volte quella di un anno fa. Se le misure hanno mostrato picchi brevi e comprimibili — pagine fredde che occupano spazio mentre il working set attivo ci sta comodamente — questo è il post in cui la compressione si guadagna il suo posto.

Voglio essere onesto su una cosa, perché "abilita zram" è diventato il consiglio riflesso in ogni thread sui sistemi con poca memoria: zram e zswap non creano memoria gratis. Spendono cicli CPU per comprimere pagine che non stai usando attivamente. Quando i dati si comprimono bene e la CPU ha margine, lo scambio è ottimo. Quando non è così, hai aggiunto un livello di complessità senza guadagnare niente. L'obiettivo quindi non è abilitare tutto: è scegliere un meccanismo consapevolmente e dimostrare che aiuta.

## Zram, zswap e swap su disco: cosa cambia davvero

I nomi si somigliano in modo fastidioso, quindi partiamo dalla distinzione che conta. Zram è uno swap device che vive interamente in RAM: le pagine vengono compresse e restano in memoria, nessun disco coinvolto, nessun fallback. Zswap è una cache compressa *davanti* a uno swap reale: quando il pool si riempie, può espellere le pagine sul disco.

| Meccanismo | Dove finiscono le pagine | Vantaggio | Limite |
|---|---|---|---|
| Swap su disco | SSD/NVMe | capacità e protezione dai picchi | latenza e scritture |
| zram | blocco compresso in RAM | molto veloce, nessun I/O disco | usa RAM e CPU, nessun fallback implicito |
| zswap | cache compressa davanti allo swap | riduce I/O e può espellere sul disco | richiede swap di backing, più livelli da osservare |

In pratica: zram va bene per desktop e host piccoli dove non c'è uno storage veloce da dedicare allo swap. Zswap va bene per macchine che hanno già swap su storage decente e vogliono meno scritture su disco e latenza più bassa sulla parte calda.

## Prima di tutto: guarda cosa hai già

Questo è il passaggio che tutti saltano, ed è quello che causa i problemi più strani. Molte distribuzioni arrivano con uno di questi meccanismi già attivo — e se ne aggiungi un secondo senza accorgertene, ti ritrovi con due swap compressi che si contendono le stesse pagine.

```bash
swapon --show --output=NAME,TYPE,SIZE,USED,PRIO
zramctl
cat /sys/module/zswap/parameters/enabled 2>/dev/null || true
cat /proc/sys/vm/swappiness
```

Se c'è già qualcosa di configurato, lavora con quello. Meglio regolare l'esistente che piazzargli un concorrente accanto.

## Profilo A: zram per un host piccolo

Ecco una prova non persistente che puoi eseguire in una finestra di manutenzione e annullare completamente:

```bash
sudo modprobe zram
sudo zramctl /dev/zram0 --algorithm zstd --size 8G
sudo mkswap /dev/zram0
sudo swapon --priority 100 /dev/zram0
```

Sostituisci `8G` con un valore tra il 50% e il 100% della RAM fisica come punto di partenza — e trattalo esattamente per quello che è, un'ipotesi. La dimensione virtuale non è RAM preallocata; il dispositivo consuma memoria man mano che riceve pagine. La documentazione del kernel osserva che andare oltre 2× la RAM ha poco senso assumendo una compressione tipica 2:1.

Sull'algoritmo: `lz4` privilegia velocità e bassa latenza, `zstd` di solito privilegia il rapporto di compressione. Chi vince dipende dai tuoi dati, non dal benchmark di qualcun altro. Puoi vedere cosa supporta il tuo kernel con:

```bash
cat /sys/block/zram0/comp_algorithm
```

Per rimuovere il test, assicurati prima che ci sia abbastanza memoria libera per riportare tutte le pagine in RAM, poi:

```bash
sudo swapoff /dev/zram0
sudo zramctl --reset /dev/zram0
```

Una volta validati dimensione, algoritmo e priorità, rendili persistenti usando il generatore o il servizio zram che la tua distribuzione fornisce — e resisti alla tentazione di creare un secondo servizio se ne esiste già uno.

## Profilo B: zswap con fallback su disco

Zswap comprime le pagine dirette allo swap in un pool dinamico e, quando il pool si riempie, può scriverle sul dispositivo di backing. Questo significa che ha bisogno di uno swap reale dietro — verificalo per primo:

```bash
swapon --show
```

Per una prova a runtime:

```bash
echo 1 | sudo tee /sys/module/zswap/parameters/enabled
cat /sys/module/zswap/parameters/compressor
cat /sys/module/zswap/parameters/max_pool_percent
```

Per renderlo attivo dal boot, aggiungi questo alla riga di comando del kernel con il meccanismo previsto dalla tua distribuzione:

```text
zswap.enabled=1 zswap.compressor=zstd zswap.max_pool_percent=20
```

Il 20% è un punto di partenza conservativo, e più grande non è automaticamente meglio. Un pool grosso può tenere in ostaggio in RAM pagine fredde che starebbero meglio espulse su NVMe, lasciando quella memoria al lavoro che ne ha davvero bisogno.

## Swappiness: smetti di copiare il numero più basso che trovi

Attorno a `vm.swappiness` c'è un intero folklore, costruito quasi tutto sull'idea che lo swap sia il male e quindi il numero debba essere basso. Quello che il parametro esprime davvero è il costo relativo tra swap e paging del filesystem, su una scala 0–200. Impostarlo a zero non disabilita lo swap: lo rimanda a quando la pressione è già severa, che di solito è il momento peggiore possibile.

La parte interessante per questo post: la documentazione del kernel dice esplicitamente che valori *sopra* 100 possono avere senso quando lo swap è più veloce dell'I/O del filesystem — che è esattamente il caso dello swap compresso in memoria. Quindi per una prova con zram parti da:

```bash
sudo sysctl vm.swappiness=100
```

Se il PSI resta basso e la CPU ha margine, confronta 100 con 133 e guarda cosa preferisce il tuo workload. Per lo swap solo su disco, i classici 10, 30 o 60 sono ipotesi da benchmark, non ricette universali.

Quando hai un vincitore, rendilo persistente:

```bash
echo 'vm.swappiness=100' | sudo tee /etc/sysctl.d/80-memory-tuning.conf
sudo sysctl --system
```

## Dimostra che sta aiutando davvero

Questa è la parte che separa un sistema ottimizzato da un sistema con più parti in movimento. Per zram:

```bash
zramctl
cat /sys/block/zram0/mm_stat
```

Confronta dati originali, dati compressi e memoria totale realmente usata. Un dispositivo virtuale da 8 GiB che contiene 4 GiB di pagine non equivale a 8 GiB risparmiati — il risparmio reale è la differenza tra quanto occuperebbero le pagine non compresse e quanto usa il dispositivo adesso.

Per zswap:

```bash
sudo grep -H . /sys/kernel/debug/zswap/{stored_pages,pool_total_size,written_back_pages} 2>/dev/null
```

(Debugfs potrebbe non essere montato sul tuo sistema.) In entrambi i casi, continua a registrare gli stessi segnali della parte 1:

```bash
vmstat 1
cat /proc/pressure/memory
```

Il tuning è riuscito se gli stall PSI e l'I/O di swap calano senza saturare la CPU o peggiorare la latenza applicativa. Se il rapporto di compressione è scarso, la CPU sale o il PSI `full` resta alto, la conclusione onesta è che il working set attivo ha bisogno di vera RAM o di limiti applicativi — non di altra compressione.

## Gli errori che tornano sempre

Alcune cose che segnalerei in qualsiasi review di una modifica al tuning della memoria:

- Attivare zram *e* zswap insieme senza un design specifico e un benchmark che lo giustifichi.
- Dimensionare zram guardando la capacità virtuale, come se fosse risparmio garantito.
- Impostare `swappiness=0` per "proteggere" le prestazioni.
- Eseguire `swapoff` su un host già sotto pressione — può scatenare direttamente l'OOM killer.
- Usare lo swap come soluzione a un memory leak.
- Cambiare impostazioni in produzione senza aver scritto prima il rollback.

La compressione ti protegge dai picchi, ma non può impedire a un servizio che si comporta male di mangiarsi tutto l'host. Quello è un problema di contenimento, ed è quello che la [parte 3](/it/limitare-ram-servizi-linux-systemd-cgroup-v2/) risolve con systemd e cgroup v2.

## Fonti

- [Linux kernel: zram](https://docs.kernel.org/admin-guide/blockdev/zram.html)
- [Linux kernel: zswap](https://docs.kernel.org/admin-guide/mm/zswap.html)
- [Linux kernel: `vm.swappiness`](https://docs.kernel.org/admin-guide/sysctl/vm.html#swappiness)
