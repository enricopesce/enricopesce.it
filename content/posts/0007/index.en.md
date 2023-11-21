---
title: Scalable and Serverless Data Ingestion
date: 2023-10-20T19:00:00+01:00
draft: true
tags:
  - functions
categories:
  - serverless
cover:
  alt: Scalable and Serverless Data Ingestion
  caption: Scalable and Serverless Data Ingestion
  relative: true
---

In this article, we will leverage OCI's capabilities to the fullest, embracing the following principles:

* Scalability
* Resilience
* Flexibility
* Security
* Automation

The "loadfileintoadw" project is located in the same GitHub repository used so far to discuss OCI Function [fn-examples](https://github.com/enricopesce/fn-examples/tree/main/loadfileintoadw).

This example will help you understand how to integrate multiple OCI services and make the most of the cloud provider.

Below is the architectural design we will create.

![Project Architecture](https://github.com/enricopesce/fn-examples/blob/main/loadfileintoadw/architecture.png "Architecture")

We will simulate a series of weather stations that will write a CSV file with sampling data (temperature, humidity, etc.). The sensor will automatically upload the file to an Object Storage bucket.

Processing will be automatically invoked through a [Function](https://github.com/enricopesce/fn-examples/blob/main/loadfileintoadw/func.py) that, in this case, converts the file format from CSV to JSON and natively saves it to a serverless Autonomous Database.

The [IaC](https://github.com/enricopesce/fn-examples/blob/main/loadfileintoadw/infrastructure.tf) code has been developed to perform the entire deployment, from infrastructure to function. Therefore, within the project folder, simply execute the command to create everything:

```console
terraform apply
```

If you are not familiar with Terraform, we recommend checking the[official documentation](https://registry.terraform.io/providers/oracle/oci/latest/docs) and our [tutorial](https://docs.oracle.com/en-us/iaas/developer-tutorials/tutorials/tf-simple-infrastructure/01-summary.htm) and [video](https://www.youtube.com/watch?v=MjmikFgvKvI)
