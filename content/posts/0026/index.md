---
title: "Reduce Linux RAM Usage: A Practical Plan and Final Benchmark"
description: "A seven-step Linux plan for reducing RAM through services, workers, caches, tmpfs, cgroups and zram, with measurable purchase criteria."
date: 2026-07-31T09:00:00+00:00
lastmod: 2026-07-08T00:00:00+00:00
slug: "reduce-linux-ram-usage-plan-benchmark"
draft: false
cover:
  alt: "Plan for reducing Linux RAM consumption"
  caption: "Linux RAM series, part 4: optimize, verify, decide"
  relative: true
  image: "static/linux-ram-part-4.svg"
  width: 1200
  height: 630
keywords: ["reduce Linux RAM usage", "free Linux RAM", "Linux memory optimization", "Linux RAM benchmark", "reduce Linux processes", "Linux memory tuning"]
tags: ["Linux", "RAM", "Performance", "Benchmark", "Optimization"]
categories: ["Linux"]
inLanguage: "en"
isBasedOn:
- "https://docs.kernel.org/accounting/psi.html"
- "https://docs.kernel.org/admin-guide/sysctl/vm.html"
- "https://docs.kernel.org/admin-guide/cgroup-v2.html"
faq:
- question: "How can I actually reduce RAM usage on Linux?"
  answer: "Measure under load, disable only unnecessary services, cap application concurrency and caches, bound tmpfs and cgroups, then evaluate zram or zswap. Compare PSI, latency, swap-in and peaks before and after."
- question: "Should I change overcommit_memory to save RAM?"
  answer: "Not as a generic optimization. Overcommit controls admission of virtual allocations, not the active working set. Mode 2 can reject legitimate allocations and requires workload-specific capacity planning."
- question: "When is buying more RAM genuinely necessary?"
  answer: "When useful load is unchanged and, after fixing leaks, caches, concurrency and isolation, full PSI, swap-in, latency and OOM remain above objectives. The physical working set then does not fit available memory."
---

## In brief

The effective way to **reduce Linux RAM usage** is not a list of sysctls. It is a controlled measure-change-verify cycle. Shrink the application working set first, isolate services second, then use compression and swap; buy RAM only when pressure remains incompatible with objectives.

This concludes the series that began with [prices and diagnosis]({{< relref "/posts/0023/index.md" >}}), continued with [zram and zswap]({{< relref "/posts/0024/index.md" >}}), and added [systemd/cgroup limits]({{< relref "/posts/0025/index.md" >}}).

## 1. Define load and budget

Choose a repeatable window with the same dataset, concurrency and duration. Record at least:

```bash
date -Is
free -h
cat /proc/pressure/memory
vmstat 1 60
ps -eo pid,user,comm,rss,%mem --sort=-rss | head -n 25
```

Add p95/p99 latency, throughput, errors and job duration. “Less RAM” is not an optimization if it halves useful work.

## 2. Remove only what is unnecessary

List running services and major cgroups:

```bash
systemctl --type=service --state=running
systemd-cgtop --depth=2
```

For each candidate, identify its owner, dependencies and rollback. For a confirmed unnecessary service:

```bash
sudo systemctl disable --now example.service
```

Do not blindly disable security, networking, logging or cloud-management agents. A few MiB is not worth an unmanageable machine.

## 3. Reduce concurrency, heaps and caches at the source

A cgroup limit protects the host; correct application configuration avoids hitting it. Find three multipliers:

- **workers and threads:** 32 processes at 200 MiB consume 6.4 GiB before shared caches;
- **maximum heap:** JVMs, runtimes and databases commonly expose an explicit cap;
- **unbounded caches:** limit bytes or entries and define eviction.

Change one variable at a time. Compare throughput per GiB and latency, not only RSS. If halving workers cuts RAM 40% but throughput only 5%, that is a real improvement. Periodic restarts mitigate a leak; they do not fix it.

## 4. Bound tmpfs

`tmpfs` can grow into memory and swap. Inspect it:

```bash
findmnt -t tmpfs
df -h -t tmpfs
```

For a mount managed in `/etc/fstab`, set a workload-appropriate cap:

```fstab
tmpfs /srv/app-tmp tmpfs rw,nosuid,nodev,size=1G 0 0
```

Size is a maximum, not preallocation. Measure the peak and test how the application handles `ENOSPC` before lowering it. Do not confuse disk-backed `/tmp` with tmpfs.

## 5. Apply service budgets

Use the [part 3]({{< relref "/posts/0025/index.md" >}}) pattern: `MemoryHigh` just above normal working set, `MemoryMax` as final defense, and `MemoryLow` only for essential components.

Test a batch command in a transient scope:

```bash
systemd-run --user --scope -p MemoryHigh=2G -p MemoryMax=2500M ./job.sh
```

The job must handle slowdown, failure and retry. A limit does not automatically make a memory-hungry application efficient.

## 6. Choose zram or zswap

If cold compressible pages remain, apply one profile from [part 2]({{< relref "/posts/0024/index.md" >}}). Keep it only when:

- PSI `some` and `full` fall;
- disk swap-in/out and I/O wait fall;
- CPU retains headroom;
- p95 and p99 do not regress;
- no new OOM events appear.

## 7. Do not turn sysctls into superstition

Keep defaults until measurements identify a problem:

- `vm.swappiness` expresses relative paging cost; it is not a RAM switch;
- `vm.vfs_cache_pressure` can reclaim dentries/inodes more aggressively but hurt filesystem workloads;
- `vm.overcommit_memory` controls virtual allocation admission, not working-set size;
- `vm.drop_caches` is a test tool, not periodic maintenance;
- Transparent Huge Pages help some workloads and harm others; they are not a generic RAM-saving feature.

For every persistent change, record the old value, reason, date and rollback command.

## Before/after table

Run each configuration at least three times:

| KPI | Before | After | Goal |
|---|---:|---:|---:|
| Minimum `MemAvailable` |  |  | positive headroom |
| Service peak RSS/PSS |  |  | below budget |
| Memory PSI `some avg60` |  |  | lower |
| Memory PSI `full avg60` |  |  | near zero under normal load |
| Swap-in per minute |  |  | no thrashing |
| p95/p99 latency |  |  | within SLO |
| Throughput |  |  | unchanged or better |
| OOM/restarts |  |  | zero unexpected |

Do not judge from one spike. Compare median and worst case over equivalent windows.

## When to buy RAM despite the price

Purchasing is rational when all these are true:

1. the load is useful and cannot be removed;
2. no leaks or unbounded caches remain;
3. concurrency and heaps are sized;
4. cgroups stop one service destabilizing the host;
5. compression and swap cannot meet latency/CPU SLOs;
6. `full` PSI, paging or OOM remain repeatable.

At that point you are buying a physical working set demonstrated by evidence. With multiplied DRAM prices, the benchmark prevents both a premature upgrade and weeks of tuning a machine that is simply undersized.

## Final checklist

- [ ] Baseline recorded with load and SLOs
- [ ] Top processes checked with RSS/PSS
- [ ] Unnecessary services removed with rollback
- [ ] Workers, heaps, caches and tmpfs bounded
- [ ] `MemoryHigh` and `MemoryMax` tested
- [ ] zram **or** zswap measured
- [ ] PSI, swap, CPU, latency and throughput compared
- [ ] Decision documented: keep, resize or buy

## Sources

- [Linux kernel: Pressure Stall Information](https://docs.kernel.org/accounting/psi.html)
- [Linux kernel: virtual-memory sysctls](https://docs.kernel.org/admin-guide/sysctl/vm.html)
- [Linux kernel: Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)
