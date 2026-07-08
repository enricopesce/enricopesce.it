---
title: "Ridurre il consumo di RAM su Linux: piano pratico e benchmark finale"
description: "Un piano Linux in sette passi per ridurre RAM: servizi, worker, cache, tmpfs, cgroup, zram e criteri misurabili per decidere se acquistare memoria."
date: 2026-07-31T09:00:00+00:00
lastmod: 2026-07-08T00:00:00+00:00
slug: "ridurre-consumo-ram-linux-piano-benchmark"
draft: false
cover:
  alt: "Piano per ridurre il consumo RAM su Linux"
  caption: "Serie RAM Linux, parte 4: ottimizzare, verificare, decidere"
  relative: true
  image: "static/linux-ram-part-4.svg"
  width: 1200
  height: 630
keywords: ["ridurre consumo RAM Linux", "liberare RAM Linux", "ottimizzazione memoria Linux", "Linux RAM benchmark", "ridurre processi Linux", "Linux memory tuning"]
tags: ["Linux", "RAM", "Performance", "Benchmark", "Ottimizzazione"]
categories: ["Linux"]
inLanguage: "it-IT"
isBasedOn:
- "https://docs.kernel.org/accounting/psi.html"
- "https://docs.kernel.org/admin-guide/sysctl/vm.html"
- "https://docs.kernel.org/admin-guide/cgroup-v2.html"
faq:
- question: "Come posso ridurre davvero il consumo RAM su Linux?"
  answer: "Misura sotto carico, disabilita soltanto i servizi non necessari, limita concorrenza e cache applicative, assegna tetti a tmpfs e cgroup, poi valuta zram o zswap. Confronta PSI, latenza, swap-in e picchi prima e dopo."
- question: "Conviene modificare overcommit_memory per risparmiare RAM?"
  answer: "Non come ottimizzazione generica. Overcommit regola l'ammissione delle allocazioni virtuali, non riduce il working set. La modalita' 2 puo' far fallire allocazioni legittime e richiede capacity planning specifico."
- question: "Quando e' davvero necessario comprare altra RAM?"
  answer: "Quando, a carico utile invariato e dopo aver corretto leak, cache, concorrenza e isolamento, PSI full, swap-in, latenza e OOM restano oltre gli obiettivi. In quel caso il working set fisico non entra nella memoria disponibile."
---

## In breve

Il modo piu' efficace per **ridurre il consumo RAM su Linux** non e' una lista di sysctl: e' un ciclo controllato di misura, modifica e verifica. Riduci prima il working set applicativo, poi isola i servizi, quindi usa compressione e swap; compra RAM soltanto se la pressione resta incompatibile con gli obiettivi.

Questa e' la parte finale della serie iniziata con [prezzi e diagnosi]({{< relref "/posts/0023/index.it.md" >}}), proseguita con [zram e zswap]({{< relref "/posts/0024/index.it.md" >}}) e [limiti systemd/cgroup]({{< relref "/posts/0025/index.it.md" >}}).

## 1. Definire il carico e il budget

Scegli una finestra ripetibile: stesso dataset, stessa concorrenza, stessa durata. Registra almeno:

```bash
date -Is
free -h
cat /proc/pressure/memory
vmstat 1 60
ps -eo pid,user,comm,rss,%mem --sort=-rss | head -n 25
```

Affianca metriche applicative: p95/p99 di latenza, throughput, errori e durata dei job. L'obiettivo non e' “usare meno RAM” se il risultato e' dimezzare il lavoro utile.

## 2. Eliminare soltanto cio' che e' inutile

Elenca servizi attivi e processi maggiori:

```bash
systemctl --type=service --state=running
systemd-cgtop --depth=2
```

Per ogni candidato chiedi chi lo usa, cosa dipende da esso e come ripristinarlo. Per un servizio confermato come inutile:

```bash
sudo systemctl disable --now esempio.service
```

Non disabilitare alla cieca agenti di sicurezza, networking, logging o gestione cloud. Il risparmio di pochi MiB non vale una macchina non amministrabile.

## 3. Ridurre concorrenza, heap e cache alla fonte

Un limite cgroup protegge l'host; una configurazione applicativa corretta evita di colpire quel limite. Cerca tre moltiplicatori:

- **worker e thread:** 32 processi da 200 MiB sono 6,4 GiB prima delle cache condivise;
- **heap massimo:** JVM, runtime e database spesso hanno un tetto esplicito;
- **cache senza bound:** limita per byte o numero di elementi e definisci una politica di espulsione.

Riduci una variabile alla volta. Confronta throughput per GiB e latenza, non solo RSS. Se dimezzare i worker riduce la RAM del 40% ma il throughput soltanto del 5%, hai trovato un miglioramento reale. Se il servizio ha un leak, riavviarlo periodicamente e' una mitigazione temporanea, non la correzione.

## 4. Mettere un tetto a tmpfs

`tmpfs` puo' crescere fino a consumare memoria e swap. Controlla:

```bash
findmnt -t tmpfs
df -h -t tmpfs
```

Per un mount gestito in `/etc/fstab`, imposta una dimensione coerente con il workload:

```fstab
tmpfs /srv/app-tmp tmpfs rw,nosuid,nodev,size=1G 0 0
```

La dimensione e' un massimo, non una preallocazione. Prima di ridurla misura il picco reale e verifica come l'applicazione reagisce a `ENOSPC`. Non confondere `/tmp` su disco con un tmpfs.

## 5. Applicare budget ai servizi

Usa quanto costruito nella [parte 3]({{< relref "/posts/0025/index.it.md" >}}): `MemoryHigh` poco sopra il working set normale, `MemoryMax` come ultima difesa e `MemoryLow` soltanto per componenti essenziali.

Per un comando batch puoi provare un limite in uno scope transitorio:

```bash
systemd-run --user --scope -p MemoryHigh=2G -p MemoryMax=2500M ./job.sh
```

Il job deve gestire rallentamento, errore e retry. Un limite non trasforma automaticamente un'applicazione memory hungry in una efficiente.

## 6. Scegliere zram o zswap

Se restano pagine fredde e comprimibili, applica uno dei profili della [parte 2]({{< relref "/posts/0024/index.it.md" >}}). Conserva la configurazione solo se:

- PSI `some` e `full` diminuiscono;
- swap-in/out su disco e attesa I/O diminuiscono;
- la CPU conserva margine;
- p95 e p99 non peggiorano;
- non compaiono nuovi OOM.

## 7. Non trasformare gli sysctl in superstizione

Mantieni i default finche' una misura non identifica il problema:

- `vm.swappiness`: regola il costo relativo del paging; non e' un interruttore RAM;
- `vm.vfs_cache_pressure`: aumentarlo puo' recuperare dentry/inode piu' aggressivamente ma penalizzare workload filesystem;
- `vm.overcommit_memory`: controlla l'ammissione di memoria virtuale; non riduce il working set;
- `vm.drop_caches`: e' uno strumento per test, non manutenzione periodica;
- Transparent Huge Pages: possono aiutare alcuni workload e danneggiarne altri; non sono una soluzione generica per risparmiare RAM.

Per ogni modifica persistente registra valore precedente, motivazione, data e comando di rollback.

## Tabella prima/dopo

Compila questa tabella con almeno tre esecuzioni per configurazione:

| KPI | Prima | Dopo | Obiettivo |
|---|---:|---:|---:|
| `MemAvailable` minimo |  |  | margine positivo |
| RSS/PSS picco del servizio |  |  | sotto budget |
| PSI memory `some avg60` |  |  | in calo |
| PSI memory `full avg60` |  |  | vicino a zero nel normale carico |
| swap-in al minuto |  |  | niente thrashing |
| latenza p95/p99 |  |  | entro SLO |
| throughput |  |  | invariato o migliore |
| OOM / restart |  |  | zero inattesi |

Non usare un singolo picco come verdetto. Confronta mediana e caso peggiore su finestre equivalenti.

## Quando comprare RAM, nonostante il prezzo

L'acquisto e' razionale quando tutte queste condizioni sono vere:

1. il carico e' utile e non eliminabile;
2. non ci sono leak o cache senza limite;
3. concorrenza e heap sono gia' dimensionati;
4. cgroup impediscono a un servizio di destabilizzare l'host;
5. compressione e swap non rispettano SLO di latenza/CPU;
6. PSI `full`, paging o OOM restano ripetibili.

A quel punto non stai “sprecando” denaro: stai comprando il working set fisico dimostrato dai dati. Con prezzi DRAM moltiplicati, il benchmark evita sia un upgrade prematuro sia settimane di tuning su una macchina semplicemente sottodimensionata.

## Checklist finale

- [ ] Baseline con carico e SLO registrati
- [ ] Top processi verificati con RSS/PSS
- [ ] Servizi inutili rimossi con rollback
- [ ] Worker, heap, cache e tmpfs limitati
- [ ] `MemoryHigh` e `MemoryMax` testati
- [ ] zram **oppure** zswap misurato
- [ ] PSI, swap, CPU, latenza e throughput confrontati
- [ ] Decisione documentata: mantenere, ridimensionare o acquistare

## Fonti

- [Linux kernel: Pressure Stall Information](https://docs.kernel.org/accounting/psi.html)
- [Linux kernel: sysctl della virtual memory](https://docs.kernel.org/admin-guide/sysctl/vm.html)
- [Linux kernel: Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)
