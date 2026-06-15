---
title: "OCI Vision: identificare cereali con un modello custom"
description: "Addestra e testa un modello custom di classificazione immagini con OCI Vision usando immagini etichettate e preprocessing leggero."
date: 2024-09-21T18:00:00+01:00
lastmod: 2026-06-12T00:00:00+00:00
draft: false
slug: "oci-vision-identificare-cereali-con-modello-custom"
cover:
  alt: "Workflow OCI Vision"
  caption: "Workflow OCI Vision"
  relative: true
  image: "static/diagram.avif"
  width: 1344
  height: 553
keywords:
- "oci vision custom model"
- "image classification oracle"
- "oracle ai vision"
- "data labeling oci"
tags:
- "OCI"
- "OCI Vision"
- "Computer Vision"
- "Machine Learning"
- "Data Labeling"
categories:
- "AI and Machine Learning"
faq:
  - question: "Cos'è OCI Vision?"
    answer: "OCI Vision è un servizio AI gestito su Oracle Cloud Infrastructure per l'analisi delle immagini. Offre modelli pre-addestrati per il rilevamento di oggetti, la classificazione delle immagini e l'estrazione di testo, oltre alla possibilità di addestrare modelli personalizzati sui propri dati etichettati."
  - question: "Come si addestra un modello di classificazione immagini personalizzato con OCI Vision?"
    answer: "Si crea un progetto in OCI Vision, si caricano immagini etichettate usando OCI Data Labeling e si invia un job di training. Il servizio esegue il fine-tuning del modello sul dataset. Una volta addestrato, può essere chiamato tramite l'OCI SDK o l'API REST."
  - question: "OCI Vision è disponibile nel Free Tier OCI?"
    answer: "OCI Vision offre un tier gratuito con 1.000 transazioni di analisi immagini al mese per i modelli pre-addestrati. Il training di modelli personalizzati comporta costi di compute in base al tempo di addestramento."
---

## OCI Vision: come identifichiamo i cereali?

E' possibile usare OCI Vision per classificare immagini non incluse nel modello Vision predefinito, senza gestire infrastruttura e senza competenze ML profonde?

Si', e' possibile.

Puoi usare OCI Vision per identificare il contenuto delle immagini e integrare questa funzionalita' nel tuo software o nel tuo business.

### Vediamo come

In questo esempio ho usato cereali, ma lo stesso approccio puo' essere esteso a molti oggetti visibili.

Ricorda che i dati determinano la qualita' del risultato.

Se devi identificare un oggetto specifico, devi addestrare un modello con piu' immagini di quell'oggetto e migliorare la qualita' aggiungendo immagini rappresentative.

Ho preparato codice Python per automatizzare l'aumento del dataset e produrre piu' dati di training, ma prima servono alcune immagini di esempio.

Tutti i sample e lo script Python sono salvati in questo progetto GitHub: [https://github.com/enricopesce/oci-vision-cereals](https://github.com/enricopesce/oci-vision-cereals)

Le cartelle sono definite cosi':

```console
.
├── README.md
├── original
│   ├── corn
│   ├── sorghum
│   └── wheat
└── preprocessing.py
```

Ho scaricato immagini di esempio per tre tipi di semi:

![Semi di grano](static/wheat.jpg)
![Semi di mais](static/corn.jpg)
![Semi di sorgo](static/sorghum.jpg)

- **Grano**: una graminacea coltivata per il seme, cereale alla base dell'alimentazione mondiale. Viene tipicamente macinato in farina per pane, pasta e altri alimenti.
- **Mais**: uno dei cereali piu' coltivati al mondo. E' usato come alimento umano, mangime per animali e materia prima industriale.
- **Sorgo**: cereale versatile usato per alimentazione, mangimi e biocarburanti. Tollera la siccita' ed e' importante nelle regioni semi-aride.

Li ho salvati nella cartella **original**, raggruppati per nome del cereale.

### Preparare i dati per la rete neurale OCI Vision

Queste immagini non sono sufficienti per addestrare un modello utile. Nei miei test il modello aveva bisogno di piu' immagini filtrate e aumentate per funzionare bene.

In questa piccola iterazione ho preparato uno script per preprocessare e aumentare le immagini originali usando tecniche base:

- Resize e crop
- Rotazione casuale
- Luminosita' casuale
- Flip orizzontale casuale

Altre tecniche sono documentate [in questo paper](https://arxiv.org/pdf/2301.02830).

Trovi lo script Python qui: [https://github.com/enricopesce/oci-vision-cereals/blob/main/preprocessing.py](https://github.com/enricopesce/oci-vision-cereals/blob/main/preprocessing.py)

Lo script genera immagini ottimizzate e aumentate a partire dai sample originali, pronte per l'addestramento sui servizi OCI.

```console
python preprocessing.py
```

### Copiare i dati in un bucket OCI Object Storage

Prima di importare i file processati, copiali in un bucket OCI Object Storage. I passaggi successivi useranno questo bucket come sorgente dati.

Crea un bucket e copia tutte le cartelle processate:

```console
oci os object bulk-upload \
 --namespace-name YOURNAMESPACENAME \
 --bucket-name YOURBUCKETNAME \
 --src-dir processed/ --content-type image/jpeg
```

Ora siamo pronti a usare il servizio OCI Artificial Intelligence.

### Etichettare i dati con OCI Data Labeling

Prima di costruire il modello dobbiamo classificare le immagini. Ogni immagine deve avere un'etichetta corrispondente al suo contenuto: grano, mais o sorgo.

Questa fase puo' essere ripetitiva, ma lo script di preprocessing ha gia' generato un file metadata JSONL importabile in OCI Vision.

La nuova cartella `processed` contiene tutte le immagini elaborate, classificate per cartella, e il file metadata in formato JSON lines supportato da OCI Vision.

```console
.
├── README.md
├── original
│   ├── corn
│   ├── sorghum
│   └── wheat
├── preprocessing.py
└── processed
 ├── corn
 ├── metadata.jsonl
 ├── sorghum
 └── wheat
```

Ora il contenuto processato e' in `YOURBUCKETNAME` ed e' pronto per l'import.

Accedi alla console OCI e vai in **Analytics & AI** > **Machine Learning** > **Data Labeling** > **Dataset** > **Import dataset**.

![Import dataset in OCI Data Labeling](static/import.avif)

![Configurazione import da Object Storage](static/import2.avif)

![Dataset cereali importato](static/dataset.avif)

### Creare il modello

Finalmente possiamo costruire e usare il modello OCI Vision.

Crea un nuovo Project nella pagina OCI Vision e seleziona i dati di Data Labeling.

Vai in **Analytics & AI** > **Machine Learning** > **Vision** > **Project**.

![Progetto OCI Vision](static/project.avif)

Apri il progetto e crea un modello. Scegli **Image classification** come tipo e usa il dataset `grains` da OCI Data Labeling.

![Creazione modello OCI Vision image classification](static/model.avif)

Conferma tutto e continua per avviare la build del modello.

In questa fase OCI costruisce automaticamente il modello. Il tempo dipende dalla complessita' dei dati e puo' arrivare fino a 24 ore.

Non devi configurare server, comprare GPU, dividere manualmente i dati o applicare algoritmi. OCI Vision gestisce il workflow di training.

![Modello OCI Vision addestrato](static/trained.avif)

Il modello ha un F1 score molto buono: ora possiamo testarlo.

### Provare il modello

Ho scaricato nuove immagini casuali relative agli oggetti addestrati e le ho testate:

![Predizione OCI Vision per mais](static/corntest.avif)
![Predizione OCI Vision per grano](static/wheattest.avif)
![Predizione OCI Vision per sorgo](static/sorghumtest.avif)

Il modello ha restituito l'etichetta corretta per ogni immagine con confidenza superiore al 90%, un buon risultato per questo semplice esempio.

Ora il mio OCI Vision distingue i cereali.

### Considerazioni

OCI Vision rende semplice creare un servizio di classificazione immagini senza gestire infrastruttura.

La parte OCI e' semplice. Gran parte del lavoro e' nel preprocessing, nell'aumento e nella preparazione dei dati.
