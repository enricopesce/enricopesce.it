---
title: "Limit Linux Service RAM with systemd and cgroup v2"
description: "Use MemoryHigh, MemoryMax, MemoryLow and MemorySwapMax to stop one Linux service from driving the entire host into OOM."
date: 2026-07-24T09:00:00+00:00
lastmod: 2026-07-08T00:00:00+00:00
slug: "limit-linux-service-ram-systemd-cgroup-v2"
draft: false
cover:
  alt: "Linux systemd and cgroup v2 RAM limits"
  caption: "Linux RAM series, part 3: isolate services"
  relative: true
  image: "static/linux-ram-part-3.svg"
  width: 1200
  height: 630
keywords: ["limit Linux service RAM", "systemd MemoryMax", "systemd MemoryHigh", "cgroup v2 memory", "MemorySwapMax Linux", "Linux service OOM"]
tags: ["Linux", "RAM", "systemd", "cgroup v2", "OOM"]
categories: ["Linux"]
inLanguage: "en"
isBasedOn:
- "https://docs.kernel.org/admin-guide/cgroup-v2.html"
- "https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html"
- "https://www.freedesktop.org/software/systemd/man/latest/systemd-oomd.service.html"
faq:
- question: "What is the difference between MemoryHigh and MemoryMax?"
  answer: "MemoryHigh is a soft boundary that triggers reclaim and throttling. MemoryMax is the final hard boundary; if usage cannot be contained, the OOM killer acts inside the cgroup."
- question: "How do I temporarily limit a systemd service's RAM?"
  answer: "Use systemctl set-property --runtime name.service MemoryHigh=... MemoryMax=.... The --runtime option loses changes at reboot and is suitable for a controlled test."
- question: "Should I disable swap for a service?"
  answer: "Usually not. MemorySwapMax=0 can increase pressure and bring OOM forward. Set a cap only when the latency profile requires it and after measuring PSI and memory.events."
---

## In brief

Compression from [part 2]({{< relref "/posts/0024/index.md" >}}) protects against peaks, but it cannot stop one service starving the host. With **cgroup v2 and systemd**, `MemoryHigh` applies controlled pressure, `MemoryMax` provides the final boundary, and `MemoryLow` protects essential working sets.

When RAM is expensive, consolidating workloads is sensible only if failures remain isolated.

## Verify cgroup v2 and current usage

```bash
stat -fc %T /sys/fs/cgroup
systemctl show app.service -p ControlGroup -p MemoryCurrent -p MemoryPeak -p MemorySwapCurrent
```

The first command should print `cgroup2fs`. Replace `app.service` and observe its peak under representative load. Derive the budget from the **measured working set**, not an arbitrary host percentage.

## The four important controls

| systemd setting | cgroup v2 control | Role |
|---|---|---|
| `MemoryLow=` | `memory.low` | best-effort protection below the boundary |
| `MemoryHigh=` | `memory.high` | soft boundary with reclaim and throttling |
| `MemoryMax=` | `memory.max` | hard boundary and final OOM defense |
| `MemorySwapMax=` | `memory.swap.max` | maximum swap charged to the cgroup |

Use `MemoryHigh` as the main operational control and leave headroom before `MemoryMax`. Setting only `MemoryMax` lets a service run straight into a hard wall without an observable pressure band.

## A reversible test

Suppose the service has a 1.2 GiB stable working set and valid peaks below 1.6 GiB:

```bash
sudo systemctl set-property --runtime app.service \
  MemoryHigh=1500M MemoryMax=1800M MemorySwapMax=512M
```

Generate load and inspect:

```bash
watch -n 1 'systemctl show app.service -p MemoryCurrent -p MemoryPeak -p MemorySwapCurrent'
CG=$(systemctl show -p ControlGroup --value app.service)
sudo cat "/sys/fs/cgroup${CG}/memory.events"
sudo cat "/sys/fs/cgroup${CG}/memory.pressure"
```

In `memory.events`, rising `high` counts soft-boundary crossings. `oom` and `oom_kill` mean the budget or application needs correction. High cgroup PSI with low host PSI proves isolation works; it does not prove service latency is acceptable.

Remove only the test limits, without deleting any pre-existing overrides:

```bash
sudo systemctl set-property --runtime app.service \
  MemoryHigh=infinity MemoryMax=infinity MemorySwapMax=infinity
```

## Make the budget persistent

Create an override instead of editing a packaged unit:

```bash
sudo systemctl edit app.service
```

```ini
[Service]
MemoryHigh=1500M
MemoryMax=1800M
MemorySwapMax=512M
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl restart app.service
```

A restart changes service state; schedule it and validate application behavior.

## Protect what must stay alive

For a small essential service such as a proxy or monitoring agent, `MemoryLow=256M` asks the kernel to preserve that budget on a best-effort basis during reclaim. It works only when applied coherently through the hierarchy and when protections do not promise more RAM than exists.

```ini
[Service]
MemoryLow=256M
```

Do not protect every service. If everything is priority, nothing is.

## Predictable OOM instead of a frozen host

`systemd-oomd` uses PSI and cgroup v2 to act before pressure makes the host unusable. Check availability and status:

```bash
systemctl status systemd-oomd
oomctl
```

`ManagedOOMMemoryPressure=` and `ManagedOOMSwap=` depend on the systemd version and unit hierarchy. Before enabling them, check:

```bash
systemd --version
man systemd.resource-control
man systemd-oomd.service
```

A controlled OOM is still an outage. Configure sensible restart behavior, protect data consistency, and alert differently for an intentional kill and a crash.

## Containers: verify the real limit

Container runtimes translate limits into cgroups. Verify at the kernel level, not only in orchestration YAML:

```bash
systemd-cgls
systemd-cgtop --depth=3
```

An unlimited container is not isolated from host RAM. A limit below its normal working set causes reclaim and restarts; a huge limit exists only on paper. Apply the same baseline, soft boundary, hard defense and `memory.events` monitoring.

## Allocation strategy

On a 16 GiB host, do not distribute 16 GiB of `MemoryMax` as if the kernel, page cache and peaks did not exist. Reserve capacity for:

- kernel, slab and filesystem cache;
- access, logging and monitoring services;
- realistic simultaneous peaks;
- zram or zswap, when enabled;
- administrative recovery headroom.

[Part 4]({{< relref "/posts/0026/index.md" >}}) turns every measurement into a before/after benchmark and a buy-or-optimize decision.

## Sources

- [Linux kernel: Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)
- [systemd: resource control](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html)
- [systemd: userspace OOM killer](https://www.freedesktop.org/software/systemd/man/latest/systemd-oomd.service.html)
