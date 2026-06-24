---
title: "Backup Kopia OCI: setup S3"
description: "Crea un repository Kopia cifrato su OCI Object Storage usando API compatibile S3, snapshot, policy e workflow di restore."
date: 2024-02-06T13:00:00+01:00
lastmod: 2026-06-03T00:00:00+00:00
slug: "come-fare-backup-dei-dati-in-10-minuti-con-kopia-e-oci"
draft: false
cover:
  alt: Backup Kopia OCI setup S3
  caption: Backup Kopia OCI setup S3
  relative: true
  image: "static/home.webp"
keywords:
- "kopia oci object storage"
- "backup compatibile s3 oracle"
- "backup cloud cifrato"
- "kopia tutorial"
- "kopia backup"
- "kopia repository"
- "kopia encryption"
- "kopia backup features"
- "backup oci object storage"
tags:
- "OCI"
- "Object Storage"
- "Kopia"
- "Backup"
categories:
- "Backup e Storage"
faq:
  - question: "Cos'è Kopia?"
    answer: "Kopia è uno strumento di backup open-source che crea snapshot cifrati, compressi e deduplicati dei tuoi dati. Supporta molti backend di storage inclusi i servizi compatibili S3, rendendo OCI Object Storage una scelta naturale."
  - question: "OCI Object Storage è compatibile con l'API S3?"
    answer: "Sì. OCI Object Storage fornisce un'API compatibile S3 accessibile tramite un endpoint regionale. È necessario creare una Customer Secret Key per la compatibilità S3 dalla console OCI e usarla al posto delle credenziali AWS."
  - question: "Come Kopia cifra i backup archiviati su OCI Object Storage?"
    answer: "Kopia cifra i dati lato client prima dell'upload. Si sceglie una password durante l'inizializzazione del repository, e Kopia la usa per derivare le chiavi di cifratura. Il backend di storage non vede mai i dati non cifrati."
---

Kopia puo' usare **OCI Object Storage** come backend compatibile S3 per backup cifrati, deduplicati e compressi. L'obiettivo pratico di questa guida e' semplice: creare un repository Kopia su OCI, validarlo, eseguire il primo snapshot e sapere come riconnettersi o ripristinare dati in seguito.

## Setup rapido

| Step | Cosa serve |
|------|------------|
| 1. Creare un bucket OCI | Nome bucket, namespace e regione. |
| 2. Abilitare accesso S3-compatible | Customer access key e secret key per l'utente OCI. |
| 3. Creare il repository Kopia | `kopia repository create s3` con endpoint S3 OCI. |
| 4. Validare il repository | `kopia repository validate-provider`. |
| 5. Creare snapshot | `kopia snapshot create <path>`. |

## Perche' Kopia e OCI Object Storage

OCI Object Storage e' utile per un repository Kopia perche' offre:

- Accesso compatibile S3, quindi Kopia puo' usare il tipo repository `s3`.
- Modello con namespace e bucket dedicati per isolare i dati di backup.
- Piu' storage tier: Standard, Infrequent Access e Archive. Per un repository Kopia attivo, parti da Standard o Infrequent Access; usa Archive solo quando il processo di restore gestisce il recupero degli oggetti prima dell'accesso. Vedi la [documentazione Oracle sugli Object Storage tiers](https://docs.oracle.com/en-us/iaas/Content/Object/Concepts/understandingstoragetiers.htm).
- Policy IAM e customer secret key, cosi' l'accesso puo' essere limitato al bucket usato per i backup.

[Kopia](https://kopia.io/docs/) e' uno strumento di backup e restore con caratteristiche importanti per repository cloud:

- Cifratura lato client prima che i dati lascino la macchina.
- Deduplicazione, cosi' blocchi ripetuti vengono archiviati una sola volta.
- Compressione, per ridurre dati trasferiti e archiviati.
- Policy di retention per piani hourly, daily, weekly, monthly o custom.
- Modalita' CLI, GUI e server, a seconda del modo in cui vuoi gestirlo.

In questa implementazione ho usato la documentazione Kopia:

- [guida di installazione](https://kopia.io/docs/installation/)
- [guida getting started](https://kopia.io/docs/getting-started/)
- [reference del comando repository create s3](https://kopia.io/docs/reference/command-line/common/repository-create-s3/)

## Dettagli OCI richiesti da Kopia

Per creare un repository S3 con Kopia ti servono questi dettagli OCI:

- Bucket namespace
- Nome della regione

Questi dati compongono l'endpoint completo delle API compatibili S3:

**{bucketnamespace}.compat.objectstorage.{region}.oraclecloud.com**

Inoltre ti servono:

- Nome del bucket
- Utente con permessi e [customer access/secret key](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingcredentials.htm#Working2)

## Creare il repository Kopia S3

Una volta raccolte le informazioni, il comando sara' simile a questo. Le chiavi sono mascherate:

```console
enrico.pesce@enrico ~ % kopia repository create s3 \
  --bucket=backup \
  --region=eu-frankfurt-1 \
  --endpoint=frddomvd8z4q.compat.objectstorage.eu-frankfurt-1.oraclecloud.com \
  --access-key=3fdsfdsfdsfsdf4543gtfreterter \
  --secret-access-key=dsdsadsadsadasdasdasdau7LF/KEjKZDhb8Q=
```

Durante la creazione Kopia chiede una password del repository. Conservala fuori dal repository e fuori da OCI Object Storage: senza quella password non puoi decifrare il contenuto del backup.

Se vuoi testare Object Storage e la compatibilita', puoi eseguire un test che effettua operazioni I/O nel repository:

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

## Riconnettersi al repository Kopia

Per collegarti al repository:

```console
enrico.pesce@enrico ~ % kopia repository connect s3 \
  --bucket=backup \
  --region=eu-frankfurt-1 \
  --endpoint=frddomvd8z4q.compat.objectstorage.eu-frankfurt-1.oraclecloud.com \
  --access-key=3fdsfdsfdsfsdf4543gtfreterter \
  --secret-access-key=dsdsadsadsadasdasdasdau7LF/KEjKZDhb8Q=
```

Per controllare le informazioni del repository, incluso uno snippet utile per riconnettersi senza scrivere credenziali in chiaro nella command line:

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

Ora hai un repository pronto per archiviare i tuoi dati con Kopia.

## Creare il primo snapshot

Per esempio puoi creare un backup della cartella Downloads con questo semplice comando usando le impostazioni predefinite:

```console
enrico.pesce@enrico ~ % kopia snapshot create $HOME/Downloads
Snapshotting enrico.pesce@enrico:/Users/enrico.pesce/Downloads ...
 * 0 hashing, 0 hashed (0 B), 5175 cached (14 GB), uploaded 202 B, estimating...
Created snapshot with root k24214076e958e761485b2af904f03b0b and ID de70da14f1c0264b3cbc4016dee67a7f in 0s
```

Completata la copia, puoi gia' elencare gli snapshot creati. Nel mio caso, dopo alcuni giorni:

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

## Restore e retention di base

Un backup e' utile solo se il restore e' stato testato. Kopia puo' ripristinare un file o una directory da uno snapshot con:

```console
kopia snapshot restore <snapshot-id> ./restore-test
```

Esegui un piccolo test di restore dopo aver creato il repository, poi programma controlli periodici. Questo fa emergere problemi di accesso al repository, password, lifecycle e retention prima di un incidente.

Per la retention, configura le policy invece di affidarti alla pulizia manuale. Le policy Kopia permettono di controllare frequenza degli snapshot, finestre di retention e impostazioni di compressione per ogni percorso protetto.

## Screenshot KopiaUI

Se non ami la console, ti consiglio la GUI semplice e comoda [KopiaUI](https://github.com/kopia/kopia/releases), intuitiva da usare. Ecco alcuni screenshot:

dove puoi controllare le cartelle protette:
![Lista snapshot](static/home.webp "Lista snapshot")

vedere tutte le iterazioni di backup nel tempo con tag colorati:
![Dettagli snapshot](static/snapshots.webp "Dettagli snapshot")

la lista dei file protetti:
![Lista file protetti](static/files.webp "Lista file")

il ripristino dei file e' molto semplice:
![Ripristino file](static/filesripristino.webp "Ripristino file")

la configurazione delle policy e' completa e granulare:
![Configurazione policy](static/policy.webp "Configurazione policy")

## Checklist di troubleshooting

- Se la creazione del repository fallisce, verifica il formato dell'endpoint OCI: `{bucketnamespace}.compat.objectstorage.{region}.oraclecloud.com`.
- Se l'autenticazione fallisce, controlla customer access key e secret key, non la normale API key OCI.
- Se la validazione fallisce, conferma che l'utente possa elencare, leggere e scrivere oggetti nel bucket target.
- Se i restore sono lenti o falliscono, controlla se regole lifecycle hanno spostato oggetti del repository in Archive.
- Se lo storage cresce piu' del previsto, rivedi compressione, retention degli snapshot ed eventuali file generati da escludere.

Ora puoi usare Kopia con OCI Object Storage e testare sia backup sia restore prima di affidarti al repository.
