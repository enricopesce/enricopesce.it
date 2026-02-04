---
title: Comparing CPU Multicore Performance of OCI Compute Standard Flex Shapes
description: "Geekbench 6 multicore benchmarks for OCI shapes: AMD EPYC E5, Intel Xeon, and ARM Ampere. Performance and cost analysis included."
date: 2024-03-19T18:00:00+01:00
draft: false
cover:
  alt: Comparing CPU Multicore Performance of OCI Compute Standard Flex Shapes
  caption: Comparing CPU Multicore Performance of OCI Compute Standard Flex Shapes
  relative: true
  image: "static/logo.webp"
keywords:
- "geekbench oci shapes"
- "oci multicore benchmark"
- "arm vs x86 oracle cloud"
- "oci compute cost performance"
---

When selecting a compute instance, factors such as raw computational power, price-to-performance ratio, and workload optimization play a significant role. 

The following standard flex shapes available in most OCI regions are:

* **VM.Standard.E4.Flex** (Processor: AMD EPYC 7J13. Base frequency 2.55 GHz, max boost frequency 3.5 GHz)
* **VM.Standard.E5.Flex** (Processor: AMD EPYC 9J14. Base frequency 2.4 GHz, max boost frequency 3.7 GHz)
* **VM.Standard3.Flex** (Processor: Intel Xeon Platinum 8358. Base frequency 2.6 GHz, max turbo frequency 3.4 GHz)
* **VM.Optimized3.Flex** (Processor: Intel Xeon 6354. Base frequency 3.0 GHz, max turbo frequency 3.6 GHz)
* **VM.Standard.A1.Flex** (Each OCPU corresponds to a single hardware execution thread. Processor: Ampere Altra Q80-30. Max frequency 3.0 GHz.)

In this article: [Performance testing with PHP and OCI Compute instances]({{< relref "/posts/0008/index.md" >}}) I have tested a single PHP thread/cpu execution over all OCI standard flex shapes, now I conducted multicore benchmark tests with **Geekbench 6** using 2, 4 and 8 CPU.

For additional information on the [internal tests conducted](https://www.geekbench.com/doc/geekbench6-benchmark-internals.pdf), please refer to the provided link.

### **Performance Comparison**

Let's explore the results in multi-threaded performance test over different shapes:

{{< plotly "//plotly.com/~enricopesce/1.embed" >}}

We can see that the most powerful shape is the VM.Standard.E5.Flex. 

This new AMD-based shape significantly surpasses other shapes, a very powerful CPU for best-in-class performance needs!

But we can evaluate not only the performance; in the real world, price-to-performance is another decisive factor.

### **Cost Comparison (Monthly Pricing )**

Let's break down the monthly costs for each shape with 8 CPU and Oracle Linux based on Oracle's pricing as of March 2024:

We can observe that there are varying prices; not all shapes have the same cost. 

| **Shape**           | **Multicore score** | **Monthly price** | **Saving** |
|---------------------|---------------------|-------------------|------------|
| VM.Standard.A1.Flex | 6275                |  $59,52           | 0%         |
| VM.Standard.E4.Flex | 6266                |  $74,40           | 20%        |
| VM.Standard.E5.Flex | 8335                |  $89,28           | 33%        |
| VM.Standard3.Flex   | 5925                |  $119,04          | 50%        |
| VM.Optimized3.Flex  | 6365                |  $149,45          | 60%        |

In this table, I added a "Saving" column to represent the cost difference (in percent) compared with VM.Standard.A1.Flex than all other shapes.

### **Considerations**

If you consider the ARM shape VM.Standard.A1.Flex, you can save 60% than VM.Optimized3.Flex with very similar performance results! Awesome!! 

If performance is the main focus VM.Standard.E5.Flex is the winner! A good price and stunning performance results!

ARM architecture is not only for mobile and low watt devices, ARM processor is a real alternative of the classic x86 server CPU, please read [What is Arm?](https://www.oracle.com/hk/cloud/compute/arm/what-is-arm/) page on OCI site to best understand the benefits of OCI A1 shapes!

Remember, the right shape depends on your unique use case.

### **Detailed results**

If you want to deep dive to **Geekbench 6** tests and results excuted by me, below a table with the relative tests executed:

| **SHAPE**           | **CPU Type**                                 | **Geekbench browser**                        |
|---------------------|----------------------------------------------|----------------------------------------------|
| VM.Optimized3.Flex  | Intel(R) Xeon(R) Gold 6354 CPU @ 3.00GHz     | https://browser.geekbench.com/v6/cpu/4837669 |
| VM.Standard.A1.Flex | Neoverse-N1 BIOS virt-4.2                    | https://browser.geekbench.com/v6/cpu/4837683 |
| VM.Standard.E4.Flex | AMD EPYC 7J13 64-Core Processor              | https://browser.geekbench.com/v6/cpu/4837682 |
| VM.Standard.E5.Flex | AMD EPYC 9J14 96-Core Processor              | https://browser.geekbench.com/v6/cpu/4837947 |
| VM.Standard3.Flex   | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | https://browser.geekbench.com/v6/cpu/4837679 |

Happy computing!