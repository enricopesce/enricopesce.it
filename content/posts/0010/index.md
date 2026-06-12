---
title: "OCI Flex Shapes: E5 vs E4 vs A1"
description: "Geekbench 6 benchmark of OCI Compute Flex shapes: compare VM.Standard.E5, E4, A1, Standard3 and Optimized3 by score, cost and workload fit."
date: 2024-03-19T18:00:00+01:00
lastmod: 2026-06-03T00:00:00+00:00
slug: "comparing-cpu-multicore-performance-of-oci-compute-standard-flex-shapes"
draft: false
cover:
  alt: OCI Flex Shapes Benchmark
  caption: OCI Flex Shapes Benchmark
  relative: true
  image: "static/logo.webp"
keywords:
- "geekbench oci shapes"
- "oci multicore benchmark"
- "arm vs x86 oracle cloud"
- "oci compute cost performance"
- "oci shapes"
- "flex shapes"
- "vm.standard.e5.flex"
- "vm.standard.e4.flex"
- "vm.standard.a1.flex"
- "vm.standard3.flex"
tags:
- "OCI"
- "Compute"
- "Ampere"
- "Geekbench"
- "Benchmarks"
categories:
- "Benchmarks"
faq:
  - question: "What OCI Flex shapes are compared in the benchmark?"
    answer: "The benchmark compares VM.Standard.E5.Flex (AMD EPYC 9J14), VM.Standard.E4.Flex (AMD EPYC 7J13), VM.Standard.A1.Flex (Ampere Altra), VM.Standard3.Flex (Intel Xeon), and VM.Optimized3.Flex (Intel Xeon) using Geekbench 6."
  - question: "Which OCI shape has the best price-performance ratio?"
    answer: "VM.Standard.A1.Flex (Ampere) typically leads on price-performance due to its lower per-OCPU cost and competitive multicore scores. E5.Flex is the best x86 choice for raw performance. The optimal choice depends on your workload's single-thread vs. multicore requirements."
  - question: "Is Ampere A1 suitable for production workloads on OCI?"
    answer: "Yes. VM.Standard.A1.Flex is production-ready and is used for web servers, containerized workloads, and AI inference. Most modern software compiles and runs on ARM64 without changes. Always validate with your own workload benchmark before migrating."
---

If you are comparing **OCI Compute Flex shapes**, the short answer from this Geekbench 6 run is: **VM.Standard.E5.Flex** led in raw multicore performance, **VM.Standard.A1.Flex** was the strongest cost-conscious option, and the Intel-based shapes remained relevant when x86 compatibility is a hard requirement.

## Quick recommendation

| Goal | Start with | Why |
|------|------------|-----|
| Best multicore performance | **VM.Standard.E5.Flex** | Highest Geekbench 6 multicore score in this test. |
| Lowest cost with strong throughput | **VM.Standard.A1.Flex** | Similar score to E4/Optimized3 in this benchmark, with the lowest price in the table. |
| Existing x86 workload compatibility | **VM.Standard3.Flex** or **VM.Optimized3.Flex** | Useful when your software stack is tied to x86 packages, binaries, or vendor support. |
| Balanced AMD x86 option | **VM.Standard.E4.Flex** | Lower-cost x86 option, but behind E5 in this benchmark. |

This is a benchmark snapshot from March 2024. Use the numbers below to compare relative behavior, then verify current regional availability and pricing in the OCI Cost Estimator before making a production decision.

**2026 update:** OCI E6 Standard Compute is now available and changes the AMD x86 comparison. For the newer decision map, read [OCI E6 vs E5 vs E4: Compute Flex Shapes]({{< relref "/posts/0021/index.md" >}}).

## Tested OCI Compute shapes

The following standard flex shapes available in most OCI regions are:

* **VM.Standard.E4.Flex** (Processor: AMD EPYC 7J13. Base frequency 2.55 GHz, max boost frequency 3.5 GHz)
* **VM.Standard.E5.Flex** (Processor: AMD EPYC 9J14. Base frequency 2.4 GHz, max boost frequency 3.7 GHz)
* **VM.Standard3.Flex** (Processor: Intel Xeon Platinum 8358. Base frequency 2.6 GHz, max turbo frequency 3.4 GHz)
* **VM.Optimized3.Flex** (Processor: Intel Xeon 6354. Base frequency 3.0 GHz, max turbo frequency 3.6 GHz)
* **VM.Standard.A1.Flex** (Each OCPU corresponds to a single hardware execution thread. Processor: Ampere Altra Q80-30. Max frequency 3.0 GHz.)

In [Performance testing with PHP and OCI Compute instances]({{< relref "/posts/0008/index.md" >}}) I tested single-thread PHP execution across OCI Standard Flex shapes. In this article I focus on multicore behavior with **Geekbench 6**, using 2, 4 and 8 CPU configurations.

For additional information on the [Geekbench 6 internal tests](https://www.geekbench.com/doc/geekbench6-benchmark-internals.pdf), see the official benchmark documentation.

## Performance comparison

The chart below compares multi-threaded performance across the tested OCI Compute shapes:

{{< plotly "//plotly.com/~enricopesce/1.embed" >}}

The strongest result in this run is **VM.Standard.E5.Flex**.

The E5 AMD-based shape clearly separates itself from the other shapes in raw multicore score. That makes it the most direct choice when the application can use several CPU cores and performance is more important than minimizing the monthly bill.

The second important observation is that **VM.Standard.A1.Flex**, **VM.Standard.E4.Flex**, and **VM.Optimized3.Flex** are close enough in this run that price, architecture, and workload compatibility become decisive.

## Cost comparison

The table below uses the monthly price snapshot I collected in March 2024 for an 8 CPU Oracle Linux configuration. Treat it as a relative price-performance snapshot, not as current commercial pricing.

| **Shape**           | **Multicore score** | **Monthly price snapshot** | **A1 saving vs this shape** |
|---------------------|---------------------|----------------------------|-----------------------------|
| VM.Standard.A1.Flex | 6275                | $59.52                     | 0%                          |
| VM.Standard.E4.Flex | 6266                | $74.40                     | 20%                         |
| VM.Standard.E5.Flex | 8335                | $89.28                     | 33%                         |
| VM.Standard3.Flex   | 5925                | $119.04                    | 50%                         |
| VM.Optimized3.Flex  | 6365                | $149.45                    | 60%                         |

## How to choose between OCI shapes

Choose **VM.Standard.E5.Flex** when raw multicore CPU performance is the main requirement. In this benchmark it has the highest score and a strong price-performance position.

Choose **VM.Standard.A1.Flex** when you can run on ARM and want the lowest cost among the tested options. The benchmark score is close to E4 and Optimized3, while the monthly price snapshot is much lower.

Choose **VM.Standard3.Flex** or **VM.Optimized3.Flex** when x86 compatibility matters more than benchmark score. This can happen with commercial software, native packages, prebuilt images, or older dependencies.

Choose **VM.Standard.E4.Flex** when you need an AMD x86 shape and E5 is not required or not available for your target region and capacity plan.

ARM architecture is no longer only for mobile or low-power devices. For server workloads, ARM can be a practical alternative to classic x86 CPUs when your runtime, packages, container images, and observability stack support it. For more background, read Oracle's [What is Arm?](https://www.oracle.com/hk/cloud/compute/arm/what-is-arm/) page.

## Related benchmarks

Use this benchmark together with:

- [Performance testing with PHP and OCI Compute instances]({{< relref "/posts/0008/index.md" >}}), focused on PHP workloads.
- [OCI Compute Standard Flex Shapes: Another CPU Multicore Benchmark]({{< relref "/posts/0011/index.md" >}}), another multicore benchmark view.
- [Intel x86 vs. ARM Architecture: A Comparative Analysis for Server Technologies]({{< relref "/posts/0012/index.md" >}}), useful when the decision is mainly about architecture.
- [Generative AI: Efficient Inference on Cloud CPUs]({{< relref "/posts/0018/index.md" >}}), focused on CPU inference workloads.

## FAQ

### Which OCI Compute shape had the best Geekbench 6 multicore score?

**VM.Standard.E5.Flex** had the best score in this benchmark, with a multicore result of 8335 in the 8 CPU test.

### Is VM.Standard.A1.Flex a good low-cost option?

Yes, if your workload supports ARM. In this test, A1 was close to E4 and Optimized3 in multicore score while having the lowest monthly price snapshot.

### Should I choose ARM or x86 on OCI?

Choose ARM when your application stack is compatible and cost efficiency matters. Choose x86 when vendor support, binary compatibility, or existing deployment images require it.

## Detailed results

If you want to deep dive into the **Geekbench 6** runs, below is the table with the tests I executed:

| **SHAPE**           | **CPU Type**                                 | **Geekbench browser**                        |
|---------------------|----------------------------------------------|----------------------------------------------|
| VM.Optimized3.Flex  | Intel(R) Xeon(R) Gold 6354 CPU @ 3.00GHz     | https://browser.geekbench.com/v6/cpu/4837669 |
| VM.Standard.A1.Flex | Neoverse-N1 BIOS virt-4.2                    | https://browser.geekbench.com/v6/cpu/4837683 |
| VM.Standard.E4.Flex | AMD EPYC 7J13 64-Core Processor              | https://browser.geekbench.com/v6/cpu/4837682 |
| VM.Standard.E5.Flex | AMD EPYC 9J14 96-Core Processor              | https://browser.geekbench.com/v6/cpu/4837947 |
| VM.Standard3.Flex   | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | https://browser.geekbench.com/v6/cpu/4837679 |
