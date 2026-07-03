---
title: Oracle Autonomous Database
description: "Scopri come Oracle Autonomous Database automatizza provisioning, tuning, scaling, sicurezza, backup e patching dei database gestiti nel cloud."
date: 2023-09-21T19:00:00+01:00
lastmod: 2026-06-12T00:00:00+00:00
draft: false
cover:
  alt: Oracle Autonomous Database
  caption: Oracle Autonomous Database
  image: static/autonomous_database_vision.webp
  relative: true
keywords:
- "oracle autonomous database"
- "database autonomo"
- "autonomous data warehouse"
- "oracle cloud database"
tags:
- "OCI"
- "Autonomous Database"
- "Database"
categories:
- "Database"
faq:
  - question: "Cos'è Oracle Autonomous Database?"
    answer: "Oracle Autonomous Database è un servizio di database cloud che usa il machine learning per automatizzare tuning, sicurezza, backup e patching senza intervento del DBA. Esiste in due varianti: Autonomous Data Warehouse (ADW) per l'analisi e Autonomous Transaction Processing (ATP) per carichi OLTP."
  - question: "Oracle Autonomous Database è disponibile nel Free Tier OCI?"
    answer: "Sì. OCI Always Free include due istanze di Autonomous Database con 20 GB di storage ciascuna. Il tier gratuito supporta ATP e ADW con massimo 1 OCPU e 1 GB di RAM."
  - question: "Qual è la differenza tra ATP e ADW in Oracle Autonomous Database?"
    answer: "Autonomous Transaction Processing (ATP) è ottimizzato per carichi OLTP misti ad alta concorrenza, applicazioni web e reporting. Autonomous Data Warehouse (ADW) è ottimizzato per query analitiche, data warehousing e batch processing con storage colonnare ed esecuzione parallela."
related:
- "/posts/0006"
- "/posts/0007"
---

## Introduzione al database cloud piu' moderno del mercato

Oracle Autonomous Database e' un database cloud che usa tecniche di machine learning per automatizzare tuning, sicurezza, backup, aggiornamenti e altre procedure di gestione tradizionalmente svolte da un DBA. A differenza di un database convenzionale, Autonomous svolge queste e altre attivita' senza bisogno di intervento umano.

### Perche' usare Autonomous?

I database contengono dati aziendali critici e sono fondamentali per il funzionamento delle organizzazioni moderne. I DBA sono spesso impegnati in attivita' ripetitive e manuali di gestione e manutenzione. Quando le attivita' amministrative aumentano, cresce anche il rischio di errore umano, con possibili conseguenze molto gravi.

Le applicazioni aziendali continuano ad aggiungere record ai database esistenti e usano quei dati per creare report, analizzare trend o rilevare anomalie. Questo puo' far crescere i database fino a molti terabyte e renderli sempre piu' complessi da gestire, proteggere e ottimizzare. Allo stesso tempo, i vettori di attacco aumentano e la mancanza di aggiornamenti di sicurezza espone i dati a rischi significativi.

Questo amplifica la necessita' di una gestione efficiente e sicura del database, capace di migliorare la sicurezza dei dati, ridurre i downtime e aumentare le prestazioni diminuendo l'esposizione all'errore umano. Autonomous Database puo' rispondere a queste esigenze.

### Benefici di Autonomous

Rispetto alle soluzioni tradizionali ci sono diversi vantaggi:

- Alta disponibilita', massime prestazioni e sicurezza, inclusi aggiornamenti e fix automatici.
- Eliminazione di attivita' manuali soggette a errore tramite automazione.
- Riduzione dei costi e miglioramento della produttivita' automatizzando attivita' ripetitive.
- Possibilita' di dedicare il personale di gestione database ad attivita' a maggior valore.

### Funzionalita' principali di Autonomous

##### Provisioning automatico

Crea automaticamente database mission-critical fault tolerant e altamente affidabili. La soluzione permette scalabilita' orizzontale, protezione in caso di guasti hardware e aggiornamenti senza bloccare le applicazioni.

##### Configurazione automatica

Il database ottimizza automaticamente la propria configurazione in base al workload. Dalla memoria ai formati dati e alle strutture di accesso, tutto viene ottimizzato per migliorare le prestazioni. I clienti possono caricare i dati e iniziare.

##### Auto-indexing

Identifica automaticamente gli indici mancanti che potrebbero velocizzare le applicazioni. Valida ogni indice prima di implementarlo e usa tecniche di machine learning per imparare dai propri errori.

##### Scaling automatico

Il database scala automaticamente le risorse di calcolo verso l'alto o verso il basso in base al workload. Lo scaling avviene online senza bloccare le applicazioni.

##### Protezione automatica dei dati

Protegge automaticamente i dati sensibili e regolamentati attraverso una console di gestione unificata. Valuta configurazione, utenti, dati sensibili e attivita' anomale del database.

##### Sicurezza automatizzata

Applica automaticamente cifratura per database, backup e connessioni di rete. L'assenza di accesso al sistema operativo e di privilegi amministrativi riduce il rischio di attacchi e protegge anche da possibili utenti interni malevoli.

##### Backup automatici

Esegue backup giornalieri automatici del database. E' possibile ripristinare il database a un momento specifico entro gli ultimi 60 giorni.

##### Patching automatico

Applica patch e aggiornamenti senza downtime. Le applicazioni continuano a funzionare mentre le patch vengono installate in modo progressivo sui nodi o server del cluster.

##### Rilevamento e risoluzione automatica

Usando pattern recognition, i guasti hardware vengono previsti automaticamente senza lunghi timeout. Gli I/O vengono reindirizzati subito verso dispositivi funzionanti per evitare blocchi del database. Il monitoraggio continuo genera service request per eventi imprevisti.

##### Failover automatico

Failover automatico senza perdita di dati, trasparente per le applicazioni finali. Fornisce SLA del 99,995%.

Per approfondire, consiglio la [pagina ufficiale del prodotto](https://www.oracle.com/autonomous-database/).
