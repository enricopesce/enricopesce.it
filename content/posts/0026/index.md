---
title: "Reduce Linux RAM Usage: A Practical Plan and Final Benchmark"
description: "A seven-step Linux plan for reducing RAM through services, workers, caches, tmpfs, cgroups and zram, with measurable purchase criteria."
date: 2026-07-22T00:00:00+00:00
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

If you search "reduce Linux RAM usage", what you mostly find is lists of sysctls to paste — set swappiness to this, drop the caches, disable that. I've never seen that approach survive contact with a real production host. What works is much less glamorous: a measure-change-verify cycle, applied in the right order — shrink the application working set first, isolate services second, compress third, and buy RAM only when the numbers prove nothing else will do.

This is the final part of the series. It ties together the [pressure measurements from part 1]({{< relref "/posts/0023/index.md" >}}), the [zram and zswap profiles from part 2]({{< relref "/posts/0024/index.md" >}}), and the [systemd/cgroup limits from part 3]({{< relref "/posts/0025/index.md" >}}) into a plan you can run start to finish.

## 1. Define the load and the budget

Nothing else in this plan means anything without a repeatable test window: same dataset, same concurrency, same duration. Record at least:

```bash
date -Is
free -h
cat /proc/pressure/memory
vmstat 1 60
ps -eo pid,user,comm,rss,%mem --sort=-rss | head -n 25
```

Alongside the system numbers, capture the application ones — p95/p99 latency, throughput, error rate, job duration. This is the guard rail for the whole exercise: "less RAM" is not an optimization if it comes with half the useful work.

## 2. Remove only what is genuinely unnecessary

Start with what's actually running:

```bash
systemctl --type=service --state=running
systemd-cgtop --depth=2
```

For each candidate, answer three questions before touching it: who uses this, what depends on it, and how do I bring it back. Only then:

```bash
sudo systemctl disable --now example.service
```

The temptation here is to go hunting for every last daemon. Don't disable security agents, networking, logging or cloud-management tooling to save a few MiB — the savings are trivial and the machine you get back is one you can't manage anymore.

## 3. Reduce concurrency, heaps and caches at the source

This is where the real memory is, and it's the step people skip because it means opening application configs instead of typing sysctls. A cgroup limit protects the host; correct application sizing is what keeps you from hitting that limit in the first place. Three multipliers are worth hunting:

- **Workers and threads.** 32 worker processes at 200 MiB each is 6.4 GiB before you've counted any shared caches. Worker counts are usually set once, generously, and never revisited.
- **Maximum heap.** JVMs, language runtimes and databases almost always expose an explicit cap — check whether yours reflects what the application needs or what someone guessed years ago.
- **Unbounded caches.** Any in-process cache without a byte or entry limit will eventually find one for you. Give it a bound and an eviction policy.

Change one variable at a time, and judge by throughput per GiB and latency, not by RSS alone. If halving the workers cuts RAM by 40% and throughput by only 5%, you've found a real improvement. And if a service leaks: periodic restarts are a mitigation, not a fix — don't let them become permanent architecture.

## 4. Put a bound on tmpfs

Easy to forget: `tmpfs` grows into memory and swap like anything else. See what you have:

```bash
findmnt -t tmpfs
df -h -t tmpfs
```

For a mount you manage in `/etc/fstab`, set a size that matches the workload:

```fstab
tmpfs /srv/app-tmp tmpfs rw,nosuid,nodev,size=1G 0 0
```

The size is a maximum, not a preallocation, so bounding it costs nothing when usage is normal. Before lowering an existing one, measure the actual peak and test how the application reacts to `ENOSPC`. And check what you're actually dealing with — a disk-backed `/tmp` is not a tmpfs.

## 5. Apply service budgets

Now apply the pattern from part 3 to the services that matter: `MemoryHigh` just above the normal working set, `MemoryMax` as the final defense, `MemoryLow` only for the truly essential components.

For batch jobs, a transient scope lets you test a budget without writing any unit files:

```bash
systemd-run --user --scope -p MemoryHigh=2G -p MemoryMax=2500M ./job.sh
```

One expectation to set: the job has to handle being slowed down, failing, and retrying. A limit contains a memory-hungry application; it doesn't make it efficient.

## 6. Choose zram or zswap

If after all of the above you still have cold, compressible pages, apply one of the two profiles from part 2 — one, not both. Keep the configuration only if the full picture improves:

- PSI `some` and `full` go down;
- disk swap-in/out and I/O wait go down;
- the CPU keeps headroom;
- p95 and p99 latency don't regress;
- no new OOM events appear.

If any of those fail, compression is costing you more than it saves. Take it out.

## 7. Don't turn sysctls into superstition

I left the sysctls for last on purpose, because that's where they belong. Keep the defaults until a measurement points at a specific problem:

- `vm.swappiness` expresses the relative cost of paging — it's not a RAM switch;
- `vm.vfs_cache_pressure` can reclaim dentries and inodes more aggressively, and hurt filesystem-heavy workloads doing it;
- `vm.overcommit_memory` controls admission of virtual allocations — it does nothing to your working set;
- `vm.drop_caches` is a testing tool, not periodic maintenance;
- Transparent Huge Pages help some workloads and hurt others — they are not a generic RAM saver.

For every change you do keep, write down the old value, the reason, the date, and the rollback command. Future you, at 3 AM, will be grateful.

## The before/after table

This is the deliverable of the whole series. Run each configuration at least three times and fill it in:

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

Don't judge from a single spike in either direction. Compare medians and worst cases over equivalent windows.

## When buying RAM is the right answer

After a whole series about not buying RAM, it's only fair to say clearly when you should. The purchase is rational when all of these hold:

1. the load is useful and can't be removed;
2. no leaks or unbounded caches remain;
3. concurrency and heaps are properly sized;
4. cgroups stop any one service from destabilizing the host;
5. compression and swap can't meet your latency and CPU objectives;
6. `full` PSI, paging or OOM events remain, repeatably.

At that point you're not throwing money at a symptom — you're buying a physical working set that the evidence says doesn't fit. Even at multiplied DRAM prices, that's the right call, and the benchmark is what protects you from both failure modes: the premature upgrade, and the weeks spent tuning a machine that was simply undersized.

## The checklist

Everything from the four parts, in order:

- [ ] Baseline recorded with load and SLOs
- [ ] Top processes checked with RSS/PSS
- [ ] Unnecessary services removed, with rollback
- [ ] Workers, heaps, caches and tmpfs bounded
- [ ] `MemoryHigh` and `MemoryMax` tested
- [ ] zram **or** zswap measured
- [ ] PSI, swap, CPU, latency and throughput compared
- [ ] Decision documented: keep, resize or buy

## Sources

- [Linux kernel: Pressure Stall Information](https://docs.kernel.org/accounting/psi.html)
- [Linux kernel: virtual-memory sysctls](https://docs.kernel.org/admin-guide/sysctl/vm.html)
- [Linux kernel: Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)
