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
- question: "Qual e' la differenza tra MemoryHigh e MemoryMax?"
  answer: "MemoryHigh e' un limite morbido: oltre la soglia il cgroup subisce reclaim e rallenta. MemoryMax e' l'ultima difesa rigida: se il consumo non puo' essere contenuto, nel cgroup interviene l'OOM killer."
- question: "Come limito temporaneamente la RAM di un servizio systemd?"
  answer: "Usa systemctl set-property --runtime nome.service MemoryHigh=... MemoryMax=.... L'opzione --runtime perde le modifiche al reboot ed e' adatta a una prova controllata."
- question: "Devo disabilitare lo swap per un servizio?"
  answer: "Di norma no. MemorySwapMax=0 puo' aumentare la pressione e anticipare l'OOM. Imposta un tetto soltanto quando il profilo di latenza lo richiede e dopo aver misurato PSI e memory.events."
---

## In breve

La compressione della [parte 2]({{< relref "/posts/0024/index.it.md" >}}) protegge dai picchi, ma non impedisce a un singolo servizio di affamare l'host. Con **cgroup v2 e systemd**, `MemoryHigh` applica pressione controllata, `MemoryMax` definisce l'ultima barriera e `MemoryLow` protegge il working set dei servizi essenziali.

Con RAM molto piu' costosa, consolidare piu' workload sullo stesso host ha senso solo se il loro fallimento e' isolato.

## Verificare cgroup v2 e il consumo del servizio

```bash
stat -fc %T /sys/fs/cgroup
systemctl show app.service -p ControlGroup -p MemoryCurrent -p MemoryPeak -p MemorySwapCurrent
```

Il primo comando deve restituire `cgroup2fs`. Sostituisci `app.service` e osserva il picco sotto carico rappresentativo. Definisci il budget partendo dal **working set misurato**, non da una percentuale arbitraria dell'host.

## I quattro controlli che contano

| Impostazione systemd | Controllo cgroup v2 | Ruolo |
|---|---|---|
| `MemoryLow=` | `memory.low` | protezione best-effort sotto la soglia |
| `MemoryHigh=` | `memory.high` | limite morbido con reclaim e throttling |
| `MemoryMax=` | `memory.max` | limite rigido, ultima difesa da OOM |
| `MemorySwapMax=` | `memory.swap.max` | massimo swap attribuibile al cgroup |

Usa `MemoryHigh` come controllo operativo principale e lascia margine tra `High` e `Max`. Se imposti soltanto `MemoryMax`, il servizio puo' arrivare rapidamente contro un muro e subire OOM senza una fascia di pressione osservabile.

## Una prova reversibile

Supponiamo che il servizio abbia un working set stabile di 1,2 GiB e picchi validi sotto 1,6 GiB:

```bash
sudo systemctl set-property --runtime app.service \
  MemoryHigh=1500M MemoryMax=1800M MemorySwapMax=512M
```

`--runtime` rende il test temporaneo. Genera il carico e controlla:

```bash
watch -n 1 'systemctl show app.service -p MemoryCurrent -p MemoryPeak -p MemorySwapCurrent'
CG=$(systemctl show -p ControlGroup --value app.service)
sudo cat "/sys/fs/cgroup${CG}/memory.events"
sudo cat "/sys/fs/cgroup${CG}/memory.pressure"
```

In `memory.events`, l'aumento di `high` indica attraversamenti della soglia morbida; `oom` e `oom_kill` sono segnali che il budget o l'applicazione devono essere corretti. PSI elevato nel cgroup ma basso sull'host dimostra che l'isolamento funziona, non che la latenza del servizio sia accettabile.

Per annullare soltanto i limiti della prova, senza rimuovere eventuali override preesistenti:

```bash
sudo systemctl set-property --runtime app.service \
  MemoryHigh=infinity MemoryMax=infinity MemorySwapMax=infinity
```

## Rendere persistente il budget

Apri un override invece di modificare l'unita' del pacchetto:

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

Un restart e' una modifica di servizio: pianificalo e verifica il comportamento applicativo.

## Proteggere cio' che deve restare vivo

Per un servizio piccolo ma essenziale, per esempio il proxy o l'agente di monitoraggio, `MemoryLow=256M` richiede al kernel di preservare quel budget best-effort durante il reclaim. La protezione e' efficace solo se applicata coerentemente nella gerarchia e se la somma delle protezioni non promette piu' RAM di quella disponibile.

```ini
[Service]
MemoryLow=256M
```

Non proteggere ogni servizio: se tutto e' prioritario, niente lo e'.

## OOM prevedibile invece di host bloccato

`systemd-oomd` usa PSI e cgroup v2 per intervenire prima che la pressione renda il sistema inutilizzabile. Verifica disponibilita' e stato:

```bash
systemctl status systemd-oomd
oomctl
```

Le direttive `ManagedOOMMemoryPressure=` e `ManagedOOMSwap=` dipendono dalla versione systemd e dalla gerarchia delle unita'. Prima di abilitarle controlla:

```bash
systemd --version
man systemd.resource-control
man systemd-oomd.service
```

Un OOM controllato resta un'interruzione: assicurati che l'unita' abbia una politica di restart sensata, che i dati siano consistenti e che l'allarme distingua un kill intenzionale da un crash.

## Container: il limite deve esistere davvero

I runtime container traducono i limiti in cgroup. Verifica dal kernel, non soltanto dal file di orchestrazione:

```bash
systemd-cgls
systemd-cgtop --depth=3
```

Un container senza limite non e' isolato dalla RAM dell'host. Un limite inferiore al normale working set produce reclaim, throttling e restart; uno enorme esiste solo sulla carta. Applica gli stessi criteri: baseline, `High` con margine, `Max` come difesa e osservazione di `memory.events`.

## Strategia di allocazione

Su un host da 16 GiB non distribuire 16 GiB di `MemoryMax` come se kernel, page cache e picchi non esistessero. Riserva esplicitamente spazio per:

- kernel, slab e filesystem cache;
- servizi di accesso, logging e monitoring;
- picchi simultanei realistici;
- zram o zswap, se abilitati;
- margine di recupero amministrativo.

Nella [parte 4]({{< relref "/posts/0026/index.it.md" >}}) trasformeremo tutte le misure in un benchmark prima/dopo e in una decisione acquisto/non acquisto.

## Fonti

- [Linux kernel: Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)
- [systemd: resource control](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html)
- [systemd: userspace OOM killer](https://www.freedesktop.org/software/systemd/man/latest/systemd-oomd.service.html)
