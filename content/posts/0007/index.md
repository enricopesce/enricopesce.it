---
title: Scalable and Serverless Data Ingestion with OCI Functions
description: "Build a scalable data pipeline: weather station CSV to Autonomous Database using OCI Functions, Object Storage, and Terraform."
date: 2023-10-20T19:00:00+01:00
lastmod: 2026-06-12T00:00:00+00:00
draft: false
cover:
  alt: Scalable and Serverless Data Ingestion with OCI Functions
  caption: Scalable and Serverless Data Ingestion with OCI Functions
  relative: true
  image: "static/architecture.webp"
keywords:
- "oci data ingestion"
- "csv to autonomous database"
- "serverless etl oracle"
- "oci function pipeline"
tags:
- "OCI"
- "Functions"
- "Object Storage"
- "Autonomous Database"
- "Terraform"
categories:
- "Serverless"
faq:
  - question: "How do I build a serverless ETL pipeline on Oracle Cloud?"
    answer: "The standard OCI pattern uses Object Storage as the landing zone, an Event Rule to trigger an OCI Function on file upload, and the Function to parse and load data into Autonomous Database. Terraform provisions the full pipeline as infrastructure as code."
  - question: "Can OCI Functions process large CSV files from Object Storage?"
    answer: "Yes. OCI Functions can download objects directly from Object Storage using the OCI Python SDK, parse CSV data with pandas or the standard csv module, and insert rows into Autonomous Database. For very large files, consider chunking or using OCI Data Integration instead."
  - question: "Is a serverless data ingestion pipeline on OCI cost-effective?"
    answer: "Yes. With OCI Functions you pay only for actual execution time. Object Storage charges are minimal for typical CSV workloads. For intermittent or batch ingestion patterns, this approach is significantly cheaper than a continuously running VM or managed ETL service."
related:
- "/posts/0004"
- "/posts/0006"
- "/posts/0009"
---

In this article, we will leverage OCI's capabilities to the fullest, embracing the following principles:

* Scalability
* Resilience
* Flexibility
* Security
* Automation

The "loadfileintoadw" project is located in the same GitHub repository used so far to discuss OCI Function [fn-examples](https://github.com/enricopesce/fn-examples/tree/main/loadfileintoadw).

This example will help you understand how to integrate multiple OCI services and make the most of the cloud provider.

We will simulate a series of weather stations that will write a CSV file with sampling data (temperature, humidity, etc.). The sensor will automatically upload the file to an Object Storage bucket.

Processing will be automatically invoked through a [Function](https://github.com/enricopesce/fn-examples/blob/main/loadfileintoadw/func.py) that, in this case, converts the file format from CSV to JSON and natively saves it to a serverless Autonomous Database.

The [IaC](https://github.com/enricopesce/fn-examples/blob/main/loadfileintoadw/infrastructure.tf) code has been developed to perform the entire deployment, from infrastructure to function. Therefore, within the project folder, simply execute the command to create everything:

```console
terraform apply
```

If you are not familiar with Terraform, we recommend checking the[official documentation](https://registry.terraform.io/providers/oracle/oci/latest/docs) and our [tutorial](https://docs.oracle.com/en-us/iaas/Content/dev/terraform/tutorials/tf-simple-infrastructure.htm) and [video](https://www.youtube.com/watch?v=MjmikFgvKvI)
