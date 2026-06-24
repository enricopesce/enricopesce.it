---
title: "Kopia OCI Backup: S3 Setup Guide"
description: "Create an encrypted Kopia backup repository on OCI Object Storage using the S3-compatible API, snapshots, policies and restore workflow."
date: 2024-02-06T13:00:00+01:00
lastmod: 2026-06-03T00:00:00+00:00
slug: "how-to-backup-your-data-in-10-minutes-with-kopia-and-oci"
draft: false
cover:
  alt: Kopia OCI Backup S3 Setup
  caption: Kopia OCI Backup S3 Setup
  relative: true
  image: "static/home.webp"
keywords:
- "kopia oci object storage"
- "s3 compatible backup oracle"
- "encrypted cloud backup"
- "kopia tutorial"
- "kopia backup"
- "kopia repository"
- "kopia encryption"
- "kopia backup features"
- "oci object storage backup"
tags:
- "OCI"
- "Object Storage"
- "Kopia"
- "Backup"
categories:
- "Backup and Storage"
faq:
  - question: "What is Kopia?"
    answer: "Kopia is an open-source backup tool that creates encrypted, compressed, and deduplicated snapshots of your data. It supports many storage backends including S3-compatible services, making OCI Object Storage a natural fit."
  - question: "Is OCI Object Storage compatible with the S3 API?"
    answer: "Yes. OCI Object Storage provides an S3-compatible API accessible via a regional endpoint. You need to create an S3 compatibility Customer Secret Key from the OCI console and use it in place of AWS credentials."
  - question: "How does Kopia encrypt backups stored on OCI Object Storage?"
    answer: "Kopia encrypts data client-side before uploading. You choose a password during repository initialization, and Kopia uses it to derive encryption keys. The storage backend never sees unencrypted data."
---

Kopia can use **OCI Object Storage** as an S3-compatible backend for encrypted, deduplicated and compressed backups. The practical goal of this guide is simple: create a Kopia repository on OCI, validate it, run the first snapshot, and know how to reconnect or restore data later.

## Quick setup

| Step | What you need |
|------|---------------|
| 1. Create an OCI bucket | Bucket name, namespace and region. |
| 2. Enable S3-compatible access | Customer access key and secret key for the OCI user. |
| 3. Create the Kopia repository | `kopia repository create s3` with the OCI S3 endpoint. |
| 4. Validate the repository | `kopia repository validate-provider`. |
| 5. Create snapshots | `kopia snapshot create <path>`. |

## Why Kopia and OCI Object Storage

OCI Object Storage is useful for a Kopia backup repository because it provides:

- S3-compatible access, so Kopia can use the `s3` repository type.
- A dedicated namespace and bucket model for isolating backup data.
- Multiple storage tiers: Standard, Infrequent Access, and Archive. For an active Kopia repository, start with Standard or Infrequent Access; use Archive only when your restore process can handle object retrieval before access. See Oracle's [Object Storage tiers documentation](https://docs.oracle.com/en-us/iaas/Content/Object/Concepts/understandingstoragetiers.htm).
- IAM policies and customer secret keys, so access can be limited to the bucket used for backups.

[Kopia](https://kopia.io/docs/) is a backup and restore tool with features that matter for cloud repositories:

- Client-side encryption before data leaves the machine.
- Deduplication, so repeated file blocks are stored only once.
- Compression, which reduces transferred and stored data.
- Snapshot retention policies for hourly, daily, weekly, monthly or custom backup plans.
- CLI, GUI and server modes, depending on how you want to operate it.

For this implementation I used the Kopia documentation:

- [installation guide](https://kopia.io/docs/installation/)
- [getting-started guide](https://kopia.io/docs/getting-started/)
- [S3 repository command reference](https://kopia.io/docs/reference/command-line/common/repository-create-s3/)

## OCI details required by Kopia

You need these OCI details to create an S3 repository with Kopia:

- Bucket namespace
- Region name

These form the complete endpoint address of S3-compatible APIs:

**{bucketnamespace}.compat.objectstorage.{region}.oraclecloud.com**

Additionally, you'll need:

- Bucket name
- User with access rights and [customer access and secret key](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingcredentials.htm#Working2)

## Create the Kopia S3 repository

Once you have the information, the command looks like this. The keys are masked:

```console
enrico.pesce@enrico ~ % kopia repository create s3 \
  --bucket=backup \
  --region=eu-frankfurt-1 \
  --endpoint=frddomvd8z4q.compat.objectstorage.eu-frankfurt-1.oraclecloud.com \
  --access-key=3fdsfdsfdsfsdf4543gtfreterter \
  --secret-access-key=dsdsadsadsadasdasdasdau7LF/KEjKZDhb8Q=
```

Kopia asks for a repository password during creation. Keep it outside the repository and outside OCI Object Storage: without that password you cannot decrypt the backup content.

If you want to test Object Storage and its compatibility, you can run a test that performs I/O operations in the repository:

```console
enrico.pesce@enrico ~ % kopia repository validate-provider
Opening 4 equivalent storage connections...
Validating storage capacity and usage
Validating blob list responses
Validating non-existent blob responses
Writing blob (5000000 bytes)
Validating conditional creates...
Validating list responses...
Validating partial reads...
Validating full reads...
Validating metadata...
Running concurrency test for 30s...
All good.
Cleaning up temporary data...
```

## Reconnect to the Kopia repository

To connect on the repository:

```console
enrico.pesce@enrico ~ % kopia repository connect s3 \
  --bucket=backup \
  --region=eu-frankfurt-1 \
  --endpoint=frddomvd8z4q.compat.objectstorage.eu-frankfurt-1.oraclecloud.com \
  --access-key=3fdsfdsfdsfsdf4543gtfreterter \
  --secret-access-key=dsdsadsadsadasdasdasdau7LF/KEjKZDhb8Q=
```

To check repository information, including a useful quick-reconnect snippet without writing clear credentials in the command line:

```console
enrico.pesce@enrico ~ % kopia repository status -t -s
Config file:         /Users/enrico.pesce/Library/Application Support/kopia/repository.config

Description:         Repository in S3: frddomvd8z4q.compat.objectstorage.eu-frankfurt-1.oraclecloud.com backup
Hostname:            enrico
Username:            enrico.pesce
Read-only:           false
Format blob cache:   15m0s

Storage type:        s3
Storage capacity:    unbounded
Storage config:      {
                       "bucket": "backup",
                       "endpoint": "frddomvd8z4q.compat.objectstorage.eu-frankfurt-1.oraclecloud.com",
                       "accessKeyID": ....

...To reconnect to the repository use:

$ kopia repository connect from-config --token eyJ2ZXJzaW9uIjoiMSIsInN0b3JhZ2UiOnsidHlwZSI6InMzIiwiY29uZmlnIjp7ImJ1Y2tldCI6ImJhY2t1cCIsImVuZHBvaW50IjoiZnJkZG9tdmQ4ejRxLmNvbXBhdC5vYmplY3RzdG9yYWdlLmVdsgfdsgdfsgfdsgo537hn9058jg9v-5869g5k89d-kf8946578bj06vfm056jvk0y458bnj908jg9v6k8fy989f658965jgy968jg94586b9k4869g84y6hgb8j69b8hj69hk8g95687h969bmtiomgufiunfbter
```

Now you have a ready repository to store your data with Kopia!

## Create the first snapshot

For example, you can create a folder backup with this simple command using default settings:

```console
enrico.pesce@enrico ~ % kopia snapshot create $HOME/Downloads
Snapshotting enrico.pesce@enrico:/Users/enrico.pesce/Downloads ...
 * 0 hashing, 0 hashed (0 B), 5175 cached (14 GB), uploaded 202 B, estimating...
Created snapshot with root k24214076e958e761485b2af904f03b0b and ID de70da14f1c0264b3cbc4016dee67a7f in 0s
```

Once the copy process is complete, you can already list the created snapshots, in my case after a few days:

```console
enrico.pesce@enrico ~ % kopia snapshot list $HOME/Downloads
enrico.pesce@enrico:/Users/enrico.pesce/Downloads
  2024-02-01 00:06:22 CET k081e4271a2db92d7eefe1ca035ff72c2 15.2 GB drwx------ files:11881 dirs:3150 (daily-5,monthly-2)
  2024-02-01 15:00:00 CET k5ed33706ce70d8984d89a8e8258a959f 15.2 GB drwx------ files:11882 dirs:3150 (latest-6..10,daily-4)
  + 4 identical snapshots until 2024-02-02 01:03:16 CET
  2024-02-02 13:31:20 CET k0db08b85d87ee5f366904d44eb149079 15.2 GB drwx------ files:11883 dirs:3150 (latest-5,daily-3,weekly-2)
  2024-02-05 11:52:21 CET k2e413b9843f14822438c57be23a1356a 15.2 GB drwx------ files:11895 dirs:3151 (latest-3..4,hourly-3..4,daily-2)
  + 1 identical snapshots until 2024-02-05 13:00:00 CET
  2024-02-06 10:46:14 CET k9eeba61e888e68e09ab26cd2aca07095 15.4 GB drwx------ files:11898 dirs:3158 (latest-1..2,hourly-1..2,daily-1,weekly-1,monthly-1,annual-1)
  + 1 identical snapshots until 2024-02-06 13:00:00 CET
```

## Restore and retention basics

Backups are only useful if restore is tested. Kopia can restore a file or directory from a snapshot with:

```console
kopia snapshot restore <snapshot-id> ./restore-test
```

Run a small restore test after creating the repository, then schedule periodic restore checks. This catches repository access, password, lifecycle and retention problems before an incident.

For retention, configure policies instead of relying on manual cleanup. Kopia policies let you control snapshot frequency, retention windows and compression settings for each protected path.

## KopiaUI screenshots

If you're not a fan of the console, I recommend using the simple and convenient GUI, [KopiaUI](https://github.com/kopia/kopia/releases), which is intuitive and easy to use. Here are some screenshots:

where you can check the protected folders
![List of snapshots](static/home.webp "List of snapshots")
view all backup iterations over time with convenient color-coded tags
![Snapshot details](static/snapshots.webp "Snapshot details")
the list of protected files
![List of protected files](static/files.webp "List of files")
file restoration is very simple
![File restoration](static/filesripristino.webp "File restoration")
policy configuration is very comprehensive and granular
![Policy configuration](static/policy.webp "Policy configuration")

## Troubleshooting checklist

- If repository creation fails, verify the OCI endpoint format: `{bucketnamespace}.compat.objectstorage.{region}.oraclecloud.com`.
- If authentication fails, check the customer access key and secret key, not the regular OCI API key.
- If validation fails, confirm that the user can list, read and write objects in the target bucket.
- If restores are slow or fail, check whether lifecycle rules moved repository objects to Archive.
- If storage grows faster than expected, review compression, snapshot retention and whether large generated files should be excluded.

Now you can use Kopia with OCI Object Storage and test both backup and restore before relying on it.
