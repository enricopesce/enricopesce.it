---
title: "OCI Compute Standard Flex Shapes: Another CPU Multicore Benchmark"
description: "OCI compute price-performance analysis with Geekbench 6. Compare AMD, Intel, and ARM shapes for optimal cloud instance selection."
date: 2024-02-10T18:00:00+01:00
lastmod: 2026-06-12T00:00:00+00:00
slug: "another-cpu-multicore-performance-of-oci-compute-standard-flex-shapes"
draft: false
keywords:
- "oci flex shapes benchmark"
- "ampere a1 performance"
- "oracle cloud vm comparison"
- "oci price performance"
tags:
- "OCI"
- "Compute"
- "Ampere"
- "Geekbench"
- "Benchmarks"
categories:
- "Benchmarks"
faq:
  - question: "What are OCI Flex Shapes?"
    answer: "OCI Flex Shapes are compute instances where you independently configure the number of OCPUs and RAM rather than choosing a fixed size. Available shapes include VM.Standard.E4.Flex (AMD), VM.Standard.E5.Flex (AMD), VM.Standard3.Flex (Intel), VM.Optimized3.Flex (Intel), and VM.Standard.A1.Flex (ARM Ampere)."
  - question: "How does VM.Standard.E5.Flex compare to E4.Flex in multicore benchmarks?"
    answer: "In Geekbench 6 multicore tests, E5.Flex (AMD EPYC 9J14) outperforms E4.Flex (AMD EPYC 7J13) by approximately 20-30% at the same OCPU count. E5 also has a higher max boost frequency at 3.7 GHz versus 3.5 GHz for E4."
  - question: "Which OCI shape is best for multicore workloads?"
    answer: "For maximum raw multicore performance, VM.Standard.E5.Flex is the best x86 option. For the best price-per-core ratio, VM.Standard.A1.Flex (Ampere) is highly competitive, especially when workloads can utilize many cores simultaneously."
related:
- "/posts/0010"
- "/posts/0021"
- "/posts/0012"
---

When selecting a compute instance, factors such as raw computational power, price-to-performance ratio, and workload optimization play a significant role. Let's focus on the following standard flex shapes available in most OCI regions:

* **VM.Standard.E4.Flex** (Processor: AMD EPYC 7J13. Base frequency 2.55 GHz, max boost frequency 3.5 GHz)
* **VM.Standard.E5.Flex** (Processor: AMD EPYC 9J14. Base frequency 2.4 GHz, max boost frequency 3.7 GHz)
* **VM.Standard3.Flex** (Processor: Intel Xeon Platinum 8358. Base frequency 2.6 GHz, max turbo frequency 3.4 GHz)
* **VM.Optimized3.Flex** (Processor: Intel Xeon 6354. Base frequency 3.0 GHz, max turbo frequency 3.6 GHz)
* **VM.Standard.A1.Flex** (Each OCPU corresponds to a single hardware execution thread. Processor: Ampere Altra Q80-30. Max frequency 3.0 GHz.)

I conducted benchmark tests with **Geekbench 6** on three CPU configurations: 2, 4, and 8 cores.

For additional information on the [internal tests conducted](https://www.geekbench.com/doc/geekbench6-benchmark-internals.pdf), please refer to the provided link.

Let's explore the results in multi-threaded performance:

{{< plotly "//plotly.com/~enricopesce/7.embed" >}}

We can see that the most powerful shape is the VM.Standard.E5.Flex. This new AMD-based shape significantly surpasses other
shapes; in fact, the results are slightly similar.

But we can evaluate not only the performance; in the real world, price-to-performance is another decisive factor.

### **Cost Comparison (Monthly Pricing)**

Let's break down the approximate monthly costs for each shape based on Oracle's pricing as of February 2024:

{{< plotly "//plotly.com/~enricopesce/5.embed" >}}

We can observe that there are varying prices; not all shapes have the same cost. If we consider the Ampere ARM shape VM.Standard.A1.Flex, we can understand that similar performance can be achieved with 90% of the cost for VM.Optimized3.Flex or 75% for VM.Standard3.Flex.

### **Recommendations**

Choose your OCI compute instance wisely by weighing performance, cost, and workload requirements. Whether you're running databases, analytics, or AI workloads, understanding CPU multicore performance empowers informed decisions.

The right shape depends on your workload, performance target, and budget.
