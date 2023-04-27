---
title: Oracle Autonomous Database
date: 2023-02-20T19:00:00+01:00
draft: false
tags:
  - autonomous
categories:
  - database
cover:
  alt: IAM Identity domains
  caption: IAM Identity domains
  image: static/autonomous_database_vision.png
  relative: true
---

## Introduzione al database cloud piu’ moderno del mercato

Oracle Autonomous e’ un database cloud che utilizza tecniche di machine learning per automatizzare il suo tuning, la sua sicurezza, il suo backup, gli aggiornamenti e altre procedure di gestione tradizionalmente eseguite da un DBA. Diversamente da un database convenzionale Autonomos esegue tutte queste e altre attivita’ senza la necessita di un internvento umano.

#### Perche’ utilizzare Autonomous?

I database contengono dati critici per il business e sono essentiali per l’efficente funzionamento delle organizzazioni moderne. I DBA sono spesso impegnati da attivita’ ripetitive e manuali di gestione e manutenzione del database. All’aumentare delle attivita’ di amministrazione il rischio di un errore umano e’ sempre maggiore con conseguenze catastrofiche.

Le applicazioni aziendali aggiungono sempre di piu’ negli anni nuovi record ai database esistenti e utilizzano le informazioni del database per creare report, analizzare tendenze o cercare anomalie. Ciò può far sì che i database crescano fino a raggiungere dimensioni di molti terabyte e diventino estremamente complessi, rendendoli ancora più difficili da gestire, proteggere e ottimizzare per le massime prestazioni. Allo stesso tempo i vettori di attacco verso i dati sono sempre maggiori e mancati aggiornamenti di sicurezza espongono i dati a rischi importanti.

Ciò amplifica la necessità di una gestione del database efficiente e sicura che migliori la sicurezza dei dati, riduca i tempi di inattività, migliori le prestazioni aumentando l’espozione all’errore umano. Un database Autonomous può risolvere tutte queste problematiche.

#### Benefici di Autonomous

Ci sono diversi vantaggi rispetto alle soluzioni tradizionali:

- Uptime elevato, massime prestazioni e sicurezza del database, inclusi aggiornamenti e correzioni automatiche
- Eliminazione delle attività di gestione manuali soggette a errori tramite l’automazione
- Riduzione dei costi e miglioramento della produttività automatizzando le attività di routine manuali
- L’utilizzo di Autonomous consente a un’organizzazione di utilizzre il personale addetto alla gestione del database su attività di livello superiore creando un maggiore valore aziendale.

#### Nel dettaglio, le funzionalita' piu importanti:

##### Facile scalabilità:

Può espandere o ridurre istantaneamente le proprie risorse di calcolo e memoria, a seconda delle necessità. Ad esempio, un’azienda potrebbe passare da 8 core di elaborazione di database a 16 core per l’elaborazione di fine trimestre, per poi passare agli 8 core meno costosi in seguito. Infatti, tutte le risorse di calcolo potrebbero essere spente durante il fine settimana per ridurre i costi, per poi essere riavviate il lunedì mattina. Il tutto senza alcun blocco del servizio.

##### Patching del database

Molte violazioni dei dati sono abilitate da vulnerabilità del sistema per le quali era già disponibile una patch di sicurezza o di vulnerabilità ma non ancora applicata. Un database Autonomous previene questo problema applicando automaticamente le patch ai server cloud in una sequenza progettata per eliminare i tempi di inattività dell’azienda.

##### Intelligenza integrata

Il database integra funzionalità di monitoraggio, gestione e analisi che sfruttano l’apprendimento automatico e le tecniche di intelligenza artificiale. L’obiettivo è automatizzare l’ottimizzazione del database, prevenire interruzioni dell’applicazione e rafforzare la sicurezza nell’intera applicazione del database.

#### Le funzionalita’ chiave di Autonomous

Di seguito piu’ informazioni specifiche delle funzionalita’ chiave di Autonomous

##### Provisioning automatico

Automaticamente puoi creare database mission-critical che sono tolleranti ai guasti e in alta affidabilita’. La soluzione permette di avere una perfetta scalabilità orizzontale, protezione in caso di errore hardware e consente di eseguire gli aggiornamenti del database senza bloccare le applicazioni che lo usano.

##### Configurazione automatica

Automaticamente il database ottimizza la sua configurazione in base al carico di lavoro specifico. Dalla configurazione della memoria, ai formati dei dati e alle strutture di accesso, è ottimizzato per migliorare le prestazioni. I clienti possono semplicemente caricare i dati e partire.

##### Auto-indicizzazione

Automaticamente vengono identificati indici mancanti che potrebbero accelerare le applicazioni. Convalida ogni indice per garantirne i vantaggi prima di implementarlo e utilizza tecniche di machine learning per imparare dai propri errori.

##### Ridimensionamento automatico

Automaticamente il database ridimensiona le risorse di calcolo aumentandole o diminuendole quando necessario per il carico di lavoro. Il ridimensionamento avviene online durante l’esecuzione senza bloccare le applicazioni che utilizzano il database.

##### Protezione automatizzata dei dati

Automaticamente protegge i dati di tipo sensibile e regolamentato nel database, il tutto tramite una console di gestione unificata. Valuta la sicurezza della configurazione, degli utenti, dei dati sensibili e delle attività insolite del database.

##### Sicurezza automatizzata

Automaticame la crittografia viene applicata per l’intero database, i backup e tutte le connessioni di rete. Nessun accesso al sistema operativo o privilegi di amministratore prevenendo gli attacchi di phishing. Protegge il sistema dalle operazioni cloud e da eventuali utenti interni malintenzionati.

##### Backup automatici

Backup giornaliero automatico del database. Ripristino del database in qualsiasi momento specificato della giornata negli ultimi 60 giorni.

##### Patching automatico

Patch e aggiornamenti automatici senza tempi di inattività. Le applicazioni continuano a essere eseguite mentre l’installazione delle patch avviene in modo round-robin tra i nodi oi server del cluster senza bloccare le applicazioni che utilizzano il database.

##### Rilevamento e risoluzione automatizzati

Utilizzando il riconoscimento dei modelli, i guasti hardware vengono previsti automaticamente senza lunghi timeout. Gli IO vengono immediatamente reindirizzati su dispositivi funzionanti per evitare blocchi del database. Il monitoraggio continuo per ogni database genera automaticamente service request per qualsiasi evento non previsto.

##### Failover automatico

Failover automatico senza perdita di dati. È completamente trasparente per le applicazioni dell’utente finale. Fornisce il 99,995% di SLA.