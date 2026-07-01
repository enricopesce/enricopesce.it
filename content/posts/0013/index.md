---
title: "Get a Kubernetes Cluster in Minutes on OCI"
description: "Deploy production-ready OKE clusters in minutes with OKED. Automated Kubernetes setup on Oracle Cloud without OCI expertise."
date: 2024-09-15T18:00:00+01:00
lastmod: 2026-06-12T00:00:00+00:00
draft: false
slug: "get-a-kubernetes-cluster-in-minutes-on-oci"
cover:
  alt: "Get a Kubernetes cluster in minutes on OCI"
  caption: "Get a Kubernetes cluster in minutes on OCI"
  relative: true
  image: "static/logo.webp"
keywords:
- "oke terraform deploy"
- "oracle kubernetes engine"
- "oked automation"
- "oci kubernetes cluster"
tags:
- "OCI"
- "OKE"
- "Kubernetes"
- "Automation"
- "Terraform"
categories:
- "Kubernetes"
faq:
  - question: "What is Oracle Kubernetes Engine (OKE)?"
    answer: "OKE is Oracle Cloud Infrastructure's managed Kubernetes service. It provisions and manages the control plane, handles node upgrades, and integrates with OCI services like Load Balancer, Block Volume, and Container Registry. You pay only for worker nodes, not the control plane."
  - question: "Can I run OKE on the OCI Free Tier?"
    answer: "OKE control plane is free. Worker nodes use compute instances, which can be Always Free A1.Flex shapes (up to 4 OCPUs and 24 GB RAM combined). With Ampere nodes you can run a small but functional Kubernetes cluster at zero cost."
  - question: "What is OKED and how does it simplify OKE deployment?"
    answer: "OKED (Oracle Kubernetes Engine Deploy) is an open-source CLI tool that automates provisioning of a production-ready OKE cluster with best-practice defaults. It handles networking, IAM policies, node pools, and cluster add-ons, reducing deployment to a single command."
---

## My first OCI automation project

After 10 years of experience with DevOps practices, automation, infrastructure as code, and many customer discussions, I decided to build a tool that helps people deploy a well-defined Kubernetes architecture without needing deep infrastructure expertise.

### Oracle Kubernetes Engine Deploy project (OKED)

OKED helps you deploy a complete Kubernetes infrastructure on OCI, including the required network dependencies, without requiring OCI expertise.

This is the **Terraform** edition of OKED. If you prefer Python-based infrastructure as code instead, see the [Pulumi edition of OKED]({{< relref "/posts/0017/index.md" >}}).

The main requirements that motivated me to develop this project are as follows:

- **Simplicity**: Customers ask to be up and running in minutes without complex prompts or deep infrastructure expertise.
- **Working**: Most online examples available are complex to understand and some are non-functional.
- **Well-architected**: Customers want security best practices and sound design applied by default.

The main features that differentiate this tool from the OCI Console wizard and other Terraform projects are:

- Automatic creation of the VCN and the subnetting; you only need to define the supernet CIDR.
- Automatic discovery and configuration of all availability domains to spread nodes and improve availability.
- Automatic discovery and configuration of the latest, correct, and optimized OKE node image to use.
- Kubernetes config file generated and ready to use, for example with `export KUBECONFIG=$PWD/kubeconfig`.
- Code that can be extended as your OCI skills grow.

You can find all the information on the [GitHub project page](https://github.com/enricopesce/oracle-kubernetes-engine-deploy).

Here is a short demo:

![OKED deployment demo](static/demo.webp)
