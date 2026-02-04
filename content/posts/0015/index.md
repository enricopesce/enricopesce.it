---
title: "Stop OCI VM instance"
description: "Gracefully stop OCI instances from within using instance metadata and principal authentication. Simple bash alias included."
date: 2024-12-09T18:00:00+01:00
draft: false
cover:
  alt: "Stop OCI VM instance"
  caption: "Stop OCI VM instance"
  relative: true
  image: "static/switch.webp"    
keywords:
- "oci instance principal"
- "stop vm oracle cloud"
- "oci metadata api"
- "oci cli instance action"
---

# A Practical Guide to Graceful Stop an OCI Instance

## Introduction
When running workloads on Oracle Cloud Infrastructure (OCI), managing your instances efficiently is crucial. This guide will show you how to create a simple, efficient way to shut down your OCI instance from within the instance itself, using instance metadata and instance principal authentication.

## Prerequisites
- An OCI instance with instance principal authentication enabled
- OCI CLI installed on your instance
- Basic understanding of command-line operations

## Understanding the Components

### Instance Metadata
Every OCI instance has access to its own metadata through a local endpoint. This metadata includes crucial information like:
- Instance OCID (Oracle Cloud Identifier)
- Region
- Compartment ID
- Availability Domain

You can access this information without any authentication when querying from within the instance itself:
```bash
curl http://169.254.169.254/opc/v1/instance/id
curl http://169.254.169.254/opc/v1/instance/region
```

### Instance Principal Authentication
Instance Principal is a secure way to authenticate OCI API calls without managing configuration files or API keys. When enabled, your instance can make API calls using its own identity.

## The Basic Command
Here's the basic command to perform a graceful shutdown:
```bash
oci compute instance action \
    --action SOFTSTOP \
    --instance-id $(curl -s http://169.254.169.254/opc/v1/instance/id) \
    --auth instance_principal \
    --region $(curl -s http://169.254.169.254/opc/v1/instance/region)
```

Let's break down what each part does:
- `oci compute instance action`: The base command for instance operations
- `--action SOFTSTOP`: Specifies a graceful shutdown
- `--instance-id $(...)`: Gets the current instance's ID from metadata
- `--auth instance_principal`: Uses the instance's identity for authentication
- `--region $(...)`: Gets the current region from metadata

## Making Life Easier with an Alias
To simplify this process, you can create an alias. Here's how:

1. Open your shell configuration file:
```bash
nano ~/.bashrc  # for bash users
# or
nano ~/.zshrc   # for zsh users
```

2. Add the alias:
```bash
alias ocishutdown='oci compute instance action \
    --action SOFTSTOP \
    --instance-id $(curl -s http://169.254.169.254/opc/v1/instance/id) \
    --auth instance_principal \
    --region $(curl -s http://169.254.169.254/opc/v1/instance/region)'
```

3. Reload your configuration:
```bash
source ~/.bashrc  # for bash
# or
source ~/.zshrc   # for zsh
```

Now you can simply type `ocishutdown` to gracefully stop your instance!

## Conclusion
By leveraging instance metadata and instance principal authentication, you can create efficient, secure ways to manage your OCI instances. This approach eliminates the need for storing credentials and simplifies instance management tasks.

Remember that while this guide focuses on shutdown operations, the same principles apply to other instance management tasks like start, reset, or even gathering instance information. Feel free to adapt these examples for your specific needs.