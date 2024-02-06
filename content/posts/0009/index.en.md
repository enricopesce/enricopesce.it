---
title: Data Backup on OCI with Kopia.io
date: 2024-02-06T13:00:00+01:00
draft: false
tags:
  - backup
  - object storage
categories:
  - storage
cover:
  alt: Data Backup on OCI with Kopia.io
  caption: Data Backup on OCI with Kopia.io
  relative: true
  image: "static/home.png"
---

I often receive questions about data backup on OCI that includes hybrid systems. Recently, I tested [Kopia.io](kopia.io) and its compatibility with OCI.

Given the success of my tests, I want to share what I've achieved with you.

From the tests, I had no issues integrating it with our Object Storage using the [S3-compatible API](https://docs.oracle.com/en-us/iaas/Content/Object/Tasks/s3compatibleapi.htm).

The object storage service has various [endpoints](https://docs.oracle.com/en-us/iaas/Content/Object/Concepts/dedicatedendpoints.htm) that allow leveraging the service by emulating different types of APIs. Currently supported are:

- Native
- S3-compatible
- Swift (OpenStack Object Storage)
- PARs (Pre-Authenticated Requests)

Kopia supports various storage treated as [repositories](https://kopia.io/docs/repositories/), including many existing cloud services. Additionally, you can privately manage a repository through a [Kopia Repository Server](https://kopia.io/docs/repository-server/), not using public cloud services but, for example, a private VM.

In my test, I wanted to try OCI Object Storage. Here's the [installation guide](https://kopia.io/docs/installation/) for Kopia.

Once installed, I followed the simple [getting-started](https://kopia.io/docs/getting-started/).

You essentially need these OCI details to create an S3 repository on Kopia:

- Bucket namespace
- Region name

These form the complete endpoint address of S3-compatible APIs:

**{bucketnamespace}.compat.objectstorage.{region}.oraclecloud.com**

Additionally, you'll need:

- Bucket name
- User with access rights and [customer access and secret key](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingcredentials.htm#Working2)

The command, once you have the information, would look like this (keys are masked):

```console
enrico.pesce@enrico ~ % kopia repository create s3 \
  --bucket=backup \
  --region=eu-frankfurt-1 \
  --endpoint=frddomvd8z4q.compat.objectstorage.eu-frankfurt-1.oraclecloud.com \
  --access-key=3fdsfdsfdsfsdf4543gtfreterter \
  --secret-access-key=dsdsadsadsadasdasdasdau7LF/KEjKZDhb8Q=
```

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

If everything went well, as in this case, you can decide to connect to the repository to use it:

```console
enrico.pesce@enrico ~ % kopia repository connect s3 \
  --bucket=backup \
  --region=eu-frankfurt-1 \
  --endpoint=frddomvd8z4q.compat.objectstorage.eu-frankfurt-1.oraclecloud.com \
  --access-key=3fdsfdsfdsfsdf4543gtfreterter \
  --secret-access-key=dsdsadsadsadasdasdasdau7LF/KEjKZDhb8Q=
```

To check some information, including a useful snippet for reconnecting without using clear credentials:

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

Now you have a repository to store your data with Kopia. For example, you can create a backup of a folder with this simple command using default settings:

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

If you're not a fan of the console, I recommend using a simple and convenient GUI, [KopiaUI](https://github.com/kopia/kopia/releases/tag/v0.15.0), which is very intuitive and easy to use. Here are some screenshots:

where you can check the protected folders
![List of snapshots](static/home.png "List of snapshots")
view all backup iterations over time with convenient color-coded tags
![Snapshot details](static/snapshots.png "Snapshot details")
the list of protected files
![List of protected files](static/files.png "List of files")
file restoration is very simple
![File restoration](static/filesripristino.png "File restoration")
policy configuration is very comprehensive and granular
![Policy configuration](static/policy.png "Policy configuration")

Now you just need to try Kopia and test it on OCI!
