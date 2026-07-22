---
title: "Ridurre il consumo di RAM su Linux: piano pratico e benchmark finale"
description: "Un piano Linux in sette passi per ridurre RAM: servizi, worker, cache, tmpfs, cgroup, zram e criteri misurabili per decidere se acquistare memoria."
date: 2026-07-22T00:00:00+00:00
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
  answer: "Non come ottimizzazione generica. Overcommit regola l'ammissione delle allocazioni virtuali, non riduce il working set. La modalità 2 può far fallire allocazioni legittime e richiede capacity planning specifico."
- question: "Quando è davvero necessario comprare altra RAM?"
  answer: "Quando, a carico utile invariato e dopo aver corretto leak, cache, concorrenza e isolamento, PSI full, swap-in, latenza e OOM restano oltre gli obiettivi. In quel caso il working set fisico non entra nella memoria disponibile."
---

Se cerchi "ridurre consumo RAM Linux", quello che trovi sono per lo più liste di sysctl da incollare — metti swappiness a questo valore, svuota le cache, disabilita quest'altro. Non ho mai visto quell'approccio sopravvivere al contatto con un host di produzione vero. Quello che funziona è molto meno glamour: un ciclo misura-modifica-verifica, applicato nell'ordine giusto — prima ridurre il working set applicativo, poi isolare i servizi, poi comprimere, e comprare RAM solo quando i numeri dimostrano che non c'è altra strada.

Questa è la parte finale della serie. Mette insieme le [misure di pressione della parte 1]({{< relref "/posts/0023/index.it.md" >}}), i [profili zram e zswap della parte 2]({{< relref "/posts/0024/index.it.md" >}}) e i [limiti systemd/cgroup della parte 3]({{< relref "/posts/0025/index.it.md" >}}) in un piano da eseguire dall'inizio alla fine.

## 1. Definisci il carico e il budget

Niente di questo piano significa qualcosa senza una finestra di test ripetibile: stesso dataset, stessa concorrenza, stessa durata. Registra almeno:

```bash
date -Is
free -h
cat /proc/pressure/memory
vmstat 1 60
ps -eo pid,user,comm,rss,%mem --sort=-rss | head -n 25
```

Accanto ai numeri di sistema, cattura quelli applicativi — latenza p95/p99, throughput, tasso di errori, durata dei job. È il guard rail dell'intero esercizio: "meno RAM" non è un'ottimizzazione se arriva con metà del lavoro utile.

## 2. Elimina solo quello che è davvero inutile

Parti da quello che sta effettivamente girando:

```bash
systemctl --type=service --state=running
systemd-cgtop --depth=2
```

Per ogni candidato, rispondi a tre domande prima di toccarlo: chi lo usa, cosa dipende da lui, come lo riporto indietro. Solo allora:

```bash
sudo systemctl disable --now esempio.service
```

La tentazione qui è andare a caccia di ogni ultimo demone. Non disabilitare agenti di sicurezza, networking, logging o gestione cloud per risparmiare qualche MiB — il risparmio è irrisorio e la macchina che ti ritrovi è una che non riesci più ad amministrare.

## 3. Riduci concorrenza, heap e cache alla fonte

È qui che sta la memoria vera, ed è il passo che tutti saltano perché significa aprire le configurazioni applicative invece di digitare sysctl. Un limite cgroup protegge l'host; un dimensionamento applicativo corretto è quello che ti evita di colpire quel limite. Tre moltiplicatori vale la pena cercarli:

- **Worker e thread.** 32 processi worker da 200 MiB l'uno fanno 6,4 GiB prima ancora di contare le cache condivise. Il numero di worker di solito viene impostato una volta, con generosità, e mai più rivisto.
- **Heap massimo.** JVM, runtime e database espongono quasi sempre un tetto esplicito — controlla se il tuo riflette quello che serve all'applicazione o quello che qualcuno ha stimato anni fa.
- **Cache senza limite.** Qualsiasi cache in-process senza un limite in byte o elementi prima o poi ne troverà uno al posto tuo. Dalle un bound e una politica di espulsione.

Cambia una variabile alla volta, e giudica da throughput per GiB e latenza, non solo dall'RSS. Se dimezzare i worker taglia la RAM del 40% e il throughput solo del 5%, hai trovato un miglioramento reale. E se un servizio ha un leak: i restart periodici sono una mitigazione, non una correzione — non lasciare che diventino architettura permanente.

## 4. Metti un tetto a tmpfs

Facile da dimenticare: `tmpfs` cresce dentro memoria e swap come qualsiasi altra cosa. Guarda cosa hai:

```bash
findmnt -t tmpfs
df -h -t tmpfs
```

Per un mount che gestisci in `/etc/fstab`, imposta una dimensione coerente con il workload:

```fstab
tmpfs /srv/app-tmp tmpfs rw,nosuid,nodev,size=1G 0 0
```

La dimensione è un massimo, non una preallocazione, quindi il tetto non costa nulla finché l'uso è normale. Prima di abbassarne uno esistente, misura il picco reale e prova come reagisce l'applicazione a `ENOSPC`. E controlla con cosa hai davvero a che fare — un `/tmp` su disco non è un tmpfs.

## 5. Applica i budget ai servizi

Ora applica il pattern della parte 3 ai servizi che contano: `MemoryHigh` poco sopra il working set normale, `MemoryMax` come ultima difesa, `MemoryLow` solo per i componenti davvero essenziali.

Per i job batch, uno scope transitorio ti permette di provare un budget senza scrivere nessun file di unità:

```bash
systemd-run --user --scope -p MemoryHigh=2G -p MemoryMax=2500M ./job.sh
```

Un'aspettativa da mettere in chiaro: il job deve saper gestire rallentamento, fallimento e retry. Un limite contiene un'applicazione affamata di memoria; non la rende efficiente.

## 6. Scegli zram o zswap

Se dopo tutto questo restano ancora pagine fredde e comprimibili, applica uno dei due profili della parte 2 — uno, non entrambi. Conserva la configurazione solo se il quadro completo migliora:

- PSI `some` e `full` calano;
- swap-in/out su disco e attesa I/O calano;
- la CPU conserva margine;
- p95 e p99 non peggiorano;
- non compaiono nuovi OOM.

Se uno di questi punti fallisce, la compressione ti sta costando più di quello che rende. Toglila.

## 7. Non trasformare i sysctl in superstizione

Ho lasciato i sysctl per ultimi apposta, perché è lì che devono stare. Mantieni i default finché una misura non punta a un problema specifico:

- `vm.swappiness` esprime il costo relativo del paging — non è un interruttore della RAM;
- `vm.vfs_cache_pressure` può recuperare dentry e inode più aggressivamente, e penalizzare i workload filesystem-intensive nel farlo;
- `vm.overcommit_memory` regola l'ammissione delle allocazioni virtuali — non fa nulla al tuo working set;
- `vm.drop_caches` è uno strumento da test, non manutenzione periodica;
- le Transparent Huge Pages aiutano alcuni workload e ne danneggiano altri — non sono un risparmia-RAM generico.

Per ogni modifica che decidi di tenere, scrivi valore precedente, motivazione, data e comando di rollback. Il te stesso delle 3 di notte ringrazierà.

## La tabella prima/dopo

Questo è il deliverable dell'intera serie. Esegui ogni configurazione almeno tre volte e compilala:

| KPI | Prima | Dopo | Obiettivo |
|---|---:|---:|---:|
| `MemAvailable` minimo |  |  | margine positivo |
| RSS/PSS picco del servizio |  |  | sotto budget |
| PSI memory `some avg60` |  |  | in calo |
| PSI memory `full avg60` |  |  | vicino a zero nel carico normale |
| swap-in al minuto |  |  | niente thrashing |
| latenza p95/p99 |  |  | entro SLO |
| throughput |  |  | invariato o migliore |
| OOM / restart |  |  | zero inattesi |

Non giudicare da un singolo picco, in nessuna delle due direzioni. Confronta mediane e casi peggiori su finestre equivalenti.

## Quando comprare RAM è la risposta giusta

Dopo un'intera serie sul non comprare RAM, è giusto dire chiaramente quando invece va comprata. L'acquisto è razionale quando valgono tutte queste condizioni:

1. il carico è utile e non eliminabile;
2. non restano leak o cache senza limite;
3. concorrenza e heap sono dimensionati correttamente;
4. i cgroup impediscono a un singolo servizio di destabilizzare l'host;
5. compressione e swap non rispettano gli obiettivi di latenza e CPU;
6. PSI `full`, paging o OOM restano, in modo ripetibile.

A quel punto non stai buttando soldi su un sintomo: stai comprando un working set fisico che i dati dicono non entrare. Anche a prezzi DRAM moltiplicati è la scelta giusta, e il benchmark è quello che ti protegge da entrambi i modi di sbagliare: l'upgrade prematuro e le settimane di tuning su una macchina semplicemente sottodimensionata.

## La checklist

Tutto quello delle quattro parti, in ordine:

- [ ] Baseline registrata con carico e SLO
- [ ] Top processi verificati con RSS/PSS
- [ ] Servizi inutili rimossi, con rollback
- [ ] Worker, heap, cache e tmpfs limitati
- [ ] `MemoryHigh` e `MemoryMax` testati
- [ ] zram **oppure** zswap misurato
- [ ] PSI, swap, CPU, latenza e throughput confrontati
- [ ] Decisione documentata: mantenere, ridimensionare o comprare

## Fonti

- [Linux kernel: Pressure Stall Information](https://docs.kernel.org/accounting/psi.html)
- [Linux kernel: sysctl della virtual memory](https://docs.kernel.org/admin-guide/sysctl/vm.html)
- [Linux kernel: Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)
