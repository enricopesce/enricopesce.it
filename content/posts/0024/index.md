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

## In brief

With contract DRAM more than four times its Q3 2025 level, **zram and zswap can defer an upgrade**, but they do not create free memory. They spend CPU cycles compressing cold pages and work best when data is compressible and the processor has headroom.

This is [part 2 of the series]({{< relref "/posts/0023/index.md" >}}). The key rule is: **choose zram or zswap deliberately** instead of stacking mechanisms without measurement.

## Zram, zswap and disk swap

| Mechanism | Page destination | Advantage | Constraint |
|---|---|---|---|
| Disk swap | SSD/NVMe | capacity and peak protection | latency and writes |
| zram | compressed RAM block device | fast, no disk I/O | consumes RAM and CPU, no implicit fallback |
| zswap | compressed cache in front of swap | reduces I/O and can evict to disk | needs backing swap and more monitoring |

Inventory the current system first:

```bash
swapon --show --output=NAME,TYPE,SIZE,USED,PRIO
zramctl
cat /sys/module/zswap/parameters/enabled 2>/dev/null || true
cat /proc/sys/vm/swappiness
```

Many distributions already configure one mechanism. Identify it before creating a competing compressed swap.

## Profile A: zram on a small host

For a non-persistent maintenance-window test:

```bash
sudo modprobe zram
sudo zramctl /dev/zram0 --algorithm zstd --size 8G
sudo mkswap /dev/zram0
sudo swapon --priority 100 /dev/zram0
```

Replace `8G` with **50–100% of physical RAM** as a starting hypothesis. Virtual size is not preallocated RAM, but memory consumption grows with stored pages. Kernel documentation notes little value above 2× RAM when assuming a 2:1 ratio.

Check supported algorithms:

```bash
cat /sys/block/zram0/comp_algorithm
```

`lz4` favors speed and latency; `zstd` often favors ratio. Benchmark your data. To remove the test, first ensure enough free memory exists to page everything back in:

```bash
sudo swapoff /dev/zram0
sudo zramctl --reset /dev/zram0
```

Persistence is distribution-specific. Use the system's packaged zram generator or service with the size, algorithm and priority you validated; do not create a second service if one exists.

## Profile B: zswap with disk fallback

Zswap compresses pages entering swap in a dynamic pool, then may evict them to its backing device when full. Confirm real swap exists:

```bash
swapon --show
```

Runtime test:

```bash
echo 1 | sudo tee /sys/module/zswap/parameters/enabled
cat /sys/module/zswap/parameters/compressor
cat /sys/module/zswap/parameters/max_pool_percent
```

For boot-time activation, add this through your distribution's kernel-command-line mechanism:

```text
zswap.enabled=1 zswap.compressor=zstd zswap.max_pool_percent=20
```

Twenty percent is a conservative baseline. A larger pool can retain cold pages that would be better evicted to NVMe so active work can use the RAM.

## Swappiness: do not copy the lowest number

`vm.swappiness` represents the relative cost of swap and filesystem paging on a 0–200 scale. Zero does not fully disable swap and can postpone it until pressure is severe. Kernel documentation says **values above 100 can make sense for in-memory swap**.

Start a zram test with:

```bash
sudo sysctl vm.swappiness=100
```

If PSI stays low and CPU has headroom, compare 100 with 133. For disk-only swap, treat 10, 30 or 60 as benchmark hypotheses, not universal recipes.

Persist the winning value:

```bash
echo 'vm.swappiness=100' | sudo tee /etc/sysctl.d/80-memory-tuning.conf
sudo sysctl --system
```

## Prove compression is worthwhile

For zram:

```bash
zramctl
cat /sys/block/zram0/mm_stat
```

Compare original data, compressed data and total memory actually used. An 8 GiB virtual device containing 4 GiB of pages is not 8 GiB saved.

For zswap:

```bash
sudo grep -H . /sys/kernel/debug/zswap/{stored_pages,pool_total_size,written_back_pages} 2>/dev/null
```

Debugfs may not be mounted. In both cases also record:

```bash
vmstat 1
cat /proc/pressure/memory
```

The tuning succeeds when PSI stalls and swap I/O fall without saturating CPU or worsening application latency. Poor compression, higher CPU or persistent `full` PSI means the active set needs real RAM or application limits.

## Mistakes to avoid

- Enabling zram and zswap together without a specific design and benchmark.
- Sizing zram from virtual capacity alone.
- Setting `swappiness=0` to “protect” performance.
- Running `swapoff` under pressure; it can cause OOM.
- Treating swap as a memory-leak fix.
- Changing production settings without a rollback.

[Part 3]({{< relref "/posts/0025/index.md" >}}) stops one service from consuming the whole host using systemd and cgroup v2.

## Sources

- [Linux kernel: zram](https://docs.kernel.org/admin-guide/blockdev/zram.html)
- [Linux kernel: zswap](https://docs.kernel.org/admin-guide/mm/zswap.html)
- [Linux kernel: `vm.swappiness`](https://docs.kernel.org/admin-guide/sysctl/vm.html#swappiness)
