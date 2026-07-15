---
title: "Zram, zswap and Linux Swap: A Practical Configuration Guide"
description: "How to choose and configure zram, zswap and Linux swap, tune swappiness, and measure compression, latency and paging."
date: 2026-07-17T09:00:00+00:00
lastmod: 2026-07-08T00:00:00+00:00
slug: "zram-zswap-linux-swap-configuration"
draft: false
cover:
  alt: "Configuring zram zswap and swap on Linux"
  caption: "Linux RAM series, part 2: compress cold pages"
  relative: true
  image: "static/linux-ram-part-2.svg"
  width: 1200
  height: 630
keywords: ["configure zram Linux", "zram vs zswap", "zram swappiness", "optimize Linux swap", "zswap Linux configuration", "Linux compressed memory"]
tags: ["Linux", "RAM", "zram", "zswap", "Swap"]
categories: ["Linux"]
inLanguage: "en"
isBasedOn:
- "https://docs.kernel.org/admin-guide/blockdev/zram.html"
- "https://docs.kernel.org/admin-guide/mm/zswap.html"
- "https://docs.kernel.org/admin-guide/sysctl/vm.html"
faq:
- question: "Is zram or zswap better on Linux?"
  answer: "Zram is a compressed swap device entirely in RAM; zswap is a compressed cache in front of a real swap device and can evict pages to disk. Zram is simple for desktops and small hosts, while zswap fits systems that also need disk fallback capacity."
- question: "What swappiness value should I use with zram?"
  answer: "Kernel documentation allows values above 100 for in-memory swap that is faster than filesystem I/O. A cautious starting point is 100-133, validated with PSI, vmstat and workload latency."
- question: "Does zram replace physical RAM?"
  answer: "No. It trades CPU cycles for compressing cold pages and absorbing peaks; incompressible data and active working sets still require physical RAM."
---

In [part 1 of this series]({{< relref "/posts/0023/index.md" >}}) I made the case for measuring memory pressure before spending money on RAM that now costs more than four times what it did a year ago. If your measurements showed short, compressible peaks — cold pages sitting around while the active working set fits fine — this is the post where compression earns its keep.

I want to be upfront about one thing, because "just enable zram" has become the reflexive advice in every forum thread about low memory: zram and zswap do not create free memory. They spend CPU cycles compressing pages you are not actively using. When the data compresses well and the CPU has headroom, that trade is excellent. When it doesn't, you've added a layer of complexity and gained nothing. So the goal here is not to enable everything — it's to pick one mechanism deliberately and prove it helps.

## Zram, zswap and disk swap: what actually differs

The names are confusingly similar, so here is the distinction that matters. Zram is a swap device that lives entirely in RAM: pages get compressed and stay in memory, no disk involved, no fallback. Zswap is a compressed cache *in front of* a real swap device: when its pool fills up, it evicts pages to disk.

| Mechanism | Page destination | Advantage | Constraint |
|---|---|---|---|
| Disk swap | SSD/NVMe | capacity and peak protection | latency and writes |
| zram | compressed RAM block device | fast, no disk I/O | consumes RAM and CPU, no implicit fallback |
| zswap | compressed cache in front of swap | reduces I/O and can evict to disk | needs backing swap and more monitoring |

In practice: zram fits desktops and small hosts where there is no swap device worth having. Zswap fits machines that already have swap on decent storage and want fewer disk writes and lower latency on the hot part of it.

## First, check what you already have

This is the step that gets skipped, and it's the one that causes the weirdest problems. Many distributions ship with one of these mechanisms already enabled — and if you add a second compressed swap on top without noticing, you end up with two layers competing for the same pages.

```bash
swapon --show --output=NAME,TYPE,SIZE,USED,PRIO
zramctl
cat /sys/module/zswap/parameters/enabled 2>/dev/null || true
cat /proc/sys/vm/swappiness
```

If something is already configured, work with it. Tune what's there instead of bolting a competitor next to it.

## Profile A: zram on a small host

Here is a non-persistent test you can run in a maintenance window and undo completely:

```bash
sudo modprobe zram
sudo zramctl /dev/zram0 --algorithm zstd --size 8G
sudo mkswap /dev/zram0
sudo swapon --priority 100 /dev/zram0
```

Replace `8G` with somewhere between 50% and 100% of physical RAM as a starting hypothesis — and treat it as exactly that, a hypothesis. The virtual size is not preallocated RAM; the device consumes memory as it receives pages. The kernel documentation notes there is little value going above 2× RAM if you assume a typical 2:1 compression ratio.

On the algorithm: `lz4` favors speed and low latency, `zstd` usually favors compression ratio. Which one wins depends on your data, not on someone else's benchmark. You can see what your kernel supports with:

```bash
cat /sys/block/zram0/comp_algorithm
```

To remove the test, make sure there is enough free memory to page everything back in first, then:

```bash
sudo swapoff /dev/zram0
sudo zramctl --reset /dev/zram0
```

Once you've validated a size, algorithm and priority, make it persistent using whatever zram generator or service your distribution packages — and resist the temptation to create a second service if one already exists.

## Profile B: zswap with disk fallback

Zswap compresses pages on their way to swap into a dynamic pool, and when the pool fills, it can write them out to the backing device. That means it needs real swap behind it — confirm that first:

```bash
swapon --show
```

For a runtime test:

```bash
echo 1 | sudo tee /sys/module/zswap/parameters/enabled
cat /sys/module/zswap/parameters/compressor
cat /sys/module/zswap/parameters/max_pool_percent
```

To make it active from boot, add this to the kernel command line through your distribution's mechanism:

```text
zswap.enabled=1 zswap.compressor=zstd zswap.max_pool_percent=20
```

Twenty percent is a conservative starting point, and bigger is not automatically better. A large pool can end up holding cold pages hostage in RAM when they would be better off evicted to NVMe, leaving the memory for work that actually needs it.

## Swappiness: stop copying the lowest number you can find

There is a whole folklore around `vm.swappiness`, most of it built on the idea that swap is bad and therefore the number should be low. What the parameter actually expresses is the relative cost of swapping versus filesystem paging, on a 0–200 scale. Setting it to zero doesn't disable swap — it postpones swapping until pressure is already severe, which is usually the worst possible moment.

The interesting part for this post: the kernel documentation explicitly says values *above* 100 can make sense when your swap is faster than filesystem I/O — which is exactly what in-memory compressed swap is. So for a zram test, start at:

```bash
sudo sysctl vm.swappiness=100
```

If PSI stays low and the CPU has headroom, compare 100 against 133 and see which your workload prefers. For plain disk swap, the traditional 10, 30 or 60 are benchmark hypotheses, not universal recipes.

When you have a winner, persist it:

```bash
echo 'vm.swappiness=100' | sudo tee /etc/sysctl.d/80-memory-tuning.conf
sudo sysctl --system
```

## Prove it's actually helping

This is the part that separates a tuned system from a system with extra moving parts. For zram:

```bash
zramctl
cat /sys/block/zram0/mm_stat
```

Compare original data, compressed data, and total memory actually used. An 8 GiB virtual device holding 4 GiB of pages is not 8 GiB saved — the real saving is the difference between what the pages would occupy uncompressed and what the device uses now.

For zswap:

```bash
sudo grep -H . /sys/kernel/debug/zswap/{stored_pages,pool_total_size,written_back_pages} 2>/dev/null
```

(Debugfs may not be mounted on your system.) In both cases, keep recording the same signals from part 1:

```bash
vmstat 1
cat /proc/pressure/memory
```

The tuning succeeded if PSI stalls and swap I/O go down without saturating the CPU or hurting application latency. If compression ratios are poor, CPU usage climbs, or `full` PSI stays high, the honest conclusion is that your active working set needs real RAM or application-level limits — not more compression.

## The mistakes that keep coming back

A few things I would flag in any review of a memory-tuning change:

- Enabling zram *and* zswap together without a specific design and a benchmark to justify it.
- Sizing zram by its virtual capacity, as if that were reserved savings.
- Setting `swappiness=0` to "protect" performance.
- Running `swapoff` on a host already under pressure — that can trigger the OOM killer directly.
- Treating swap as a fix for a memory leak.
- Changing production settings without writing down the rollback first.

Compression protects you from peaks, but it can't stop one badly behaved service from eating the whole host. That's a containment problem, and it's what [part 3](/limit-linux-service-ram-systemd-cgroup-v2/) solves with systemd and cgroup v2.

## Sources

- [Linux kernel: zram](https://docs.kernel.org/admin-guide/blockdev/zram.html)
- [Linux kernel: zswap](https://docs.kernel.org/admin-guide/mm/zswap.html)
- [Linux kernel: `vm.swappiness`](https://docs.kernel.org/admin-guide/sysctl/vm.html#swappiness)
