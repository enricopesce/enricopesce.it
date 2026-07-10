---
title: "Limitare la RAM dei servizi Linux con systemd e cgroup v2"
description: "Come usare MemoryHigh, MemoryMax, MemoryLow e MemorySwapMax per impedire che un servizio Linux porti l'intero host in OOM."
date: 2026-07-24T09:00:00+00:00
lastmod: 2026-07-08T00:00:00+00:00
slug: "limitare-ram-servizi-linux-systemd-cgroup-v2"
draft: false
cover:
  alt: "Limiti RAM systemd e cgroup v2 su Linux"
  caption: "Serie RAM Linux, parte 3: isolare i servizi"
  relative: true
  image: "static/linux-ram-part-3.svg"
  width: 1200
  height: 630
keywords: ["limitare RAM servizio Linux", "systemd MemoryMax", "systemd MemoryHigh", "cgroup v2 memoria", "MemorySwapMax Linux", "Linux OOM servizio"]
tags: ["Linux", "RAM", "systemd", "cgroup v2", "OOM"]
categories: ["Linux"]
inLanguage: "it-IT"
isBasedOn:
- "https://docs.kernel.org/admin-guide/cgroup-v2.html"
- "https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html"
- "https://www.freedesktop.org/software/systemd/man/latest/systemd-oomd.service.html"
faq:
- question: "Qual è la differenza tra MemoryHigh e MemoryMax?"
  answer: "MemoryHigh è un limite morbido: oltre la soglia il cgroup subisce reclaim e rallenta. MemoryMax è l'ultima difesa rigida: se il consumo non può essere contenuto, nel cgroup interviene l'OOM killer."
- question: "Come limito temporaneamente la RAM di un servizio systemd?"
  answer: "Usa systemctl set-property --runtime nome.service MemoryHigh=... MemoryMax=.... L'opzione --runtime perde le modifiche al reboot ed è adatta a una prova controllata."
- question: "Devo disabilitare lo swap per un servizio?"
  answer: "Di norma no. MemorySwapMax=0 può aumentare la pressione e anticipare l'OOM. Imposta un tetto soltanto quando il profilo di latenza lo richiede e dopo aver misurato PSI e memory.events."
---

Chiunque abbia gestito server Linux per un po' ha vissuto una versione di questo incidente: un servizio — un'applicazione con un leak, un job batch, una query impazzita — cresce finché l'intero host inizia a fare thrashing, e quando finalmente l'OOM killer si sveglia, ammazza qualcosa che ti interessava più del vero colpevole. Il lavoro su zram e zswap della [parte 2]({{< relref "/posts/0024/index.it.md" >}}) ti protegge dai picchi, ma contro questo non fa nulla. La compressione compra margine; non assegna responsabilità.

E oggi la questione pesa più di prima. Con la RAM ai prezzi del 2026, la risposta naturale è consolidare più workload sugli host che hai già — e consolidare è sensato solo se il fallimento di un servizio non può trascinarsi dietro gli altri. È esattamente quello che cgroup v2 e systemd ti danno, e la buona notizia è che il sottoinsieme utile sono quattro impostazioni.

## Parti da quello che il servizio consuma davvero

Prima di impostare qualsiasi limite, verifica di essere su cgroup v2 e guarda il consumo reale del servizio:

```bash
stat -fc %T /sys/fs/cgroup
systemctl show app.service -p ControlGroup -p MemoryCurrent -p MemoryPeak -p MemorySwapCurrent
```

Il primo comando deve stampare `cgroup2fs`. Sostituisci `app.service` con il tuo servizio e osserva il picco sotto un carico rappresentativo. Il budget viene da questo numero — il working set misurato, non "il 25% dell'host" o qualunque frazione arbitraria sembri equa.

## Le quattro impostazioni che contano

systemd espone i controlli di memoria di cgroup v2 come proprietà delle unità:

| Impostazione systemd | Controllo cgroup v2 | Ruolo |
|---|---|---|
| `MemoryLow=` | `memory.low` | protezione best-effort sotto la soglia |
| `MemoryHigh=` | `memory.high` | limite morbido con reclaim e throttling |
| `MemoryMax=` | `memory.max` | limite rigido, ultima difesa da OOM |
| `MemorySwapMax=` | `memory.swap.max` | massimo swap attribuibile al cgroup |

Vale la pena capire l'intento del design, perché la maggior parte delle persone va dritta su `MemoryMax` e si ferma lì. `MemoryHigh` è pensato come il tuo controllo operativo principale: superarlo scatena reclaim e throttling dentro il cgroup, il servizio rallenta e la cosa compare nel monitoring — pressione che puoi osservare e a cui puoi reagire. `MemoryMax` è il muro dietro. Se imposti solo il muro, il servizio ci arriva contro a tutta velocità e subisce OOM senza nessuna fascia di preavviso visibile.

## Prima una prova reversibile

Supponiamo che il servizio abbia un working set stabile di 1,2 GiB e picchi legittimi sotto 1,6 GiB. Un primo budget ragionevole:

```bash
sudo systemctl set-property --runtime app.service \
  MemoryHigh=1500M MemoryMax=1800M MemorySwapMax=512M
```

Il flag `--runtime` significa che tutto sparisce al reboot, che è esattamente quello che vuoi per un test. Ora genera il carico e guarda cosa succede:

```bash
watch -n 1 'systemctl show app.service -p MemoryCurrent -p MemoryPeak -p MemorySwapCurrent'
CG=$(systemctl show -p ControlGroup --value app.service)
sudo cat "/sys/fs/cgroup${CG}/memory.events"
sudo cat "/sys/fs/cgroup${CG}/memory.pressure"
```

In `memory.events`, un contatore `high` che sale significa che il servizio ha attraversato la soglia morbida — normale ogni tanto, un problema se è costante. `oom` e `oom_kill` significano che è sbagliato il budget oppure l'applicazione. Una sottigliezza che vale la pena interiorizzare: PSI alto dentro il cgroup con PSI basso sull'host dimostra che l'*isolamento* funziona. Non dice nulla sul fatto che la latenza del servizio sia ancora accettabile — quella va verificata a parte.

Per annullare solo i limiti della prova, senza toccare eventuali override preesistenti:

```bash
sudo systemctl set-property --runtime app.service \
  MemoryHigh=infinity MemoryMax=infinity MemorySwapMax=infinity
```

## Rendilo persistente

Quando il budget sopravvive al carico reale, mettilo in un override — mai modificare direttamente il file dell'unità pacchettizzata:

```bash
sudo systemctl edit app.service
```

```ini
[Service]
MemoryHigh=1500M
MemoryMax=1800M
MemorySwapMax=512M
```

Poi:

```bash
sudo systemctl daemon-reload
sudo systemctl restart app.service
```

Il restart è una vera interruzione del servizio: pianificalo come tale e verifica l'applicazione dopo.

## Proteggi quello che deve restare vivo

I limiti spingono verso il basso; `MemoryLow` spinge nella direzione opposta. Per un servizio piccolo ma essenziale — il proxy, l'agente di monitoraggio, la cosa che ti serve funzionante *soprattutto* quando l'host è sotto pressione — chiede al kernel di risparmiare quel budget durante il reclaim, best-effort:

```ini
[Service]
MemoryLow=256M
```

Due avvertenze. Funziona solo se applicato coerentemente lungo la gerarchia dei cgroup, e le protezioni che distribuisci non possono sommarsi a più RAM di quella che esiste. Da cui la disciplina ovvia: non proteggere tutto. Se ogni servizio è prioritario, non lo è nessuno.

## Un OOM prevedibile è meglio di un host congelato

Anche con i budget a posto, un host può comunque finire nei guai, e l'OOM killer del kernel tende ad arrivare tardi e a scegliere male. `systemd-oomd` usa PSI e cgroup v2 per intervenire prima, mentre l'host è ancora reattivo:

```bash
systemctl status systemd-oomd
oomctl
```

Le direttive `ManagedOOMMemoryPressure=` e `ManagedOOMSwap=` dipendono dalla versione di systemd e dalla gerarchia delle unità, quindi controlla prima di abilitarle:

```bash
systemd --version
man systemd.resource-control
man systemd-oomd.service
```

E manteniamo la prospettiva: un OOM controllato resta un'interruzione. Assicurati che l'unità abbia una politica di restart sensata, che i dati restino consistenti dopo un kill e che gli allarmi sappiano distinguere un kill intenzionale da un crash.

## Container: il limite deve esistere davvero

I runtime container traducono i loro limiti di memoria in questi stessi cgroup — il che significa che lo YAML può dire una cosa e il kernel un'altra. Verifica a livello kernel:

```bash
systemd-cgls
systemd-cgtop --depth=3
```

Un container senza limite non è affatto isolato dalla RAM dell'host. Un limite sotto il suo working set normale significa reclaim continuo e restart. Un limite enorme esiste solo sulla carta. Il metodo si applica identico: baseline del working set, soglia morbida con margine, difesa rigida dietro, e occhio a `memory.events`.

## Non allocare memoria che non c'è

Ultima trappola: su un host da 16 GiB, non distribuire 16 GiB di `MemoryMax` tra i servizi come se il kernel, la page cache e i picchi simultanei non esistessero. Lascia spazio esplicito per il kernel e le sue slab cache, per la cache del filesystem che fa lavoro utile, per i servizi di accesso, logging e monitoring, per picchi sovrapposti realistici, per zram o zswap se li hai abilitati nella parte 2 — e abbastanza margine da poter ancora entrare in SSH e sistemare le cose quando qualcosa va storto.

A questo punto della serie sai misurare la pressione, assorbire i picchi con la compressione e contenere i singoli servizi. La [parte 4]({{< relref "/posts/0026/index.it.md" >}}) mette tutto insieme: un benchmark prima/dopo e una risposta onesta alla domanda da cui è partito tutto — ottimizzare, o comprare la RAM.

## Fonti

- [Linux kernel: Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)
- [systemd: resource control](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html)
- [systemd: userspace OOM killer](https://www.freedesktop.org/software/systemd/man/latest/systemd-oomd.service.html)
