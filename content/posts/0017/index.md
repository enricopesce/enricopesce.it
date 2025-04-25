---
title: "Deploy Oracle Kubernetes Engine Clusters in Minutes"
date: 2024-04-25T18:00:00+01:00
draft: false
cover:
  alt: "Deploy Oracle Kubernetes Engine Clusters in Minutes"
  caption: "Deploy Oracle Kubernetes Engine Clusters in Minutes"
  relative: true
  image: ""
keywords:
- "oci"
- "kubernetes"
- "pulumi"
---

# OKED: Deploy Oracle Kubernetes Engine Clusters in Minutes

In today's cloud-native landscape, Kubernetes has become the *de facto* standard for container orchestration. However, setting up a production-ready Kubernetes cluster can still be a complex and time-consuming process, especially for those new to the ecosystem. Enter **OKED** (*Oracle Kubernetes Engine Deploy*), an elegant solution that streamlines the deployment of Kubernetes clusters on Oracle Cloud Infrastructure.

![OKED Deployment Demo](https://github.com/enricopesce/oracle-kubernetes-engine-deploy/blob/main/demo.gif?raw=true)

## What is OKED?

OKED is an automated tool that simplifies the deployment of Oracle Kubernetes Engine (OKE) clusters. Built on the Pulumi framework, it enables users to have a fully functional Kubernetes environment up and running in minutes—without requiring extensive expertise in either OCI or Kubernetes.

> "Up and running in minutes without any prompt and OCI expertise."

The tool handles all aspects of cluster deployment, from infrastructure provisioning to network configuration, making it ideal for both beginners looking to experiment with Kubernetes and experienced developers seeking a reliable foundation for production deployments.

## Key Features

What makes OKED stand out from other deployment methods, including OCI's web console wizard?

* **Zero-Expertise Deployment**: Get a functioning cluster without deep knowledge of OCI or Kubernetes
* **Automatic VCN Creation**: Simply define a supernet CIDR, and OKED handles all subnet calculations
* **Multi-Availability Domain Configuration**: Automatic discovery and configuration of availability domains for maximum cluster resilience
* **Optimized Node Images**: Automatic selection of the latest and most optimized OKE node images
* **Ready-to-Use Configuration**: Generates a Kubernetes config file that works immediately with kubectl
* **Well-Architected Security**: Implements security best practices based on official OCI recommendations
* **Extensibility**: Built on Pulumi, making it easy to customize and extend for specific requirements

## The Architecture

OKED deploys a `BASIC` cluster type (which incurs no management fees) following the recommended architecture from [Oracle's documentation](https://docs.oracle.com/en-us/iaas/Content/ContEng/Concepts/contengnetworkconfigexample.htm#example-oci-cni-publick8sapi_privateworkers_publiclb). 

![OKED Architecture](https://github.com/enricopesce/oracle-kubernetes-engine-deploy/blob/main/arch.png?raw=true)

The deployed environment includes:

1. Public Kubernetes API endpoint with private worker nodes
2. Support for public load balancers
3. Proper network segmentation with security lists and route tables
4. High availability across multiple availability domains

What's particularly compelling is that with default settings, you can deploy a simple cluster leveraging **Oracle Cloud Free Tier** resources at **absolutely no cost**, utilizing the free ARM Ampere A1 Compute instances.

## Getting Started

Getting started with OKED requires minimal setup:

```bash
# Clone the repository
git clone https://github.com/enricopesce/oracle-kubernetes-engine-deploy.git
cd oracle-kubernetes-engine-deploy

# Set up environment
python -m venv .venv
source .venv/bin/activate
pip install poetry
pulumi install

# Configure and deploy
pulumi stack init testing
pulumi config set compartment_ocid "your-compartment-ocid"
pulumi up
```

Within 10-15 minutes, you'll have a fully operational Kubernetes cluster ready for your applications:

```bash
chmod 600 kubeconfig
export KUBECONFIG=$PWD/kubeconfig
kubectl get pods -A
```

## Why Choose OKED?

The creator of OKED developed this tool out of frustration with existing solutions, which were often complex to understand and sometimes non-functional. The project addresses three core requirements:

1. **Simplicity**: Deploy quickly without extensive knowledge or manual configuration
2. **Reliability**: Unlike many examples found online, OKED actually works as advertised
3. **Best Practices**: Follows Oracle's well-architected framework recommendations

For teams looking to quickly bootstrap Kubernetes environments on OCI—whether for development, testing, or production—OKED offers a streamlined path that removes much of the complexity and potential for error.

## Try It Today

Whether you're looking to experiment with Kubernetes on Oracle Cloud's Free Tier or deploy production-ready clusters, OKED provides an excellent starting point. The project is open-source and actively seeking feedback and contributions from the community.

You can find the complete project on GitHub at [github.com/enricopesce/oracle-kubernetes-engine-deploy](https://github.com/enricopesce/oracle-kubernetes-engine-deploy).

---

*Are you using Kubernetes on Oracle Cloud? What has your experience been with deployment automation tools? Share your thoughts in the comments below!*