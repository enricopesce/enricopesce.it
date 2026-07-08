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
- question: "E' meglio zram o zswap su Linux?"
  answer: "Zram e' uno swap device compresso interamente in RAM; zswap e' una cache compressa davanti a uno swap device reale e puo' espellere pagine sul disco. Zram e' semplice per desktop e host piccoli, zswap e' adatto quando serve anche una capacita' di fallback su disco."
- question: "Quale valore di swappiness usare con zram?"
  answer: "La documentazione del kernel ammette valori superiori a 100 per swap in memoria piu' veloce del filesystem. Un punto di partenza prudente e' 100-133, da validare con PSI, vmstat e latenza del workload."
- question: "Zram sostituisce RAM fisica?"
  answer: "No. Scambia cicli CPU per comprimere pagine fredde e assorbire picchi; dati incomprimibili e working set attivi continuano a richiedere RAM fisica."
---

## In breve

Con la DRAM oltre quattro volte il livello del Q3 2025 sul mercato contrattuale, **zram e zswap possono rinviare un upgrade**, ma non creano memoria gratis. Comprimono pagine fredde usando CPU: funzionano bene quando i dati sono comprimibili e il collo di bottiglia non e' gia' il processore.

Questa e' la [parte 2 della serie]({{< relref "/posts/0023/index.it.md" >}}). La regola piu' importante e': **scegli consapevolmente zram oppure zswap**, non sommare meccanismi senza misurare.

## Zram, zswap e swap: differenze

| Meccanismo | Dove finiscono le pagine | Vantaggio | Limite |
|---|---|---|---|
| Swap su disco | SSD/NVMe | capacita' e protezione dai picchi | latenza e scritture |
| zram | blocco compresso in RAM | molto veloce, nessun I/O disco | usa RAM e CPU, nessun fallback implicito |
| zswap | cache compressa in RAM davanti allo swap | riduce I/O e puo' espellere sul disco | richiede swap di backing, piu' livelli da osservare |

Prima fotografa lo stato:

```bash
swapon --show --output=NAME,TYPE,SIZE,USED,PRIO
zramctl
cat /sys/module/zswap/parameters/enabled 2>/dev/null || true
cat /proc/sys/vm/swappiness
```

Molte distribuzioni configurano gia' uno dei due sistemi. Modificare una configurazione che non hai identificato porta facilmente a due swap compressi concorrenti.

## Profilo A: zram per un host piccolo

Per una prova non persistente, eseguita in una finestra di manutenzione:

```bash
sudo modprobe zram
sudo zramctl /dev/zram0 --algorithm zstd --size 8G
sudo mkswap /dev/zram0
sudo swapon --priority 100 /dev/zram0
```

Sostituisci `8G` con **50–100% della RAM fisica** come punto di partenza, non come dogma. La dimensione virtuale non e' RAM preallocata, ma il dispositivo consuma memoria mano a mano che riceve pagine. La documentazione kernel osserva che oltre 2× la RAM ha poco senso assumendo compressione 2:1.

Se `zstd` non e' disponibile, verifica gli algoritmi:

```bash
cat /sys/block/zram0/comp_algorithm
```

`lz4` privilegia velocita' e bassa latenza; `zstd` tende a privilegiare il rapporto di compressione. La scelta va misurata sul tuo carico.

Per rimuovere il test devi prima avere abbastanza memoria libera per riportare le pagine in RAM:

```bash
sudo swapoff /dev/zram0
sudo zramctl --reset /dev/zram0
```

La persistenza e' specifica della distribuzione: usa il generatore o il servizio zram fornito dal sistema, trasferendo dimensione, algoritmo e priorita' gia' validati. Non creare un secondo servizio se ne esiste uno.

## Profilo B: zswap con fallback su disco

Zswap intercetta le pagine dirette allo swap, le comprime in un pool dinamico e, quando il pool si riempie, puo' espellerle sul dispositivo di backing. Verifica prima che esista uno swap reale:

```bash
swapon --show
```

Test runtime:

```bash
echo 1 | sudo tee /sys/module/zswap/parameters/enabled
cat /sys/module/zswap/parameters/compressor
cat /sys/module/zswap/parameters/max_pool_percent
```

Per renderlo attivo dal boot, aggiungi alla riga di comando del kernel, con il meccanismo previsto dalla tua distribuzione:

```text
zswap.enabled=1 zswap.compressor=zstd zswap.max_pool_percent=20
```

Il 20% e' un punto di partenza conservativo. Un pool piu' grande non e' automaticamente migliore: puo' trattenere pagine fredde che sarebbe preferibile espellere su NVMe per liberare RAM al working set.

## Swappiness: non copiare il numero piu' basso

`vm.swappiness` esprime il costo relativo tra swap e paging del filesystem su una scala 0–200. `0` non disabilita completamente lo swap e puo' ritardarlo fino a una pressione severa. Con swap compressa in memoria, la documentazione kernel suggerisce che **valori oltre 100 possono avere senso**.

Per zram prova inizialmente:

```bash
sudo sysctl vm.swappiness=100
```

Se PSI resta basso e la CPU ha margine, confronta 100 e 133. Per swap solo su disco, 10, 30 o 60 vanno trattati come ipotesi di benchmark, non ricette universali.

Dopo la prova, rendi persistente il valore:

```bash
echo 'vm.swappiness=100' | sudo tee /etc/sysctl.d/80-memory-tuning.conf
sudo sysctl --system
```

## Misurare se la compressione conviene

Per zram:

```bash
zramctl
cat /sys/block/zram0/mm_stat
```

Confronta dati originali, dati compressi e memoria totale realmente usata. Un dispositivo virtuale da 8 GiB che contiene 4 GiB di pagine non equivale a 8 GiB di RAM risparmiata.

Per zswap:

```bash
sudo grep -H . /sys/kernel/debug/zswap/{stored_pages,pool_total_size,written_back_pages} 2>/dev/null
```

Debugfs puo' non essere montato. In entrambi i casi registra anche:

```bash
vmstat 1
cat /proc/pressure/memory
```

Il tuning e' riuscito se diminuiscono gli stall PSI e l'I/O di swap senza saturare la CPU o peggiorare la latenza applicativa. Se il rapporto di compressione e' scarso, la CPU cresce o `full` PSI resta elevato, il working set ha bisogno di vera RAM oppure di limiti applicativi.

## Errori da evitare

- Attivare zram e zswap insieme senza un obiettivo e un benchmark.
- Dimensionare zram guardando solo la capacita' virtuale.
- Impostare `swappiness=0` per “proteggere” le prestazioni.
- Eseguire `swapoff` su un host sotto pressione: puo' provocare OOM.
- Usare swap come soluzione a un memory leak.
- Cambiare algoritmo e parametri direttamente in produzione senza rollback.

Nella [parte 3]({{< relref "/posts/0025/index.it.md" >}}) impediremo a un servizio di consumare tutta la memoria tramite systemd e cgroup v2.

## Fonti

- [Linux kernel: zram](https://docs.kernel.org/admin-guide/blockdev/zram.html)
- [Linux kernel: zswap](https://docs.kernel.org/admin-guide/mm/zswap.html)
- [Linux kernel: `vm.swappiness`](https://docs.kernel.org/admin-guide/sysctl/vm.html#swappiness)
